classdef DataPipeline < handle
    % DataPipeline - Robust preprocessing pipeline for football GPS data
    % Handles real SecondSpectrum data and prepares it for TDA analysis
    
    properties
        rawData
        processedData
        metadata
        fieldDimensions = [105, 68]  % Standard field dimensions in meters
        samplingRate = 10  % Hz
        coordinateSystem = 'pitch_fixed'  % 'pitch_fixed' or 'ball_relative'
    end
    
    methods
        function obj = DataPipeline()
            % Initialize the data pipeline
            obj.rawData = struct();
            obj.processedData = struct();
            obj.metadata = struct();
        end
        
        function loadSecondSpectrumData(obj, filename)
            % Load and parse SecondSpectrum JSONL data
            fprintf('Loading SecondSpectrum data from: %s\n', filename);
            
            % Read the JSONL file
            fid = fopen(filename, 'r');
            raw_lines = {};
            line_count = 0;
            
            while ~feof(fid)
                line = fgetl(fid);
                if ~isempty(line)
                    line_count = line_count + 1;
                    raw_lines{line_count} = line;
                end
            end
            fclose(fid);
            
            % Parse JSON data
            obj.rawData = struct();
            obj.rawData.timestamps = zeros(line_count, 1);
            obj.rawData.home_players = zeros(line_count, 10, 3);  % 10 players, xyz
            obj.rawData.away_players = zeros(line_count, 10, 3);
            obj.rawData.ball_position = zeros(line_count, 3);
            obj.rawData.game_clock = zeros(line_count, 1);
            obj.rawData.period = zeros(line_count, 1);
            
            for i = 1:line_count
                try
                    data = jsondecode(raw_lines{i});
                    obj.rawData.timestamps(i) = data.wallClock;
                    obj.rawData.game_clock(i) = data.gameClock;
                    obj.rawData.period(i) = data.period;
                    
                    % Extract home team players (first 10)
                    for j = 1:min(10, length(data.homePlayers))
                        if isfield(data.homePlayers(j), 'xyz') && ~isempty(data.homePlayers(j).xyz)
                            obj.rawData.home_players(i, j, :) = data.homePlayers(j).xyz;
                        end
                    end
                    
                    % Extract away team players (first 10)
                    for j = 1:min(10, length(data.awayPlayers))
                        if isfield(data.awayPlayers(j), 'xyz') && ~isempty(data.awayPlayers(j).xyz)
                            obj.rawData.away_players(i, j, :) = data.awayPlayers(j).xyz;
                        end
                    end
                    
                    % Extract ball position
                    if isfield(data, 'ball') && isfield(data.ball, 'xyz') && ~isempty(data.ball.xyz)
                        obj.rawData.ball_position(i, :) = data.ball.xyz;
                    end
                    
                catch ME
                    warning('Error parsing line %d: %s', i, ME.message);
                end
            end
            
            fprintf('Loaded %d data points\n', line_count);
        end
        
        function preprocessData(obj)
            % Clean and preprocess the raw data
            fprintf('Preprocessing data...\n');
            
            % Remove invalid data points
            valid_indices = obj.findValidDataPoints();
            obj.rawData = obj.filterDataByIndices(obj.rawData, valid_indices);
            
            % Normalize coordinates to pitch dimensions
            obj.normalizeCoordinates();
            
            % Synchronize timestamps
            obj.synchronizeTimestamps();
            
            % Compute derived metrics
            obj.computeDerivedMetrics();
            
            fprintf('Data preprocessing complete\n');
        end
        
        function valid_indices = findValidDataPoints(obj)
            % Find data points with valid player positions
            n_points = size(obj.rawData.home_players, 1);
            valid_indices = true(n_points, 1);
            
            for i = 1:n_points
                % Check if we have enough valid player positions
                home_valid = sum(~isnan(obj.rawData.home_players(i, :, 1)));
                away_valid = sum(~isnan(obj.rawData.away_players(i, :, 1)));
                
                % Require at least 8 players from each team
                if home_valid < 8 || away_valid < 8
                    valid_indices(i) = false;
                end
            end
            
            fprintf('Found %d valid data points out of %d total\n', ...
                sum(valid_indices), n_points);
        end
        
        function filtered_data = filterDataByIndices(obj, data, indices)
            % Filter data structure by valid indices
            field_names = fieldnames(data);
            filtered_data = struct();
            
            for i = 1:length(field_names)
                field_name = field_names{i};
                field_data = data.(field_name);
                
                if ismatrix(field_data)
                    filtered_data.(field_name) = field_data(indices, :);
                elseif ndims(field_data) == 3
                    filtered_data.(field_name) = field_data(indices, :, :);
                else
                    filtered_data.(field_name) = field_data(indices);
                end
            end
        end
        
        function normalizeCoordinates(obj)
            % Normalize coordinates to standard pitch dimensions
            fprintf('Normalizing coordinates...\n');
            
            % Get current coordinate ranges
            all_home = obj.rawData.home_players(~isnan(obj.rawData.home_players));
            all_away = obj.rawData.away_players(~isnan(obj.rawData.away_players));
            all_ball = obj.rawData.ball_position(~isnan(obj.rawData.ball_position));
            
            if isempty(all_home) || isempty(all_away)
                warning('No valid coordinate data found for normalization');
                return;
            end
            
            % Find coordinate bounds
            min_x = min([min(all_home(1:3:end)), min(all_away(1:3:end)), min(all_ball(1:3:end))]);
            max_x = max([max(all_home(1:3:end)), max(all_away(1:3:end)), max(all_ball(1:3:end))]);
            min_y = min([min(all_home(2:3:end)), min(all_away(2:3:end)), min(all_ball(2:3:end))]);
            max_y = max([max(all_home(2:3:end)), max(all_away(2:3:end)), max(all_ball(2:3:end))]);
            
            % Normalize to [0, fieldDimensions]
            scale_x = obj.fieldDimensions(1) / (max_x - min_x);
            scale_y = obj.fieldDimensions(2) / (max_y - min_y);
            
            % Apply normalization
            obj.rawData.home_players(:, :, 1) = (obj.rawData.home_players(:, :, 1) - min_x) * scale_x;
            obj.rawData.home_players(:, :, 2) = (obj.rawData.home_players(:, :, 2) - min_y) * scale_y;
            
            obj.rawData.away_players(:, :, 1) = (obj.rawData.away_players(:, :, 1) - min_x) * scale_x;
            obj.rawData.away_players(:, :, 2) = (obj.rawData.away_players(:, :, 2) - min_y) * scale_y;
            
            obj.rawData.ball_position(:, 1) = (obj.rawData.ball_position(:, 1) - min_x) * scale_x;
            obj.rawData.ball_position(:, 2) = (obj.rawData.ball_position(:, 2) - min_y) * scale_y;
            
            fprintf('Coordinates normalized to [0, %d] x [0, %d]\n', ...
                obj.fieldDimensions(1), obj.fieldDimensions(2));
        end
        
        function synchronizeTimestamps(obj)
            % Ensure consistent time sampling
            fprintf('Synchronizing timestamps...\n');
            
            % Create regular time grid
            start_time = min(obj.rawData.timestamps);
            end_time = max(obj.rawData.timestamps);
            dt = 1 / obj.samplingRate;
            regular_times = start_time:dt:end_time;
            
            % Interpolate data to regular grid
            n_regular = length(regular_times);
            n_players = size(obj.rawData.home_players, 2);
            
            % Initialize interpolated data
            interp_home = zeros(n_regular, n_players, 3);
            interp_away = zeros(n_regular, n_players, 3);
            interp_ball = zeros(n_regular, 3);
            
            % Interpolate each player's trajectory
            for p = 1:n_players
                for coord = 1:3
                    % Home players
                    valid_home = ~isnan(obj.rawData.home_players(:, p, coord));
                    if sum(valid_home) > 1
                        interp_home(:, p, coord) = interp1(obj.rawData.timestamps(valid_home), ...
                            obj.rawData.home_players(valid_home, p, coord), regular_times, 'linear', 'extrap');
                    end
                    
                    % Away players
                    valid_away = ~isnan(obj.rawData.away_players(:, p, coord));
                    if sum(valid_away) > 1
                        interp_away(:, p, coord) = interp1(obj.rawData.timestamps(valid_away), ...
                            obj.rawData.away_players(valid_away, p, coord), regular_times, 'linear', 'extrap');
                    end
                end
            end
            
            % Interpolate ball position
            for coord = 1:3
                valid_ball = ~isnan(obj.rawData.ball_position(:, coord));
                if sum(valid_ball) > 1
                    interp_ball(:, coord) = interp1(obj.rawData.timestamps(valid_ball), ...
                        obj.rawData.ball_position(valid_ball, coord), regular_times, 'linear', 'extrap');
                end
            end
            
            % Update data with interpolated values
            obj.rawData.timestamps = regular_times';
            obj.rawData.home_players = interp_home;
            obj.rawData.away_players = interp_away;
            obj.rawData.ball_position = interp_ball;
            
            fprintf('Synchronized to %d time points at %.1f Hz\n', n_regular, obj.samplingRate);
        end
        
        function computeDerivedMetrics(obj)
            % Compute derived metrics for analysis
            fprintf('Computing derived metrics...\n');
            
            n_times = size(obj.rawData.home_players, 1);
            n_players = size(obj.rawData.home_players, 2);
            
            % Initialize metrics
            obj.processedData = struct();
            obj.processedData.home_centroid = zeros(n_times, 2);
            obj.processedData.away_centroid = zeros(n_times, 2);
            obj.processedData.home_spread = zeros(n_times, 1);
            obj.processedData.away_spread = zeros(n_times, 1);
            obj.processedData.inter_team_distance = zeros(n_times, 1);
            obj.processedData.team_shape_ratio = zeros(n_times, 1);
            
            for t = 1:n_times
                % Home team metrics
                home_pos = squeeze(obj.rawData.home_players(t, :, 1:2));
                valid_home = ~isnan(home_pos(:, 1));
                if sum(valid_home) > 0
                    obj.processedData.home_centroid(t, :) = mean(home_pos(valid_home, :), 1);
                    obj.processedData.home_spread(t) = std(home_pos(valid_home, :), [], 'all');
                end
                
                % Away team metrics
                away_pos = squeeze(obj.rawData.away_players(t, :, 1:2));
                valid_away = ~isnan(away_pos(:, 1));
                if sum(valid_away) > 0
                    obj.processedData.away_centroid(t, :) = mean(away_pos(valid_away, :), 1);
                    obj.processedData.away_spread(t) = std(away_pos(valid_away, :), [], 'all');
                end
                
                % Inter-team metrics
                if sum(valid_home) > 0 && sum(valid_away) > 0
                    obj.processedData.inter_team_distance(t) = norm(obj.processedData.home_centroid(t, :) - obj.processedData.away_centroid(t, :));
                    obj.processedData.team_shape_ratio(t) = obj.processedData.home_spread(t) / (obj.processedData.away_spread(t) + eps);
                end
            end
            
            fprintf('Derived metrics computed\n');
        end
        
        function exportProcessedData(obj, output_dir)
            % Export processed data for analysis
            if ~exist(output_dir, 'dir')
                mkdir(output_dir);
            end
            
            % Export player positions
            home_positions = obj.rawData.home_players(:, :, 1:2);
            away_positions = obj.rawData.away_players(:, :, 1:2);
            
            % Reshape for CSV export
            n_times = size(home_positions, 1);
            n_players = size(home_positions, 2);
            
            % Create position matrix [time, home_x1, home_y1, ..., home_x10, home_y10, away_x1, away_y1, ..., away_x10, away_y10]
            position_matrix = zeros(n_times, 2 * n_players * 2);
            
            for p = 1:n_players
                col_idx = (p-1)*2 + 1;
                position_matrix(:, col_idx) = home_positions(:, p, 1);      % home x
                position_matrix(:, col_idx + 1) = home_positions(:, p, 2);  % home y
                
                col_idx = n_players*2 + (p-1)*2 + 1;
                position_matrix(:, col_idx) = away_positions(:, p, 1);      % away x
                position_matrix(:, col_idx + 1) = away_positions(:, p, 2);  % away y
            end
            
            % Save to CSV
            writematrix(position_matrix, fullfile(output_dir, 'processed_positions.csv'));
            
            % Save metadata
            metadata = struct();
            metadata.field_dimensions = obj.fieldDimensions;
            metadata.sampling_rate = obj.samplingRate;
            metadata.n_timesteps = n_times;
            metadata.n_players_per_team = n_players;
            metadata.timestamps = obj.rawData.timestamps;
            
            % Save derived metrics
            writematrix(obj.processedData.home_centroid, fullfile(output_dir, 'home_centroid.csv'));
            writematrix(obj.processedData.away_centroid, fullfile(output_dir, 'away_centroid.csv'));
            writematrix(obj.processedData.inter_team_distance, fullfile(output_dir, 'inter_team_distance.csv'));
            writematrix(obj.processedData.team_shape_ratio, fullfile(output_dir, 'team_shape_ratio.csv'));
            
            % Save metadata as JSON
            fid = fopen(fullfile(output_dir, 'metadata.json'), 'w');
            fprintf(fid, jsonencode(metadata, 'PrettyPrint', true));
            fclose(fid);
            
            fprintf('Processed data exported to: %s\n', output_dir);
        end
        
        function visualizeData(obj, time_range)
            % Visualize the processed data
            if nargin < 2
                time_range = [1, min(100, size(obj.rawData.home_players, 1))];
            end
            
            figure('Position', [100, 100, 1200, 800]);
            
            % Plot 1: Player positions at a specific time
            subplot(2, 3, 1);
            t = time_range(1);
            home_pos = squeeze(obj.rawData.home_players(t, :, 1:2));
            away_pos = squeeze(obj.rawData.away_players(t, :, 1:2));
            
            valid_home = ~isnan(home_pos(:, 1));
            valid_away = ~isnan(away_pos(:, 1));
            
            scatter(home_pos(valid_home, 1), home_pos(valid_home, 2), 100, 'b', 'filled');
            hold on;
            scatter(away_pos(valid_away, 1), away_pos(valid_away, 2), 100, 'r', 'filled');
            scatter(obj.rawData.ball_position(t, 1), obj.rawData.ball_position(t, 2), 50, 'k', 'filled');
            
            xlim([0, obj.fieldDimensions(1)]);
            ylim([0, obj.fieldDimensions(2)]);
            title(sprintf('Player Positions at t=%.1fs', obj.rawData.timestamps(t)));
            xlabel('X Position (m)');
            ylabel('Y Position (m)');
            legend('Home', 'Away', 'Ball', 'Location', 'best');
            grid on;
            
            % Plot 2: Team centroids over time
            subplot(2, 3, 2);
            plot(obj.processedData.home_centroid(time_range(1):time_range(2), 1), ...
                 obj.processedData.home_centroid(time_range(1):time_range(2), 2), 'b-', 'LineWidth', 2);
            hold on;
            plot(obj.processedData.away_centroid(time_range(1):time_range(2), 1), ...
                 obj.processedData.away_centroid(time_range(1):time_range(2), 2), 'r-', 'LineWidth', 2);
            xlim([0, obj.fieldDimensions(1)]);
            ylim([0, obj.fieldDimensions(2)]);
            title('Team Centroid Movement');
            xlabel('X Position (m)');
            ylabel('Y Position (m)');
            legend('Home', 'Away', 'Location', 'best');
            grid on;
            
            % Plot 3: Inter-team distance
            subplot(2, 3, 3);
            plot(obj.rawData.timestamps(time_range(1):time_range(2)), ...
                 obj.processedData.inter_team_distance(time_range(1):time_range(2)), 'g-', 'LineWidth', 2);
            title('Inter-team Distance');
            xlabel('Time (s)');
            ylabel('Distance (m)');
            grid on;
            
            % Plot 4: Team shape ratio
            subplot(2, 3, 4);
            plot(obj.rawData.timestamps(time_range(1):time_range(2)), ...
                 obj.processedData.team_shape_ratio(time_range(1):time_range(2)), 'm-', 'LineWidth', 2);
            title('Team Shape Ratio (Home/Away)');
            xlabel('Time (s)');
            ylabel('Ratio');
            grid on;
            
            % Plot 5: Team spread
            subplot(2, 3, 5);
            plot(obj.rawData.timestamps(time_range(1):time_range(2)), ...
                 obj.processedData.home_spread(time_range(1):time_range(2)), 'b-', 'LineWidth', 2);
            hold on;
            plot(obj.rawData.timestamps(time_range(1):time_range(2)), ...
                 obj.processedData.away_spread(time_range(1):time_range(2)), 'r-', 'LineWidth', 2);
            title('Team Spread');
            xlabel('Time (s)');
            ylabel('Spread (m)');
            legend('Home', 'Away', 'Location', 'best');
            grid on;
            
            % Plot 6: Ball trajectory
            subplot(2, 3, 6);
            ball_pos = obj.rawData.ball_position(time_range(1):time_range(2), 1:2);
            valid_ball = ~isnan(ball_pos(:, 1));
            plot(ball_pos(valid_ball, 1), ball_pos(valid_ball, 2), 'k-', 'LineWidth', 2);
            xlim([0, obj.fieldDimensions(1)]);
            ylim([0, obj.fieldDimensions(2)]);
            title('Ball Trajectory');
            xlabel('X Position (m)');
            ylabel('Y Position (m)');
            grid on;
        end
    end
end
