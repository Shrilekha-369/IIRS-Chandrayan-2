import xml.etree.ElementTree as ET
import os

# Get the current working directory
current_directory = os.getcwd()

# Define the input XML file path (corrected for Windows path)
xml_file_path = r'C:\\Users\\ayush pathak\\Desktop\\VISHWAM\\PRACTIVE IIRS\\ch2_iir_nci_20240209T0809549481_d_img_d18\\data\\calibrated\\20240209\\ch2_iir_nci_20240209T0809549481_d_img_d18.xml'

# Define the output text file path
output_file_path = os.path.join(current_directory, 'band_data.txt')

# Parse the XML file with namespaces
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Define namespaces
namespaces = {
    'ns0': 'http://pds.nasa.gov/pds4/pds/v1'
}

# Function to recursively search for Band_Bin elements
def find_band_bins(element):
    band_bins = []
    for child in element:
        if child.tag.endswith('Band_Bin'):
            band_bins.append(child)
        band_bins.extend(find_band_bins(child))
    return band_bins

# Find all Band_Bin elements
band_bins = find_band_bins(root)

print(f"Number of Band_Bin elements found: {len(band_bins)}")

# Open a new text file to write the data
with open(output_file_path, 'w') as f:
    # Write column headings
    f.write("Band Number\tBand Width (nm)\tCenter Wavelength (nm)\tStarting Wavelength (nm)\tEnding Wavelength (nm)\n")

    # Extract and write data for each band
    for band in band_bins:
        band_number = band.find('.//ns0:band_number', namespaces)
        band_width = band.find('.//ns0:band_width', namespaces)
        center_wavelength = band.find('.//ns0:center_wavelength', namespaces)

        if band_number is not None and band_width is not None and center_wavelength is not None:
            # Calculate starting and ending wavelengths
            band_width_val = float(band_width.text)
            center_wavelength_val = float(center_wavelength.text)
            starting_wavelength = center_wavelength_val - (band_width_val / 2)
            ending_wavelength = center_wavelength_val + (band_width_val / 2)

            # Write the data to the file
            f.write(f"{band_number.text}\t{band_width.text}\t{center_wavelength.text}\t{starting_wavelength:.2f}\t{ending_wavelength:.2f}\n")
        else:
            print(f"Incomplete data for a band: {ET.tostring(band, encoding='unicode')}")

print(f"Data has been written to: {output_file_path}")

# Print the XML structure for debugging
def print_element_structure(element, level=0):
    print('  ' * level + f"{element.tag}")
    for child in element:
        print_element_structure(child, level + 1)

print("\nXML Structure:")
print_element_structure(root)
