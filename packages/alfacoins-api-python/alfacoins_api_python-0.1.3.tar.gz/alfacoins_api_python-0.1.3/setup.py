import re
from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'alfacoins_api_python', '__init__.py')) as v_file:
    package_version = re.\
        compile(r".*__version__ = '(.*?)'", re.S).\
        match(v_file.read()).\
        group(1)


dependencies = [
    'requests'
]


setup(
    name="alfacoins_api_python",
    version=package_version,
    author="Arash Fatahzade",
    author_email="fatahzade@gmail.com",
    description="ALFAcoins API Python 3.6+ Library",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/alfacoins/alfacoins-api-python',
    install_requires=dependencies,
    packages=find_packages(),
    test_suite="tests",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
