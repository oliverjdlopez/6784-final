#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "energyplus::energyplusapi" for configuration "Release"
set_property(TARGET energyplus::energyplusapi APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(energyplus::energyplusapi PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/./libenergyplusapi.23.1.0.dylib"
  IMPORTED_SONAME_RELEASE "@executable_path/libenergyplusapi.23.1.0.dylib"
  )

list(APPEND _cmake_import_check_targets energyplus::energyplusapi )
list(APPEND _cmake_import_check_files_for_energyplus::energyplusapi "${_IMPORT_PREFIX}/./libenergyplusapi.23.1.0.dylib" )

# Import target "energyplus::energyplus" for configuration "Release"
set_property(TARGET energyplus::energyplus APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(energyplus::energyplus PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/./energyplus-23.1.0"
  )

list(APPEND _cmake_import_check_targets energyplus::energyplus )
list(APPEND _cmake_import_check_files_for_energyplus::energyplus "${_IMPORT_PREFIX}/./energyplus-23.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
