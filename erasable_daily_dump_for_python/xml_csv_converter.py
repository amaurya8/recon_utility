import xml.etree.ElementTree as ET
import csv

def flatten_element(elem, parent_path='', sep='_'):
    """Flatten XML element into a dictionary."""
    items = {}
    for child in elem:
        path = f"{parent_path}{sep}{child.tag}" if parent_path else child.tag
        if list(child):
            items.update(flatten_element(child, path, sep))
        else:
            items[path] = child.text
    return items

def xml_to_csv(xml_file, csv_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Prepare CSV file for writing
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Collect all records from XML
        records = []
        for elem in root:
            record = flatten_element(elem)
            records.append(record)

        if records:
            # Write headers
            headers = sorted(set().union(*(record.keys() for record in records)))
            writer.writerow(headers)

            # Write rows
            for record in records:
                writer.writerow([record.get(header, '') for header in headers])

if __name__ == "__main__":
    xml_file = 'input.xml'  # Path to your XML file
    csv_file = 'output.csv'  # Path to the output CSV file
    xml_to_csv(xml_file, csv_file)
    print(f'Converted {xml_file} to {csv_file}')