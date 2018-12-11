#!/usr/bin/python3
"""
This script performs a few checkouts on branches on robotpkg, and then tries to compile and test everything
"""
import argparse
import logging
import os
import socket
import subprocess
from pathlib import Path
from shutil import rmtree

# Shell colors
BOLD = '\033[1m'
RED = '\033[1;31m'
GREEN = '\033[1;32m'
PURPLE = '\033[1;35m'
NC = '\033[0m'

# Robotpkg configuration
ACCEPTABLE_LICENSES = [
    'openhrp-grx-license', 'cnrs-hpp-closed-source', 'gnu-gpl', 'motion-analysis-license', 'pal-license'
]
PREFER_SYSTEM = [
    'gnupg', 'urdfdom', 'urdfdom-headers', 'ros-catkin', 'ros-comm', 'ros-genlisp', 'ros-message-generation',
    'ros-std-msgs', 'ros-rospack', 'ros-message-runtime', 'ros-roscpp-core', 'ros-xacro', 'ros-common-msgs',
    'ros-lint', 'ros-com-msgs', 'ros-com-msgs', 'bullet', 'ros-ros', 'ros-cmake-modules', 'ros-dynamic-reconfigure',
    'ros-realtime-tools', 'ros-control-toolbox', 'ros-bond-core', 'ros-class-loader', 'ros-pluginlib', 'ros-rqt',
    'ros-humanoid-msgs', 'ros-genmsg', 'ros-actionlib', 'ros-geometry', 'collada-dom', 'orocos-kdl', 'ros-angles ',
    'ros-console-bridge', 'ros-eigen-stl-containers', 'ros-random-numbers', 'ros-resource-retriever',
    'ros-shape-tools', 'ros-geometric-shapes', 'ros-srdfdom', 'ros-robot-model', 'ros-orocos-kdl', 'assimp'
]

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('robotpkg_root', nargs='?', type=Path, default=Path.home() / 'devel-src/robotpkg-test-rc')
parser.add_argument('-v', '--verbose', action='count', default=0)
parser.add_argument('-d', '--delete', action='store_true')
parser.add_argument('-c', '--clean', action='store_true')
parser.add_argument('--robotpkg_git', default='https://git.openrobots.org/robots/robotpkg.git')
parser.add_argument('--robotpkg_wip_git', default='ssh://git@git.openrobots.org/robots/robotpkg/robotpkg-wip')
parser.add_argument('--conf', type=Path)


def env_join(base, dirs, old=None):
    """
    format an environment variable with <dirs> in <base>, and eventually keep <old> value at the end
    """
    paths = [str(Path(base) / path) for path in dirs]
    if old is not None:
        paths += old.split(':')
    return ':'.join(paths)


