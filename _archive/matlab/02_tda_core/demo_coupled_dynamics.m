% Demo script for Coupled Team Dynamics Analysis
% This script demonstrates the complete coupled dynamics analysis pipeline

clear; clc; close all;

fprintf('=== Coupled Team Dynamics Analysis Demo ===\n\n');

%% Step 1: Generate or load team data
fprintf('Step 1: Preparing team data...\n');

% Generate synthetic data for demonstration
generator = FootballDataGenerator();

% Generate data for different scenarios to show coupled dynamics
scenarios = {'defensive_press', 'attacking_buildup', 'possession'};
all_data = {};

for i = 1:length(scenarios)
    data = generator.generateMatchData('f442', scenarios{i});
    all_data{i} = data;
end

% Use defensive press scenario for detailed analysis
data = all_data{1};
n_times = size(data.positions, 1);
n_players = size(data.positions, 2);

% Create home and away team positions
home_positions = zeros(n_times, n_players, 3);
away_positions = zeros(n_times, n_players, 3);

% Home team: use original positions
home_positions(:, :, 1:2) = data.positions(:, :, :);

% Away team: create opposing formation with some interaction
for t = 1:n_times
    for p = 1:n_players
        % Away team starts in opposite half
        away_positions(t, p, 1) = 105 - data.positions(t, p, 1) + 10 * sin(t/50); % Add some movement
        away_positions(t, p, 2) = 68 - data.positions(t, p, 2) + 5 * cos(t/30);
        away_positions(t, p, 3) = 0; % Z coordinate
    end
end

% Add some tactical interaction
for t = 1:n_times
    % Home team pressing forward
    if t > n_times/3
        home_positions(t, :, 1) = home_positions(t, :, 1) + 5 * sin(t/20);
    end
    
    % Away team responding
    if t > n_times/2
        away_positions(t, :, 1) = away_positions(t, :, 1) - 3 * cos(t/25);
    end
end

timestamps = (1:n_times)' / 10; % 10 Hz sampling

metadata = struct();
metadata.formation = 'f442';
metadata.scenario = 'defensive_press';
metadata.field_dimensions = [105, 68];

fprintf('Generated team data: %d time points, %d players per team\n', n_times, n_players);

%% Step 2: Initialize coupled dynamics analyzer
fprintf('\nStep 2: Initializing coupled dynamics analyzer...\n');

coupled_analyzer = CoupledTeamDynamics();

% Set analysis parameters
params = struct();
params.fieldDimensions = [105, 68];
params.samplingRate = 10;
params.attractorThreshold = 0.1;
params.minAttractorDuration = 5.0;
params.symmetryThreshold = 0.05;
params.zeroSumThreshold = 0.8;

coupled_analyzer.setParameters(params);

% Load team data
coupled_analyzer.loadTeamData(home_positions, away_positions, timestamps, metadata);

fprintf('Coupled dynamics analyzer initialized\n');

%% Step 3: Compute coupled metrics
fprintf('\nStep 3: Computing coupled team dynamics metrics...\n');

coupled_analyzer.computeCoupledMetrics();

fprintf('Coupled metrics computed\n');

%% Step 4: Identify attractor states
fprintf('\nStep 4: Identifying attractor states...\n');

coupled_analyzer.identifyAttractorStates();

fprintf('Attractor states identified\n');

%% Step 5: Analyze symmetry breaking
fprintf('\nStep 5: Analyzing symmetry breaking...\n');

coupled_analyzer.analyzeSymmetryBreaking();

fprintf('Symmetry analysis complete\n');

%% Step 6: Analyze zero-sum dynamics
fprintf('\nStep 6: Analyzing zero-sum dynamics...\n');

coupled_analyzer.analyzeZeroSumDynamics();

fprintf('Zero-sum analysis complete\n');

%% Step 7: Visualize results
fprintf('\nStep 7: Visualizing coupled dynamics...\n');

coupled_analyzer.visualizeCoupledDynamics();

%% Step 8: Analyze results
fprintf('\nStep 8: Analyzing results...\n');

% Print summary statistics
metrics = coupled_analyzer.coupledMetrics;
fprintf('\nCoupled Dynamics Analysis Summary:\n');
fprintf('Time period: %.1f - %.1f seconds\n', min(timestamps), max(timestamps));
fprintf('Number of time points analyzed: %d\n', length(timestamps));

