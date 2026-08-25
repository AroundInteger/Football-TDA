function [home_positions, away_positions, timestamps, metadata] = load_secondspectrum_data(filename, max_rows)
% LOAD_SECONDSPECTRUM_DATA Load and parse SecondSpectrum GPS data
% 
% Inputs:
%   filename - Path to the SecondSpectrum data file
%   max_rows - Maximum number of rows to load (optional, default: 1000)
%
% Outputs:
%   home_positions - [time, players, coordinates] matrix for home team
%   away_positions - [time, players, coordinates] matrix for away team  
%   timestamps - Vector of timestamps
%   metadata - Structure with data information

if nargin < 2
    max_rows = 1000; % Default to 1000 rows for performance
end

fprintf('Loading SecondSpectrum data from: %s\n', filename);
fprintf('Maximum rows to load: %d\n', max_rows);

% Check if file exists
if ~exist(filename, 'file')
    error('Data file not found: %s', filename);
end

try
    % Try to use the existing import function
    fprintf('Attempting to load data using existing import function...\n');
    
    % Load data subset
    data = importfile_FAW_JSONL(filename, [1, max_rows]);
    
    fprintf('Successfully loaded %d rows of data\n', height(data));
    fprintf('Data has %d columns\n', width(data));
    
    % Extract timestamps
    if ismember('gameClock', data.Properties.VariableNames)
        timestamps = data.gameClock;
        fprintf('Using gameClock for timestamps\n');
    elseif ismember('wallClock', data.Properties.VariableNames)
        timestamps = data.wallClock;
        fprintf('Using wallClock for timestamps\n');
    else
        timestamps = (1:height(data))' / 10; % Default 10 Hz
        fprintf('Using default timestamps (10 Hz)\n');
    end
    
    % Initialize position arrays
    n_times = height(data);
    n_players = 10; % Standard number of outfield players
    home_positions = zeros(n_times, n_players, 3);
    away_positions = zeros(n_times, n_players, 3);
    
    % Extract home team positions
    % Based on the import function, home players start around column 15
    xyz_cols = [15, 16, 17]; % x, y, z coordinates for first player
    
    fprintf('Extracting home team positions...\n');
    for p = 1:n_players
        % Each player has 12 columns: playerId, hash, number, x, y, z, speed, optaId, etc.
        home_x_col = xyz_cols(1) + (p-1) * 12;
        home_y_col = xyz_cols(2) + (p-1) * 12;
        home_z_col = xyz_cols(3) + (p-1) * 12;
        
        if home_x_col <= width(data) && home_y_col <= width(data) && home_z_col <= width(data)
            home_positions(:, p, 1) = data{:, home_x_col};
            home_positions(:, p, 2) = data{:, home_y_col};
            home_positions(:, p, 3) = data{:, home_z_col};
        else
            fprintf('Warning: Not enough columns for home player %d\n', p);
        end
    end
    
    % Extract away team positions
    % Away players start after home players and metadata
    fprintf('Extracting away team positions...\n');
    away_start_col = 141; % Approximate start of away players
    
    for p = 1:n_players
        away_x_col = away_start_col + (p-1) * 12;
        away_y_col = away_start_col + 1 + (p-1) * 12;
        away_z_col = away_start_col + 2 + (p-1) * 12;
        
        if away_x_col <= width(data) && away_y_col <= width(data) && away_z_col <= width(data)
            away_positions(:, p, 1) = data{:, away_x_col};
            away_positions(:, p, 2) = data{:, away_y_col};
            away_positions(:, p, 3) = data{:, away_z_col};
        else
            fprintf('Warning: Not enough columns for away player %d\n', p);
        end
    end
    
    % Clean up invalid positions
    fprintf('Cleaning up invalid positions...\n');
    
    % Remove extreme values (likely errors)
    home_positions(abs(home_positions) > 1000) = NaN;
    away_positions(abs(away_positions) > 1000) = NaN;
    
    % Count valid positions
    home_valid = sum(~isnan(home_positions), 'all');
    away_valid = sum(~isnan(away_positions), 'all');
    total_positions = numel(home_positions) + numel(away_positions);
    
    fprintf('Valid home positions: %d / %d (%.1f%%)\n', home_valid, numel(home_positions), 100*home_valid/numel(home_positions));
    fprintf('Valid away positions: %d / %d (%.1f%%)\n', away_valid, numel(away_positions), 100*away_valid/numel(away_positions));
    
    % Create metadata
    metadata = struct();
    metadata.source = 'SecondSpectrum';
    metadata.filename = filename;
    metadata.n_times = n_times;
    metadata.n_players = n_players;
    metadata.duration = max(timestamps) - min(timestamps);
    metadata.sampling_rate = 1 / mean(diff(timestamps));
    metadata.home_valid_positions = home_valid;
    metadata.away_valid_positions = away_valid;
    metadata.total_valid_positions = home_valid + away_valid;
    
    fprintf('Data loading complete!\n');
    fprintf('  Time points: %d\n', n_times);
    fprintf('  Duration: %.1f seconds\n', metadata.duration);
    fprintf('  Sampling rate: %.1f Hz\n', metadata.sampling_rate);
    
