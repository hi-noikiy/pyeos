if (APPLE)
    set(_symbols_list "${CMAKE_CURRENT_SOURCE_DIR}/symbols.list")
    set(LINK_FLAGS "${LINK_FLAGS} -Wl,-exported_symbols_list,'${_symbols_list}'")
else()
    set(_version_script "${CMAKE_CURRENT_SOURCE_DIR}/version.script")
    set(LINK_FLAGS "${LINK_FLAGS} -Wl,--version-script,\"${_version_script}\"")
endif (APPLE)

set(PYTHON3 "LD_LIBRARY_PATH=${CMAKE_SOURCE_DIR}/externals/python;${CMAKE_SOURCE_DIR}/externals/python/dist/bin/python3")

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/vm_cpython.wrap.cpp
    COMMAND ${PYTHON3} -m cython --cplus ${CMAKE_CURRENT_SOURCE_DIR}/vm_cpython.pyx -o ${CMAKE_CURRENT_SOURCE_DIR}/vm_cpython.wrap.cpp
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/vm_cpython.pyx
)

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/test.wrap.cpp
    COMMAND ${PYTHON3} -m cython --cplus ${CMAKE_CURRENT_SOURCE_DIR}/test.pyx -o ${CMAKE_CURRENT_SOURCE_DIR}/test.wrap.cpp
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/test.pyx
)

add_library(vm_cpython_ss SHARED
            vm_cpython.wrap.cpp
            inspector.wrap.cpp
            opcode.cc
            test.wrap.cpp
            vm_cpython.cpp)

set_target_properties(vm_cpython_ss  PROPERTIES LINK_FLAGS "${LINK_FLAGS}")

target_link_libraries(vm_cpython_ss PRIVATE python3-ss vmapi4python)

target_include_directories(vm_cpython_ss PRIVATE ${Boost_INCLUDE_DIR}
#   PRIVATE ${CMAKE_SOURCE_DIR}/contracts/libc++/upstream/include
#   PRIVATE ${CMAKE_SOURCE_DIR}/contracts/libc++/include/libc++/upstream/include
#   PRIVATE ${CMAKE_SOURCE_DIR}/contracts/libc++/musl/include/musl/upstream/include
#    PRIVATE ${CMAKE_SOURCE_DIR}/contracts/musl/upstream/include
    PRIVATE ${CMAKE_SOURCE_DIR}/externals/magic_get/include
    PRIVATE ${CMAKE_BINARY_DIR}/libraries/appbase/include
    PUBLIC ${CMAKE_SOURCE_DIR}/libraries/chainbase/include
    PUBLIC ${CMAKE_SOURCE_DIR}/libraries/softfloat/source/include

    PUBLIC ${CMAKE_SOURCE_DIR}/externals/python/Include
    PUBLIC ${CMAKE_SOURCE_DIR}/externals/python

    PRIVATE ${CMAKE_BINARY_DIR}/libraries/fc/include
#    PRIVATE ${CMAKE_BINARY_DIR}/libraries/chain/include
    PRIVATE ${CMAKE_SOURCE_DIR}/contracts
)

