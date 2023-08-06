#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'xdcs-agent',
        version = '0.1.0.dev20191125215215',
        description = '',
        long_description = '',
        author = 'Kamil Jarosz, Krystian Życiński, Adam Szczerba, Jan Rodzoń',
        author_email = 'kjarosz@student.agh.edu.pl, zycinski@student.agh.edu.pl, adamszczerba19@gmail.com, rodzonjan@wp.pl',
        license = 'GNU GPLv3 ',
        url = 'https://github.com/xdcs-team/xdcs',
        scripts = [],
        packages = [
            'xdcs',
            'xdcs.cmd'
        ],
        namespace_packages = [],
        py_modules = ['__main__'],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {
            'console_scripts': ['xdcs-agent = xdcs.agent_cli:main']
        },
        data_files = [
            ('/usr/config', ['xdcs/conf/xdcs-agent.toml'])
        ],
        package_data = {},
        install_requires = [
            'distro',
            'lazy',
            'packaging',
            'py-cpuinfo',
            'pyopencl'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
        include_package_data=True,
    )
