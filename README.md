# WAT
Conan packages for Qt Cryptographic Architecture - build from [KDE/qca](https://github.com/KDE/qca)

## Published builds
Into a private conan repository since bintray is no longer.

# Upgrade QCA

- be sure to check if the patches still apply
- change the version in `conanfile.py`
  - the conan-recipe version
  - the SCM tag version 

# Upgrade QT

- change the QT requires version in the `conanfiley.py`
    ```
    requires = [
        "qt/5.14.2@kwconan/stable",
    ```
# Patches

`patches/qca_relative_imported_include_path.patch`
Does fix the issue that for windows libraries are expected in `bin/` but for macOS and linux, they are expected in `lib/`.
This is especially important if QCA is used as a shared lib to link against dynamically in your own project, when dealing with x-platform builds.

Also fixes that QCA's exported include files use a relocatable path.

`patches/qca_target_file_for_configuration.patch`
Fix CMake files when using Visual Studio. Otherwise you will get

```
Error message:
    CMake Error at cmake/modules/QcaMacro.cmake:109 (get_target_property):
      The LOCATION property may not be read from target "qcatool-qt5".  Use the
      target name directly with add_custom_command, or use the generator
      expression $<TARGET_FILE>, as appropriate.
```
