% Function to update channel display based on slider value
function updateChannel(source, channel_display, channel_text, hyperspectralData)
    channel = round(source.Value);
    if channel >= 1 && channel <= size(hyperspectralData, 3)
        channel_display.CData = hyperspectralData(:, :, channel);
        channel_text.String = ['Channel: ' num2str(channel)];
    else
        disp('Channel out of bounds');
    end
end

