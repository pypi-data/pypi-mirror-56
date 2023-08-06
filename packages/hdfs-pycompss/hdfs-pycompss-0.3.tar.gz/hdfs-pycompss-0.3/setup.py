import setuptools


def get_requirements():
    """
    lists the requirements to install.
    """
    try:
        with open('requirements.txt') as f:
            requirements = f.read().splitlines()
    except OSError:
        requirements = []

    return requirements


def get_readme():
    try:
        with open('README.md') as f:
            readme = f.read()
    except OSError:
        readme = ''
    return readme


setuptools.setup(
     name='hdfs-pycompss',  
     version='0.3',
     author="Lucas Miguel Ponce",
     author_email="lucasmsp@dcc.ufmg.br",
     description="HDFSPyCOMPSs is an API that enables PyCOMPSs to read HDFS "
                 "files in parallel.",
     platforms=['Linux'],
     long_description=get_readme(),
     long_description_content_type='text/markdown',
     url="https://github.com/eubr-bigsea/compss-hdfs",
     license='Apache License, Version 2.0',
     classifiers=[
         'Programming Language :: Python :: 3',
         "Programming Language :: Python :: 3.6",
         'License :: OSI Approved :: Apache Software License',
         "Operating System :: POSIX :: Linux",
         "Topic :: Software Development :: Libraries",
         "Topic :: Software Development :: Libraries :: Python Modules",
         "Topic :: System :: Distributed Computing",
     ],
     packages=setuptools.find_packages(),
     install_requires=get_requirements(),

 )
