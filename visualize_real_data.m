% Visualize Real SecondSpectrum Data
% This script creates key visualizations for the real GPS data

clear; clc; close all;

fprintf('=== Real SecondSpectrum Data Visualization ===\n\n');

%% Step 1: Load real data
fprintf('Step 1: Loading real SecondSpectrum data...\n');

% File path
data_file = '/Users/iMacPro/Documents/GitHub/Football-TDA/FieldTest/g2293068_SecondSpectrum_Data copy.txt';

% Load data using our custom function
[home_positions, away_positions, timestamps, metadata] = load_secondspectrum_data(data_file, 1000);

fprintf('Data loaded successfully!\n');
fprintf('  Time points: %d\n', metadata.n_times);
fprintf('  Duration: %.1f seconds\n', metadata.duration);
fprintf('  Sampling rate: %.1f Hz\n', metadata.sampling_rate);

%% Step 2: Create key visualizations
fprintf('\nStep 2: Creating key visualizations...\n');

% Create main visualization figure
figure('Position', [100, 100, 1600, 1000]);

% Plot 1: Team formations at key moments
subplot(2, 3, 1);
key_times = [1, round(metadata.n_times/4), round(metadata.n_times/2), round(3*metadata.n_times/4), metadata.n_times];
colors = {'b', 'r', 'g', 'm', 'c'};

for i = 1:length(key_times)
    t = key_times(i);
    if t <= metadata.n_times
        home_pos = squeeze(home_positions(t, :, 1:2));
        away_pos = squeeze(away_positions(t, :, 1:2));
        
        % Only plot valid positions
        valid_home = ~isnan(home_pos(:, 1));
        valid_away = ~isnan(away_pos(:, 1));
        
        if sum(valid_home) > 0
            scatter(home_pos(valid_home, 1), home_pos(valid_home, 2), 100, colors{i}, 'filled', 'MarkerFaceAlpha', 0.7);
            hold on;
        end
        if sum(valid_away) > 0
            scatter(away_pos(valid_away, 1), away_pos(valid_away, 2), 100, colors{i}, 'filled', 'MarkerFaceAlpha', 0.7);
        end
    end
end

xlim([0, 105]); ylim([0, 68]);
xlabel('X Position (m)'); ylabel('Y Position (m)');
title('Team Formations (Key Moments)');
legend('t=1', 't=25%', 't=50%', 't=75%', 't=100%', 'Location', 'best');
grid on;

% Plot 2: Team centroid movement
subplot(2, 3, 2);
% Calculate team centroids
home_centroid = zeros(metadata.n_times, 2);
away_centroid = zeros(metadata.n_times, 2);

for t = 1:metadata.n_times
    home_pos = squeeze(home_positions(t, :, 1:2));
    away_pos = squeeze(away_positions(t, :, 1:2));
    
    valid_home = ~isnan(home_pos(:, 1));
    valid_away = ~isnan(away_pos(:, 1));
    
    if sum(valid_home) > 0
        home_centroid(t, :) = mean(home_pos(valid_home, :), 1);
    end
    if sum(valid_away) > 0
        away_centroid(t, :) = mean(away_pos(valid_away, :), 1);
    end
end

plot(home_centroid(:, 1), home_centroid(:, 2), 'b-', 'LineWidth', 2);
hold on;
plot(away_centroid(:, 1), away_centroid(:, 2), 'r-', 'LineWidth', 2);
xlabel('X Position (m)'); ylabel('Y Position (m)');
title('Team Centroid Movement');
legend('Home', 'Away', 'Location', 'best');
grid on;

% Plot 3: Inter-team distance over time
subplot(2, 3, 3);
inter_team_distance = zeros(metadata.n_times, 1);
for t = 1:metadata.n_times
    if ~isnan(home_centroid(t, 1)) && ~isnan(away_centroid(t, 1))
        inter_team_distance(t) = norm(home_centroid(t, :) - away_centroid(t, :));
    end
end

plot(timestamps, inter_team_distance, 'g-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Distance (m)');
title('Inter-team Distance');
grid on;

% Plot 4: Team spread over time
subplot(2, 3, 4);
home_spread = zeros(metadata.n_times, 1);
away_spread = zeros(metadata.n_times, 1);

for t = 1:metadata.n_times
    home_pos = squeeze(home_positions(t, :, 1:2));
    away_pos = squeeze(away_positions(t, :, 1:2));
    
    valid_home = ~isnan(home_pos(:, 1));
    valid_away = ~isnan(away_pos(:, 1));
    
    if sum(valid_home) > 1
        home_spread(t) = std(home_pos(valid_home, :), [], 'all');
    end
    if sum(valid_away) > 1
        away_spread(t) = std(away_pos(valid_away, :), [], 'all');
    end
