from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class GccConan(ConanFile):
    name = "gcc"
    version = "9.4.0"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Binutils here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    requires = "binutils/2.36.1"
    build_requires = "flex/2.6.4", "bison/3.7.1"

    def init(self):
        self._args = ['--disable-multilib','--enable-languages=c,c++']

    def layout(self):
        self.folders.source = 'src'
        self.folders.build = 'build'
        self.folders.package = 'package'

    def source(self):
        gitdata = self.conan_data['sources'][self.version]
        git = tools.Git()
        git.clone(url=gitdata['url'],branch=gitdata['tag'],shallow=True)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir=self.folders.source_folder,args=self._args,target='x86_64-w64-mingw32')
        autotools.make(target='all-gcc')

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.make(target='install-gcc')

    def package_info(self):
        self.env_info.CC = os.path.join(self.folders.package_folder,'bin','x86_64-w64-mingw32-gcc')
        self.env_info.CXX = os.path.join(self.folders.package_folder,'bin','x86_64-w64-mingw32-g++')
        self.env_info.COMPILER_PATH = os.path.join(self.deps_cpp_info['binutils'].rootpath,'x86_64-w64-mingw32','bin')
