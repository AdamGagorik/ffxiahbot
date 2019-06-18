# Requirements

You must use **python 3.7** or greater!

The following python modules must also be installed.

* python 3.7.3
* sqlalchemy 1.3.4
* pymysql 0.9.3
* bs4 4.7.1
* pyyaml 5.1

The easiest way to setup the Python is to create a [conda environment][conda].
Do this by using the conda command on the environment.yml file in the bin directory.
After the environment is created you must activate it before calling any of the scripts.

##### Anaconda Environment

```bash
> cd /D "C:\path\to\pydarkstar\bin"
> conda env remove --name pydarkstar
> conda env create -f environment.yml
```

[conda]: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
