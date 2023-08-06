#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interface to use the Integration API between HDFS and COMPSs."""

import pyarrow as pa
import pandas as pd

from io import StringIO


class Block(object):
    blk = None
    dfs = None
    opened = False

    def __init__(self, block):
        """Open the BlockObject."""
        if isinstance(block, list):
            if len(block) > 1:
                raise Exception('Please inform only one block.')
            else:
                block = block[0]
        if not all(k in block for k in ('length', 'port', 'path',
                                        'start', 'length')):
            raise Exception('Invalid block object!')
        self.blk = block
        try:
            if all(['host' in block, 'port' in block]):
                host = block['host']
                port = block['port']
            else:
                host = 'default'
                port = 0

            user = block.get('user', None)

            self.dfs = pa.hdfs.connect(host=host, port=port, user=user)
        except Exception as e:
            raise e

    def __del__(self):
        del self.blk
        self.dfs.close()

    def read_dataframe(self, format_file='csv', infer=False, dtype='str',
                       separator=',', header=True, **kwargs):
        """Read a fragment as a pandas's DataFrame."""

        header_op = header

        header = ''
        filename = self.blk['path']
        with self.dfs.open(filename) as f:
            if format_file == 'csv':
                # adding header
                if self.blk['start'] > 0 and header_op:
                    content = f.read(nbytes=2048).decode('utf-8')
                    header_idx = content.find('\n')
                    header = content[0:header_idx]+'\n'

            # adding the physical content (hdfs block)
            data = f.read_at(nbytes=self.blk['length'],
                             offset=self.blk['start']).decode('utf-8')

            if self.blk['start'] > 0:
                index = data.find("\n")
                if index != -1:
                    data = data[index+1:]

            data = header + data
            # adding the logical content (block --> split)
            if not self.blk['lastBlock']:
                f.seek(self.blk['start'] + self.blk['length'])
                delimiter = False
                line = ""
                while not delimiter:
                    tmp = f.read(nbytes=2048).decode('utf-8')
                    index = tmp.find("\n")
                    if index > 0:
                        tmp = tmp[:index]
                        delimiter = True
                    line += tmp
                data += line

        print("[INFO] data-reader: download completed.")

        try:

            if format_file == 'csv':
                if header_op:
                    header_op = 'infer'
                else:
                    header_op = None

                if infer:
                    data = pd.read_csv(StringIO(data), sep=separator,
                                       header=header_op,
                                       **kwargs)

                else:
                    data = pd.read_csv(StringIO(data), sep=separator,
                                       header=header_op,
                                       dtype=dtype,
                                       **kwargs)

                if not header_op:
                    n_cols = len(data.columns)
                    new_columns = ['col_{}'.format(i) for i in range(n_cols)]
                    data.columns = new_columns

            elif format_file == 'json':
                if infer:
                    data = pd.read_json(StringIO(data), orient='records',
                                        lines=True)
                else:
                    data = pd.read_json(StringIO(data), orient='records',
                                        dtype=dtype, lines=True)

        except Exception as e:
            raise e

        return data

    def read_block(self):
        """Read the fragment as a common file. Return a StringIO file."""
        try:

            filename = self.blk['path']
            with self.dfs.open(filename) as f:

                data = f.read_at(nbytes=self.blk['length'],
                                 offset=self.blk['start']).decode('utf-8')

                if self.blk['start'] > 0:
                    index = data.find("\n")
                    if index != -1:
                        data = data[index + 1:]

                # adding the logical content (block --> split)
                if not self.blk['lastBlock']:
                    f.seek(self.blk['start'] + self.blk['length'])
                    delimiter = False
                    line = ""
                    while not delimiter:
                        tmp = f.read(nbytes=2048).decode('utf-8')
                        index = tmp.find("\n")
                        if index > 0:
                            tmp = tmp[:index+1]
                            delimiter = True
                        line += tmp
                    data += line

        except Exception as e:
            raise e
        return StringIO(data)

    def read_binary(self, n_bytes=-1):
        """Read all file as binary, for instance, to read shapefile."""

        with self.dfs.open(self.blk['path']) as f:
            if n_bytes == -1:
                n_bytes = f.info()['size']
            data = f.read(n_bytes)

        return data
