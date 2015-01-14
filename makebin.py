from sys import platform
import logging
import stat
import os

logging.basicConfig(level=logging.DEBUG)

def chmod(path):
    os.chmod(path,
        # user
        stat.S_IRUSR | # read
        stat.S_IWUSR | # write
        stat.S_IXUSR | # execute

        # group
        stat.S_IRGRP | # read
        stat.S_IWGRP | # write
        stat.S_IXGRP | # execute

        # other
        stat.S_IROTH | # read
       #stat.S_IWOTH | # write
        stat.S_IXOTH   # execute
    )

# set paths
work = os.getcwd()
pdir = os.path.join(work, 'pydarkstar')
adir = os.path.join(work, 'apps')
bdir = os.path.join(work, 'bin')

# check paths
assert os.path.exists(pdir)
assert os.path.exists(adir)

# find apps
apps = []
for root, dirs, files in os.walk(adir):
    for f in files:
        stub, ext = os.path.splitext(f)
        if ext.lower() == '.py':
            apps.append(os.path.abspath(os.path.join(root, f)))

# batch script templates
LTEMPLATE = \
r"""
#!/bin/bash
export PYTHONPATH=$PYTHONPATH:{path}
{interp} {script} $*
"""[1:-1]

WTEMPLATE = \
r"""
@ECHO OFF
set PYTHONPATH=%PYTHONPATH%;{path}
{interp} {script} %*
PAUSE
"""[1:-1]

# select template based on platform
if platform in ['linux', 'linux2', 'darwin']:
    logging.info('LINUX')
    template = LTEMPLATE
    ostub = '{}.sh'

elif platform in ['win32', 'win64']:
    logging.debug('WINDOWS')
    template = WTEMPLATE
    ostub = '{}.bat'

else:
    raise RuntimeError('unknown platform: %s', platform)

# create bin directory
if not os.path.exists(bdir):
    os.mkdir(bdir)

# create app scripts
for app in apps:

    # create output name
    base = os.path.basename(app)
    stub, ext = os.path.splitext(base)
    oname = os.path.join(bdir, ostub.format(stub))

    # write script
    logging.info(oname)
    with open(oname, 'wb') as handle:
        handle.write(template.format(path=work,
            interp='python', script=app))

    chmod(oname)