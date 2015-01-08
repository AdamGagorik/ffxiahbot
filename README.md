pydarkstar
==========

A python module for interacting with a darkstar server.

Features
========
* create prices database
* human editable price database
* populate auction house with prices
* buy items put up for sale by players

Requires
========
* python 2.7.8
* sqlalchemy 0.9.8
* pymysql 0.6.2
* bs4 4.3.2
* pyyaml 3.11

*The requirements can be installed using pip, however, there are many other ways*

```bash
pip install sqlalchemy
pip install pymysql
pip install beautifulsoup4
```

Usage
=====

* **option 1**
 The main scripts are located in ./path/to/pydarkstar/apps.
 They should work if run *from that directory*.

 ```bash
 cd ./path/to/pydarkstar/apps
 python ./scrub.py --help
 ```

*To run the script from another directory, you must tell python where the pydarkstar module is.*

* **option 2** : add to PYTHONPATH temporarily

 ```bash
 export PYTHONPATH=$PYTHONPATH:/path/to/pydarkstar/
 ```

* **option 3** : add to PYTHONPATH permanently, on Linux

 ```bash
 echo "PYTHONPATH=$PYTHONPATH:/path/to/pydarkstar/" >> ~/.bashrc
 source ~/.bashrc
 ```

* **option 4** : install module

 ```bash
 cd ./path/to/pydarkstar/
 python setup.py
 ```

*If using options 2, 3, or 4, you can run aps from anywhere.*

 ```bash
 cd /somewhere/else
 python ./path/to/pydarkstar/apps/scrub.py
 ```
 
Tests
=====
Tests are in ./path/to/pydarkstar/tests
