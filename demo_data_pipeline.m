% Demo script for the new DataPipeline class
% This script demonstrates how to use the enhanced data preprocessing pipeline

clear; clc; close all;

%% Initialize the data pipeline
fprintf('=== Football TDA Data Pipeline Demo ===\n\n');

pipeline = DataPipeline();

%% Option 1: Load real SecondSpectrum data (if available)
% Uncomment and modify the path to your real data file
% real_data_file = '/path/to/your/secondspectrum_data.jsonl';
% if exist(real_data_file, 'file')
%     fprintf('Loading real SecondSpectrum data...\n');
%     pipeline.loadSecondSpectrumData(real_data_file);
%     pipeline.preprocessData();
%     pipeline.visualizeData();
%     pipeline.exportProcessedData('./processed_real_data');
% else
%     fprintf('Real data file not found. Using synthetic data instead.\n\n');
% end

%% Option 2: Generate and process synthetic data
fprintf('Generating synthetic match data...\n');

% Create synthetic data generator
generator = FootballDataGenerator();

% Generate data for different scenarios
scenarios = {'defensive_press', 'attacking_buildup', 'possession'};
formations = {'f442', 'f433', 'f352'};

for i = 1:length(scenarios)
    fprintf('\n--- Processing scenario: %s ---\n', scenarios{i});
    
    % Generate synthetic data
    data = generator.generateMatchData(formations{1}, scenarios{i});
    
    % Convert to pipeline format
    pipeline.rawData = struct();
    pipeline.rawData.timestamps = (1:size(data.positions, 1))' / pipeline.samplingRate;
    pipeline.rawData.home_players = zeros(size(data.positions, 1), 10, 3);
    pipeline.rawData.away_players = zeros(size(data.positions, 1), 10, 3);
    pipeline.rawData.ball_position = zeros(size(data.positions, 1), 3);
    
    % Fill in player positions (assuming first 10 are home team, next 10 are away team)
    n_players = min(10, size(data.positions, 2));
    pipeline.rawData.home_players(:, 1:n_players, 1:2) = data.positions(:, 1:n_players, :);
    pipeline.rawData.away_players(:, 1:n_players, 1:2) = data.positions(:, 1:n_players, :) + [20, 0]; % Offset away team
    
    % Add some ball movement
    pipeline.rawData.ball_position(:, 1) = 50 + 10 * sin((1:size(data.positions, 1))' / 100);
    pipeline.rawData.ball_position(:, 2) = 34 + 5 * cos((1:size(data.positions, 1))' / 150);
    
    % Preprocess the data
    pipeline.preprocessData();
    
    % Visualize the data
    pipeline.visualizeData([1, min(200, size(pipeline.rawData.home_players, 1))]);
    sgtitle(sprintf('Scenario: %s (%s formation)', scenarios{i}, formations{1}));
    
    % Export processed data
    output_dir = sprintf('./processed_%s_data', scenarios{i});
    pipeline.exportProcessedData(output_dir);
    
    fprintf('Scenario %s processed and exported to: %s\n', scenarios{i}, output_dir);
end

%% Demonstrate data analysis capabilities
fprintf('\n=== Data Analysis Demo ===\n');

% Load one of the processed datasets for analysis
if exist('./processed_defensive_press_data', 'dir')
    fprintf('Loading processed defensive press data for analysis...\n');
    
    % Load the processed data
    positions = readmatrix('./processed_defensive_press_data/processed_positions.csv');
    home_centroid = readmatrix('./processed_defensive_press_data/home_centroid.csv');
    away_centroid = readmatrix('./processed_defensive_press_data/away_centroid.csv');
    inter_team_distance = readmatrix('./processed_defensive_press_data/inter_team_distance.csv');
    team_shape_ratio = readmatrix('./processed_defensive_press_data/team_shape_ratio.csv');
    
    % Create analysis figure
    figure('Position', [200, 200, 1400, 600]);
    
    % Plot 1: Team dynamics over time
    subplot(1, 3, 1);
    time_axis = (1:length(inter_team_distance)) / pipeline.samplingRate;
    plot(time_axis, inter_team_distance, 'b-', 'LineWidth', 2);
    hold on;
    plot(time_axis, team_shape_ratio * 20, 'r-', 'LineWidth', 2); % Scale for visibility
    xlabel('Time (s)');
    ylabel('Distance (m) / Scaled Ratio');
    title('Team Dynamics Over Time');
    legend('Inter-team Distance', 'Team Shape Ratio (×20)', 'Location', 'best');
    grid on;
    
    % Plot 2: Phase space (centroid positions)
    subplot(1, 3, 2);
    plot(home_centroid(:, 1), home_centroid(:, 2), 'b-', 'LineWidth', 2);
    hold on;
    plot(away_centroid(:, 1), away_centroid(:, 2), 'r-', 'LineWidth', 2);
    xlabel('X Position (m)');
    ylabel('Y Position (m)');
    title('Team Centroid Phase Space');
    legend('Home Team', 'Away Team', 'Location', 'best');
    grid on;
    axis equal;
    
    % Plot 3: Statistical analysis
    subplot(1, 3, 3);
    histogram(inter_team_distance, 20, 'FaceAlpha', 0.7);
    hold on;
    histogram(team_shape_ratio, 20, 'FaceAlpha', 0.7);
    xlabel('Value');
    ylabel('Frequency');
    title('Distribution of Team Metrics');
    legend('Inter-team Distance', 'Team Shape Ratio', 'Location', 'best');
    grid on;
    
    % Print summary statistics
    fprintf('\nSummary Statistics for Defensive Press Scenario:\n');
    fprintf('Inter-team Distance: Mean=%.2f, Std=%.2f, Range=[%.2f, %.2f]\n', ...
        mean(inter_team_distance), std(inter_team_distance), ...
        min(inter_team_distance), max(inter_team_distance));
    fprintf('Team Shape Ratio: Mean=%.2f, Std=%.2f, Range=[%.2f, %.2f]\n', ...
        mean(team_shape_ratio), std(team_shape_ratio), ...
        min(team_shape_ratio), max(team_shape_ratio));
end

%% Demonstrate TDA preparation
fprintf('\n=== TDA Preparation Demo ===\n');

% Show how to extract point clouds for TDA analysis
if exist('./processed_defensive_press_data', 'dir')
    fprintf('Preparing point clouds for TDA analysis...\n');
    
    % Extract a few time points for TDA analysis
    time_points = [50, 100, 150, 200]; % Sample time points
    point_clouds = {};
    
    for i = 1:length(time_points)
        t = time_points(i);
        if t <= size(positions, 1)
            % Extract 22-player point cloud (10 home + 10 away + 2 additional)
            point_cloud = zeros(22, 2);
            
            % Home team players (first 10)
            for p = 1:10
                point_cloud(p, 1) = positions(t, (p-1)*2 + 1);      % x
                point_cloud(p, 2) = positions(t, (p-1)*2 + 2);      % y
            end
            
            % Away team players (next 10)
            for p = 1:10
                point_cloud(10 + p, 1) = positions(t, 20 + (p-1)*2 + 1);  % x
                point_cloud(10 + p, 2) = positions(t, 20 + (p-1)*2 + 2);  % y
            end
            
            % Add ball position (if available)
            point_cloud(21, :) = [50, 34]; % Center of field as ball proxy
            
            % Add a reference point
            point_cloud(22, :) = [0, 0]; % Corner as reference
            
            point_clouds{i} = point_cloud;
            
            fprintf('Time point %d: Extracted %d-point cloud\n', t, size(point_cloud, 1));
        end
    end
    
    % Visualize the point clouds
    figure('Position', [300, 300, 1200, 400]);
    for i = 1:length(point_clouds)
        subplot(1, length(point_clouds), i);
        pc = point_clouds{i};
        scatter(pc(1:10, 1), pc(1:10, 2), 100, 'b', 'filled');
        hold on;
        scatter(pc(11:20, 1), pc(11:20, 2), 100, 'r', 'filled');
        scatter(pc(21, 1), pc(21, 2), 150, 'k', 'filled', 'diamond');
        scatter(pc(22, 1), pc(22, 2), 50, 'g', 'filled', 's');
        
        xlim([0, 105]);
        ylim([0, 68]);
        title(sprintf('Point Cloud at t=%d', time_points(i)));
        xlabel('X Position (m)');
        ylabel('Y Position (m)');
        legend('Home', 'Away', 'Ball', 'Ref', 'Location', 'best');
        grid on;
    end
    
    fprintf('Point clouds prepared for TDA analysis!\n');
    fprintf('Next step: Apply persistent homology computation to these point clouds.\n');
end

fprintf('\n=== Demo Complete ===\n');
fprintf('The data pipeline is now ready for TDA analysis.\n');
fprintf('Key outputs:\n');
fprintf('  - Clean, synchronized player position data\n');
fprintf('  - Derived team metrics (centroids, spreads, distances)\n');
fprintf('  - Point clouds ready for persistent homology computation\n');
fprintf('  - Comprehensive visualizations of team dynamics\n');
