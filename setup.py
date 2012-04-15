
from distutils.core import setup
from os import walk
from os.path import join


import re
__version__ = re.search(r'(?m)^__version__\s*=\s*"([\d.]+)"', open('ttgo/__init__.py').read()).group(1)

package_data_ext = [ 'png' ]
ttgo_package_data = set([ '*.kv' ])

for root, subFolders, files in walk('ttgo/data'):
    for fn in files:
        ext = fn.split('.')[-1].lower()
        if ext not in package_data_ext:
            continue
        filename = join(root, fn).replace("ttgo/", "")
        ttgo_package_data.add(filename)


setup(
    name='TabletopGo',
    version=__version__,
    author='Dean Serenevy',
    author_email='dean@serenevy.net',
    packages=['ttgo', 'gogame'],
    scripts=['bin/ttgo'],
    url='https://github.com/duelafn/tabletop-go',
    license='LICENSE',
    description='Go game built on the kivy framework',
    long_description=open('README').read(),
    package_data={'ttgo': list(ttgo_package_data)},
    install_requires=[
        "Kivy >= 1.2.0",
        "TabletopLib >= 0.1.0",
    ],
)
