# json2struct
Converts json templates to Go structs.

## What this does
When passed a template JSON (can be a list or an object), recursively creates (a) Go-like `struct` structure(s) from the JSON,
and outputs all the created `struct`s into `out_filename` (defaults to `types.go`). 

Example JSON input can be found in `test_json.json`, example Go output can be found in `types.go`.

Fair warning, this hasn't been tested on every possible use case. 

## Getting/Using 

- `pip3 install json2struct`

- `json2struct [-h] [-n STRUCT_NAME] [-p PACKAGE_NAME] [-o OUTPUT_FILENAME]
               [-s STD_OUT]
               template_json`
  - `template_json`: Template JSON file to structify. Gets resolved internally to the absolute path of the file. Required. 
  - `-n` `--struct_name`: String. Name of the root struct. Defaults to `DataStuff`.
  - `-p` `--package_name`: String. Name of the go package you want to use in the output file. Defaults to `main`.
  - `-o` `--output_filename`: String. Name of the output Go file. Defaults to `types.go`. 
  - `-e` `--omit_empty`: Boolean. Whether or not the JSON struct tag `omitempty` should be added to generated structs. Defaults to `true`.
  - `-s` `--std_out`: Boolean. If `true`, file output will also be output to stdout. Defaults to `false`. 
