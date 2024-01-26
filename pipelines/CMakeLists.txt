
if( VIAME_ENABLE_PYTHON )
  kwiver_add_python_module(
    ${CMAKE_CURRENT_SOURCE_DIR}/species_detector.py
    arrows/species_detector
    species_detector)
endif()

