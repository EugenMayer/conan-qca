from conans import ConanFile, CMake, tools

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
    requires = [
        "qt/5.13.2@kwconan/stable",
        "openssl/1.1.1d"
    ]
    scm = {
        "type": "git",
        "url": "https://github.com/KDE/qca.git",
        "revision": "v2.2.1"
    }
    exports = ["patches/*.patch"]

    def source(self):
        tools.patch(patch_file="patches/qca_relative_imported_include_path.patch")


    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["USE_RELATIVE_PATHS"] = "ON" # Make QCA (try to) avoid absolute (conan-specific) paths
        cmake.definitions["CMAKE_INSTALL_SO_NO_EXE"] = "OFF" # Force CMake to set execution permission, even on Debian-based build systems
        cmake.definitions["CMAKE_INSTALL_RPATH"] = '\\$ORIGIN:\\$ORIGIN/lib:\\$ORIGIN/../lib:.:lib:../lib' # Do not load other libraries, only local ones!
        cmake.definitions["CMAKE_EXE_LINKER_FLAGS"] = '-Wl,--unresolved-symbols=ignore-in-shared-libs' # Do not complain about missing transitive dependencies while linking!
        cmake.definitions["CMAKE_SHARED_LINKER_FLAGS"] = '-Wl,--unresolved-symbols=ignore-in-shared-libs' # Do not complain about missing transitive dependencies while linking!
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
