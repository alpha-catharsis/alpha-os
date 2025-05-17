from setuptools import setup, find_packages

setup(
    name='alpha-os',
    version='0.0.1',
    url='https://github.com/alpha-catharsis/alpha-os.git',
    author='Alpha Catharsis',
    author_email='alpha.catharsis@gmail.com',
    description='Homemade linux distribution',
    packages=['alpha_lib'],
    install_requires=[],
    scripts = ['bin/alpha-os.py']
)
