% Main Code

% Step 1: Load the Moon basemap
moonBasemap = imread('C:\Users\ayush pathak\Desktop\VISHWAM\moon_map.png');

% Step 2: Load the Hyperspectral Data
hyperspectralData = read_qub_file('C:\Users\ayush pathak\Desktop\VISHWAM\PRACTIVE IIRS\ch2_iir_nci_20240209T0809549481_d_img_d18\data\calibrated\20240209\ch2_iir_nci_20240209T0809549481_d_img_d18.qub');

% Step 3: Define Coordinates
upperLeftLat = 13.094611;
upperLeftLon = 137.556296;
upperRightLat = 13.086826;
upperRightLon = 137.129348;
lowerLeftLat = 39.070788;
lowerLeftLon = 137.030449;
lowerRightLat = 39.060936;
lowerRightLon = 136.482021;

% Step 4: Calculate Pixel Indices
[xUL, yUL] = latlon2pix(moonBasemap, upperLeftLat, upperLeftLon);
[xUR, yUR] = latlon2pix(moonBasemap, upperRightLat, upperRightLon);
[xLL, yLL] = latlon2pix(moonBasemap, lowerLeftLat, lowerLeftLon);
[xLR, yLR] = latlon2pix(moonBasemap, lowerRightLat, lowerRightLon);

% Step 5: Create the main figure
figure('Name', 'Moon Map with IIRS Strip', 'Position', [100, 100, 1200, 600]);

% Display the global Moon map
subplot(1, 2, 1);
imshow(moonBasemap);
hold on;
plot([xUL, xUR, xLR, xLL, xUL], [yUL, yUR, yLR, yLL, yUL], 'r-', 'LineWidth', 2);
title('Global Moon Map with IIRS Strip');

% Create a subplot for the IIRS channel display
subplot(1, 2, 2);
iirs_channel_display = imagesc(hyperspectralData(:,:,1)); % Display first channel
colorbar;
title('IIRS Channel Display');

% Create UI controls
channel_slider = uicontrol('Style', 'slider', 'Min', 1, 'Max', size(hyperspectralData, 3), ...
    'Value', 1, 'Position', [900, 50, 200, 20], ...
    'Callback', @(src, event) updateChannel(src, iirs_channel_display, channel_text, hyperspectralData));

channel_text = uicontrol('Style', 'text', 'Position', [900, 70, 200, 20], ...
    'String', 'Channel: 1');

% Create a new figure for spectrum display
spectrum_fig = figure('Name', 'Spectrum Display', 'Position', [1300, 100, 500, 400]);
spectrum_plot = plot(1:size(hyperspectralData, 3), zeros(1, size(hyperspectralData, 3)));
title('Spectrum at Selected Point');
xlabel('Channel');
ylabel('Intensity');

% Set up cursor data function
set(gca, 'ButtonDownFcn', @(src, event) cursorClick(spectrum_fig, spectrum_plot, hyperspectralData));

