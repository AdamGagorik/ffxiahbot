#!/bin/bash
PACKAGEDIR=$(dirname $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd))
PYTHON=`which python`
MODULE=pydarkstar
APP=$1


# find the apps
function usage {
    echo "usage:"
    echo "    ${MODULE} <app> <args>"
    echo ""
    echo "apps:"
    echo "    broker"
    echo "    scrub"
    echo "    alter"
    echo ""
    echo "note:"
    echo "    please use ${MODULE} <app> --help for more information"
    echo ""
}


# print help message
if [[ $# -ge 1 ]]; then
    if [[ $1 == "--help" ]] || \
       [[ $1 == "-help" ]] || \
       [[ $1 == "--h" ]] || \
       [[ $1 == "-h" ]]
    then
        usage
        exit 0
    fi
fi


# show variables
function echo_append {
    echo "$1" 2>&1 | tee -a ${MODULE}.log
}
echo_append "################################################################################"
echo_append "PACKAGEPATH : ${PACKAGEDIR}"
echo_append "PYTHON      : ${PYTHON}"
echo_append "MODULE      : ${MODULE}"
echo_append "APP         : ${APP}"
echo_append ""


# check the package dir
if [ ! -d ${PACKAGEDIR} ] || \
   [ ! -d ${PACKAGEDIR}/${MODULE} ] || \
   [ ! -f ${PACKAGEDIR}/${MODULE}/__init__.py ]
then
    usage
    echo "error:"
    echo "    can not validate ${MODULE} package location"
    echo "        PACKAGEDIR: ${PACKAGEDIR}"
    echo ""
    exit -1
fi


# check that there is at least one command line argument
if [[ $# -lt 1 ]]; then
    usage
    echo "error:"
    echo "    <app> argument missing"
    echo ""
    exit -1
fi


# check that the app specified is valid
if [ ! -f ${PACKAGEDIR}/${MODULE}/apps/${APP}/run.py ]; then
    usage
    echo "error:"
    echo "    can not validate ${APP} location"
    echo "        APP: ${PACKAGEDIR}/${MODULE}/apps/${APP}/run.py"
    echo ""
    exit -1
fi


# drop the first command line argument
shift


# update the PYTHONPATH with the package directory
export PYTHONPATH=${PYTHONPATH}:${PACKAGEDIR}


# call the app
${PYTHON} -m ${MODULE}.apps.${APP}.run $@