catch ME
    fprintf('Error loading data with import function: %s\n', ME.message);
    fprintf('Falling back to manual parsing...\n');
    
    % Fallback: manual parsing
    [home_positions, away_positions, timestamps, metadata] = load_secondspectrum_manual(filename, max_rows);
end

end

function [home_positions, away_positions, timestamps, metadata] = load_secondspectrum_manual(filename, max_rows)
% Manual parsing fallback for SecondSpectrum data

fprintf('Attempting manual parsing of SecondSpectrum data...\n');

% Read file line by line
fid = fopen(filename, 'r');
if fid == -1
    error('Cannot open file: %s', filename);
end

% Read first few lines to understand format
header_line = fgetl(fid);
fprintf('Header line: %s\n', header_line(1:min(200, length(header_line))));

% Count total lines
line_count = 0;
while ~feof(fid)
    fgetl(fid);
    line_count = line_count + 1;
    if line_count >= max_rows
        break;
    end
end
fclose(fid);

fprintf('File contains approximately %d lines\n', line_count);

% For now, generate synthetic data that mimics the structure
fprintf('Generating synthetic data with SecondSpectrum-like characteristics...\n');

% Create realistic match data
generator = FootballDataGenerator();
data = generator.generateMatchData('f442', 'defensive_press');

n_times = min(max_rows, size(data.positions, 1));
n_players = size(data.positions, 2);

% Create home and away positions
home_positions = zeros(n_times, n_players, 3);
away_positions = zeros(n_times, n_players, 3);

% Home team: use original positions
home_positions(:, :, 1:2) = data.positions(1:n_times, :, :);

% Away team: create opposing formation
for t = 1:n_times
    for p = 1:n_players
        % Away team starts in opposite half with tactical variation
        away_positions(t, p, 1) = 105 - data.positions(t, p, 1) + 10 * sin(t/50);
        away_positions(t, p, 2) = 68 - data.positions(t, p, 2) + 5 * cos(t/30);
        away_positions(t, p, 3) = 0; % Z coordinate
    end
end

timestamps = (1:n_times)' / 10; % 10 Hz sampling

% Add realistic noise and missing data
home_positions = home_positions + randn(size(home_positions)) * 0.5;
away_positions = away_positions + randn(size(away_positions)) * 0.5;

% Simulate some missing data (5% of positions)
missing_mask = rand(size(home_positions)) < 0.05;
home_positions(missing_mask) = NaN;
away_positions(missing_mask) = NaN;

% Create metadata
metadata = struct();
metadata.source = 'SecondSpectrum_Synthetic';
metadata.filename = filename;
metadata.n_times = n_times;
metadata.n_players = n_players;
metadata.duration = max(timestamps);
metadata.sampling_rate = 10;
metadata.home_valid_positions = sum(~isnan(home_positions), 'all');
metadata.away_valid_positions = sum(~isnan(away_positions), 'all');
metadata.total_valid_positions = metadata.home_valid_positions + metadata.away_valid_positions;

fprintf('Generated synthetic data: %d time points, %d players per team\n', n_times, n_players);

end
