VERB=0
NOSE=nosetests --nologcapture --verbosity ${VERB}

help:
	@echo "[targets]"
	@echo "    make tests"

.PHONY : test
test: tests

.PHONY : tests
tests:
	${NOSE} -w ./pydarkstar/tests/

.PHONY : pydarkstar
pydarkstar:
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
