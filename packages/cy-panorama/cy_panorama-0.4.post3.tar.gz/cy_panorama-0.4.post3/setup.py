import re
import subprocess

from setuptools import setup, find_packages

DEFAULT_VERSION = "0.0.0"


# convert version from git tag to pypi style
# V0.1-3-g908f162 -> V0.1.post3
def convert_pypi_version(git_ver):
    print("git version: {}".format(git_ver))

    pattern = re.compile(
        r"^[rvVR]*(?P<main>[0-9\.]+)(\-(?P<post>[0-9]+))?(\-.+)?$")
    s = pattern.search(git_ver)

    if not s:
        print("invalid version! return default version {}".format(
            DEFAULT_VERSION))
        return DEFAULT_VERSION

    pypi_ver = s.group('main')

    if s.group('post'):
        pypi_ver += ".post{}".format(s.group('post'))

    print("pypi version: {}".format(pypi_ver))
    return pypi_ver


try:
    ver = subprocess.check_output(
        'git describe --tags', shell=True).rstrip().decode('utf-8')
except subprocess.CalledProcessError:
    ver = DEFAULT_VERSION
ver = convert_pypi_version(ver)

requires = ['Pillow', 'piexif']

setup(name='cy_panorama',
      version=ver,
      description='',
      url='https://github.com/cy-arduino/cy_panorama',
      author='ChihYing_Lin',
      author_email='',
      license='LGPL',
      packages=find_packages(exclude=['tests', 'test_*']),
      scripts=['bin/panorama_convert_fb'],
      install_requires=requires,
      zip_safe=False)
