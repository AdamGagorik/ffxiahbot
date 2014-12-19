HEADER=**********************************************************************

help:
	@echo "[targets]"
	@echo "    make tests"
	@echo "    make darkobject"
	@echo "    make timeutils"
	@echo "    make database"
	@echo "    make broker"
	@echo "    make tables/base"
	@echo "    make tables/auction_house"
	@echo "    make tables/delivery_box"

.PHONY : test
test: tests

.PHONY : tests
tests: \
 logutils \
 darkobject \
 timeutils \
 database \
 broker \
 tables/base \
 tables/auction_house \
 tables/delivery_box \

.PHONY : logutils
logutils:
	@echo "${HEADER}"
	@echo "logutils"
	python ${PWD}/tests/logutils.py
	@echo "${HEADER}"
	@echo ""

.PHONY : darkobject
darkobject:
	@echo "${HEADER}"
	@echo "darkobject"
	python ${PWD}/tests/darkobject.py
	@echo "${HEADER}"
	@echo ""

.PHONY : timeutils
timeutils:
	@echo "${HEADER}"
	@echo "timeutils"
	python ${PWD}/tests/timeutils.py
	@echo "${HEADER}"
	@echo ""

.PHONY : database
database:
	@echo "${HEADER}"
	@echo "database"
	python ${PWD}/tests/database.py
	@echo "${HEADER}"
	@echo ""

.PHONY : broker
broker:
	@echo "${HEADER}"
	@echo "broker"
	python ${PWD}/tests/broker.py
	@echo "${HEADER}"
	@echo ""

.PHONY : tables/base
tables/base:
	@echo "${HEADER}"
	@echo "tables/base"
	python ${PWD}/tests/tables/base.py
	@echo "${HEADER}"
	@echo ""

.PHONY : tables/auction_house
tables/auction_house:
	@echo "${HEADER}"
	@echo "tables/auction_house"
	python ${PWD}/tests/tables/auction_house.py
	@echo "${HEADER}"
	@echo ""

.PHONY : tables/delivery_box
tables/delivery_box:
	@echo "${HEADER}"
	@echo "tables/delivery_box"
	python ${PWD}/tests/tables/delivery_box.py
	@echo "${HEADER}"
	@echo ""
