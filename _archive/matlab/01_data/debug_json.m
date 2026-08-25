% Debug JSON structure
clear; clc;

data_file = '/Users/iMacPro/Documents/GitHub/Football-TDA/FieldTest/g2293068_SecondSpectrum_Data copy.txt';

fid = fopen(data_file, 'r');
line = fgetl(fid);
fclose(fid);

fprintf('First line length: %d\n', length(line));
fprintf('First 200 chars: %s\n', line(1:min(200, length(line))));

try
    data = jsondecode(line);
    fprintf('JSON decode successful!\n');
    fprintf('JSON structure:\n');
    disp(fieldnames(data));
    
    if isfield(data, 'homePlayers')
        fprintf('Home players count: %d\n', length(data.homePlayers));
        fprintf('First home player structure:\n');
        disp(fieldnames(data.homePlayers{1}));
        fprintf('First home player xyz: [%.2f, %.2f, %.2f]\n', data.homePlayers{1}.xyz);
    end
    
    if isfield(data, 'awayPlayers')
        fprintf('Away players count: %d\n', length(data.awayPlayers));
    end
    
    if isfield(data, 'gameClock')
        fprintf('Game clock: %.2f\n', data.gameClock);
    end
    
catch ME
    fprintf('JSON decode error: %s\n', ME.message);
end
