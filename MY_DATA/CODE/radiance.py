import csv
import math

def radiance_to_reflectance(radiance, solar_zenith_angle, solar_irradiance, earth_sun_distance):
    solar_zenith_rad = math.radians(solar_zenith_angle)
    cos_i = math.cos(solar_zenith_rad)
    reflectance = (radiance * math.pi * earth_sun_distance**2) / (solar_irradiance * cos_i)
    return reflectance

# Input and output files
input_file = 'C:\\Users\\ayush pathak\\Desktop\\VISHWAM\\PRACTIVE IIRS\\ch2_iir_nci_20240209T0809549481_d_img_d18\\MY_DATA\\post_radiance.txt'  # Replace with your input file path
output_file = 'C:\\Users\\ayush pathak\\Desktop\\VISHWAM\\PRACTIVE IIRS\\ch2_iir_nci_20240209T0809549481_d_img_d18\\MY_DATA\\reflectance_data.txt'  # Updated output file path

# Constants for solar zenith angle and Earth-Sun distance (updated with provided values)
solar_zenith_angle = 54.611005  # Updated value based on provided metadata
earth_sun_distance = 0.998929  # Updated value based on provided metadata

# Metadata value for detector pixel width in micrometers
detector_pixel_width = 30  # Example value, replace with actual if available

# Open input and output files
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerow(['Band', 'Max_SR', 'Dynamic_Range', 'Reflectance_Per_Pixel_Width'])

    # Skip the header line
    next(infile)

    # Read each line from input file
    for line in infile:
        band, max_sr, dynamic_range = line.strip().split()
        band = int(band)
        max_sr = float(max_sr)
        dynamic_range = float(dynamic_range)

        # Estimate solar irradiance using dynamic range
        solar_irradiance = dynamic_range / math.pi

        # Calculate reflectance using radiance-to-reflectance function
        reflectance = radiance_to_reflectance(max_sr, solar_zenith_angle, solar_irradiance, earth_sun_distance)

        # Convert reflectance to reflectance per unit pixel width
        reflectance_per_pixel_width = reflectance / detector_pixel_width if detector_pixel_width else reflectance

        # Write results to CSV file
        csv_writer.writerow([band, max_sr, dynamic_range, reflectance_per_pixel_width])

print(f"Reflectance values per pixel width have been saved to {output_file}")