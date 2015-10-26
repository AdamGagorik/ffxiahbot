"""
Create wrapper scripts for running apps.
"""
import argparse
import logging
import shutil
import stat
import os
import re


def setup_logging(**kwargs):
    """
    Setup python logging module.
    """
    lfmt = '%(levelname)-5s: %(message)s'
    dfmt = "%Y-%m-%d %H:%M:%S"
    _kwargs = dict(level=logging.DEBUG, format=lfmt, datefmt=dfmt)
    _kwargs.update(**kwargs)
    logging.basicConfig(**_kwargs)


def log_parameter(k, v, fmt='%-14s: %s', level=logging.INFO):
    logging.log(level, fmt, k, v)


class Options:
    def __init__(self):
        self.work = os.getcwd()
        self.python = shutil.which('python3')
        self.project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.package_name = 'pydarkstar'
        self.package_path = os.path.join(self.project_path, self.package_name)
        self.apps_path = os.path.join(self.package_path, 'apps')
        self.bin_path = os.path.join(self.project_path, 'bin')
        self.apps_list = {
            'broker': 'pydarkstar.apps.broker.run',
            'seller': 'pydarkstar.apps.seller.run',
            'buyer': 'pydarkstar.apps.buyer.run',
            'refill': 'pydarkstar.apps.refill.run',
            'clear': 'pydarkstar.apps.clear.run',
            'scrub': 'pydarkstar.apps.scrub.run',
            'alter': 'pydarkstar.apps.alter.run',
        }

        if self.python is None:
            self.python = 'python'

        log_parameter('work', self.work)
        log_parameter('project_path', self.project_path)
        log_parameter('package_name', self.package_name)
        log_parameter('package_path', self.package_path)
        log_parameter('python', self.python)
        log_parameter('bin_path', self.bin_path)

        parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.parse_args()

        try:
            assert os.path.exists(self.work)
            assert os.path.exists(self.project_path)
            assert os.path.exists(self.package_path)
            assert os.path.exists(self.apps_path)
        except AssertionError:
            logging.exception('invalid configuration')
            exit(-1)


def find_apps(top, regex=r'(run|main)\.py'):
    """
    Search for applications.
    """
    if isinstance(regex, str):
        regex = re.compile(regex)

    found = []
    logging.info('looking for apps...')
    for root, dirs, files in os.walk(top):
        for f in files:
            m = regex.match(f)
            if m:
                p = os.path.join(root, f)
                found.append(p)

    found.sort(key=lambda x: x.split(os.sep))

    for f in found:
        logging.info('found app! %s', f)

    return found


LTEMPLATE = r"""
#!/bin/bash
export PYTHONPATH=$PYTHONPATH:{path}
{python} -m {spec} $*
"""[1:-1]


WTEMPLATE = r"""
@ECHO OFF
set PYTHONPATH="%PYTHONPATH%;{path}"
{python} -m {spec} %*
"""[1:-1]


def choose_template():
    """
    Choose script template based on platform.
    """
    from sys import platform
    log_parameter('platform', platform)

    # select template based on platform
    if platform in ['linux', 'linux2', 'darwin']:
        return LTEMPLATE, '{}.sh'

    elif platform in ['win32', 'win64']:
        return WTEMPLATE, '{}.bat'

    else:
        raise RuntimeError('unknown platform: %s', platform)


def chmod(path):
    os.chmod(path,
             # user
             stat.S_IRUSR |  # read
             stat.S_IWUSR |  # write
             stat.S_IXUSR |  # execute

             # group
             stat.S_IRGRP |  # read
             stat.S_IWGRP |  # write
             stat.S_IXGRP |  # execute

             # other
             stat.S_IROTH |  # read
             # stat.S_IWOTH | # write
             stat.S_IXOTH  # execute
             )


def main():
    setup_logging()
    opts = Options()

    # choose script template and output file name
    template, ostub = choose_template()

    # create bin directory
    if not os.path.exists(opts.bin_path):
        logging.info('mkdir -p %s', opts.bin_path)
        os.makedirs(opts.bin_path)

    for app in opts.apps_list:
        log_parameter(app, opts.apps_list[app])

        opath = os.path.join(opts.bin_path, ostub.format(app))

        with open(opath, 'w') as handle:
            handle.write(template.format(python=opts.python, path=os.path.dirname(opts.package_path),
                                         spec=opts.apps_list[app]))

        chmod(opath)


if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        main()
    except Exception:
        logging.exception('')
        exit(-1)
