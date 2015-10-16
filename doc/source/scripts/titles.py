import shutil
import os
import re

work = os.getcwd()
found = []
regex = re.compile(r'pydarkstar\.(.*)\.rst')
for root, dirs, files in os.walk(work):
    for f in files:
        m = regex.match(f)
        if m:
            found.append((root, f))

for root, f in found:
    path = os.path.join(root, f)
    with open(path, 'r') as handle:
        lines = handle.readlines()

    with open(path, 'w') as handle:
        for i, line in enumerate(lines):
            if i == 0:
                line = re.sub(r'\s+package$', '', line)
                line = re.sub(r'\s+module$', '', line)
                line = re.sub(r'^pydarkstar\.', '', line)

            #print('{:2d} {}'.format(i, line.rstrip()))
            handle.write(line)
        #print('')

# fix main file
with open('pydarkstar.rst', 'r') as handle:
    lines = handle.readlines()

z = 0
with open('pydarkstar.rst', 'w') as handle:
    for i, line in enumerate(lines):
        if i == 0:
            line = re.sub(r'\s+package$', '', line)

        if re.match(r'^\s\s\spydarkstar.*$', line):
            handle.write('    {}'.format(line.lstrip()))
        else:
            handle.write(line)

        if '.. toctree::' in line:
            if z:
                handle.write('    :maxdepth: {}\n'.format(z))
            else:
                z += 1

