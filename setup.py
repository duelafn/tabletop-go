
from distutils.core import setup

import re
__version__ = re.search(r'(?m)^__version__\s*=\s*"([\d.]+)"', open('ttgo/__init__.py').read()).group(1)


setup(
    name='TabletopGo',
    version=__version__,
    author='Dean Serenevy',
    author_email='dean@serenevy.net',
    packages=['ttgo', 'gogame'],
    scripts=['ttgo.py'],
    url='https://github.com/duelafn/tabletop-go',
    license='LICENSE',
    description='Go game built on the kivy framework',
    long_description=open('README').read(),
    install_requires=[
        "Kivy >= 1.2.0",
        "TabletopLib >= 0.1.0",
    ],
)
