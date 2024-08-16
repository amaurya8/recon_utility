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

        # Get all records from XML
        rows = [flatten_element(elem) for elem in root]

        if rows:
            # Write headers
            headers = sorted(set().union(*(row.keys() for row in rows)))
            writer.writerow(headers)

            # Write rows
            for row in rows:
                writer.writerow([row.get(header, '') for header in headers])

if __name__ == "__main__":
    xml_file = 'input.xml'  # Path to your XML file
    csv_file = 'output.csv'  # Path to the output CSV file
    xml_to_csv(xml_file, csv_file)
    print(f'Converted {xml_file} to {csv_file}')