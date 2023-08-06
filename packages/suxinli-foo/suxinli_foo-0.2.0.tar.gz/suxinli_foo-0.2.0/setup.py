from setuptools import setup
setup(name='suxinli_foo',
    version='0.2.0',
    package=['suxinli_foo'],
    entry_points={
        'console_scripts': ['suxinli_add=suxinli_foo.add:add'],
    },
)
