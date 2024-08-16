import xml.etree.ElementTree as ET
import pandas as pd


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


def xml_to_dataframe(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Collect all records from XML
    records = [flatten_element(elem) for elem in root]

    # Create a DataFrame
    df = pd.DataFrame(records)

    return df


def save_dataframe_to_csv(df, csv_file):
    # Save DataFrame to CSV
    df.to_csv(csv_file, index=False, encoding='utf-8')


if __name__ == "__main__":
    xml_file = 'input.xml'  # Path to your XML file
    csv_file = 'output.csv'  # Path to the output CSV file

    # Convert XML to DataFrame
    df = xml_to_dataframe(xml_file)

    # Save DataFrame to CSV
    save_dataframe_to_csv(df, csv_file)

    print(f'Converted {xml_file} to {csv_file}')