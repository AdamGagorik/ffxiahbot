VERB=0
NOSE=nosetests --nologcapture --verbosity ${VERB}

help:
	@echo "[targets]"
	@echo "    make tests     : tests : all"
	@echo "    make core      : tests : module"
	@echo "    make auction   : tests : subpackage"
	@echo "    make tables    : tests : subpackage"
	@echo "    make scrubbing : tests : subpackage"
	@echo "    make imports   : tests : imports"
	@echo "    make clean     : tidy up"
	@echo "    make bin       : create batch scripts"

.PHONY : test
test: tests

.PHONY : tests
tests:
	${NOSE} -w ./pydarkstar/tests/

.PHONY : core
core:
	@${NOSE} -w ./pydarkstar/tests/ \
		test_common.py     \
		test_darkobject.py \
		test_database.py   \
		test_itemlist.py   \
		test_item.py       \
		test_logutils.py   \
		test_options.py    \
		test_timeutils.py

.PHONY : auction
auction:
	@${NOSE} -w ./pydarkstar/tests/auction

.PHONY : tables
tables:
	@${NOSE} -w ./pydarkstar/tests/tables

.PHONY : scrubbing
scrubbing:
	@${NOSE} -w ./pydarkstar/tests/scrubbing

.PHONY : imports
imports:
	@${NOSE} ./tests/test_imports.py

.PHONY : clean
clean:
	-find ./pydarkstar -type f -name \*.pyc | xargs -I xxx rm xxx
	-find ./pydarkstar -type d -name __pycache__ | xargs -I xxx rm -rf xxx
	-rm -rf ./bin

.PHONY : bin
bin:
	python ./makebin.py
