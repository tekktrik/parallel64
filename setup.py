from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'parallel64',
    packages = ['parallel64', 'parallel64.inpoutdlls'],
    version = 'v0.6.1',  # Ideally should be same as your GitHub release tag varsion
    description = 'Python package for working with parallel ports in a 64-bit Windows environment',
    long_description = long_description,
    author = 'Alec Delaney',
    author_email = 'tekktrik@gmail.com',
    url = 'https://github.com/tekktrik/parallel64',
    download_url = 'https://github.com/tekktrik/parallel64/archive/refs/tags/v0.6.00.tar.gz',
    include_package_data = True,
    package_data = {"bitbang_pwm": ['parallel64.bitbang.bitbang_pwm.pyd']},
    keywords = ['parallel', 'port', 'spp', 'epp', 'ecp', 'gpio'],
    classifiers = [],
)