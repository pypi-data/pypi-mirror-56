import setuptools

with open('README.rst', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='ubiltools',
    version='1.0.4',
    packages=setuptools.find_packages(),
    url='https://github.com/umanther/ubiltools',
    author='Geoff Hellstrand',
    author_email='ubil@hotmail.com',
    description='A collection of tools I use',
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
