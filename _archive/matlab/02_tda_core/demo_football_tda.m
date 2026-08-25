% Demo script for Football TDA Analysis
% This script demonstrates the complete pipeline from data preprocessing to TDA analysis

clear; clc; close all;

fprintf('=== Football TDA Analysis Demo ===\n\n');

%% Step 1: Generate or load data
fprintf('Step 1: Preparing data...\n');

% Generate synthetic data for demonstration
generator = FootballDataGenerator();
data = generator.generateMatchData('f442', 'defensive_press');

% Convert to point cloud format for TDA
n_times = size(data.positions, 1);
n_players = size(data.positions, 2);

% Create 22-player point clouds (10 home + 10 away + 2 reference points)
point_clouds = {};
timestamps = (1:n_times)' / 10; % 10 Hz sampling

for t = 1:min(100, n_times) % Analyze first 100 time points
    point_cloud = zeros(22, 2);
    
    % Home team players (first 10)
    for p = 1:min(10, n_players)
        point_cloud(p, :) = data.positions(t, p, :);
    end
    
    % Away team players (offset for demonstration)
    for p = 1:min(10, n_players)
        point_cloud(10 + p, :) = data.positions(t, p, :) + [20, 0];
    end
    
    % Add ball position (center of field)
    point_cloud(21, :) = [50, 34];
    
    % Add reference point (corner)
    point_cloud(22, :) = [0, 0];
    
    point_clouds{t} = point_cloud;
end

fprintf('Generated %d point clouds for analysis\n', length(point_clouds));

%% Step 2: Initialize TDA analyzer
fprintf('\nStep 2: Initializing TDA analyzer...\n');

tda = FootballTDA();

% Set analysis parameters
params = struct();
params.maxDimension = 1;           % Focus on 0D and 1D homology
params.maxDistance = 40;           % Maximum distance for VR complex
params.distanceStep = 1.0;         % Step size for filtration
params.minPersistence = 2.0;       % Minimum persistence threshold
params.fieldDimensions = [105, 68]; % Field dimensions

tda.setParameters(params);

% Add point clouds to analyzer
for t = 1:length(point_clouds)
    metadata = struct();
    metadata.time_index = t;
    metadata.formation = 'f442';
    metadata.scenario = 'defensive_press';
    
    tda.addPointCloud(point_clouds{t}, timestamps(t), metadata);
end

fprintf('TDA analyzer initialized with %d point clouds\n', length(point_clouds));

%% Step 3: Compute persistent homology
fprintf('\nStep 3: Computing persistent homology...\n');

% Compute persistent homology for all point clouds
tda.computePersistentHomology();

fprintf('Persistent homology computation complete\n');

%% Step 4: Extract topological features
fprintf('\nStep 4: Extracting topological features...\n');

tda.extractTopologicalFeatures();

fprintf('Topological features extracted\n');

%% Step 5: Visualize results
fprintf('\nStep 5: Visualizing results...\n');

% Visualize persistence diagrams for selected time points
selected_times = [1, 25, 50, 75];
tda.visualizePersistenceDiagrams(selected_times);

% Visualize topological features over time
tda.visualizeTopologicalFeatures();

%% Step 6: Analyze results
fprintf('\nStep 6: Analyzing results...\n');

% Print summary statistics
features = tda.topologicalFeatures;
fprintf('\nTopological Analysis Summary:\n');
fprintf('Time period: %.1f - %.1f seconds\n', min(features.timestamps), max(features.timestamps));
fprintf('Number of time points analyzed: %d\n', length(features.timestamps));

fprintf('\n0-Dimensional Homology (Connected Components):\n');
fprintf('  Average number of components: %.2f ± %.2f\n', mean(features.num_components), std(features.num_components));
fprintf('  Average maximum persistence: %.2f ± %.2f\n', mean(features.max_persistence_0d), std(features.max_persistence_0d));
fprintf('  Average total persistence: %.2f ± %.2f\n', mean(features.total_persistence_0d), std(features.total_persistence_0d));

fprintf('\n1-Dimensional Homology (Loops/Holes):\n');
fprintf('  Average number of loops: %.2f ± %.2f\n', mean(features.num_loops), std(features.num_loops));
fprintf('  Average maximum persistence: %.2f ± %.2f\n', mean(features.max_persistence_1d), std(features.max_persistence_1d));
fprintf('  Average total persistence: %.2f ± %.2f\n', mean(features.total_persistence_1d), std(features.total_persistence_1d));

%% Step 7: Identify interesting patterns
fprintf('\nStep 7: Identifying interesting patterns...\n');

% Find time points with high topological activity
high_activity_0d = features.num_components > mean(features.num_components) + std(features.num_components);
high_activity_1d = features.num_loops > mean(features.num_loops) + std(features.num_loops);

