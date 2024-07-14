% Function to convert latitude and longitude to pixel indices
function [x, y] = latlon2pix(map, lat, lon)
    mapWidth = size(map, 2);
    mapHeight = size(map, 1);
    x = round(mapWidth * (lon + 180) / 360);
    y = round(mapHeight * (90 - lat) / 180);
end
