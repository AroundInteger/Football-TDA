function [data, metadata] = load_secondspectrum_properly(data_file, start_frame, end_frame)
    % LOAD_SECONDSPECTRUM_PROPERLY - Properly load SecondSpectrum data
    % 
    % This function loads SecondSpectrum data using the same method as
    % Load_WFA_Github_3.m, which is the correct approach.
    %
    % Inputs:
    %   data_file - Path to the SecondSpectrum data file
    %   start_frame - Starting frame (optional, default: 1)
    %   end_frame - Ending frame (optional, default: Inf)
    %
    % Outputs:
    %   data - Structure containing processed data
    %   metadata - Metadata about the data
    %
    % Author: GPS-TDA Research Team
    % Date: December 2024
    
    fprintf('=== Loading SecondSpectrum Data Properly ===\n\n');
    
    % Default parameters
    if nargin < 2, start_frame = 1; end
    if nargin < 3, end_frame = Inf; end
    
    % Constants from Load_WFA_Github_3.m
    fs = 25;  % Sampling rate (Hz)
    dt = 1/fs;  % Time step (seconds)
    
    fprintf('Loading data from: %s\n', data_file);
    fprintf('Sampling rate: %d Hz\n', fs);
    fprintf('Time step: %.3f seconds\n', dt);
    
    % Add FieldTest folder to path if needed
    fieldtest_path = fullfile(fileparts(data_file), '..', 'FieldTest');
    if exist(fieldtest_path, 'dir')
        addpath(fieldtest_path);
    end
    
    % Load data using the same method as Load_WFA_Github_3.m
    fprintf('Loading data using importfile_FAW_JSONL_R1...\n');
    T = importfile_FAW_JSONL_R1(data_file, [start_frame, end_frame]);
    
    % Get data dimensions
    N_Rows = height(T);
    fprintf('Loaded %d rows of data\n', N_Rows);
    
    % Check available column names
    fprintf('Available columns: %s\n', strjoin(T.Properties.VariableNames, ', '));
    
    % Extract time information
    if ismember('FrameIdx', T.Properties.VariableNames)
        frame_idx = T.FrameIdx;
        if ismember('GameClock', T.Properties.VariableNames)
            game_clock = T.GameClock;
        else
            game_clock = frame_idx * dt;
        end
        time_span = max(game_clock) - min(game_clock);
        fprintf('Time span: %.1f seconds (%.1f minutes)\n', time_span, time_span/60);
    else
        frame_idx = (1:N_Rows)';
        game_clock = frame_idx * dt;
        time_span = N_Rows * dt;
        fprintf('Time span: %.1f seconds (%.1f minutes)\n', time_span, time_span/60);
    end
    
    % Extract home team positions (columns 6:5:56 for X, 7:5:57 for Y)
    cols_x_h = 6:5:56;  % Home team X coordinates
    cols_y_h = cols_x_h + 1;  % Home team Y coordinates
    
    fprintf('Extracting home team positions...\n');
    xh = T{:, cols_x_h};  % Home team X coordinates (N_Rows x 11)
    yh = T{:, cols_y_h};  % Home team Y coordinates (N_Rows x 11)
    
    % Extract away team positions (columns 61:5:111 for X, 62:5:112 for Y)
    cols_x_a = 61:5:111;  % Away team X coordinates
    cols_y_a = cols_x_a + 1;  % Away team Y coordinates
    
    fprintf('Extracting away team positions...\n');
    xa = T{:, cols_x_a};  % Away team X coordinates (N_Rows x 11)
    ya = T{:, cols_y_a};  % Away team Y coordinates (N_Rows x 11)
    
    % Extract ball positions (columns 115, 116)
    fprintf('Extracting ball positions...\n');
    xb = T{:, 115};  % Ball X coordinate
    yb = T{:, 116};  % Ball Y coordinate
    
    % Extract player numbers
    fprintf('Extracting player numbers...\n');
    player_numbers_h = T{1, 5:5:56};  % Home team player numbers
    player_numbers_a = T{1, 60:5:110};  % Away team player numbers
    
    % Extract possession information (if available)
    possession = [];
    if ismember('lastTouch', T.Properties.VariableNames)
        possession = T.lastTouch;
        fprintf('Possession data available\n');
    end
    
    % Extract ball status (if available)
    ball_in_play = [];
    if ismember('live', T.Properties.VariableNames)
        ball_in_play = T.live;
        fprintf('Ball status data available\n');
    end
    
    % Calculate field dimensions
    all_x = [xh(:); xa(:); xb];
    all_y = [yh(:); ya(:); yb];
    
    field_bounds.x_min = min(all_x);
    field_bounds.x_max = max(all_x);
    field_bounds.y_min = min(all_y);
    field_bounds.y_max = max(all_y);
    field_bounds.length = field_bounds.x_max - field_bounds.x_min;
    field_bounds.width = field_bounds.y_max - field_bounds.y_min;
    
    fprintf('Field dimensions: %.1f x %.1f meters\n', field_bounds.length, field_bounds.width);
    
    % Calculate team centroids
    fprintf('Calculating team centroids...\n');
    home_centroid_x = mean(xh, 2);
    home_centroid_y = mean(yh, 2);
    away_centroid_x = mean(xa, 2);
    away_centroid_y = mean(ya, 2);
    
    % Calculate inter-team distance
    inter_team_distance = sqrt((home_centroid_x - away_centroid_x).^2 + ...
                              (home_centroid_y - away_centroid_y).^2);
    
    % Calculate team spreads (standard deviation of player positions)
    home_spread = zeros(N_Rows, 1);
    away_spread = zeros(N_Rows, 1);
    
    for i = 1:N_Rows
        home_positions = [xh(i, :); yh(i, :)];
        away_positions = [xa(i, :); ya(i, :)];
        
        home_spread(i) = std(sqrt(sum((home_positions - [home_centroid_x(i); home_centroid_y(i)]).^2, 1)));
        away_spread(i) = std(sqrt(sum((away_positions - [away_centroid_x(i); away_centroid_y(i)]).^2, 1)));
    end
    
    % Calculate team areas (convex hull areas)
    home_area = zeros(N_Rows, 1);
    away_area = zeros(N_Rows, 1);
    
    for i = 1:N_Rows
        try
            home_hull = convhull(xh(i, :), yh(i, :));
            home_area(i) = polyarea(xh(i, home_hull), yh(i, home_hull));
        catch
            home_area(i) = NaN;
        end
        
        try
            away_hull = convhull(xa(i, :), ya(i, :));
            away_area(i) = polyarea(xa(i, away_hull), ya(i, away_hull));
        catch
            away_area(i) = NaN;
        end
    end
    
    % Calculate team area ratio
    team_area_ratio = home_area ./ away_area;
    
    % Calculate Nearest Opponent Distance (NOD)
    home_nod = zeros(N_Rows, 1);
    away_nod = zeros(N_Rows, 1);
    
    for i = 1:N_Rows
        % Home team NOD
        home_distances = [];
        for j = 1:11
            distances_to_away = sqrt((xh(i, j) - xa(i, :)).^2 + (yh(i, j) - ya(i, :)).^2);
            home_distances = [home_distances, min(distances_to_away)];
        end
        home_nod(i) = mean(home_distances);
        
        % Away team NOD
        away_distances = [];
        for j = 1:11
            distances_to_home = sqrt((xa(i, j) - xh(i, :)).^2 + (ya(i, j) - yh(i, :)).^2);
            away_distances = [away_distances, min(distances_to_home)];
        end
        away_nod(i) = mean(away_distances);
    end
    
    % Package data structure
    data = struct();
    data.frame_idx = frame_idx;
    data.game_clock = game_clock;
    data.time_span = time_span;
    data.sampling_rate = fs;
    data.time_step = dt;
    data.n_frames = N_Rows;
    
    % Player positions
    data.home_positions.x = xh;
    data.home_positions.y = yh;
    data.away_positions.x = xa;
    data.away_positions.y = ya;
    data.ball_positions.x = xb;
    data.ball_positions.y = yb;
    
    % Player numbers
    data.player_numbers.home = player_numbers_h;
    data.player_numbers.away = player_numbers_a;
    
    % Team metrics
    data.team_metrics.home_centroid_x = home_centroid_x;
    data.team_metrics.home_centroid_y = home_centroid_y;
    data.team_metrics.away_centroid_x = away_centroid_x;
    data.team_metrics.away_centroid_y = away_centroid_y;
    data.team_metrics.inter_team_distance = inter_team_distance;
    data.team_metrics.home_spread = home_spread;
    data.team_metrics.away_spread = away_spread;
    data.team_metrics.home_area = home_area;
    data.team_metrics.away_area = away_area;
    data.team_metrics.team_area_ratio = team_area_ratio;
    data.team_metrics.home_nod = home_nod;
    data.team_metrics.away_nod = away_nod;
    
    % Additional data
    if ~isempty(possession)
        data.possession = possession;
    end
    if ~isempty(ball_in_play)
        data.ball_in_play = ball_in_play;
    end
    
    % Field information
    data.field_bounds = field_bounds;
    
    % Package metadata
    metadata = struct();
    metadata.data_file = data_file;
    metadata.load_time = datetime('now');
    metadata.sampling_rate = fs;
    metadata.time_step = dt;
    metadata.n_frames = N_Rows;
    metadata.time_span = time_span;
    metadata.field_dimensions = field_bounds;
    metadata.player_numbers = data.player_numbers;
    
    % Summary statistics
    metadata.summary.inter_team_distance_mean = mean(inter_team_distance);
    metadata.summary.inter_team_distance_std = std(inter_team_distance);
    metadata.summary.team_area_ratio_mean = nanmean(team_area_ratio);
    metadata.summary.team_area_ratio_std = nanstd(team_area_ratio);
    metadata.summary.home_nod_mean = mean(home_nod);
    metadata.summary.home_nod_std = std(home_nod);
    metadata.summary.away_nod_mean = mean(away_nod);
    metadata.summary.away_nod_std = std(away_nod);
    
    fprintf('\n=== Data Loading Complete ===\n');
    fprintf('Frames loaded: %d\n', N_Rows);
    fprintf('Time span: %.1f minutes\n', time_span/60);
    fprintf('Field size: %.1f x %.1f meters\n', field_bounds.length, field_bounds.width);
    fprintf('Inter-team distance: %.1f ± %.1f meters\n', metadata.summary.inter_team_distance_mean, metadata.summary.inter_team_distance_std);
    fprintf('Team area ratio: %.2f ± %.2f\n', metadata.summary.team_area_ratio_mean, metadata.summary.team_area_ratio_std);
    fprintf('Home NOD: %.1f ± %.1f meters\n', metadata.summary.home_nod_mean, metadata.summary.home_nod_std);
    fprintf('Away NOD: %.1f ± %.1f meters\n', metadata.summary.away_nod_mean, metadata.summary.away_nod_std);
    
    % Save loaded data
    save('secondspectrum_data_loaded.mat', 'data', 'metadata');
    fprintf('Data saved to secondspectrum_data_loaded.mat\n');
end
