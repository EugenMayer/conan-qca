import os

from conans import ConanFile, tools, CMake
from conans.tools import replace_in_file

class QcaConan(ConanFile):
    name = "qca"
    description = "Qt Cryptographic Architecture"
    version = "2.2.1"
    license = "LGPL 2.1"
    url = "https://github.com/KDE/qca"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True]}
    default_options = "shared=True"
    generators = "cmake_find_package"
    requires = "qt/5.13.1@bincrafters/stable", "openssl/1.1.1d"
    scm = {
        "type": "git",
        "url": "https://github.com/KDE/qca.git",
        "revision": "v2.2.1"
    }

    def build(self):
        cmake = CMake(self) # it will find the packages by using our auto-generated FindXXX.cmake files
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "install"
        cmake.configure()
        cmake.build()
        cmake.install()
        
    def package(self):
        install_dir = "conan_install"
        self.copy("*", src="install", keep_path=True, symlinks=True)
    
    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["qca-qt5.lib"]
        else:
            self.cpp_info.libs = ["qca-qt5"]