fprintf('\nTeam Coupling Metrics:\n');
fprintf('  Average inter-team distance: %.2f ± %.2f m\n', mean(metrics.inter_team_distance), std(metrics.inter_team_distance));
fprintf('  Average team shape ratio: %.2f ± %.2f\n', mean(metrics.team_shape_ratio), std(metrics.team_shape_ratio));
fprintf('  Average nearest opponent distance: %.2f ± %.2f m\n', mean(metrics.mean_nearest_opponent_distance), std(metrics.mean_nearest_opponent_distance));
fprintf('  Average relative velocity: %.2f ± %.2f m/s\n', mean(metrics.relative_velocity), std(metrics.relative_velocity));
fprintf('  Average space control ratio: %.2f ± %.2f\n', mean(metrics.space_control_ratio), std(metrics.space_control_ratio));
fprintf('  Average pressure intensity: %.2f ± %.2f\n', mean(metrics.pressure_intensity), std(metrics.pressure_intensity));

% Attractor analysis
if isfield(coupled_analyzer.attractorStates, 'n_clusters')
    fprintf('\nAttractor States:\n');
    fprintf('  Number of attractor states: %d\n', coupled_analyzer.attractorStates.n_clusters);
    
    for i = 1:coupled_analyzer.attractorStates.n_clusters
        stats = coupled_analyzer.attractorStates.cluster_stats{i};
        fprintf('  Attractor %d: Duration=%.1fs, Frequency=%.2f\n', i, stats.duration, stats.frequency);
    end
end

% Phase transitions
if isfield(coupled_analyzer.phaseTransitions, 'n_transitions')
    fprintf('\nPhase Transitions:\n');
    fprintf('  Number of transitions: %d\n', coupled_analyzer.phaseTransitions.n_transitions);
    if coupled_analyzer.phaseTransitions.n_transitions > 0
        fprintf('  Average transition interval: %.1f ± %.1f time points\n', ...
            coupled_analyzer.phaseTransitions.mean_interval, coupled_analyzer.phaseTransitions.std_interval);
    end
end

% Symmetry analysis
if isfield(coupled_analyzer.symmetryAnalysis, 'overload_events')
    fprintf('\nSymmetry Analysis:\n');
    fprintf('  Overload events: %d\n', length(coupled_analyzer.symmetryAnalysis.overload_events));
    fprintf('  Symmetry breaking events: %d\n', length(coupled_analyzer.symmetryAnalysis.symmetry_breaking_events));
end

% Zero-sum analysis
if isfield(coupled_analyzer.analysisResults, 'zero_sum_analysis')
    fprintf('\nZero-sum Dynamics:\n');
    fprintf('  Shape correlation: %.3f\n', coupled_analyzer.analysisResults.zero_sum_analysis.shape_correlation);
    fprintf('  Zero-sum strength: %.3f\n', coupled_analyzer.analysisResults.zero_sum_analysis.zero_sum_strength);
    fprintf('  Pressure correlation: %.3f\n', coupled_analyzer.analysisResults.zero_sum_analysis.pressure_correlation);
end

%% Step 9: Create detailed analysis figure
fprintf('\nStep 9: Creating detailed analysis...\n');

figure('Position', [200, 200, 1800, 1200]);

% Plot 1: Team formations at key moments
subplot(3, 5, 1);
key_times = [1, 25, 50, 75];
colors = {'b', 'r', 'g', 'm'};
for i = 1:length(key_times)
    t = key_times(i);
    home_pos = squeeze(home_positions(t, :, 1:2));
    away_pos = squeeze(away_positions(t, :, 1:2));
    
    scatter(home_pos(:, 1), home_pos(:, 2), 100, colors{i}, 'filled', 'MarkerFaceAlpha', 0.7);
    hold on;
    scatter(away_pos(:, 1), away_pos(:, 2), 100, colors{i}, 'filled', 'MarkerFaceAlpha', 0.7);
end
xlim([0, 105]); ylim([0, 68]);
xlabel('X Position (m)'); ylabel('Y Position (m)');
title('Team Formations (Key Moments)');
legend('t=1s', 't=2.5s', 't=5s', 't=7.5s', 'Location', 'best');
grid on;

% Plot 2: Inter-team distance evolution
subplot(3, 5, 2);
plot(timestamps, metrics.inter_team_distance, 'b-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Distance (m)');
title('Inter-team Distance');
grid on;

% Plot 3: Team shape ratio
subplot(3, 5, 3);
plot(timestamps, metrics.team_shape_ratio, 'r-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Ratio');
title('Team Shape Ratio');
grid on;

% Plot 4: Nearest opponent distances
subplot(3, 5, 4);
plot(timestamps, metrics.mean_nearest_opponent_distance, 'g-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Distance (m)');
title('Marking Intensity');
grid on;

