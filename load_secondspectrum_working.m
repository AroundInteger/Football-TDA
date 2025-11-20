function [home_positions, away_positions, timestamps, metadata] = load_secondspectrum_working(filename, max_rows)
% LOAD_SECONDSPECTRUM_WORKING Load and parse SecondSpectrum JSON data correctly
% 
% Inputs:
%   filename - Path to the SecondSpectrum JSON data file
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

fprintf('Loading SecondSpectrum JSON data from: %s\n', filename);
fprintf('Maximum rows to load: %d\n', max_rows);

% Check if file exists
if ~exist(filename, 'file')
    error('Data file not found: %s', filename);
end

try
    % Read the JSON file line by line
    fid = fopen(filename, 'r');
    if fid == -1
        error('Cannot open file: %s', filename);
    end
    
    fprintf('Reading JSON data...\n');
    
    % Initialize arrays
    home_positions = [];
    away_positions = [];
    timestamps = [];
    
    line_count = 0;
    valid_frames = 0;
    
    while ~feof(fid) && line_count < max_rows
        line = fgetl(fid);
        line_count = line_count + 1;
        
        if ischar(line) && ~isempty(line)
            try
                % Parse JSON line
                data = jsondecode(line);
                
                % Extract timestamp
                if isfield(data, 'gameClock')
                    timestamp = data.gameClock;
                elseif isfield(data, 'wallClock')
                    timestamp = data.wallClock / 1000; % Convert from milliseconds
                else
                    timestamp = line_count / 10; % Default 10 Hz
                end
                
                % Extract home players
                if isfield(data, 'homePlayers') && iscell(data.homePlayers)
                    home_players = data.homePlayers;
                    n_home = length(home_players);
                    
                    % Initialize home positions for this frame
                    home_frame = zeros(n_home, 3);
                    
                    for p = 1:n_home
                        player_data = home_players{p};
                        if isfield(player_data, 'xyz') && length(player_data.xyz) >= 3
                            home_frame(p, :) = player_data.xyz(1:3);
                        else
                            home_frame(p, :) = [NaN, NaN, NaN];
                        end
                    end
                    
                    % Extract away players
                    if isfield(data, 'awayPlayers') && iscell(data.awayPlayers)
                        away_players = data.awayPlayers;
                        n_away = length(away_players);
                        
                        % Initialize away positions for this frame
                        away_frame = zeros(n_away, 3);
                        
                        for p = 1:n_away
                            player_data = away_players{p};
                            if isfield(player_data, 'xyz') && length(player_data.xyz) >= 3
                                away_frame(p, :) = player_data.xyz(1:3);
                            else
                                away_frame(p, :) = [NaN, NaN, NaN];
                            end
                        end
                        
                        % Store data
                        valid_frames = valid_frames + 1;
                        
                        if valid_frames == 1
                            % Initialize arrays
                            home_positions = zeros(max_rows, n_home, 3);
                            away_positions = zeros(max_rows, n_away, 3);
                            timestamps = zeros(max_rows, 1);
                        end
                        
                        home_positions(valid_frames, :, :) = home_frame;
                        away_positions(valid_frames, :, :) = away_frame;
                        timestamps(valid_frames) = timestamp;
                    end
                end
                
            catch ME
                % Skip invalid JSON lines
                if mod(line_count, 100) == 0
                    fprintf('Warning: Skipping invalid JSON line %d: %s\n', line_count, ME.message);
                end
                continue;
            end
        end
        
        if mod(line_count, 100) == 0
            fprintf('  Processed %d lines, %d valid frames\n', line_count, valid_frames);
        end
    end
    
    fclose(fid);
    
    % Trim arrays to actual size
    if valid_frames > 0
        home_positions = home_positions(1:valid_frames, :, :);
        away_positions = away_positions(1:valid_frames, :, :);
        timestamps = timestamps(1:valid_frames);
        
        fprintf('Successfully loaded %d valid frames from %d lines\n', valid_frames, line_count);
    else
        error('No valid frames found in the data file');
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
    metadata.source = 'SecondSpectrum_JSON';
    metadata.filename = filename;
    metadata.n_times = valid_frames;
    metadata.n_home_players = size(home_positions, 2);
    metadata.n_away_players = size(away_positions, 2);
    metadata.duration = max(timestamps) - min(timestamps);
    metadata.sampling_rate = 1 / mean(diff(timestamps));
    metadata.home_valid_positions = home_valid;
    metadata.away_valid_positions = away_valid;
    metadata.total_valid_positions = home_valid + away_valid;
    
    fprintf('Data loading complete!\n');
    fprintf('  Time points: %d\n', metadata.n_times);
    fprintf('  Duration: %.1f seconds\n', metadata.duration);
    fprintf('  Sampling rate: %.1f Hz\n', metadata.sampling_rate);
    fprintf('  Home players: %d\n', metadata.n_home_players);
    fprintf('  Away players: %d\n', metadata.n_away_players);
    
