#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Installation:
    You shouldnt need to install the python package if you are using this as a
    vim plugin. Is should find it via the path.

Developing:
    git clone https://github.com/Erotemic/vimtk.git
    pip install -e vimtk
"""
from setuptools import setup
from setuptools import find_packages
import sys


def parse_version(package):
    """
    Statically parse the version number from __init__.py

    CommandLine:
        python -c "import setup; print(setup.parse_version('vimtk'))"
    """
    from os.path import dirname, join
    import ast
    init_fpath = join(dirname(__file__), package, '__init__.py')
    with open(init_fpath) as file_:
        sourcecode = file_.read()
    pt = ast.parse(sourcecode)
    class VersionVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            for target in node.targets:
                if target.id == '__version__':
                    self.version = node.value.s
    visitor = VersionVisitor()
    visitor.visit(pt)
    return visitor.version


def parse_requirements(fname='requirements.txt'):
    """
    Parse the package dependencies listed in a requirements file but strips
    specific versioning information.

    TODO:
        perhaps use https://github.com/davidfischer/requirements-parser instead

    CommandLine:
        python -c "import setup; print(setup.parse_requirements())"
    """
    from os.path import exists
    import re
    require_fpath = fname

    def parse_line(line):
        """
        Parse information from a line in a requirements text file
        """
        if line.startswith('-r '):
            # Allow specifying requirements in other files
            target = line.split(' ')[1]
            for info in parse_require_file(target):
                yield info
        elif line.startswith('-e '):
            info = {}
            info['package'] = line.split('#egg=')[1]
            yield info
        else:
            # Remove versioning from the package
            pat = '(' + '|'.join(['>=', '==', '>']) + ')'
            parts = re.split(pat, line, maxsplit=1)
            parts = [p.strip() for p in parts]

            info = {}
            info['package'] = parts[0]
            if len(parts) > 1:
                op, rest = parts[1:]
                if ';' in rest:
                    # Handle platform specific dependencies
                    # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-platform-specific-dependencies
                    version, platform_deps = map(str.strip, rest.split(';'))
                    info['platform_deps'] = platform_deps
                else:
                    version = rest  # NOQA
                info['version'] = (op, version)
            yield info

    def parse_require_file(fpath):
        with open(fpath, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    for info in parse_line(line):
                        yield info

    # This breaks on pip install, so check that it exists.
    packages = []
    if exists(require_fpath):
        for info in parse_require_file(require_fpath):
            package = info['package']
            if not sys.version.startswith('3.4'):
                # apparently package_deps are broken in 3.4
                platform_deps = info.get('platform_deps')
                if platform_deps is not None:
                    package += ';' + platform_deps
            packages.append(package)
    return packages


def parse_description():
    """
    Parse the description in the README file

    CommandLine:
        pandoc --from=markdown --to=rst --output=README.rst README.md
        python -c "import setup; print(setup.parse_description())"
    """
    from os.path import dirname, join, exists
    readme_fpath = join(dirname(__file__), 'README.rst')
    # This breaks on pip install, so check that it exists.
    if exists(readme_fpath):
        with open(readme_fpath, 'r') as f:
            text = f.read()
        return text
    return ''


version = parse_version('vimtk')  # needs to be a global var for git tags

if __name__ == '__main__':
    setup(
        name='vimtk',
        version=version,
        author='Jon Crall',
        description='Python backend for vimtk plugin',
        long_description=parse_description(),
        long_description_content_type='text/x-rst',
        # install_requires=parse_requirements('requirements/runtime.txt'),
        # extras_require={
        #     'all': parse_requirements('requirements.txt'),
        #     'tests': parse_requirements('requirements/tests.txt'),
        #     'optional': parse_requirements('requirements/optional.txt'),
        # },
        include_package_data=True,
        package_data={
            'vim': [
                'plugin',
                'autoload',
            ],
        },
        author_email='erotemic@gmail.com',
        keywords='vim, gvim, python',
        url='https://github.com/Erotemic/vimtk',
        license='Apache 2',
        # packages=['vimtk' 'vimtk._demo', 'vimtk._demo.vimmock'],
        packages=find_packages(include='vimtk.*'),
        classifiers=[
            # List of classifiers available at:
            # https://pypi.python.org/pypi?%3Aaction=list_classifiers
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            "Topic :: Text Editors",
            # This should be interpreted as Apache License v2.0
            'License :: OSI Approved :: Apache Software License',
            # Supported Python versions
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
        ],
    )