% Plot 5: Relative velocity
subplot(3, 5, 5);
plot(timestamps, metrics.relative_velocity, 'm-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Velocity (m/s)');
title('Relative Velocity');
grid on;

% Plot 6: Space control ratio
subplot(3, 5, 6);
plot(timestamps, metrics.space_control_ratio, 'c-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Ratio');
title('Space Control');
grid on;

% Plot 7: Pressure intensity
subplot(3, 5, 7);
plot(timestamps, metrics.pressure_intensity, 'k-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Intensity');
title('Pressure Dynamics');
grid on;

% Plot 8: Attractor states
subplot(3, 5, 8);
if isfield(coupled_analyzer.attractorStates, 'cluster_ids')
    scatter(timestamps, coupled_analyzer.attractorStates.cluster_ids, 50, coupled_analyzer.attractorStates.cluster_ids, 'filled');
    xlabel('Time (s)'); ylabel('Attractor State');
    title('Attractor Evolution');
    colorbar;
else
    text(0.5, 0.5, 'No attractor data', 'HorizontalAlignment', 'center');
    title('Attractor States');
end

% Plot 9: Symmetry analysis
subplot(3, 5, 9);
if isfield(coupled_analyzer.symmetryAnalysis, 'field_symmetry')
    plot(timestamps, coupled_analyzer.symmetryAnalysis.field_symmetry, 'b-', 'LineWidth', 2);
    hold on;
    plot(timestamps, coupled_analyzer.symmetryAnalysis.formation_symmetry, 'r-', 'LineWidth', 2);
    xlabel('Time (s)'); ylabel('Symmetry');
    title('Symmetry Analysis');
    legend('Field', 'Formation', 'Location', 'best');
    grid on;
else
    text(0.5, 0.5, 'No symmetry data', 'HorizontalAlignment', 'center');
    title('Symmetry Analysis');
end

% Plot 10: Phase transitions
subplot(3, 5, 10);
plot(timestamps, metrics.inter_team_distance, 'b-', 'LineWidth', 1);
hold on;
if isfield(coupled_analyzer.phaseTransitions, 'transition_times')
    for i = 1:length(coupled_analyzer.phaseTransitions.transition_times)
        xline(coupled_analyzer.phaseTransitions.transition_times(i), 'r--', 'LineWidth', 2);
    end
end
xlabel('Time (s)'); ylabel('Distance (m)');
title('Phase Transitions');
grid on;

% Plot 11: State space
subplot(3, 5, 11);
if isfield(coupled_analyzer.attractorStates, 'cluster_ids')
    state_space = coupled_analyzer.createStateSpace();
    scatter(state_space(:, 1), state_space(:, 2), 50, coupled_analyzer.attractorStates.cluster_ids, 'filled');
    xlabel('Inter-team Distance (norm)'); ylabel('Team Shape Ratio (norm)');
    title('State Space');
    colorbar;
else
    text(0.5, 0.5, 'No state space data', 'HorizontalAlignment', 'center');
    title('State Space');
end

% Plot 12: Zero-sum analysis
subplot(3, 5, 12);
if isfield(coupled_analyzer.analysisResults, 'zero_sum_analysis')
    bar([coupled_analyzer.analysisResults.zero_sum_analysis.shape_correlation, ...
         coupled_analyzer.analysisResults.zero_sum_analysis.zero_sum_strength]);
    set(gca, 'XTickLabel', {'Shape Corr', 'Zero-sum'});
    ylabel('Correlation');
    title('Zero-sum Dynamics');
    grid on;
else
    text(0.5, 0.5, 'No zero-sum data', 'HorizontalAlignment', 'center');
    title('Zero-sum Analysis');
end

% Plot 13: Metric correlations
subplot(3, 5, 13);
metric_matrix = [metrics.inter_team_distance, metrics.team_shape_ratio, ...
                metrics.mean_nearest_opponent_distance, metrics.relative_velocity, ...
                metrics.space_control_ratio, metrics.pressure_intensity];
correlation_matrix = corrcoef(metric_matrix);
imagesc(correlation_matrix);
colorbar;
title('Metric Correlations');
set(gca, 'XTickLabel', {'Dist', 'Shape', 'Marking', 'Velocity', 'Space', 'Pressure'});
set(gca, 'YTickLabel', {'Dist', 'Shape', 'Marking', 'Velocity', 'Space', 'Pressure'});

