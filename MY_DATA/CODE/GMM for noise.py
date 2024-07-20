import numpy as np
import rasterio
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

# Load the .qub file using memory mapping
header_info = {
    'rows': 9340,
    'cols': 250,
    'bands': 256,
    'data_type': np.float32
}
file_path = r"C:\\Users\\ayush pathak\\Desktop\\VISHWAM\\PRACTIVE IIRS\\ch2_iir_nci_20240209T0809549481_d_img_d18\\data\\calibrated\\20240209\\ch2_iir_nci_20240209T0809549481_d_img_d18.qub"

# Memory-map the file
data = np.memmap(file_path, dtype=header_info['data_type'], mode='r', shape=(header_info['rows'], header_info['cols'], header_info['bands']))

# Reshape the data for GMM and select the first 200 bands
reshaped_data = data.reshape((-1, header_info['bands']))[:, :200]

# Fit Gaussian Mixture Model to the reshaped data
n_components = 5
gmm = GaussianMixture(n_components=n_components, random_state=42)
gmm.fit(reshaped_data)

# Predict labels for the data
labels = gmm.predict(reshaped_data)

# Identify noisy and non-noisy data
noisy_mask = labels == 1  # Adjust based on GMM output
non_noisy_mask = labels != 1

# Plotting
plt.figure(figsize=(12, 6))
bands = np.arange(200)  # Adjust band range for plotting

# Aggregate and plot noisy and non-noisy spectra
plt.plot(bands, np.mean(reshaped_data[noisy_mask], axis=0), color='red', label='Noisy Spectra')
plt.plot(bands, np.mean(reshaped_data[non_noisy_mask], axis=0), color='blue', label='Non-Noisy Spectra')

plt.title('Mean Spectra: Noisy vs Non-Noisy (First 200 Bands)')
plt.xlabel('Band Number')
plt.ylabel('Reflectance')
plt.legend()
plt.grid()
plt.show()
