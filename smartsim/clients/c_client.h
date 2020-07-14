/* The C wrappers in this file were autogenerated by c_code_generator.py */

#ifndef SMARTSIM_C_CLIENT_H
#define SMARTSIM_C_CLIENT_H
#include "client.h"
///@file
///\brief C-wrappers for the C++ SmartSimClient class
//! Put an array of type double into the database
extern "C" void put_array_double_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type float into the database
extern "C" void put_array_float_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type int64_t into the database
extern "C" void put_array_int64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type int32_t into the database
extern "C" void put_array_int32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type uint64_t into the database
extern "C" void put_array_uint64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type uint32_t into the database
extern "C" void put_array_uint32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type double from the database
extern "C" void get_array_double_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type float from the database
extern "C" void get_array_float_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type int64_t from the database
extern "C" void get_array_int64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type int32_t from the database
extern "C" void get_array_int32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type uint64_t from the database
extern "C" void get_array_uint64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type uint32_t from the database
extern "C" void get_array_uint32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put a scalar of type double into the database
extern "C" void put_scalar_double_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    double scalar       /*!< Scalar value to store in the database */
);

//! Put a scalar of type float into the database
extern "C" void put_scalar_float_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    float scalar       /*!< Scalar value to store in the database */
);

//! Put a scalar of type int64_t into the database
extern "C" void put_scalar_int64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    int64_t scalar       /*!< Scalar value to store in the database */
);

//! Put a scalar of type int32_t into the database
extern "C" void put_scalar_int32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    int32_t scalar       /*!< Scalar value to store in the database */
);

//! Put a scalar of type uint64_t into the database
extern "C" void put_scalar_uint64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    uint64_t scalar       /*!< Scalar value to store in the database */
);

//! Put a scalar of type uint32_t into the database
extern "C" void put_scalar_uint32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    uint32_t scalar       /*!< Scalar value to store in the database */
);

//! Get an array of type double from the database
extern "C" double get_scalar_double_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Get an array of type float from the database
extern "C" float get_scalar_float_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Get an array of type int64_t from the database
extern "C" int64_t get_scalar_int64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Get an array of type int32_t from the database
extern "C" int32_t get_scalar_int32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Get an array of type uint64_t from the database
extern "C" uint64_t get_scalar_uint64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Get an array of type uint32_t from the database
extern "C" uint32_t get_scalar_uint32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_key_and_check_scalar_double_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    double scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_key_and_check_scalar_float_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    float scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_key_and_check_scalar_int64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    int64_t scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_key_and_check_scalar_int32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    int32_t scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_key_and_check_scalar_uint64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    uint64_t scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_key_and_check_scalar_uint32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    uint32_t scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

//! Put an array of type double into the database
extern "C" void put_exact_key_array_double_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type float into the database
extern "C" void put_exact_key_array_float_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type int64_t into the database
extern "C" void put_exact_key_array_int64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type int32_t into the database
extern "C" void put_exact_key_array_int32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type uint64_t into the database
extern "C" void put_exact_key_array_uint64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type uint32_t into the database
extern "C" void put_exact_key_array_uint32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type double from the database
extern "C" void get_exact_key_array_double_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type float from the database
extern "C" void get_exact_key_array_float_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type int64_t from the database
extern "C" void get_exact_key_array_int64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type int32_t from the database
extern "C" void get_exact_key_array_int32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type uint64_t from the database
extern "C" void get_exact_key_array_uint64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type uint32_t from the database
extern "C" void get_exact_key_array_uint32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    void* array             /*!< Array to get from the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type double into the database
extern "C" void put_exact_key_scalar_double_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    double scalar       /*!< Scalar value to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type float into the database
extern "C" void put_exact_key_scalar_float_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    float scalar       /*!< Scalar value to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type int64_t into the database
extern "C" void put_exact_key_scalar_int64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    int64_t scalar       /*!< Scalar value to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type int32_t into the database
extern "C" void put_exact_key_scalar_int32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    int32_t scalar       /*!< Scalar value to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type uint64_t into the database
extern "C" void put_exact_key_scalar_uint64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    uint64_t scalar       /*!< Scalar value to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Put an array of type uint32_t into the database
extern "C" void put_exact_key_scalar_uint32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    uint32_t scalar       /*!< Scalar value to store in the database */,
    int** dimensions        /*!< Length along each dimension of the array */,
    int* ndims              /*!< Number of dimensions of the array */
);

//! Get an array of type double from the database
extern "C" double get_exact_key_scalar_double_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Get an array of type float from the database
extern "C" float get_exact_key_scalar_float_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Get an array of type int64_t from the database
extern "C" int64_t get_exact_key_scalar_int64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Get an array of type int32_t from the database
extern "C" int32_t get_exact_key_scalar_int32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Get an array of type uint64_t from the database
extern "C" uint64_t get_exact_key_scalar_uint64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Get an array of type uint32_t from the database
extern "C" uint32_t get_exact_key_scalar_uint32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_exact_key_and_check_scalar_double_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    double scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_exact_key_and_check_scalar_float_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    float scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_exact_key_and_check_scalar_int64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    int64_t scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_exact_key_and_check_scalar_int32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    int32_t scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_exact_key_and_check_scalar_uint64_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    uint64_t scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

//! Poll the database for a key and check its value
extern "C" bool poll_exact_key_and_check_scalar_uint32_c(
    void* SmartSimClient_p  /*!< Pointer to an initialized SmartSim Client */,
    const char* key         /*!< Identifier for this object in th database */,
    uint32_t scalar       /*!< Scalar value against which to check */,
    int poll_frequency_ms   /*!< How often to check the database in milliseconds */,
    int num_tries           /*!< Number of times to check the database */
);

#endif // SMARTSIM_C_CLIENT_H