end

plot(timestamps, home_spread, 'b-', 'LineWidth', 2);
hold on;
plot(timestamps, away_spread, 'r-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Spread (m)');
title('Team Spread');
legend('Home', 'Away', 'Location', 'best');
grid on;

% Plot 5: Player trajectories (sample players)
subplot(2, 3, 5);
% Plot trajectories for first 3 players from each team
for p = 1:3
    home_traj = squeeze(home_positions(:, p, 1:2));
    away_traj = squeeze(away_positions(:, p, 1:2));
    
    valid_home = ~isnan(home_traj(:, 1));
    valid_away = ~isnan(away_traj(:, 1));
    
    if sum(valid_home) > 10
        plot(home_traj(valid_home, 1), home_traj(valid_home, 2), 'b-', 'LineWidth', 1);
        hold on;
    end
    if sum(valid_away) > 10
        plot(away_traj(valid_away, 1), away_traj(valid_away, 2), 'r-', 'LineWidth', 1);
    end
end

xlim([0, 105]); ylim([0, 68]);
xlabel('X Position (m)'); ylabel('Y Position (m)');
title('Player Trajectories (Sample)');
legend('Home Players', 'Away Players', 'Location', 'best');
grid on;

% Plot 6: Data quality and summary
subplot(2, 3, 6);
% Create summary statistics
text(0.1, 0.9, sprintf('Data Summary:'), 'FontSize', 14, 'FontWeight', 'bold');
text(0.1, 0.8, sprintf('Source: %s', metadata.source), 'FontSize', 12);
text(0.1, 0.7, sprintf('Time Points: %d', metadata.n_times), 'FontSize', 12);
text(0.1, 0.6, sprintf('Duration: %.1f s', metadata.duration), 'FontSize', 12);
text(0.1, 0.5, sprintf('Sampling Rate: %.1f Hz', metadata.sampling_rate), 'FontSize', 12);
text(0.1, 0.4, sprintf('Home Valid: %.1f%%', 100*metadata.home_valid_positions/numel(home_positions)), 'FontSize', 12);
text(0.1, 0.3, sprintf('Away Valid: %.1f%%', 100*metadata.away_valid_positions/numel(away_positions)), 'FontSize', 12);
text(0.1, 0.2, sprintf('Avg Inter-team Dist: %.1f m', mean(inter_team_distance)), 'FontSize', 12);
text(0.1, 0.1, sprintf('Avg Home Spread: %.1f m', mean(home_spread)), 'FontSize', 12);
axis off;

sgtitle('Real SecondSpectrum Data Analysis');

%% Step 3: Create additional detailed visualizations
fprintf('\nStep 3: Creating additional detailed visualizations...\n');

% Create second figure for detailed analysis
figure('Position', [200, 200, 1600, 800]);

% Plot 1: Heatmap of player positions
subplot(2, 4, 1);
% Create position heatmap for home team
home_x_all = home_positions(:, :, 1);
home_y_all = home_positions(:, :, 2);
valid_positions = ~isnan(home_x_all) & ~isnan(home_y_all);

if sum(valid_positions) > 0
    histogram2(home_x_all(valid_positions), home_y_all(valid_positions), 20, 20, 'FaceColor', 'flat');
    xlabel('X Position (m)'); ylabel('Y Position (m)');
    title('Home Team Position Heatmap');
    colorbar;
    xlim([0, 105]); ylim([0, 68]);
end

% Plot 2: Heatmap of away team positions
subplot(2, 4, 2);
away_x_all = away_positions(:, :, 1);
away_y_all = away_positions(:, :, 2);
valid_positions = ~isnan(away_x_all) & ~isnan(away_y_all);

if sum(valid_positions) > 0
    histogram2(away_x_all(valid_positions), away_y_all(valid_positions), 20, 20, 'FaceColor', 'flat');
    xlabel('X Position (m)'); ylabel('Y Position (m)');
    title('Away Team Position Heatmap');
    colorbar;
    xlim([0, 105]); ylim([0, 68]);
end

% Plot 3: Team shape evolution
subplot(2, 4, 3);
team_shape_ratio = home_spread ./ (away_spread + eps);
plot(timestamps, team_shape_ratio, 'k-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Shape Ratio (Home/Away)');
title('Team Shape Evolution');
grid on;

