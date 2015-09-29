#### LINUX

* Linux already comes with python.  **You should use python3**, which is not the default.

```bash
bash:~$ sudo apt-get install git
bash:~$ sudo apt-get install pip

bash:~$ sudo pip install sqlalchemy
bash:~$ sudo pip install pymysql
bash:~$ sudo pip install beautifulsoup4
bash:~$ sudo pip install pyyaml

bash:~$ git clone git@github.com:AdamGagorik/pydarkstar.git

# enter the correct path!
bash:~$ cd ./path/to/pydarkstar
bash:~$ python3 ./makebin.py
```

**Edit the config.yaml in "C:\path\to\pydarkstar\bin" with your settings (use a text editor).**

```bash
bash:~$ cd /path/to/pydarkstar/bin

# to download new data from ffxiah.com (takes forever)
bash:~$ ./scrub.sh

# to start the broker
bash:~$ ./broker.sh
```