import io

from setuptools import setup


with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()


setup(
    name='lndhub',
    version='0.0.1',
    url='https://github.com/eillarra/lndhub',
    author='eillarra',
    author_email='eneko@illarra.com',
    license='MIT',
    description='',
    long_description=readme,
    keywords='bitcoin lightning-network lndhub lnurl',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    packages=[],
    install_requires=[],
    zip_safe=False
)
