from setuptools import setup, find_packages
import os


def clean_dist():
    dist_path = 'dist'
    if os.path.isdir('dist'):
        files = [f for f in os.listdir(dist_path) if os.path.isfile(os.path.join(dist_path, f))]
        for file in files:
            os.remove(os.path.join(dist_path, file))


def read_file(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name), encoding="utf-8").read()


def convert_to_m2r(file_name):
    rst_file = file_name.split('.')[0] + ".rst"
    try:
        os.remove(os.path.join(os.path.dirname(__file__), rst_file))
    finally:
        os.system("m2r " + os.path.join(os.path.dirname(__file__), file_name))
        return rst_file


def upload_to_pypi():
    os.system("twine upload dist/*")


clean_dist()


setup(
    name='dictipy',
    version="0.0.2",
    author='Gioele Crispo',
    author_email='crispogioele@gmail.com',
    package_dir={'dictipy': 'dictipy'},
    packages=find_packages('.'),
    # scripts=['bin/script1', 'bin/script2'],
    url='https://github.com/gioelecrispo/dictipy.git',
    license='MIT',
    license_file='LICENSE',
    platform='any',
    description='Dictipy creates the right dict also for nested objects using recursion.',
    long_description=read_file(convert_to_m2r('README.md')),
    install_requires=read_file('requirements.txt').splitlines(),
    python_requires='>=3',
    package_data={
        # '': ['package_data.dat'],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

upload_to_pypi()

