import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import pywt
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

# Load the data using memory mapping
header_info = {
    'rows': 9340,
    'cols': 250,
    'bands': 256,
    'data_type': np.float32
}
file_path = r"C:\\Users\\ayush pathak\\Desktop\\VISHWAM\\PRACTIVE IIRS\\ch2_iir_nci_20240209T0809549481_d_img_d18\\data\\calibrated\\20240209\\ch2_iir_nci_20240209T0809549481_d_img_d18.qub"
header_size = 0
data = np.memmap(file_path, dtype=header_info['data_type'], mode='r', offset=header_size, shape=(header_info['rows'], header_info['cols'], header_info['bands']))

rows, cols, bands = data.shape

def calculate_metrics(original, denoised):
    data_range = np.max(original) - np.min(original)
    psnr = peak_signal_noise_ratio(original, denoised, data_range=data_range)
    ssim = structural_similarity(original, denoised, data_range=data_range)
    return psnr, ssim

def wavelet_denoise(data, wavelet='db4', level=1):
    coeffs = pywt.wavedec2(data, wavelet, level=level)
    threshold = 0.1 * np.max(coeffs[0])
    coeffs[1:] = [(pywt.threshold(c, threshold, mode='soft') for c in detail) for detail in coeffs[1:]]
    coeffs[1:] = [tuple(c) for c in coeffs[1:]]  # Convert generators to tuples
    return pywt.waverec2(coeffs, wavelet)

def dynamic_contamination(band_data):
    skewness = np.abs(np.mean((band_data - np.mean(band_data))**3) / np.std(band_data)**3)
    return min(max(0.01, skewness / 10), 0.1)  # Limit between 0.01 and 0.1

def replace_outliers_median(data, mask, window_size=3):
    denoised_data = np.empty_like(data)
    pad = window_size // 2
    padded_data = np.pad(data, ((pad, pad), (pad, pad)), mode='reflect')
    
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if mask[i, j]:  # Outlier
                neighborhood = padded_data[i:i+window_size, j:j+window_size]
                denoised_data[i, j] = np.median(neighborhood)
            else:
                denoised_data[i, j] = data[i, j]
    
    return denoised_data

# Memory-map the denoised data
denoised_data = np.memmap('denoised_data_advanced.npy', dtype=np.float32, mode='w+', shape=(rows, cols, bands))
metrics = {'psnr': [], 'ssim': []}

for b in range(bands):
    print(f"Processing band {b+1}/{bands}")
    band_data = data[:, :, b]
    
    # Dynamic contamination
    contamination = dynamic_contamination(band_data.flatten())
    print(f"  Using contamination: {contamination:.4f}")
    
    # Isolation Forest
    clf = IsolationForest(contamination=contamination, random_state=42)
    outliers = clf.fit_predict(band_data.reshape(-1, 1))
    outlier_mask = outliers.reshape((rows, cols)) == -1
    
    # Apply both median filtering and wavelet denoising
    denoised_median = replace_outliers_median(band_data, outlier_mask)
    denoised_wavelet = wavelet_denoise(band_data)
    
    # Choose the best result
    psnr_median, ssim_median = calculate_metrics(band_data, denoised_median)
    psnr_wavelet, ssim_wavelet = calculate_metrics(band_data, denoised_wavelet)
    
    if psnr_median > psnr_wavelet:
        denoised_data[:, :, b] = denoised_median
        metrics['psnr'].append(psnr_median)
        metrics['ssim'].append(ssim_median)
        print(f"  Used median filtering. PSNR: {psnr_median:.2f}, SSIM: {ssim_median:.4f}")
    else:
        denoised_data[:, :, b] = denoised_wavelet
        metrics['psnr'].append(psnr_wavelet)
        metrics['ssim'].append(ssim_wavelet)
        print(f"  Used wavelet denoising. PSNR: {psnr_wavelet:.2f}, SSIM: {ssim_wavelet:.4f}")

# Flush memory-mapped file to disk
denoised_data.flush()

# Visualize results for a specific band
band_to_show = 50
plt.figure(figsize=(20, 10))

plt.subplot(2, 3, 1)
plt.title('Original Data (Band {})'.format(band_to_show))
plt.imshow(data[:, :, band_to_show], cmap='gray')
plt.colorbar()

plt.subplot(2, 3, 2)
plt.title('Denoised Data (Band {})'.format(band_to_show))
plt.imshow(denoised_data[:, :, band_to_show], cmap='gray')
plt.colorbar()

plt.subplot(2, 3, 3)
plt.title('Difference (Original - Denoised)')
plt.imshow(data[:, :, band_to_show] - denoised_data[:, :, band_to_show], cmap='seismic')
plt.colorbar()

plt.subplot(2, 3, 4)
plt.title('Histogram of Original Data')
plt.hist(data[:, :, band_to_show].flatten(), bins=50, alpha=0.7)
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

plt.subplot(2, 3, 5)
plt.title('Histogram of Denoised Data')
plt.hist(denoised_data[:, :, band_to_show].flatten(), bins=50, alpha=0.7)
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

plt.subplot(2, 3, 6)
plt.title('PSNR and SSIM Across Bands')
plt.plot(range(bands), metrics['psnr'], label='PSNR')
plt.plot(range(bands), metrics['ssim'], label='SSIM')
plt.xlabel('Band Number')
plt.ylabel('Metric Value')
plt.legend()

plt.tight_layout()
plt.show()

print("Denoising complete. Shape of denoised data:", denoised_data.shape)
print(f"Average PSNR: {np.mean(metrics['psnr']):.2f}")
print(f"Average SSIM: {np.mean(metrics['ssim']):.4f}")
