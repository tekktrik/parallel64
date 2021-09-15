from setuptools import setup, find_packages

setup(
    name = 'parallel64',
    packages = ['parallel64', 'parallel64.bitbang', 'parallel64.inpoutdlls'],  # Ideally should be same as your GitHub release tag varsion
    description = 'Python package for working with parallel ports in a 64-bit Windows environment',
    author = 'Alec Delaney',
    author_email = 'tekktrik@gmail.com',
    url = 'https://github.com/tekktrik/parallel64',
    download_url = 'https://github.com/tekktrik/parallel64/archive/refs/tags/v0.4.16.tar.gz',
    include_package_data = True,
    package_data = {"bitbang_pwm": ['parallel64.bitbang.bitbang_pwm.pyd']},
    keywords = ['parallel', 'port', 'spp', 'epp', 'ecp'],
    classifiers = [],
)