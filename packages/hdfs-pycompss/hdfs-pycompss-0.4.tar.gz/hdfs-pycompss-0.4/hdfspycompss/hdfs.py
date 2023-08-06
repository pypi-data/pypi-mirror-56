#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interface to use the Integration API between HDFS and COMPSs."""
import pyarrow as pa
from math import ceil

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class HDFS(object):

    dfs = None
    host = 'default'
    port = 0
    user = None

    def __init__(self, host='default', port=0, user=None):
        """

        :param host: NameNode. "default" for fs.defaultFS from core-site.xml.
        :param port: NameNode's port. 0 for default or logical (HA) nodes.
        :param user: Username when connecting to HDFS; None implies login user.
        """
        self.dfs = pa.hdfs.connect(host, port, driver='libhdfs')
        self.port = port
        self.host = host
        self.user = user

    def __del__(self):
        self.dfs.close()

    # ------------------------------------------------
    # Methods to retrieve the fragment list
    def find_blocks(self, filename):
        """
        Retrieve the HDFS blocks used to represent a file in HDFS.

        :param filename:
        :return:
        """

        try:
            stats = self.dfs.info(filename)
            block_size_new = stats['block_size']
            list_blocks = self._split_in_blocks(filename, stats, block_size_new)

        except Exception as e:
            raise e
        return list_blocks

    def find_n_blocks(self, filename, n_frag):
        """Get a list of N fragments of a file."""

        try:
            stats = self.dfs.info(filename)
            size = stats['size']
            block_size_new = ceil(size / n_frag)
            list_blocks = self._split_in_blocks(filename, stats, block_size_new)

        except Exception as e:
            raise e

        return list_blocks

    def _split_in_blocks(self, filename, stats, block_size_new):
        list_blocks = []

        size = stats['size']

        id_block = 1
        i_start = 0
        remain = size
        while remain > block_size_new:
            block = {'id_block': id_block, 'host': self.host,
                     'port': self.port, 'path': filename,
                     'length': block_size_new, 'start': i_start,
                     'lastBlock': False, 'user': self.user}
            i_start = i_start + block_size_new
            list_blocks.append(block)
            id_block += 1
            remain -= block_size_new

        block_size = size - i_start
        block = {'id_block': id_block, 'host': self.host, 'port': self.port,
                 'path': filename, 'length': block_size, 'start': i_start,
                 'lastBlock': True, 'user': self.user}
        list_blocks.append(block)

        return list_blocks

    # -------------------------------------------------------------
    #   Methods to Write Data:
    #
    def write_block(self, filename, data, append=False, overwrite=True):
        """
        Write a fragment of file into a opened file (writing in serial).
        You must use this method in the master COMPSs node.
        """
        if append:
            mode = 'ab'
        else:
            mode = 'wb'
            if not overwrite and self.dfs.exists(filename):
                raise Exception('File {} already exists.'.format(filename))

        with self.dfs.open(filename, mode) as f:
            f.write(data.encode())
            f.close()

        return True

    def write_dataframe(self, filename, data, append=False,
                        overwrite=False, params_pandas=None):
        """
        :param filename:
        :param data:
        :param params_pandas:  Parameters to be used in pandas;
        :param append: True to append;
        :param overwrite: True to overwrite if exists;
        :return: True if it was save with success.
        """
        if params_pandas is None:
            params_pandas = {'header': True, 'index': False, 'sep': ','}
        else:
            params_pandas['index'] = False

        if append:
            mode = 'ab'
        else:
            mode = 'wb'
            if not overwrite and self.dfs.exists(filename):
                raise Exception('File {} already exists.'.format(filename))

        with self.dfs.open(filename, mode) as f:
            s = StringIO()
            data.to_csv(s, **params_pandas)
            f.write(s.getvalue())
            f.close()

        return True

    def write_json(self, filename, data, append=False, overwrite=False):
        """
        :param filename: the output name;
        :param data:
        :param append:
        :param overwrite: 
        """
        if append:
            mode = 'ab'
        else:
            mode = 'wb'
            if not overwrite and self.dfs.exists(filename):
                raise Exception('File {} already exists.'.format(filename))

        with self.dfs.open(filename, mode) as f:
            s = StringIO()
            data.to_json(s, orient='records')
            f.write(s.getvalue())
            f.close()

    def copy_files_to_hdfs(self, src, dst=None):
        """Copy local files to HDFS."""
        import os
        if not dst or dst == '':
            dst = src
            if isinstance(dst, list):
                for i, out in enumerate(dst):
                    dst[i] = "/"+os.path.basename(out)
            else:
                dst = "/"+os.path.basename(dst)

        if isinstance(src, list) and isinstance(dst, list):
            for source in src:
                for out in dst:
                    with open(source, 'rb') as f_upl:
                        self.dfs.upload(out, f_upl)
        else:
            with open(src, 'rb') as f_upl:
                self.dfs.upload(dst, f_upl)

    # ------------------------------------
    #  Util tools
    def exist(self, path):
        """Check if file or dir is in HDFS."""
        return self.dfs.exists(path)

    def mkdir(self, path):
        """Create a folder in HDFS."""
        return self.dfs.mkdir(path)

    def ls(self, path):
        """List files at path in HDFS."""
        return self.dfs.ls(path)

    def rm(self, path, recursive=False):
        """Use recursive for rm -r, i.e., delete directory and contents."""
        return self.dfs.rm(path, recursive)

    def isdir(self, fpath):
        """Check if path is file or folder"""
        return self.dfs.isdir(fpath)

    @staticmethod
    def merge_files(src, dst, wait=True, rm=True):
        """Merge files in HDFS.

        * src: mask of files to be merged;
        * dst: output name;
        * wait: True to wait the end of operation (default);
        * rm: Remove the input files after the merge.
        """
        import os
        import subprocess
        f_null = open(os.devnull, 'w')

        if rm:
            command = "hdfs dfs -text {} | hdfs dfs -put - {} && "\
                      "hdfs dfs -rm -r {}".format(src, dst, src)
        else:
            command = "hdfs dfs -text {0} | hdfs dfs -put - {1}".\
                      format(src, dst)
        if wait:
            code = subprocess.call(command, shell=True, stdout=f_null,
                                   stderr=subprocess.STDOUT)
        else:
            code = subprocess.Popen(command, shell=True, stdout=f_null,
                                    stderr=subprocess.STDOUT)
        return code == 0
