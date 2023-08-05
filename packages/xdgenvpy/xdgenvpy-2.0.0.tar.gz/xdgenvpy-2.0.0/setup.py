# /usr/bin/env python3

from pathlib import Path
from shutil import rmtree

from setuptools import Command
from setuptools import find_packages
from setuptools import setup

PROJECT_NAME = 'xdgenvpy'
PROJECT_VERSION = '2.0.0'


def get_repo_file(*args):
    """
    Joins all the arguments into a single string that will be normalized into an
    absolute file path.  Essentially the path will point to a file within this
    repository.

    :param args: Names to join that make up a relative file path.

    :rtype: Path
    :return: The absolute path to a file within this repository.
    """
    return Path(__file__).resolve().parent.joinpath(*args)


def read_file(filename):
    """
    Reads the specified file and returns the full contents as a single string.

    :param filename: The file to read.

    :rtype: str
    :return: The full contents of the specified file.
    """
    with open(filename) as f:
        return f.read()


def get_xdgenvpy_packages():
    """
    Finds all packages within this project and only returns the production ready
    ones.  Meaning, test packages will not be included.

    :rtype tuple
    :return: A sequence of package names that will be built into the file
            distribution.
    """
    packages = find_packages()
    packages = [p for p in packages if not p.endswith('_test')]
    return tuple(packages)


class CleanCommand(Command):
    """
    A custom clean command that removes any intermediate build directories.
    """

    description = 'Custom clean command that forcefully removes build, dist,' \
                  ' and other similar directories.'
    user_options = []

    def __init__(self, *args, **kwargs):
        """Initialized the custom clean command with a list of directories."""
        super(CleanCommand, self).__init__(*args, **kwargs)
        project_path = Path(__file__).resolve().parent
        self._clean_paths = {
            'build',
            'dist',
            PROJECT_NAME + '.egg-info',
        }
        self._clean_paths = {project_path.joinpath(p)
                             for p in self._clean_paths}
        self._clean_paths = {d for d in self._clean_paths if d.exists()}

    def initialize_options(self):
        """Unused, but required when implementing :class:`Command`."""
        pass

    def finalize_options(self):
        """Unused, but required when implementing :class:`Command`."""
        pass

    def run(self):
        """Performs the actual removal of the intermediate build directories."""
        for path in self._clean_paths:
            print(f'removing {path}')
            rmtree(path)


setup(name=PROJECT_NAME,
      version=PROJECT_VERSION,

      author='Mike Durso',
      author_email='rbprogrammer@gmail.com',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
      ],
      cmdclass={'clean': CleanCommand},
      install_requires=(),
      description='Another XDG Base Directory Specification utility.',
      long_description=read_file(get_repo_file('README.md')),
      long_description_content_type="text/markdown",
      packages=get_xdgenvpy_packages(),
      scripts=('bin/xdg-env',),
      tests_require=(),
      url='https://gitlab.com/rbprogrammer/xdgenvpy',
      )
