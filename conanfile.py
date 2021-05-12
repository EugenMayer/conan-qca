import os
from conans import ConanFile, CMake, tools
from conans.tools import replace_in_file

class QcaConan(ConanFile):
    name = "qca"
    description = "Qt Cryptographic Architecture"
    version = "2.3.1"
    license = "LGPL 2.1"
    url = "https://github.com/KDE/qca"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True]}
    default_options = "shared=True"
    generators = "cmake_find_package"
    requires = [
        "qt/5.15.2@kwconan/stable",
        "openssl/1.1.1h"
    ]
    scm_to_conandata = True
    scm = {
        "type": "git",
        "url": "https://github.com/KDE/qca.git",
        # when you have to build a specific revision
        "revision": "0684db8255cb0e73bbf00b27210a4ac95472a9d0"
        
        # otherwise rather use the tag
        #"revision": "v2.3.1"
    }
    exports = ["patches/*.patch"]
    revision_mode = "scm"
    
    def source(self):
        tools.patch(patch_file="patches/qca_relative_imported_include_path.patch")
        tools.patch(patch_file="patches/qca_target_file_for_configuration.patch")

        # Fix QCA's CMAKE_MODULE_PATH:
        replace_in_file("CMakeLists.txt",
            'set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules" )',
            'set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH};${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules")',
        )

        # Fix Conan's OpenSSL target:
        # (Conan should export OpenSSL::SSL and ::Crypto, but exports only OpenSSL::OpenSSL)
        replace_in_file(os.path.join("plugins", "qca-ossl", "CMakeLists.txt"),
            'target_link_libraries(qca-ossl OpenSSL::SSL OpenSSL::Crypto)',
            'target_link_libraries(qca-ossl OpenSSL::OpenSSL)',
        )

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["OSX_FRAMEWORK"] = "OFF" # Do not build a framework on macOS, but normal libraries.
        cmake.definitions["USE_RELATIVE_PATHS"] = "ON" # Make QCA (try to) avoid absolute (conan-specific) paths
        if self.settings.os == 'Linux':
            cmake.definitions["CMAKE_INSTALL_RPATH"] = '\\$ORIGIN:\\$ORIGIN/lib:\\$ORIGIN/../lib:.:lib:../lib' # Do not load other libraries, only local ones!
            cmake.definitions["CMAKE_INSTALL_SO_NO_EXE"] = "OFF" # Force CMake to set execution permission, even on Debian-based build systems
            cmake.definitions["CMAKE_EXE_LINKER_FLAGS"] = '-Wl,--unresolved-symbols=ignore-in-shared-libs' # Do not complain about missing transitive dependencies while linking!
            cmake.definitions["CMAKE_SHARED_LINKER_FLAGS"] = '-Wl,--unresolved-symbols=ignore-in-shared-libs' # Do not complain about missing transitive dependencies while linking!
        elif self.settings.os == 'Macos':
            cmake.definitions["CMAKE_INSTALL_RPATH"] = '@executable_path/../lib' # Do not load other libraries, only local ones!
            cmake.definitions["CMAKE_MACOSX_RPATH"] = 'ON' # Make targets that use QCA's libraries use @rpath!
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["qca-qt5.lib"]
        else:
            self.cpp_info.libs = ["qca-qt5"]
