import json

with open("json_files/test.json", 'r', encoding='utf-8') as f:
    test1 = json.load(f)
    test1_string = json.dumps(test1, indent=2)

print(test1_string)

def extract_leaf_nodes(node, result):
    if "subcomponents" not in node:
        # This is a leaf node
        result.append({
            "leaf text": node["text"],
            "id": node["token_id"],
            "info": node["explanation"]
        })
    else:
        # Recursively process subcomponents
        for subcomponent in node["subcomponents"]:
            extract_leaf_nodes(subcomponent, result)

# Initialize an empty list to store the leaf nodes
leaf_nodes = []

# Extract leaf nodes starting from the root
extract_leaf_nodes(test1, leaf_nodes)

# Convert the result to JSON format
result_json = json.dumps(leaf_nodes, indent=4)

file_path = "new_json_files/test.json"  # Specify the file path
with open(file_path, "w") as json_file:
    json.dump(result_json, json_file, indent=4)

# Print the result
print(result_json)