% Plot 14: Summary statistics
subplot(3, 5, 14);
summary_stats = [mean(metrics.inter_team_distance), mean(metrics.team_shape_ratio), ...
                mean(metrics.mean_nearest_opponent_distance), mean(metrics.relative_velocity)];
bar(summary_stats);
set(gca, 'XTickLabel', {'Distance', 'Shape', 'Marking', 'Velocity'});
title('Average Values');
ylabel('Value');
grid on;

% Plot 15: Analysis summary
subplot(3, 5, 15);
text(0.1, 0.8, sprintf('Analysis Summary:'), 'FontSize', 12, 'FontWeight', 'bold');
text(0.1, 0.7, sprintf('Time Points: %d', length(timestamps)), 'FontSize', 10);
text(0.1, 0.6, sprintf('Duration: %.1f s', max(timestamps)), 'FontSize', 10);
if isfield(coupled_analyzer.attractorStates, 'n_clusters')
    text(0.1, 0.5, sprintf('Attractors: %d', coupled_analyzer.attractorStates.n_clusters), 'FontSize', 10);
end
if isfield(coupled_analyzer.phaseTransitions, 'n_transitions')
    text(0.1, 0.4, sprintf('Transitions: %d', coupled_analyzer.phaseTransitions.n_transitions), 'FontSize', 10);
end
if isfield(coupled_analyzer.symmetryAnalysis, 'overload_events')
    text(0.1, 0.3, sprintf('Overloads: %d', length(coupled_analyzer.symmetryAnalysis.overload_events)), 'FontSize', 10);
end
if isfield(coupled_analyzer.analysisResults, 'zero_sum_analysis')
    text(0.1, 0.2, sprintf('Zero-sum: %.3f', coupled_analyzer.analysisResults.zero_sum_analysis.zero_sum_strength), 'FontSize', 10);
end
axis off;

sgtitle('Coupled Team Dynamics Analysis Results');

%% Step 10: Export results
fprintf('\nStep 10: Exporting results...\n');

output_dir = './coupled_dynamics_results';
coupled_analyzer.exportResults(output_dir);

% Save additional data
save(fullfile(output_dir, 'team_positions.mat'), 'home_positions', 'away_positions', 'timestamps');
save(fullfile(output_dir, 'metadata.mat'), 'metadata');

fprintf('Results exported to: %s\n', output_dir);

%% Step 11: Generate analysis report
fprintf('\nStep 11: Generating analysis report...\n');

report_file = fullfile(output_dir, 'coupled_dynamics_report.txt');
fid = fopen(report_file, 'w');

fprintf(fid, 'Coupled Team Dynamics Analysis Report\n');
fprintf(fid, '====================================\n\n');
fprintf(fid, 'Analysis Parameters:\n');
fprintf(fid, '  Field Dimensions: [%.0f, %.0f] m\n', params.fieldDimensions);
fprintf(fid, '  Sampling Rate: %.0f Hz\n', params.samplingRate);
fprintf(fid, '  Attractor Threshold: %.2f\n', params.attractorThreshold);
fprintf(fid, '  Min Attractor Duration: %.1f s\n', params.minAttractorDuration);
fprintf(fid, '  Symmetry Threshold: %.3f\n', params.symmetryThreshold);
fprintf(fid, '\n');

fprintf(fid, 'Data Summary:\n');
fprintf(fid, '  Time Points: %d\n', length(timestamps));
fprintf(fid, '  Duration: %.1f - %.1f seconds\n', min(timestamps), max(timestamps));
fprintf(fid, '  Formation: %s\n', metadata.formation);
fprintf(fid, '  Scenario: %s\n', metadata.scenario);
fprintf(fid, '\n');

fprintf(fid, 'Coupled Dynamics Metrics:\n');
fprintf(fid, '  Inter-team Distance: %.2f ± %.2f m\n', mean(metrics.inter_team_distance), std(metrics.inter_team_distance));
fprintf(fid, '  Team Shape Ratio: %.2f ± %.2f\n', mean(metrics.team_shape_ratio), std(metrics.team_shape_ratio));
fprintf(fid, '  Nearest Opponent Distance: %.2f ± %.2f m\n', mean(metrics.mean_nearest_opponent_distance), std(metrics.mean_nearest_opponent_distance));
fprintf(fid, '  Relative Velocity: %.2f ± %.2f m/s\n', mean(metrics.relative_velocity), std(metrics.relative_velocity));
fprintf(fid, '  Space Control Ratio: %.2f ± %.2f\n', mean(metrics.space_control_ratio), std(metrics.space_control_ratio));
fprintf(fid, '  Pressure Intensity: %.2f ± %.2f\n', mean(metrics.pressure_intensity), std(metrics.pressure_intensity));
fprintf(fid, '\n');

