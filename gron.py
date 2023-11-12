import json
import sys

def flatten_json(json_obj, parent_key='', separator='.'):
    flattened = {}
    for key, value in json_obj.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, dict):
            flattened.update(flatten_json(value, new_key, separator))
        else:
            flattened[new_key] = value

    return flattened

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File not found: {filename}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Unable to parse JSON in file: {filename}")
            sys.exit(1)
    else:
        # Read from stdin if no filename is provided
        try:
            input_json = sys.stdin.read()
            json_data = json.loads(input_json)
        except json.JSONDecodeError:
            print("Error: Unable to parse JSON from stdin.")
            sys.exit(1)

    flattened_json = flatten_json(json_data)

    for key, value in flattened_json.items():
        print(f'json{key} = {json.dumps(value)};')

    sys.exit(0)
