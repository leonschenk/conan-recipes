from conans import ConanFile, AutoToolsBuildEnvironment, tools

import os

class MingwCrtConan(ConanFile):
    name = "mingw-crt"
    version = "9.0.0"
    license = "<Put the package license here>"
    author = "Leon Schenk <leon_schenk@live.nl>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Binutils here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    requires = "mingw-headers/9.0.0"
    build_requires = "gcc/9.4.0"

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
        autotools.configure(configure_dir=os.path.join(self.folders.source_folder,'mingw-w64-crt'),host='x86_64-w64-mingw32')
        autotools.make()

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.install()

