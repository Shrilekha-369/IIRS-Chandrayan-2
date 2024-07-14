% Function to handle cursor clicks and update spectrum display
function cursorClick(spectrum_fig, spectrum_plot, hyperspectralData)
    point = get(gca, 'CurrentPoint');
    x = round(point(1, 1));
    y = round(point(1, 2));
    
    if x >= 1 && x <= size(hyperspectralData, 2) && y >= 1 && y <= size(hyperspectralData, 1)
        spectrum = squeeze(hyperspectralData(y, x, :));
        figure(spectrum_fig);
        set(spectrum_plot, 'YData', spectrum);
        title(['Spectrum at (', num2str(x), ', ', num2str(y), ')']);
    else
        disp('Clicked point out of bounds.');
    end
end