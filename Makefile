NOSE=nosetests --nologcapture --verbosity 0

help:
	@echo "[targets]"
	@echo "    make tests     : tests : all"
	@echo "    make clean     : tidy up"

.PHONY : test
test: tests

.PHONY : tests
tests:
	${NOSE} -w ./pydarkstar/tests/

.PHONY : bin
bin:
	python3 ./makebin.py

.PHONY : clean
clean:
	-find ./pydarkstar -type d -name __pycache__ | xargs -I xxx rm -rf xxx
	-find ./pydarkstar -type f -name \*.pyc | xargs -I xxx rm xxx
	-find ./bin -type f -name \*.log | xargs -I xxx rm xxx
	$(MAKE) --no-print-directory -C ./doc clean