class RobotpkgTestRC:
    def __init__(self, robotpkg_root, verbose, delete, clean, robotpkg_git, robotpkg_wip_git, conf):
        """ Init environment variables
        """
        self.robotpkg_root = robotpkg_root
        self.robotpkg_base = self.robotpkg_root / 'install'
        self.delete = delete
        self.clean = clean
        self.robotpkg_git = robotpkg_git
        self.robotpkg_wip_git = robotpkg_wip_git
        self.conf = conf

        logging.basicConfig(format='%(message)s', level=40 - verbose * 10)
        logging.critical('enabled logging of CRITICALs')
        logging.error(RED + 'enabled logging of ERRORs' + NC)
        logging.warning(PURPLE + 'enabled logging of WARNINGs' + NC)
        logging.info(GREEN + 'enabled logging of INFOs' + NC)
        logging.debug(BOLD + 'enabled logging of DEBUGs\n' + NC)

        self.init_environment_variables()
        self.init_robotpkg_conf_add()

    def init_environment_variables(self):
        """Prepare the environment variables.

        Specifies the environment when starting commands
        """
        self.env = os.environ.copy()
        self.env["ROBOTPKG_BASE"] = str(self.robotpkg_base)
        # For binaries
        self.env["PATH"] = env_join(self.robotpkg_base, ['sbin', 'bin'], self.env['PATH'])

        # For libraries
        self.env["LD_LIBRARY_PATH"] = env_join(self.robotpkg_base, ['lib', 'lib/plugin', 'lib64'],
                                               self.env.get('LD_LIBRARY_PATH'))

        # For python
        self.env["PYTHON_PATH"] = env_join(self.robotpkg_base,
                                           ['lib/python2.7/site-packages', 'lib/python2.7/dist-packages'],
                                           self.env.get('PYTHON_PATH', ''))

        # For pkgconfig
        self.env["PKG_CONFIG_PATH"] = env_join(self.robotpkg_base, ['lib/pkgconfig'],
                                               self.env.get("PKG_CONFIG_PATH", ''))

        # For ros packages
        self.env["ROS_PACKAGE_PATH"] = env_join(self.robotpkg_base, ['share', 'stacks'],
                                                self.env.get("ROS_PACKAGE_PATH", ''))

        # For cmake
        self.env["CMAKE_PREFIX_PATH"] = str(self.robotpkg_base) + ':' + self.env.get("CMAKE_PREFIX_PATH", '')

    def init_robotpkg_conf_add(self):
        self.robotpkg_conf_lines = ['ROS_PACKAGE_PATH=${ROBOTPKG_BASE}/share:$ROS_PACKAGE_PATH']
        self.robotpkg_conf_lines += ['ACCEPTABLE_LICENSES += %s' % license for license in ACCEPTABLE_LICENSES]
        self.robotpkg_conf_lines += ['PREFER.%s = system' % pkg for pkg in PREFER_SYSTEM]

    def execute(self, command, cwd=None):
        """ Execute command

        Keyword arguments:
        command -- the command to be run
        cwd -- the Current Working Directory in which execute the command

        It returns a list of binary string that can be iterate
        and decode.

        """
        logging.debug(BOLD + "execute command: %s" + NC, command)
        outputdata = subprocess.check_output(command.split(), env=self.env, cwd=str(cwd), universal_newlines=True)
        for stdout_line in outputdata.splitlines():
            logging.debug(BOLD + stdout_line + NC)
        return outputdata

    def prepare_robotpkg(self):
        """
        Prepare the robotpkg environment

        Make robotpkg directoriers, clone it with wip, bootstrap and add
        information in the file ${ROBOTPKG_BASE}/etc/robotpkg.conf
        """
        self.make_robotpkg_dirs()
        self.cloning_robotpkg_main()
        self.cloning_robotpkg_wip()
        self.bootstrap_robotpkg()
        self.complete_robotpkg_conffile()

    def make_robotpkg_dirs(self):
        """
        Create directories for robotpkg
        and eventually delete or clean them, depending on the argparser's options
        """
        if self.delete and self.robotpkg_root.is_dir():
            logging.warning(PURPLE + 'rm -rf %s' % self.robotpkg_root + NC + '\n')
            rmtree(str(self.robotpkg_root))
        if self.clean:
            if self.robotpkg_base.is_dir():
                logging.warning(PURPLE + 'rm -rf %s' % self.robotpkg_base + NC + '\n')
                rmtree(str(self.robotpkg_base))
        logging.info(GREEN + 'Creating the repositories' + NC)
        self.robotpkg_base.mkdir(parents=True, exist_ok=True)

    def cloning_robotpkg_main(self):
        """Clones the main robotpkg repository"""
        logging.info(GREEN + 'Cloning robotpkg' + NC + '\n')
        if (self.robotpkg_root / 'robotpkg').exists():
            self.execute("git pull", cwd=self.robotpkg_root / 'robotpkg')
        else:
            self.execute("git clone %s" % self.robotpkg_git, cwd=self.robotpkg_root)

    def cloning_robotpkg_wip(self):
        """Clones the wip robotpkg repository"""
        logging.info(GREEN + 'Cloning robotpkg/wip' + NC + '\n')
        if (self.robotpkg_root / 'robotpkg/wip').exists():
            self.execute("git pull", cwd=self.robotpkg_root / 'robotpkg/wip')
        else:
            self.execute("git clone %s wip" % self.robotpkg_wip_git, cwd=self.robotpkg_root / 'robotpkg')

    def bootstrap_robotpkg(self):
        """ bootstrap robotpkg

        This method calls:
        bootstrap --prefix=${robotpkg_base}
        only if there is no
        ${robotpkg_base}/etc/robotpkg.conf
        already present.
        """
        # Test if a file in robotpkg_base/etc/robotpkg.conf already exists
        rpkg_conf_file = self.robotpkg_base / 'etc/robotpkg.conf'
        if rpkg_conf_file.is_file():
            logging.warning(PURPLE + str(rpkg_conf_file) + NC + ' already exists\n')
            return
        logging.info(GREEN + 'Boostrap robotpkg' + NC + '\n')
        self.execute('./bootstrap --prefix=%s' % self.robotpkg_base, cwd=self.robotpkg_root / 'robotpkg/bootstrap')

    def complete_robotpkg_conffile(self):
        """Add the contents of robotpkg_conf_lines in robotpkg.conf file

        Avoid to add two times the same information.
        """
        logging.info(GREEN + 'Adding information to ' + str(self.robotpkg_base) + '/etc/robotpkg.conf\n')

        # Open the file, read it and stores it in file_robotpkg_contents
        with (self.robotpkg_base / 'etc/robotpkg.conf').open() as file_robotpkgconf:
            file_robotpkgconf_contents = file_robotpkgconf.read()

        # Append the optional conf file given as parameter
        if self.conf is not None and self.conf.exists():
            with self.conf.open() as f:
                file_robotpkgconf_contents += f.read()

        # Add new lines at the end of robotpkg.conf file.
        with (self.robotpkg_base / 'etc/robotpkg.conf').open('a') as file_robotpkgconf:
            for stdout_line in self.robotpkg_conf_lines:
                if file_robotpkgconf_contents.find(stdout_line) == -1:
                    file_robotpkgconf.write(stdout_line + '\n')

    def build_rpkg_checkout_package(self, packagename, category):
        ''' Execute cmd in the working directory of packagename'''
        # Going into the repository directory
        pathname = self.robotpkg_root / 'robotpkg' / category / packagename / ('work.' + socket.gethostname())
        return pathname

    def apply_rpkg_checkout_package(self, packagename, branchname, category):
        """ Performs a make checkout in packagename directory

        packagename: The name of package in which the git clone will be perfomed.
        branchname: The name of the branch used in the repository.
        category: the category of the package

        The location of the repository is specified in the robotpkg Makefile.
        """
        logging.info(GREEN + 'Checkout ' + packagename + ' in robotpkg/' + category + NC + '\n')
        # Checking if we need to clean or not the package

        # First check if the working directory exists
        directory_to_clean = True
        checkoutdir_packagename = self.build_rpkg_checkout_package(packagename, category)

        if checkoutdir_packagename.exists():
            logging.debug(BOLD + 'Going into :\n' + str(checkoutdir_packagename) + NC)

            # If it does then maybe this is not a git directory
            for folder in checkoutdir_packagename.iterdir():
                if not folder.is_dir():
                    continue
                logging.debug(BOLD + "Going into: %s" % folder + NC)
                # Check if there is a git folder
                if (folder / '.git').is_dir():
                    logging.debug(BOLD + 'Git folder found' + NC)
                    # Now that we detected a git folder
                    # Check the branch
                    outputdata = self.execute("git symbolic-ref --short -q HEAD", cwd=folder)
                    for stdout_line in outputdata.splitlines():
                        if stdout_line != branchname:
                            logging.error(RED + ' Wrong branch name: ' + stdout_line + ' instead of ' +
                                              branchname + NC)
                        else:
                            finaldirectory = folder
                            directory_to_clean = False
                    break

        logging.debug(BOLD + 'Directory to clean: ' + str(directory_to_clean) + NC)
        if directory_to_clean:
            # Going into the directory of the package
            cwd = self.robotpkg_root / 'robotpkg' / category / packagename
            self.execute("make clean confirm", cwd=cwd)
            self.execute("make checkout", cwd=cwd)
        else:
            # Remove all the files which may have been modified.
            self.execute("git reset --hard", cwd=finaldirectory)
            # Pull all the modification push upstream.
            self.execute("git pull origin " + branchname + ':' + branchname, cwd=finaldirectory)
            self.execute("git submodule update", cwd=finaldirectory)

    def apply_git_checkout_branch(self, packagename, branchname, category):
        """
        Changes the branch of a git repository in robotpkg.

        The method first detects that the package working directory is
        really a git repository. Then it performs the branch switch.
        """
        checkoutdir_packagename = self.build_rpkg_checkout_package(packagename, category)
        for folder in checkoutdir_packagename.iterdir():
            if not folder.is_dir():
                continue
            logging.debug(BOLD + "Going into: %s" % folder + NC)
            if (folder / '.git').is_dir():
                self.execute('git checkout ' + branchname, cwd=folder)
                self.execute('git submodule update', cwd=folder)

    def compile_package(self, packagename, category):
        """ Performs make replace confirm in package working directory
        """
        # Going into the directory of the package
        logging.info(GREEN + 'Compile ' + packagename + ' in robotpkg/' + category + NC + '\n')
        # Compiling the repository
        self.execute("make replace confirm", cwd=self.robotpkg_root / 'robotpkg' / category / packagename)

    def handle_package(self, packagename, branchname, category):
        """Compile and install packagename with branch branchname

        First performs the proper make checkout and git operation to get the branch
        Then compile the package with make replace.
        Do not use make update confirm, this install the release version (the tar file).
        """
        self.apply_rpkg_checkout_package(packagename, branchname, category)
        self.apply_git_checkout_branch(packagename, branchname, category)
        self.compile_package(packagename, category)

    def perform_test(self, arch_release_candidates):
        """Install packages specifued by release_candidates

        arch_release_candidates: tuple of triples [ ('category', 'package_name','branch_name'), ... ]
        """
        self.prepare_robotpkg()
        for category, package_name, branch_name in arch_release_candidates:
            self.handle_package(package_name, branch_name, category)


arch_release_candidates = [
    ('math', 'pinocchio', 'devel'),
    ('math', 'py-pinocchio', 'devel'),
    ('wip', 'sot-core-v3', 'topic/pinocchio_v2'),
    ('wip', 'py-sot-core-v3', 'topic/pinocchio_v2'),
    ('wip', 'sot-dynamic-pinocchio-v3', 'topic/pinocchio_v2'),
    ('wip', 'py-sot-dynamic-pinocchio-v3', 'topic/pinocchio_v2'),
    ('wip', 'sot-talos', 'master'),
]

if __name__ == '__main__':
    RobotpkgTestRC(**vars(parser.parse_args())).perform_test(arch_release_candidates)