if isfield(coupled_analyzer.attractorStates, 'n_clusters')
    fprintf(fid, 'Attractor States:\n');
    fprintf(fid, '  Number of Attractors: %d\n', coupled_analyzer.attractorStates.n_clusters);
    for i = 1:coupled_analyzer.attractorStates.n_clusters
        stats = coupled_analyzer.attractorStates.cluster_stats{i};
        fprintf(fid, '  Attractor %d: Duration=%.1fs, Frequency=%.2f\n', i, stats.duration, stats.frequency);
    end
    fprintf(fid, '\n');
end

if isfield(coupled_analyzer.phaseTransitions, 'n_transitions')
    fprintf(fid, 'Phase Transitions:\n');
    fprintf(fid, '  Number of Transitions: %d\n', coupled_analyzer.phaseTransitions.n_transitions);
    if coupled_analyzer.phaseTransitions.n_transitions > 0
        fprintf(fid, '  Average Interval: %.1f ± %.1f time points\n', ...
            coupled_analyzer.phaseTransitions.mean_interval, coupled_analyzer.phaseTransitions.std_interval);
    end
    fprintf(fid, '\n');
end

if isfield(coupled_analyzer.symmetryAnalysis, 'overload_events')
    fprintf(fid, 'Symmetry Analysis:\n');
    fprintf(fid, '  Overload Events: %d\n', length(coupled_analyzer.symmetryAnalysis.overload_events));
    fprintf(fid, '  Symmetry Breaking Events: %d\n', length(coupled_analyzer.symmetryAnalysis.symmetry_breaking_events));
    fprintf(fid, '\n');
end

if isfield(coupled_analyzer.analysisResults, 'zero_sum_analysis')
    fprintf(fid, 'Zero-sum Dynamics:\n');
    fprintf(fid, '  Shape Correlation: %.3f\n', coupled_analyzer.analysisResults.zero_sum_analysis.shape_correlation);
    fprintf(fid, '  Zero-sum Strength: %.3f\n', coupled_analyzer.analysisResults.zero_sum_analysis.zero_sum_strength);
    fprintf(fid, '  Pressure Correlation: %.3f\n', coupled_analyzer.analysisResults.zero_sum_analysis.pressure_correlation);
    fprintf(fid, '\n');
end

fprintf(fid, 'Key Findings:\n');
fprintf(fid, '  - Inter-team distance shows tactical positioning dynamics\n');
fprintf(fid, '  - Team shape ratio indicates formation flexibility\n');
fprintf(fid, '  - Nearest opponent distances reveal marking intensity\n');
fprintf(fid, '  - Relative velocity captures team movement coordination\n');
fprintf(fid, '  - Space control ratio measures territorial dominance\n');
fprintf(fid, '  - Pressure intensity quantifies defensive/offensive pressure\n');
fprintf(fid, '\n');

fprintf(fid, 'Interpretation:\n');
fprintf(fid, '  - High inter-team distance: Teams maintaining defensive shape\n');
fprintf(fid, '  - Low inter-team distance: High pressing or compact play\n');
fprintf(fid, '  - High team shape ratio: One team more spread than the other\n');
fprintf(fid, '  - Low nearest opponent distance: Tight marking\n');
fprintf(fid, '  - High relative velocity: Rapid tactical changes\n');
fprintf(fid, '  - High space control ratio: Territorial advantage\n');
fprintf(fid, '  - High pressure intensity: Intense pressing or counter-pressing\n');

fclose(fid);

fprintf('Analysis report saved to: %s\n', report_file);

%% Summary
fprintf('\n=== Coupled Dynamics Analysis Complete ===\n');
fprintf('The coupled team dynamics analysis has been completed successfully.\n');
fprintf('Key outputs:\n');
fprintf('  - Coupled team dynamics metrics\n');
fprintf('  - Attractor state identification and analysis\n');
fprintf('  - Phase transition detection\n');
fprintf('  - Symmetry breaking analysis\n');
fprintf('  - Zero-sum dynamics quantification\n');
fprintf('  - Comprehensive visualizations\n');
fprintf('  - Statistical analysis and interpretation\n');
fprintf('\nNext steps:\n');
fprintf('  - Apply this analysis to real match data\n');
fprintf('  - Integrate with topological data analysis\n');
fprintf('  - Link to performance metrics and outcomes\n');
fprintf('  - Develop predictive models for team effectiveness\n');
