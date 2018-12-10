#!/usr/bin/python3
import os
import socket
import subprocess
from pathlib import Path


class RobotpkgTestRC:
    def __init__(self, ROBOTPKG_ROOT=None):
        """ Init colors and  environment variables

        Arguments:
        ROBOTPKG_ROOT: The directory where the whole robotpkg install takes place.
        """
        if ROBOTPKG_ROOT is None:
            self.ROBOTPKG_ROOT = str(Path.home()) + '/devel-src/robotpkg-test-rc'
        else:
            self.ROBOTPKG_ROOT = ROBOTPKG_ROOT

        self.init_colors()
        self.init_environment_variables(self.ROBOTPKG_ROOT)
        self.init_robotpkg_conf_add()
        self.debug = 0

    def init_colors(self):
        """ Initialize colors for beautification

        The following variables are available:
        REG, GREEN, PURPLE, NC (no color)
        """
        self.RED = '\033[0;31m'
        self.GREEN = '\033[0;32m'
        self.PURPLE = '\033[0;35m'
        self.NC = '\033[0m'

    def init_environment_variables(self, ROBOTPKG_ROOT):
        """Prepare the environment variables.

        Specifies the environment when starting bash commands
        """
        self.ROBOTPKG_ROOT = ROBOTPKG_ROOT
        self.env = os.environ.copy()
        ROBOTPKG_BASE = self.ROBOTPKG_ROOT + '/install'
        self.env["ROBOTPKG_BASE"] = ROBOTPKG_BASE
        # Imposes bash as the shell
        self.env["SHELL"] = "/usr/bin/bash"
        # For binaries
        self.env["PATH"] = ROBOTPKG_BASE+'/sbin:' + \
            ROBOTPKG_BASE+'/bin:'+self.env["PATH"]

        # For libraries
        prev_LD_LIBRARY_PATH = ''
        if "LD_LIBRARY_PATH" in self.env:
            prev_LD_LIBRARY_PATH = self.env["LD_LIBRARY_PATH"]
        self.env["LD_LIBRARY_PATH"] = ROBOTPKG_BASE+'/lib:' \
            +ROBOTPKG_BASE+'/lib/plugin:' \
            +ROBOTPKG_BASE+'/lib64:' \
            +prev_LD_LIBRARY_PATH

        # For python
        prev_PYTHON_PATH = ''
        if "PYTHON_PATH" in self.env:
            prev_PYTHON_PATH = self.env["PYTHON_PATH"]
        self.env["PYTHON_PATH"]=ROBOTPKG_BASE+'/lib/python2.7/site-packages:' \
            +ROBOTPKG_BASE+'/lib/python2.7/dist-packages:' \
            +prev_PYTHON_PATH

        # For pkgconfig
        prev_PKG_CONFIG_PATH = ''
        if "PKG_CONFIG_PATH" in self.env:
            prev_PKG_CONFIG_PATH = self.env["PKG_CONFIG_PATH"]

        self.env["PKG_CONFIG_PATH"]=ROBOTPKG_BASE+'/lib/pkgconfig:' \
            +prev_PKG_CONFIG_PATH

        # For ros packages
        prev_ROS_PACKAGE_PATH = ''
        if "ROS_PACKAGE_PATH" in self.env:
            prev_ROS_PACKAGE_PATH = self.env["ROS_PACKAGE_PATH"]

        self.env["ROS_PACKAGE_PATH"]=ROBOTPKG_BASE+'/share:' \
            +ROBOTPKG_BASE+'/stacks' \
            +prev_ROS_PACKAGE_PATH

        # For cmake
        prev_CMAKE_PREFIX_PATH = ''
        if "CMAKE_PREFIX_PATH" in self.env:
            prev_CMAKE_PREFIX_PATH = self.env["CMAKE_PREFIX_PATH"]

        self.env["CMAKE_PREFIX_PATH"] = ROBOTPKG_BASE + ':' + prev_CMAKE_PREFIX_PATH

    def init_robotpkg_conf_add(self):
        self.robotpkg_conf_lines = [
            'ACCEPTABLE_LICENSES+=openhrp-grx-license', 'ACCEPTABLE_LICENSES+=cnrs-hpp-closed-source',
            'ACCEPTABLE_LICENSES+=gnu-gpl', 'ACCEPTABLE_LICENSES+=motion-analysis-license', 'PREFER.gnupg=system',
            'PREFER.urdfdom=system', 'PREFER.urdfdom-headers=system', 'PREFER.ros-catkin = system',
            'PREFER.ros-comm = system', 'PREFER.ros-genlisp = system', 'PREFER.ros-message-generation = system',
            'PREFER.ros-std-msgs = system', 'PREFER.ros-rospack = system', 'PREFER.ros-message-runtime = system',
            'PREFER.ros-roscpp-core = system', 'PREFER.ros-xacro = system', 'PREFER.ros-common-msgs = system',
            'PREFER.ros-lint = system', 'PREFER.ros-com-msgs = system', 'PREFER.ros-com-msgs = system',
            'PREFER.bullet = system', 'PREFER.ros-ros = system', 'PREFER.ros-cmake-modules = system',
            'PREFER.ros-dynamic-reconfigure = system', 'PREFER.ros-realtime-tools = system',
            'PREFER.ros-control-toolbox = system', 'PREFER.ros-bond-core = system', 'PREFER.ros-class-loader = system',
            'PREFER.ros-pluginlib = system', 'PREFER.ros-rqt = system', 'PREFER.ros-humanoid-msgs = system',
            'PREFER.ros-genmsg = system', 'PREFER.ros-actionlib = system', 'PREFER.ros-geometry = system',
            'PREFER.collada-dom = system', 'PREFER.orocos-kdl = system', 'PREFER.ros-angles  = system',
            'PREFER.ros-console-bridge = system', 'PREFER.ros-eigen-stl-containers = system',
            'PREFER.ros-random-numbers = system', 'PREFER.ros-resource-retriever = system',
            'PREFER.ros-shape-tools = system', 'PREFER.ros-geometric-shapes = system', 'PREFER.ros-srdfdom = system',
            'PREFER.ros-robot-model = system', 'PREFER.ros-orocos-kdl = system', 'PREFER.assimp=system',
            'ACCEPTABLE_LICENSES+=pal-license', 'ROS_PACKAGE_PATH=${ROBOTPKG_ROOT}/install/share:$ROS_PACKAGE_PATH	'
        ]

    def execute(self, bashCommand):
        """ Execute baschCommand

        Keyword arguments:
        bashCommand -- the bashCommand to be run in a bash script

        It returns a list of binary string that can be iterate
        and decode.

        """
        # TODO: Handle error
        if self.debug > 3:
            print("execute bash command: " + bashCommand)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, env=self.env)
        outputdata, error = process.communicate()
        for stdout_line in outputdata.splitlines():
            print(stdout_line.decode('ascii'))
        return outputdata

    def prepare_robotpkg(self):
        """
        Prepare the robotpkg environment

        Make robotpkg directoriers, clone it with wip, bootstrap and add
        information in the file ${ROBOTPKG_ROOT}/install/etc/robotpkg.conf
        """
        self.make_robotpkg_dirs()
        self.cloning_robotpkg_main()
        self.cloning_robotpkg_wip()
        self.bootstrap_robotpkg()
        self.complete_robotpkg_conffile()

    def make_robotpkg_dirs(self):
        """Create directories for robotpkg

        ROBOTPKG_ROOT
        ROBOTPKG_ROOT/install
        """
        print(self.GREEN + 'Creating the repositories' + self.NC)
        dirname = self.ROBOTPKG_ROOT + '/'
        os.makedirs(dirname, 0o777, True)
        dirname = self.ROBOTPKG_ROOT + '/install'
        os.makedirs(dirname, 0o777, True)

    def cloning_robotpkg_main(self):
        """Clones the main robotpkg repository"""
        print(self.GREEN + 'Cloning robotpkg' + self.NC + '\n')
        os.chdir(self.ROBOTPKG_ROOT)
        self.execute("git clone https://git.openrobots.org/robots/robotpkg.git")

    def cloning_robotpkg_wip(self):
        """Clones the wip robotpkg repository"""
        os.chdir(self.ROBOTPKG_ROOT + '/robotpkg')
        print(self.GREEN + 'Cloning robotpkg/wip' + self.NC + '\n')
        self.execute("git clone ssh://git@git.openrobots.org/robots/robotpkg/robotpkg-wip wip")

    def bootstrap_robotpkg(self):
        """ bootstrap robotpkg

        This method calls:
        bootstrap --prefix=${ROBOTPKG_ROOT}/install
        only if there is no
        ${ROBOTPKG_ROOT}/install/etc/robotpkg.conf
        already present.
        """
        # Test if a file in ROBOTPKG_ROOT/install/etc/robotpkg.conf already exists
        rpkg_conf_filename = self.ROBOTPKG_ROOT + '/install/etc/robotpkg.conf'
        rpkg_conf_file = Path(rpkg_conf_filename)
        if rpkg_conf_file.is_file():
            print(self.PURPLE + rpkg_conf_filename + self.NC + ' already exists\n')
            return
        os.chdir(self.ROBOTPKG_ROOT + '/robotpkg/bootstrap')
        print(self.GREEN + 'Boostrap robotpkg' + self.NC + '\n')
        self.execute('./bootstrap --prefix=' + self.ROBOTPKG_ROOT + '/install')

    def complete_robotpkg_conffile(self):
        """Add the contents of robotpkg_conf_lines in robotpkg.conf file

        Avoid to add two times the same information.
        """
        os.chdir(self.ROBOTPKG_ROOT + '/install/etc')
        print(self.GREEN + 'Adding information to ' + self.ROBOTPKG_ROOT + '/install/etc/robotpkg.conf\n')

        # Open the file, read it and stores it in file_robotpkg_contents
        file_robotpkgconf = open("robotpkg.conf", 'r')
        file_robotpkgconf_contents = file_robotpkgconf.read()
        file_robotpkgconf.close()

        # Add new lines at the end of robotpkg.conf file.
        file_robotpkgconf = open("robotpkg.conf", 'a')
        for stdout_line in self.robotpkg_conf_lines:
            if file_robotpkgconf_contents.find(stdout_line) == -1:
                file_robotpkgconf.write(stdout_line + '\n')
        file_robotpkgconf.close()

    def build_rpkg_checkout_package(self, packagename):
        ''' Execute bashcmd in the working directory of packagename'''
        # Going into the repository directory
        hostname = socket.gethostname()
        pathname = self.ROBOTPKG_ROOT + '/robotpkg/wip/' + packagename + '/work.' + hostname
        return pathname

    def apply_rpkg_checkout_package(self, packagename, branchname):
        """ Performs a make checkout in packagename directory

        packagename: The name of package in which the git clone will be perfomed.
        branchname: The name of the branch used in the repository.

        The location of the repository is specified in the robotpkg Makefile.
        """
        print(self.GREEN + 'Checkout ' + packagename + ' in robotpkg/wip' + self.NC + '\n')
        # Checking if we need to clean or not the package

        # First check if the working directory exists
        directory_to_clean = True
        checkoutdir_packagename = self.build_rpkg_checkout_package(packagename)

        if os.path.isdir(checkoutdir_packagename):
            if self.debug > 3:
                print('Going into :\n' + checkoutdir_packagename)
            os.chdir(checkoutdir_packagename)

            # If it does then maybe this is not a git directory
            folders = [f.path for f in os.scandir(checkoutdir_packagename) if f.is_dir()]
            for folder in folders:
                if self.debug > 3:
                    print("Going into: " + folder)
                os.chdir(folder)
                # Check if there is a git folder
                git_folder = folder + '/.git'
                if os.path.isdir(git_folder):
                    if self.debug > 3:
                        print('Git folder found:')
                    # Now that we detected a git folder
                    # Check the branch
                    outputdata = self.execute("git symbolic-ref --short -q HEAD")
                    for stdout_line in outputdata.splitlines():
                        lstr = str(stdout_line.decode('ascii'))
                        if lstr != branchname:
                            print(self.RED + ' Wrong branch name: ' + lstr + ' instead of ' + branchname + self.NC)
                        else:
                            finaldirectory = folder
                            directory_to_clean = False

        if self.debug > 3:
            print('Directory to clean: ' + str(directory_to_clean))
        if directory_to_clean:
            # Going into the directory of the package
            os.chdir(self.ROBOTPKG_ROOT + '/robotpkg/wip/' + packagename)
            self.execute("make clean confirm")
            self.execute("make checkout")
        else:
            os.chdir(finaldirectory)
            # Remove all the files which may have been modified.
            self.execute("git reset --hard")
            # Pull all the modification push upstream.
            self.execute("git pull origin " + branchname + ':' + branchname)

    def apply_git_checkout_branch(self, packagename, branchname):
        """
        Changes the branch of a git repository in robotpkg.

        The method first detects that the package working directory is
        really a git repository. Then it performs the branch switch.
        """
        bashcmd = 'git checkout ' + branchname
        checkoutdir_packagename = self.build_rpkg_checkout_package(packagename)
        folders = [f.path for f in os.scandir(checkoutdir_packagename) if f.is_dir()]
        for folder in folders:
            if self.debug > 3:
                print("Going into: " + folder)
            os.chdir(folder)
            git_folder = folder + '/.git'
            if os.path.isdir(git_folder):
                self.execute(bashcmd)

    def compile_package(self, packagename):
        """ Performs make replace confirm in package working directory
        """
        # Going into the directory of the package
        os.chdir(self.ROBOTPKG_ROOT + '/robotpkg/wip/' + packagename)
        print(self.GREEN + 'Compile ' + packagename + ' in robotpkg/wip' + self.NC + '\n')
        # Compiling the repository
        self.execute("make replace confirm")

    def handle_package(self, packagename, branchname):
        """Compile and install packagename with branch branchname

        First performs the proper make checkout and git operation to get the branch
        Then compile the package with make replace.
        Do not use make update confirm, this install the release version (the tar file).
        """
        self.apply_rpkg_checkout_package(packagename, branchname)
        self.apply_git_checkout_branch(packagename, branchname)
        self.compile_package(packagename)

    def perform_test(self, arch_release_candidates):
        """Install packages specifued by release_candidates

        arch_release_candidates: tuple of pair [ ('package_name','branch_name'), ... ]
        """
        self.prepare_robotpkg()
        for package_name, branch_name in arch_release_candidates:
            self.handle_package(package_name, branch_name)


arch_release_candidates = [('dynamic-graph-v3', 'devel'), ('py-dynamic-graph-v3', 'devel'),
                           ('sot-core-v3', 'rc-v3.3.0'), ('py-sot-core-v3', 'rc-v3.3.0'), ('sot-dyninv-v3', 'master'),
                           ('py-sot-dyninv-v3', 'master'), ('sot-dynamic-pinocchio-v3', 'rc-v3.2.4'),
                           ('py-sot-dynamic-pinocchio-v3', 'rc-v3.2.4'), ('roscontrol-sot', 'master')]

arpgtestrc = RobotpkgTestRC()
arpgtestrc.perform_test(arch_release_candidates)