fprintf('Time points with high 0D activity: %d\n', sum(high_activity_0d));
fprintf('Time points with high 1D activity: %d\n', sum(high_activity_1d));

% Find time points with persistent holes (defensive gaps)
persistent_holes = features.max_persistence_1d > mean(features.max_persistence_1d) + std(features.max_persistence_1d);
fprintf('Time points with persistent defensive holes: %d\n', sum(persistent_holes));

if sum(persistent_holes) > 0
    hole_times = features.timestamps(persistent_holes);
    fprintf('Defensive holes detected at times: %.1f, %.1f, %.1f, ...\n', hole_times(1:min(3, length(hole_times))));
end

%% Step 8: Create comprehensive analysis figure
fprintf('\nStep 8: Creating comprehensive analysis...\n');

figure('Position', [300, 300, 1600, 1000]);

% Plot 1: Point cloud evolution
subplot(3, 4, 1);
t = 1;
pc = point_clouds{t};
scatter(pc(1:10, 1), pc(1:10, 2), 100, 'b', 'filled');
hold on;
scatter(pc(11:20, 1), pc(11:20, 2), 100, 'r', 'filled');
scatter(pc(21, 1), pc(21, 2), 150, 'k', 'filled', 'diamond');
xlim([0, 105]); ylim([0, 68]);
title(sprintf('Formation at t=%.1fs', timestamps(t)));
xlabel('X (m)'); ylabel('Y (m)');
legend('Home', 'Away', 'Ball', 'Location', 'best');
grid on;

% Plot 2: Topological features over time
subplot(3, 4, 2);
plot(features.timestamps, features.num_components, 'b-', 'LineWidth', 2);
hold on;
plot(features.timestamps, features.num_loops, 'r-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Count');
title('Topological Features');
legend('Components', 'Loops', 'Location', 'best');
grid on;

% Plot 3: Persistence evolution
subplot(3, 4, 3);
plot(features.timestamps, features.max_persistence_0d, 'b-', 'LineWidth', 2);
hold on;
plot(features.timestamps, features.max_persistence_1d, 'r-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Persistence');
title('Maximum Persistence');
legend('0D', '1D', 'Location', 'best');
grid on;

% Plot 4: Feature correlation
subplot(3, 4, 4);
scatter(features.num_components, features.num_loops, 50, features.timestamps, 'filled');
xlabel('Components'); ylabel('Loops');
title('Feature Correlation');
colorbar; grid on;

% Plot 5-8: Persistence diagrams for key moments
key_moments = [1, 25, 50, 75];
for i = 1:4
    subplot(3, 4, 4 + i);
    if key_moments(i) <= length(tda.persistenceDiagrams)
        diagram = tda.persistenceDiagrams{key_moments(i)};
        
        % Plot 0D persistence
        if ~isempty(diagram.births{1}) && ~isempty(diagram.deaths{1})
            scatter(diagram.births{1}, diagram.deaths{1}, 100, 'b', 'filled');
            hold on;
        end
        
        % Plot 1D persistence
        if length(diagram.births) > 1 && ~isempty(diagram.births{2}) && ~isempty(diagram.deaths{2})
            scatter(diagram.births{2}, diagram.deaths{2}, 100, 'r', 'filled');
        end
        
        % Add diagonal
        max_val = max([max(diagram.births{1}), max(diagram.deaths{1})]);
        if ~isempty(max_val) && ~isnan(max_val)
            plot([0, max_val], [0, max_val], 'k--', 'LineWidth', 1);
        end
        
        xlabel('Birth'); ylabel('Death');
        title(sprintf('Persistence (t=%.1f)', diagram.timestamp));
        grid on;
    end
end

% Plot 9: Team dynamics correlation
subplot(3, 4, 9);
plot(features.timestamps, features.total_persistence_0d, 'b-', 'LineWidth', 2);
hold on;
plot(features.timestamps, features.total_persistence_1d, 'r-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Total Persistence');
title('Team Dynamics');
legend('0D', '1D', 'Location', 'best');
grid on;

% Plot 10: Persistence entropy
subplot(3, 4, 10);
plot(features.timestamps, features.persistence_entropy_0d, 'b-', 'LineWidth', 2);
hold on;
plot(features.timestamps, features.persistence_entropy_1d, 'r-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Entropy');
title('Persistence Entropy');
legend('0D', '1D', 'Location', 'best');
grid on;

