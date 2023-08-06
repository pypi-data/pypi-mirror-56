from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hockeyjockey',
    version='1.0',
    packages=['hockeyjockey', 'hockeyjockey.api', 'hockeyjockey.menu', 'hockeyjockey.models', 'hockeyjockey.utilities'],
    install_requires=['decorest', 'ansicolors'],
    url='https://gitlab.com/ricoflow/hockeyjockey',
    license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    author='Randall Speake',
    author_email='ranspeake@gmail.com',
    description='A menu-driven console-based application for analyzing NHL hockey matchups.',
    long_description_content_type='text/markdown',
    long_description=long_description,
)
