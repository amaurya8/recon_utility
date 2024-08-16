import json
import csv

def flatten_json(y):
    """Flatten nested JSON into a flat dictionary."""
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    out = {}
    flatten(y)
    return out

def json_to_csv(json_file, csv_file):
    # Load JSON data from file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Flatten the JSON data
    flat_data = [flatten_json(record) for record in data]

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        if flat_data:
            # Write headers
            writer = csv.DictWriter(file, fieldnames=flat_data[0].keys())
            writer.writeheader()
            # Write rows
            writer.writerows(flat_data)

if __name__ == "__main__":
    json_file = 'input.json'  # Path to your JSON file
    csv_file = 'output.csv'  # Path to the output CSV file
    json_to_csv(json_file, csv_file)
    print(f'Converted {json_file} to {csv_file}')