try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='scold',
    packages=['scold'],
    version='1.1',
    description='Hurt colleagues with words',
    author='Jack Walton',
    author_email='jwalton3141@gmail.com',
    url='https://github.com/jwalton3141/scold',
    download_url='https://github.com/jwalton3141/scold/archive/1.1.tar.gz',
    keywords=['scold', 'logging'],
    classifiers=[],
    test_suite='nose.collector',
    tests_require=['nose']
)
