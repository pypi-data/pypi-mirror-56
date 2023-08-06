def get_unique_structs(struct_info):
	"""
	Returns a list containing the type mapping of all unique 
	structs (object types) in a struct datatype mapping.
	"""
	unique_structs = []

	if isinstance(struct_info, dict):
		unique_structs.append(struct_info)

	for k, v in struct_info.items():
		if isinstance(v, dict):
			unique_structs += get_unique_structs(v)
	
	return unique_structs


def generate_field_name(field_name):
	"""
	Turns a snake_case field name into a PascalCase field name.
	"""
	split_snake = field_name.split("_")
	if len(split_snake) == 1:
		struct_name = f"{field_name[0].upper()}{field_name[1:]}"
	else:
		split_snake = [s.capitalize() for s in split_snake]

		struct_name = "".join(split_snake)
	

	return struct_name


def retype_nested_types(struct_info):
	"""
	Recursively finds any nested object types in `struct_info` and 
	replaces the mapping info with the nested `__struct_name` field.
	"""
	retyped_struct = copy.deepcopy(struct_info)

	for k, v in struct_info.items():
		if isinstance(v, dict):
			if v["__is_type_array"]:
				retyped_struct[k] = f"[]{v['__struct_name']}"
			else:
				retyped_struct[k] = v["__struct_name"]

	return retyped_struct


def create_struct_strings(struct_info, omit_empty=True):
	"""
	Turns struct info maps into multiline strings which can get 
	written to a .go file. 

	Eyyyy.
	"""
	unique_structs = get_unique_structs(struct_info)

	struct_strings = []

	for i in range(len(unique_structs)):
		unique_structs[i] = retype_nested_types(unique_structs[i])
	
	for u in unique_structs:
		struct_name = u.pop("__struct_name")
		u.pop("__is_type_array")
		struct_string = f"type {struct_name} struct " + "{\n"
		for k, v in u.items():
			field_name = generate_struct_name(k)
			if omit_empty:
				struct_tag = f"`json:\"{k},omitempty\"`"
			else:
				struct_tag = f"`json:\"{k}\""
			struct_string += f"\t{field_name}\t{v}\t{struct_tag}\n"
		struct_string += "}"
		
		struct_strings.append(struct_string)
	
	return struct_strings


def write_struct_file(struct_strings, package_name, output_filename):
	with open(f"{output_filename}", "w") as structfile:
		structfile.write(f"package {package_name}\n\n")
		for s in struct_strings:
			structfile.write(s+"\n\n")
