from setuptools import setup

setup(
    name='managealooma',
    version='0.1.13',
    author='Jay Rosenthal',
    author_email='jay.rosenthal@hover.to',
    packages=['managealooma'],
    url='http://pypi.python.org/pypi/ManageAlooma/',
    license='LICENSE.txt',
    description='Code to manage the Alooma ETL tool.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    install_requires=[
        "alooma>=0.4.15",
        "pprint>=0.1",
        "requests>=2.21.0",
        "tabulate>=0.8.3",
        "pandas>=0.23.4",
        "SQLAlchemy>=1.2.15"
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
