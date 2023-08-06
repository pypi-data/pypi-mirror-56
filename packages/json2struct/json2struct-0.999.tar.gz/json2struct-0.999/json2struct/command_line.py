import os
import json
import argparse

import json2struct

def main():
	argparser = argparse.ArgumentParser(description="Turn a template JSON into a bunch of Go struct types")
	argparser.add_argument("filename", metavar="template_json", type=str, help="Template JSON file to pass. Required.")
	argparser.add_argument("-n", "--struct_name", default="DataStuff", type=str, help="Name of the root struct. Defaults to DataStuff.")
	argparser.add_argument("-p", "--package_name", default="main", type=str, help="Name of the go package you want to use in the output file. Defaults to main.")
	argparser.add_argument("-o", "--output_filename", default="types.go", type=str, help="Name of the output Go file. Defaults to types.go.")
	argparser.add_argument("-e", "--omit_empty", default=True, type=str, help="Whether or not the JSON struct tag 'omitempty' should be added to generated structs. Defaults to true.")
	argparser.add_argument("-s", "--std_out", default=False, type=bool, help="If true, file output will also be output to stdout. Defaults to false.")

	args = argparser.parse_args()

	input_filename = os.path.abspath(args.filename)
	
	with open(input_filename, "r") as json_file:
		json_data = json.load(json_file)
	
	if isinstance(json_data, list):
		json_data = json_data[0]
	
	struct_info = json2struct.generate_struct_info(json_data, args.struct_name)

	struct_strings = json2struct.create_struct_strings(struct_info, args.omit_empty)

	json2struct.write_struct_file(struct_strings, args.package_name, args.output_filename)

	if args.std_out:
		print(f"package {args.package_name}\n")
		for s in struct_strings:
			print(s+"\n")