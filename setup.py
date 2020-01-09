#!/usr/bin/env python
from setuptools import setup


def read_requirements(filename):
    dependencies = []
    with open(filename) as f:
        for l in f:
            line = l.strip()
            if line[:3] == '-r ':
                rname = line[3:].strip()
                dependencies.extend(rname)
            else:
                dependencies.append(line)
    return dependencies


install_requires = read_requirements('requirements.txt')

with open('README.rst') as f:
    long_description = f.read()


setup(
    name='mpirical',
    description='Decorate any function to make it run in parallel with MPI',
    url='https://github.com/NCAR/mpirical',
    maintainer='Kevin Paul',
    maintainer_email='kpaul@ucar.edu',
    license='https://www.apache.org/licenses/LICENSE-2.0',
    long_description=long_description,
    include_package_data=True,
    install_requires=install_requires,
    packages=['mpirical'],
    zip_safe=False,
    use_scm_version={'version_scheme': 'post-release', 'local_scheme': 'dirty-tag'},
    setup_requires=['setuptools_scm', 'setuptools>=30.3.0']
)
