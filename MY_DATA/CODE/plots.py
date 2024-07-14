import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from scipy.stats import linregress

# Load your data
reflectance_data = pd.read_csv("C:/Users/ayush pathak/Desktop/VISHWAM/PRACTIVE IIRS/ch2_iir_nci_20240209T0809549481_d_img_d18/MY_DATA/INFORMATION/reflectance.txt")
wavelength_data = pd.read_csv("C:/Users/ayush pathak/Desktop/VISHWAM/PRACTIVE IIRS/ch2_iir_nci_20240209T0809549481_d_img_d18/MY_DATA/INFORMATION/wavelength.txt", sep='\t')

# Extract relevant columns
bands = reflectance_data['Band']
reflectance_values = reflectance_data['Reflectance_Per_Pixel_Width']
center_wavelengths = wavelength_data['Center Wavelength (nm)'][:252]
band_widths = wavelength_data['Band Width (nm)'][:252]

# Define pixel width (in meters)
pixel_width = 30  # Replace with actual value from metadata if different

# Plotting begins here

# 1. Spectral Profile Plot
plt.figure()
plt.plot(center_wavelengths, reflectance_values, 'b-')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')
plt.title('Spectral Profile')
plt.grid(True)
plt.show()

# 2. Reflectance vs Band Number
plt.figure()
plt.plot(bands, reflectance_values, 'r-')
plt.xlabel('Band Number')
plt.ylabel('Reflectance')
plt.title('Reflectance vs Band Number')
plt.grid(True)
plt.show()

# 3. Reflectance vs Wavelength with Band Width
plt.figure()
plt.errorbar(center_wavelengths, reflectance_values, yerr=band_widths / 2, fmt='b.')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')
plt.title('Reflectance vs Wavelength with Band Width')
plt.grid(True)
plt.show()

# 4. Histogram of Reflectance Values
plt.figure()
plt.hist(reflectance_values, bins=30)
plt.xlabel('Reflectance')
plt.ylabel('Frequency')
plt.title('Distribution of Reflectance Values')
plt.grid(True)
plt.show()

# 5. First Derivative of Spectral Profile
first_derivative = np.diff(reflectance_values) / np.diff(center_wavelengths)
plt.figure()
plt.plot(center_wavelengths[:-1], first_derivative, 'g-')
plt.xlabel('Wavelength (nm)')
plt.ylabel('First Derivative of Reflectance')
plt.title('First Derivative of Spectral Profile')
plt.grid(True)
plt.show()

# 6. Cumulative Sum of Reflectance
cumulative_reflectance = np.cumsum(reflectance_values)
plt.figure()
plt.plot(center_wavelengths, cumulative_reflectance, 'm-')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Cumulative Reflectance')
plt.title('Cumulative Sum of Reflectance')
plt.grid(True)
plt.show()

# 7. Box Plot of Reflectance Values
plt.figure()
plt.boxplot(reflectance_values)
plt.ylabel('Reflectance')
plt.title('Box Plot of Reflectance Values')
plt.show()

# 8. Scatter Plot of Reflectance vs Wavelength
plt.figure()
plt.scatter(center_wavelengths, reflectance_values, c=bands, cmap='viridis', s=20)
plt.colorbar(label='Band Number')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')
plt.title('Scatter Plot of Reflectance vs Wavelength')
plt.show()

# 9. Polar Plot of Reflectance
plt.figure()
theta = np.deg2rad(bands)
r = reflectance_values
ax = plt.subplot(111, polar=True)
ax.plot(theta, r)
ax.set_title('Polar Plot of Reflectance')
plt.show()

# 10. Continuum Removal
max_points = argrelextrema(reflectance_values.values, np.greater)[0]
continuum = np.interp(center_wavelengths, center_wavelengths[max_points], reflectance_values[max_points])
continuum_removed = reflectance_values / continuum

plt.figure()
plt.plot(center_wavelengths, reflectance_values, 'b-', label='Original')
plt.plot(center_wavelengths, continuum, 'r--', label='Continuum')
plt.plot(center_wavelengths, continuum_removed, 'g-', label='Continuum Removed')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')
plt.title('Continuum Removal')
plt.legend()
plt.grid()
plt.show()

# 11. Normalized Difference Index
band1 = 50
band2 = 100
nd_index = (reflectance_values[band2] - reflectance_values[band1]) / (reflectance_values[band2] + reflectance_values[band1])
print(f'Normalized Difference Index (bands {band1} and {band2}): {nd_index}')

# 12. Moving Average Smoothing
window_size = 5
smoothed_reflectance = np.convolve(reflectance_values, np.ones(window_size)/window_size, mode='same')

plt.figure()
plt.plot(center_wavelengths, reflectance_values, 'b-', label='Original')
plt.plot(center_wavelengths, smoothed_reflectance, 'r-', label='Smoothed')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')
plt.title(f'Moving Average Smoothing (Window Size: {window_size})')
plt.legend()
plt.grid()
plt.show()

# 13. Rolling Standard Deviation
rolling_std = pd.Series(reflectance_values).rolling(window=5).std()

plt.figure()
plt.plot(center_wavelengths[2:-2], rolling_std[2:-2], 'g-', label='Rolling Std Dev')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Standard Deviation')
plt.title('Rolling Standard Deviation of Reflectance')
plt.grid()
plt.legend()
plt.show()

# 14. Histogram of Reflectance with Noise Threshold
plt.figure()
plt.hist(reflectance_values, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(x=0.1, color='r', linestyle='--', label='Noise Threshold')
plt.xlabel('Reflectance')
plt.ylabel('Frequency')
plt.title('Histogram of Reflectance Values with Noise Threshold')
plt.legend()
plt.grid()
plt.show()

# 15. Difference Between Successive Bands
diff_reflectance = np.diff(reflectance_values)

plt.figure()
plt.plot(bands[1:], diff_reflectance, 'b-', marker='o')
plt.xlabel('Band Number')
plt.ylabel('Difference in Reflectance')
plt.title('Difference Between Successive Bands')
plt.grid()
plt.axhline(0, color='red', linestyle='--', linewidth=0.8)  # Zero line for reference
plt.show()

# 16. Spectral Slope Calculation
slopes = []
for i in range(len(reflectance_values) - 1):
    slope, _, _, _, _ = linregress(bands[i:i+2], reflectance_values[i:i+2])
    slopes.append(slope)

plt.figure()
plt.plot(bands[:-1], slopes, 'm-', marker='o')
plt.xlabel('Band Number')
plt.ylabel('Spectral Slope')
plt.title('Spectral Slope Across Bands')
plt.grid()
plt.axhline(0, color='red', linestyle='--', linewidth=0.8)  # Zero line for reference
plt.show()
