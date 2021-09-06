from conans import ConanFile, AutoToolsBuildEnvironment, tools, util
from conans.client.build.compiler_flags import format_include_paths
import os
import shutil

class GccConan(ConanFile):
    name = "libgcc"
    version = "9.4.0"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Binutils here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    requires = "mingw-crt/9.0.0"
    build_requires = "gcc/9.4.0"

    def init(self):
        self._args = []

    def generate(self):
        #copy required gcc build environment
        shutil.copytree(self.user_info_build['gcc'].GCC_CONFIG_PATH, os.path.join(self.folders.generators_folder,'gcc-config'))

    def layout(self):
        self.folders.source = 'src'
        self.folders.build = os.path.join('build', 'libgcc', 'build')
        self.folders.package = 'package'

    def source(self):
        gitdata = self.conan_data['sources'][self.version]
        git = tools.Git()
        git.clone(url=gitdata['url'],branch=gitdata['tag'],shallow=True)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        include_path = format_include_paths(self.deps_cpp_info['mingw-headers'].include_paths, self.settings, False, None)
        autotools.flags.extend(include_path)
        autotools.configure(configure_dir=os.path.join(self.folders.source_folder,'libgcc'),args=self._args,host='x86_64-w64-mingw32')
        #create a symlink to the generators directory for the required gcc-config
        if not os.path.isdir(os.path.join(self.folders.build_folder, '..', '..', 'gcc')):
            os.symlink(os.path.join(self.folders.generators_folder,'gcc-config'), os.path.join(self.folders.build_folder, '..', '..', 'gcc'))
        autotools.make()

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.install()
