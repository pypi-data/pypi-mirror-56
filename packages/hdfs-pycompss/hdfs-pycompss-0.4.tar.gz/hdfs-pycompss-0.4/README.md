# Integration: PyCOMPSs and HDFS

The abstraction that is provided by this version is exactly the same as
 that provided by the version in java. Please read the Java version 
 before continuing.

# How to install the HDFSPyCOMPSs module

This module is available at PyPi, 

```bash
    $ pip3 install hdfs-pycompss
```

After install it, you need set up some environment variables:

 * HADOOP_HOME: the root of your installed Hadoop distribution. Often has lib/native/libhdfs.so.
 * JAVA_HOME: the location of your Java SDK installation.
 * CLASSPATH: must contain the Hadoop jars
 
```bash
export CLASSPATH=$CLASSPATH:`$HADOOP_HOME/bin/hdfs classpath --glob`
```

Because COMPSs don't copy all environment variables to all workers, it's important to set these variables at /etc/environment.


# Example of how to use the API (without StorageAPI)

```python
def wordcount(blk, word):
    from hdfspycompss.block import Block
    data = Block(blk).read_block()
    ...
    return result

def main():
    import hdfspycompss.hdfs import HDFS
    dfs = HDFS(host='localhost', port=9000)
    HDFS_BLOCKS = dfs.find_blocks('/input.data')

    nFrag = len(HDFS_BLOCKS)
    result = [{} for f in range(nFrag)]
    for f, blk in enumerate(HDFS_BLOCKS):
        result[f] = wordcount(blk, 'word')
    ...
```