% Plot 11: Activity heatmap
subplot(3, 4, 11);
activity_matrix = [features.num_components, features.num_loops, features.max_persistence_0d, features.max_persistence_1d];
imagesc(activity_matrix');
colorbar;
xlabel('Time Points');
ylabel('Features');
title('Activity Heatmap');
set(gca, 'YTickLabel', {'Components', 'Loops', 'Max Pers 0D', 'Max Pers 1D'});

% Plot 12: Summary statistics
subplot(3, 4, 12);
stats = [mean(features.num_components), mean(features.num_loops), ...
         mean(features.max_persistence_0d), mean(features.max_persistence_1d)];
bar(stats);
set(gca, 'XTickLabel', {'Components', 'Loops', 'Max Pers 0D', 'Max Pers 1D'});
title('Average Values');
ylabel('Value');
grid on;

sgtitle('Football TDA Analysis Results');

%% Step 9: Export results
fprintf('\nStep 9: Exporting results...\n');

output_dir = './tda_analysis_results';
tda.exportResults(output_dir);

% Save point clouds for further analysis
save(fullfile(output_dir, 'point_clouds.mat'), 'point_clouds', 'timestamps');

fprintf('Results exported to: %s\n', output_dir);

%% Step 10: Generate analysis report
fprintf('\nStep 10: Generating analysis report...\n');

% Create a simple text report
report_file = fullfile(output_dir, 'analysis_report.txt');
fid = fopen(report_file, 'w');

fprintf(fid, 'Football TDA Analysis Report\n');
fprintf(fid, '==========================\n\n');
fprintf(fid, 'Analysis Parameters:\n');
fprintf(fid, '  Max Dimension: %d\n', params.maxDimension);
fprintf(fid, '  Max Distance: %.1f\n', params.maxDistance);
fprintf(fid, '  Distance Step: %.1f\n', params.distanceStep);
fprintf(fid, '  Min Persistence: %.1f\n', params.minPersistence);
fprintf(fid, '\n');

fprintf(fid, 'Data Summary:\n');
fprintf(fid, '  Time Points Analyzed: %d\n', length(features.timestamps));
fprintf(fid, '  Time Range: %.1f - %.1f seconds\n', min(features.timestamps), max(features.timestamps));
fprintf(fid, '  Formation: %s\n', 'f442');
fprintf(fid, '  Scenario: %s\n', 'defensive_press');
fprintf(fid, '\n');

fprintf(fid, 'Topological Features:\n');
fprintf(fid, '  0D Homology (Components):\n');
fprintf(fid, '    Average Count: %.2f ± %.2f\n', mean(features.num_components), std(features.num_components));
fprintf(fid, '    Average Max Persistence: %.2f ± %.2f\n', mean(features.max_persistence_0d), std(features.max_persistence_0d));
fprintf(fid, '    Average Total Persistence: %.2f ± %.2f\n', mean(features.total_persistence_0d), std(features.total_persistence_0d));
fprintf(fid, '\n');

fprintf(fid, '  1D Homology (Loops/Holes):\n');
fprintf(fid, '    Average Count: %.2f ± %.2f\n', mean(features.num_loops), std(features.num_loops));
fprintf(fid, '    Average Max Persistence: %.2f ± %.2f\n', mean(features.max_persistence_1d), std(features.max_persistence_1d));
fprintf(fid, '    Average Total Persistence: %.2f ± %.2f\n', mean(features.total_persistence_1d), std(features.total_persistence_1d));
fprintf(fid, '\n');

fprintf(fid, 'Key Findings:\n');
fprintf(fid, '  High 0D activity detected at %d time points\n', sum(high_activity_0d));
fprintf(fid, '  High 1D activity detected at %d time points\n', sum(high_activity_1d));
fprintf(fid, '  Persistent defensive holes detected at %d time points\n', sum(persistent_holes));
fprintf(fid, '\n');

fprintf(fid, 'Interpretation:\n');
fprintf(fid, '  - 0D homology measures team connectivity and clustering\n');
fprintf(fid, '  - 1D homology measures defensive holes and attacking opportunities\n');
fprintf(fid, '  - High persistence indicates stable topological features\n');
fprintf(fid, '  - Entropy measures the complexity of the topological structure\n');

fclose(fid);

fprintf('Analysis report saved to: %s\n', report_file);

%% Summary
fprintf('\n=== Analysis Complete ===\n');
fprintf('The Football TDA analysis has been completed successfully.\n');
fprintf('Key outputs:\n');
fprintf('  - Persistence diagrams for each time point\n');
fprintf('  - Topological features extracted and analyzed\n');
fprintf('  - Comprehensive visualizations of team dynamics\n');
fprintf('  - Statistical analysis of topological patterns\n');
fprintf('  - Analysis report with key findings\n');
fprintf('\nNext steps:\n');
fprintf('  - Apply this analysis to real match data\n');
fprintf('  - Develop coupled team dynamics analysis\n');
fprintf('  - Link topological features to performance metrics\n');
fprintf('  - Identify attractor states in team formations\n');