% Plot 4: Velocity analysis
subplot(2, 4, 4);
% Calculate team centroid velocities
home_velocity = zeros(metadata.n_times, 1);
away_velocity = zeros(metadata.n_times, 1);

for t = 2:metadata.n_times
    if ~isnan(home_centroid(t, 1)) && ~isnan(home_centroid(t-1, 1))
        dt = timestamps(t) - timestamps(t-1);
        if dt > 0
            home_velocity(t) = norm(home_centroid(t, :) - home_centroid(t-1, :)) / dt;
        end
    end
    if ~isnan(away_centroid(t, 1)) && ~isnan(away_centroid(t-1, 1))
        dt = timestamps(t) - timestamps(t-1);
        if dt > 0
            away_velocity(t) = norm(away_centroid(t, :) - away_centroid(t-1, :)) / dt;
        end
    end
end

plot(timestamps, home_velocity, 'b-', 'LineWidth', 2);
hold on;
plot(timestamps, away_velocity, 'r-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Velocity (m/s)');
title('Team Centroid Velocity');
legend('Home', 'Away', 'Location', 'best');
grid on;

% Plot 5: Pressure analysis
subplot(2, 4, 5);
% Calculate pressure based on inter-team distance
pressure = 1 ./ (inter_team_distance + 1);
plot(timestamps, pressure, 'm-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Pressure Intensity');
title('Pressure Dynamics');
grid on;

% Plot 6: Formation stability
subplot(2, 4, 6);
% Calculate formation stability as inverse of spread change
home_spread_change = abs(diff(home_spread));
away_spread_change = abs(diff(away_spread));
stability = 1 ./ (home_spread_change + away_spread_change + eps);

plot(timestamps(2:end), stability, 'g-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Formation Stability');
title('Formation Stability');
grid on;

% Plot 7: Spatial dominance
subplot(2, 4, 7);
% Calculate which team controls more of the field
field_control = zeros(metadata.n_times, 1);
for t = 1:metadata.n_times
    if ~isnan(home_centroid(t, 1)) && ~isnan(away_centroid(t, 1))
        % Positive values mean home team is further forward
        field_control(t) = home_centroid(t, 1) - away_centroid(t, 1);
    end
end

plot(timestamps, field_control, 'c-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Field Control (m)');
title('Spatial Dominance');
grid on;
yline(0, 'k--', 'LineWidth', 1);

% Plot 8: Tactical phases
subplot(2, 4, 8);
% Identify tactical phases based on inter-team distance
phases = zeros(metadata.n_times, 1);
mean_distance = mean(inter_team_distance);
std_distance = std(inter_team_distance);

for t = 1:metadata.n_times
    if inter_team_distance(t) > mean_distance + std_distance
        phases(t) = 3; % High pressing
    elseif inter_team_distance(t) < mean_distance - std_distance
        phases(t) = 1; % Compact defense
    else
        phases(t) = 2; % Normal play
    end
end

scatter(timestamps, phases, 50, phases, 'filled');
xlabel('Time (s)'); ylabel('Tactical Phase');
title('Tactical Phases');
ylim([0.5, 3.5]);
yticks([1, 2, 3]);
yticklabels({'Compact', 'Normal', 'Pressing'});
colorbar;

sgtitle('Detailed SecondSpectrum Data Analysis');

%% Step 4: Export visualizations
fprintf('\nStep 4: Exporting visualizations...\n');

% Save figures
saveas(gcf, 'secondspectrum_detailed_analysis.png');
saveas(gcf-1, 'secondspectrum_overview.png');

% Save data
output_dir = './secondspectrum_visualization_results';
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

save(fullfile(output_dir, 'visualization_data.mat'), 'home_positions', 'away_positions', 'timestamps', 'metadata');

fprintf('Visualizations saved!\n');

%% Summary
fprintf('\n=== Visualization Complete ===\n');
fprintf('Successfully created comprehensive visualizations of real SecondSpectrum data!\n');
fprintf('Key visualizations created:\n');
fprintf('  ✓ Team formations at key moments\n');
fprintf('  ✓ Team centroid movement patterns\n');
fprintf('  ✓ Inter-team distance evolution\n');
fprintf('  ✓ Team spread and shape analysis\n');
fprintf('  ✓ Player trajectory analysis\n');
fprintf('  ✓ Position heatmaps\n');
fprintf('  ✓ Velocity and pressure dynamics\n');
fprintf('  ✓ Formation stability analysis\n');
fprintf('  ✓ Spatial dominance patterns\n');
fprintf('  ✓ Tactical phase identification\n');
fprintf('\nThe real data has been successfully analyzed and visualized!\n');
