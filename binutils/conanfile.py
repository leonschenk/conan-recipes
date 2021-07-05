from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class BinutilsConan(ConanFile):
    name = "binutils"
    version = "2.36.1"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Binutils here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    build_requires = "flex/2.6.4", "bison/3.7.1"

    def layout(self):
        self.folders.source = 'src'
        self.folders.build = 'build'
        self.folders.package = 'package'

    def source(self):
        tools.get(
          **self.conan_data["sources"][self.version],
          destination=self.folders.source_folder,
          strip_root=True
        )

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir=self.folders.source_folder,args=['--disable-multilib'],target='x86_64-w64-mingw32')
        autotools.make()

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.install()

    def package_info(self):
        bin_folder = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bin_folder))
        self.env_info.PATH.append(bin_folder)
#        self.env_info.CHOST = os.path.join(bin_folder, 'x86_64-w64-mingw32')
#        self.env_info.AR = os.path.join(bin_folder, 'x86_64-w64-mingw32-ar')
#        self.env_info.AS = os.path.join(bin_folder, 'x86_64-w64-mingw32-as')
#        self.env_info.RANLIB = os.path.join(bin_folder, 'x86_64-w64-mingw32-ranlib')
#        self.env_info.LD = os.path.join(bin_folder, 'x86_64-w64-mingw32-ld')
#        self.env_info.STRIP = os.path.join(bin_folder, 'x86_64-w64-mingw32-strip')
#        self.env_info.RC = os.path.join(bin_folder, 'x86_64-w64-mingw32-windres')