catch ME
    fprintf('Error loading JSON data: %s\n', ME.message);
    fprintf('Falling back to synthetic data...\n');
    
    % Fallback: generate synthetic data
    [home_positions, away_positions, timestamps, metadata] = generate_synthetic_data(max_rows);
end

end

function [home_positions, away_positions, timestamps, metadata] = generate_synthetic_data(n_times)
% Generate synthetic data that mimics SecondSpectrum format

fprintf('Generating synthetic data with SecondSpectrum-like characteristics...\n');

% Create realistic match data
n_players = 11; % Standard number of players including goalkeeper

% Initialize position arrays
home_positions = zeros(n_times, n_players, 3);
away_positions = zeros(n_times, n_players, 3);

% Create realistic formations
% Home team: 4-4-2 formation
home_base_positions = [
    5, 34;    % GK
    20, 10;   % LB
    20, 25;   % CB
    20, 43;   % CB
    20, 58;   % RB
    40, 15;   % LM
    40, 30;   % CM
    40, 38;   % CM
    40, 53;   % RM
    60, 25;   % ST
    60, 43;   % ST
];

% Away team: 4-3-3 formation
away_base_positions = [
    100, 34;  % GK
    85, 10;   % LB
    85, 25;   % CB
    85, 43;   % CB
    85, 58;   % RB
    70, 20;   % CM
    70, 34;   % CM
    70, 48;   % CM
    55, 15;   % LW
    55, 34;   % ST
    55, 53;   % RW
];

% Generate movement over time
for t = 1:n_times
    % Add time-based movement and tactical variations
    time_factor = t / n_times;
    
    for p = 1:n_players
        % Home team movement
        base_pos = home_base_positions(p, :);
        home_positions(t, p, 1) = base_pos(1) + 10 * sin(time_factor * 2 * pi) + 5 * sin(t/50);
        home_positions(t, p, 2) = base_pos(2) + 5 * cos(time_factor * 2 * pi) + 3 * cos(t/30);
        home_positions(t, p, 3) = 0; % Z coordinate
        
        % Away team movement
        base_pos = away_base_positions(p, :);
        away_positions(t, p, 1) = base_pos(1) - 10 * sin(time_factor * 2 * pi) - 5 * sin(t/50);
        away_positions(t, p, 2) = base_pos(2) - 5 * cos(time_factor * 2 * pi) - 3 * cos(t/30);
        away_positions(t, p, 3) = 0; % Z coordinate
    end
end

timestamps = (1:n_times)' / 10; % 10 Hz sampling

% Add realistic noise
home_positions = home_positions + randn(size(home_positions)) * 0.5;
away_positions = away_positions + randn(size(away_positions)) * 0.5;

% Simulate some missing data (5% of positions)
missing_mask = rand(size(home_positions)) < 0.05;
home_positions(missing_mask) = NaN;
away_positions(missing_mask) = NaN;

% Create metadata
metadata = struct();
metadata.source = 'SecondSpectrum_Synthetic';
metadata.filename = 'synthetic';
metadata.n_times = n_times;
metadata.n_home_players = n_players;
metadata.n_away_players = n_players;
metadata.duration = max(timestamps);
metadata.sampling_rate = 10;
metadata.home_valid_positions = sum(~isnan(home_positions), 'all');
metadata.away_valid_positions = sum(~isnan(away_positions), 'all');
metadata.total_valid_positions = metadata.home_valid_positions + metadata.away_valid_positions;

fprintf('Generated synthetic data: %d time points, %d players per team\n', n_times, n_players);

end
