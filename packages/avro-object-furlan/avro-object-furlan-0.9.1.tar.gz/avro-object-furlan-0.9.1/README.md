<!-- AvroObject documentation master file, created by
sphinx-quickstart on Tue Sep 24 23:19:20 2019.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->
# AvroObject’s documentation!

[![Coverage Status](https://coveralls.io/repos/github/guionardo/py_avroobject/badge.svg?branch=master)](https://coveralls.io/github/guionardo/py_avroobject?branch=master)

## Links


* [GitHub AvroObject](https://github.com/guionardo/py_avroobject)
* [PyPi avro-object-furlan](https://pypi.org/project/avro-object-furlan/)

## Examples

* [Basic Serialization](ex_basic_serialization.md)
* [Schema Serialization](ex_schema_serialization.md)
* [Basic Deserialization](ex_basic_deserialization.md)
* [Schema Deserialization](ex_schema_deserialization.md)

# AvroObject


#### class avro_object.AvroObject(data, schema=None)
Helper class for AVRO objects


* **Parameters**

    
    * **data** (*JSON as string**, **Dict object**, **Filename/URL as string with JSON content**, **Avro as bytes with binary serialized content*) – (un)serialized data


    * **schema** (*JSON as string**, **Dict object**, **Filename/URL as string with JSON content*) – Avro schema



#### property data()

* **Returns**

    Native unserialized data



* **Return type**

    dict



#### property json()

* **Returns**

    JSON serialized data



* **Return type**

    str



#### property last_error()

* **Returns**

    Last error message



* **Return type**

    str



#### property ok()

* **Returns**

    Avro Object successfull creation



* **Return type**

    bool



#### property origin()

* **Returns**

    Source of data (str, file, URL, Avro binary)



* **Return type**

    str



#### property schema_origin()

* **Returns**

    Source of schema (str, file, URL)



* **Return type**

    str



#### to_avro()

* **Returns**

    AVRO bytes serialized data (when schema is informed)



* **Return type**

    bytes



#### to_json()

* **Returns**

    JSON serialized data



* **Return type**

    str


# AvroTools


#### class avro_object.AvroTools()
Tools for AvroObject


#### classmethod add_fetch_method(method)
Add custom fetch method


* **Parameters**

    **method** – (str source) -> (bool Success, str JSON/Error, str origin name)



* **Returns**

    Success



* **Return type**

    bool



#### static create_schema(data: dict, name: str, namespace: str = 'namespace.test', doc: str = None)
Create schema from object (incomplete)


* **Parameters**

    
    * **data** – source object


    * **name** – Name of schema


    * **namespace** – Namespace of schema


    * **doc** – Documentation



* **Returns**

    Schema



* **Return type**

    dict



#### classmethod fetch_json(source: str)
Load JSON string from various medium and returns as string


* **Parameters**

    **source** – string JSON, file name, URL, another registered source by add_fetch_method



* **Return type**

    tuple (bool Success, str JSON or error message, origin)



#### static fetch_json_file(source: str)
Try to parse json from file


* **Parameters**

    **source** – str with file name



* **Returns**

    (bool Success, str JSON or Error, origin)



#### static fetch_json_url(source: str)
Try to parse json from url


* **Parameters**

    **source** – str with URL



* **Returns**

    (bool Success, str JSON or Error, origin)



#### classmethod reset_fetch_methods()
Resets default fetch methods (File, URL and string)

# Author

©2019, Guionardo Furlan

[https://github.com/guionardo](https://github.com/guionardo)
