import xml.etree.ElementTree as ET

# Path to your XML file
xml_file = r'C:\\Users\\ayush pathak\\Desktop\\VISHWAM\\PRACTIVE IIRS\\ch2_iir_nci_20240209T0809549481_d_img_d18\\MY_DATA\\ch2_iir_nci_20240209T0809549481_d_img_d18.xml'
# Function to parse XML and extract relevant metadata
def parse_xml_metadata(xml_file):
    # Parse XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Define namespaces
    namespaces = {
        'pds': 'http://pds.nasa.gov/pds4/pds/v1',
        'isda': 'https://isda.issdc.gov.in/pds4/isda/v1'
    }

    # Extracting observation area information
    mission_name = root.find('.//pds:Investigation_Area/pds:name', namespaces).text
    mission_type = root.find('.//pds:Investigation_Area/pds:type', namespaces).text
    mission_description = root.find('.//pds:Investigation_Area/pds:description', namespaces).text

    # Extracting observing system information
    spacecraft_name = root.find('.//pds:Observing_System/pds:Observing_System_Component[pds:name="Chandrayaan 2 Orbiter"]/pds:name', namespaces).text
    instrument_name = root.find('.//pds:Observing_System/pds:Observing_System_Component[pds:name="imaging infrared spectrometer"]/pds:name', namespaces).text
    instrument_description = root.find('.//pds:Observing_System/pds:Observing_System_Component[pds:name="imaging infrared spectrometer"]/pds:description', namespaces).text

    # Extracting mission parameters
    exposure_time = root.find('.//isda:Product_Parameters/isda:exposure_duration', namespaces).text
    gain_settings = root.find('.//isda:Product_Parameters/isda:gain', namespaces).text

    # Extracting geometry parameters
    # Example: Extracting multiple latitude and longitude entries
    system_level_coordinates = root.find('.//isda:Geometry_Parameters/isda:System_Level_Coordinates', namespaces)
    refined_corner_coordinates = root.find('.//isda:Geometry_Parameters/isda:Refined_Corner_Coordinates', namespaces)

    # Extracting all latitude and longitude entries under System_Level_Coordinates
    system_level_coords = {}
    for coord in system_level_coordinates:
        if 'latitude' in coord.tag:
            system_level_coords[coord.tag.replace('{https://isda.issdc.gov.in/pds4/isda/v1}', '')] = coord.text
        elif 'longitude' in coord.tag:
            system_level_coords[coord.tag.replace('{https://isda.issdc.gov.in/pds4/isda/v1}', '')] = coord.text

    # Extracting all latitude and longitude entries under Refined_Corner_Coordinates
    refined_corner_coords = {}
    for coord in refined_corner_coordinates:
        if 'latitude' in coord.tag:
            refined_corner_coords[coord.tag.replace('{https://isda.issdc.gov.in/pds4/isda/v1}', '')] = coord.text
        elif 'longitude' in coord.tag:
            refined_corner_coords[coord.tag.replace('{https://isda.issdc.gov.in/pds4/isda/v1}', '')] = coord.text

    # Extracting file area observational information
    file_name = root.find('.//pds:File_Area_Observational/pds:File/pds:file_name', namespaces).text
    file_creation_date = root.find('.//pds:File_Area_Observational/pds:File/pds:creation_date_time', namespaces).text
    file_size = root.find('.//pds:File_Area_Observational/pds:File/pds:file_size', namespaces).text
    md5_checksum = root.find('.//pds:File_Area_Observational/pds:File/pds:md5_checksum', namespaces).text
    file_comment = root.find('.//pds:File_Area_Observational/pds:File/pds:comment', namespaces).text

    return {
        'mission_name': mission_name,
        'mission_type': mission_type,
        'mission_description': mission_description,
        'spacecraft_name': spacecraft_name,
        'instrument_name': instrument_name,
        'instrument_description': instrument_description,
        'exposure_time': exposure_time,
        'gain_settings': gain_settings,
        'system_level_coordinates': system_level_coords,
        'refined_corner_coordinates': refined_corner_coords,
        'file_name': file_name,
        'file_creation_date': file_creation_date,
        'file_size': file_size,
        'md5_checksum': md5_checksum,
        'file_comment': file_comment
    }

# Call function to parse XML metadata
metadata = parse_xml_metadata(xml_file)

# Print extracted metadata
for key, value in metadata.items():
    if isinstance(value, dict):
        print(f"{key}:")
        for k, v in value.items():
            print(f"  {k}: {v}")
    else:
        print(f"{key}: {value}")
