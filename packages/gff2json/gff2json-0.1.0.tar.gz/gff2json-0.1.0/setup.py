from setuptools import setup, find_packages

setup(
    name = 'gff2json',
    version = '0.1.0',
    keywords='gff json convert format',
    description = 'convert gff files to json',
    license = 'MIT License',
    url = 'https://github.com/IsaacLuo/gff2json',
    author = 'Isaac Luo',
    author_email = 'yishaluo@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['gff2json=gff2json.gff2json:main'],
    }
)