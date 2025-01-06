import json
import yaml

# Load the OpenAPI JSON file
with open("openapi.json", "r") as json_file:
    openapi_json = json.load(json_file)

# Convert JSON to YAML
with open("openapi.yaml", "w") as yaml_file:
    yaml.dump(openapi_json, yaml_file, default_flow_style=False)

print("Conversion complete! The YAML file has been saved as openapi.yaml.")
