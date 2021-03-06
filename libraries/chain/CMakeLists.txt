configure_file(${CMAKE_CURRENT_SOURCE_DIR}/include/eosio/chain/core_symbol.hpp.in ${CMAKE_CURRENT_BINARY_DIR}/include/eosio/chain/core_symbol.hpp)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/genesis_state_root_key.cpp.in ${CMAKE_CURRENT_BINARY_DIR}/genesis_state_root_key.cpp)

file(GLOB HEADERS "include/eosio/chain/*.hpp" "include/eosio/chain/contracts/*.hpp")
#find_package(LevelDB)

set(PYTHON3 "LD_LIBRARY_PATH=${CMAKE_SOURCE_DIR}/externals/python;${CMAKE_SOURCE_DIR}/externals/python/dist/bin/python3")

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/rpc_interface/rpc_interface_.wrap.cpp
    COMMAND ${PYTHON3} -m cython --cplus ${CMAKE_CURRENT_SOURCE_DIR}/rpc_interface/rpc_interface_.pyx -o ${CMAKE_CURRENT_SOURCE_DIR}/rpc_interface/rpc_interface_.wrap.cpp
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/rpc_interface/rpc_interface_.pyx
)

file(GLOB HEADERS "include/eosio/chain/*.hpp"
                  "include/eosio/chain/webassembly/*.hpp"
                  "${CMAKE_CURRENT_BINARY_DIR}/include/eosio/chain/core_symbol.hpp" )

## SORT .cpp by most likely to change / break compile
add_library( eosio_chain
             SHARED
             merkle.cpp
             name.cpp
             transaction.cpp
             block_header.cpp
             block_header_state.cpp
             block_state.cpp
             fork_database.cpp
             controller.cpp
             authorization_manager.cpp
             resource_limits.cpp
             block_log.cpp
             transaction_context.cpp
             eosio_contract.cpp
             eosio_contract_abi.cpp
             chain_config.cpp
             chain_id_type.cpp
             genesis_state.cpp
             ${CMAKE_CURRENT_BINARY_DIR}/genesis_state_root_key.cpp

#             chain_config.cpp
#             block_trace.cpp
#              wast_to_wasm.cpp
              wasm_interface.cpp
#              wasm_eosio_validation.cpp
#              wasm_eosio_injection.cpp
              apply_context.cpp
              abi_serializer.cpp
              asset.cpp

#             webassembly/wavm.cpp
#             webassembly/binaryen.cpp

#             get_config.cpp
#             global_property_object.cpp
#
#             contracts/chain_initializer.cpp
#             transaction_metadata.cpp

#              micropython/mpeoslib.cpp
#              evm_interface.cpp
#              micropython_interface.cpp
              native/native.cpp
              vm_api_native/vm_api.cpp
              ${HEADERS}
             )

#add_library(secp256k STATIC IMPORTED)
#set_property(TARGET secp256k PROPERTY IMPORTED_LOCATION "${CMAKE_SOURCE_DIR}/build/deps/lib/libsecp256k1.a")

if ("${CMAKE_BUILD_TYPE}" STREQUAL "Debug")
   target_compile_options(eosio_chain PUBLIC -DDEBUG)
endif()

target_link_libraries( eosio_chain PUBLIC eosio_prods_static eos_utilities fc chainbase appbase db_api vm_manager softfloat builtins python3 ${OPENSSL_LIBRARIES})

target_include_directories( eosio_chain
                            PUBLIC ${Boost_INCLUDE_DIR}
                            PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include"
                            PUBLIC "${CMAKE_CURRENT_BINARY_DIR}/include"
                            PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/../wasm-jit/Include"
                            PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/../../externals/binaryen/src"
                            PUBLIC ${CMAKE_SOURCE_DIR}/libraries/chain
                            PUBLIC ${CMAKE_SOURCE_DIR}/externals/python/Include
                            PUBLIC ${CMAKE_SOURCE_DIR}/externals/python
                            PUBLIC ${CMAKE_SOURCE_DIR}/contracts
                            PUBLIC ${CMAKE_SOURCE_DIR}/libraries/vm_manager
                            PUBLIC ${CMAKE_SOURCE_DIR}/libraries/vm/vm_wasm
                            PUBLIC ${CMAKE_SOURCE_DIR}/externals/thrift/src
                            PUBLIC ${CMAKE_SOURCE_DIR}/externals/magic_get/include
                            )

install( TARGETS eosio_chain
   RUNTIME DESTINATION ${CMAKE_INSTALL_FULL_BINDIR}
   LIBRARY DESTINATION ${CMAKE_INSTALL_FULL_LIBDIR}
   ARCHIVE DESTINATION ${CMAKE_INSTALL_FULL_LIBDIR}
)
install( DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/eosio/chain/
      DESTINATION ${CMAKE_INSTALL_FULL_INCLUDEDIR}/eosio/chain
      FILES_MATCHING PATTERN "*.hpp" PATTERN "*.h" PATTERN "webassembly" EXCLUDE
)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/include/eosio/chain/core_symbol.hpp DESTINATION ${CMAKE_INSTALL_FULL_INCLUDEDIR}/eosio/chain)
#if(MSVC)
#  set_source_files_properties( db_init.cpp db_block.cpp database.cpp block_log.cpp PROPERTIES COMPILE_FLAGS "/bigobj" )
#endif(MSVC)
