from setuptools import setup, find_packages
from docupdater import VERSION


def read(filename):
    with open(filename) as f:
        return f.read()


def get_requirements(filename="requirements.txt"):
    """returns a list of all requirements"""
    requirements = read(filename)
    return list(filter(None, [req.strip() for req in requirements.split() if not req.startswith('#')]))


setup(
    name='docupdater',
    version=VERSION,
    maintainer='Any github maintainer',
    maintainer_email='harcher81@gmail.com',
    description='Automatically keep your docker services and your docker containers up-to-date with the latest version',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/docupdater/docupdater',
    license='MIT',
    classifiers=['Programming Language :: Python',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7'],
    packages=find_packages(),
    include_package_data=True,
    scripts=['entrypoint'],
    install_requires=get_requirements(),
    python_requires='>=3.6.2'
)
