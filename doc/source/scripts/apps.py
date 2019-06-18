from subprocess import check_output
import textwrap
import shutil
import sys
import os

PYTHONPATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PYTHONPATH)

python3 = shutil.which('python3')

master = r"""
Apps
====

{apps}
"""[1:-1]

app = r"""
{name}

.. code:: {language}

{help}

"""[1:-1]


def format_name(name, under='='):
    if under:
        return '{}\n{}'.format(name, under * len(name))
    return name


def indent(text, spaces=4):
    text = textwrap.dedent(text)
    lines = text.split('\n')
    return ' ' * spaces + '\n{}'.format(' ' * spaces).join(lines)


def kwargs(name):
    os.chdir(PYTHONPATH)
    o = check_output([python3, '-m', 'pydarkstar.apps.{}.run'.format(name), '--help']).decode('utf-8')
    return dict(
        name=format_name(name, '^'), language='python',
        help=indent(o)
    )

with open('apps.rst', 'w') as handle:
    handle.write(master.format(
        apps='\n\n'.join(
            [
                app.format(**kwargs('broker')),
                app.format(**kwargs('seller')),
                app.format(**kwargs('buyer')),
                app.format(**kwargs('clear')),
                app.format(**kwargs('refill')),
                app.format(**kwargs('scrub')),
            ]
        )
    ))
