from conans import ConanFile, AutoToolsBuildEnvironment, tools


class BinutilsConan(ConanFile):
    name = "binutils"
    version = "0.1"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Binutils here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    build_requires = "flex/2.6.4"

    def layout(self):
        self.folders.source = 'src'
        self.folders.build = 'build'
        self.folders.package = 'package'

    def source(self):
        git = tools.Git()
        git.clone("https://sourceware.org/git/binutils-gdb.git", "binutils-2_36_1", shallow=True)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir=self.folders.source_folder, target='x86_64-w64-mingw32')
        autotools.make()

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

