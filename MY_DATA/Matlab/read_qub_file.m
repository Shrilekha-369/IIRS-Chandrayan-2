% Function to read hyperspectral data from QUB file
function hyperspectralData = read_qub_file(filename)
    % Open the QUB file
    fid = fopen(filename, 'r');
    
    % Read dimensions (update these indices based on your header structure)
    numRows = 1000; % Update with actual value from header
    numCols = 1000; % Update with actual value from header
    numChannels = 256; % Fixed for your case
    
    % Read hyperspectral data
    hyperspectralData = fread(fid, [numCols, numRows * numChannels], 'float32');
    
    % Reshape the data to [numRows, numCols, numChannels]
    hyperspectralData = reshape(hyperspectralData, [numCols, numRows, numChannels]);
    
    % Close the file
    fclose(fid);
    
    % Transpose to match [rows, columns, bands] format
    hyperspectralData = permute(hyperspectralData, [2, 1, 3]);
end