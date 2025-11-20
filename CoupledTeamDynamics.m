classdef CoupledTeamDynamics < handle
    % CoupledTeamDynamics - Analysis of coupled dynamics between two football teams
    % Implements the core research methodology for analyzing team interactions
    
    properties
        teamData
        coupledMetrics
        attractorStates
        phaseTransitions
        symmetryAnalysis
        analysisResults
        parameters
    end
    
    methods
        function obj = CoupledTeamDynamics()
            % Initialize the coupled dynamics analyzer
            obj.teamData = struct();
            obj.coupledMetrics = struct();
            obj.attractorStates = struct();
            obj.phaseTransitions = struct();
            obj.symmetryAnalysis = struct();
            obj.analysisResults = struct();
            
            % Set default parameters
            obj.parameters = struct();
            obj.parameters.fieldDimensions = [105, 68];
            obj.parameters.samplingRate = 10; % Hz
            obj.parameters.attractorThreshold = 0.1; % Distance threshold for attractor identification
            obj.parameters.minAttractorDuration = 5.0; % Minimum duration for stable attractor (seconds)
            obj.parameters.symmetryThreshold = 0.05; % Threshold for symmetry breaking detection
            obj.parameters.zeroSumThreshold = 0.8; % Correlation threshold for zero-sum dynamics
        end
        
        function setParameters(obj, params)
            % Set analysis parameters
            field_names = fieldnames(params);
            for i = 1:length(field_names)
                if isfield(obj.parameters, field_names{i})
                    obj.parameters.(field_names{i}) = params.(field_names{i});
                end
            end
        end
        
        function loadTeamData(obj, home_positions, away_positions, timestamps, metadata)
            % Load team position data
            obj.teamData = struct();
            obj.teamData.home_positions = home_positions; % [time, players, coordinates]
            obj.teamData.away_positions = away_positions;
            obj.teamData.timestamps = timestamps;
            obj.teamData.metadata = metadata;
            
            fprintf('Loaded team data: %d time points, %d players per team\n', ...
                size(home_positions, 1), size(home_positions, 2));
        end
        
        function computeCoupledMetrics(obj)
            % Compute coupled team dynamics metrics
            fprintf('Computing coupled team dynamics metrics...\n');
            
            n_times = size(obj.teamData.home_positions, 1);
            n_players = size(obj.teamData.home_positions, 2);
            
            % Initialize coupled metrics
            obj.coupledMetrics = struct();
            obj.coupledMetrics.inter_team_centroid_vector = zeros(n_times, 2);
            obj.coupledMetrics.inter_team_distance = zeros(n_times, 1);
            obj.coupledMetrics.team_shape_ratio = zeros(n_times, 1);
            obj.coupledMetrics.nearest_opponent_distances = zeros(n_times, n_players);
            obj.coupledMetrics.mean_nearest_opponent_distance = zeros(n_times, 1);
            obj.coupledMetrics.team_centroid_velocity = zeros(n_times, 2);
            obj.coupledMetrics.relative_velocity = zeros(n_times, 1);
            obj.coupledMetrics.space_control_ratio = zeros(n_times, 1);
            obj.coupledMetrics.pressure_intensity = zeros(n_times, 1);
            
            for t = 1:n_times
                % Extract positions for current time
                home_pos = squeeze(obj.teamData.home_positions(t, :, 1:2));
                away_pos = squeeze(obj.teamData.away_positions(t, :, 1:2));
                
                % Remove invalid positions
                valid_home = ~isnan(home_pos(:, 1));
                valid_away = ~isnan(away_pos(:, 1));
                
                if sum(valid_home) > 0 && sum(valid_away) > 0
                    home_pos = home_pos(valid_home, :);
                    away_pos = away_pos(valid_away, :);
                    
                    % 1. Inter-team centroid vector
                    home_centroid = mean(home_pos, 1);
                    away_centroid = mean(away_pos, 1);
                    obj.coupledMetrics.inter_team_centroid_vector(t, :) = home_centroid - away_centroid;
                    obj.coupledMetrics.inter_team_distance(t) = norm(obj.coupledMetrics.inter_team_centroid_vector(t, :));
                    
                    % 2. Team shape ratio
                    home_spread = std(home_pos, [], 'all');
                    away_spread = std(away_pos, [], 'all');
                    obj.coupledMetrics.team_shape_ratio(t) = home_spread / (away_spread + eps);
                    
                    % 3. Nearest opponent distances
                    for p = 1:min(n_players, size(home_pos, 1))
                        if p <= size(home_pos, 1)
                            distances_to_opponents = pdist2(home_pos(p, :), away_pos);
                            obj.coupledMetrics.nearest_opponent_distances(t, p) = min(distances_to_opponents);
                        end
                    end
                    obj.coupledMetrics.mean_nearest_opponent_distance(t) = mean(obj.coupledMetrics.nearest_opponent_distances(t, :));
                    
                    % 4. Team centroid velocity
                    if t > 1
                        dt = obj.teamData.timestamps(t) - obj.teamData.timestamps(t-1);
                        if dt > 0
                            prev_home_centroid = mean(squeeze(obj.teamData.home_positions(t-1, valid_home, 1:2)), 1);
                            prev_away_centroid = mean(squeeze(obj.teamData.away_positions(t-1, valid_away, 1:2)), 1);
                            
                            home_velocity = (home_centroid - prev_home_centroid) / dt;
                            away_velocity = (away_centroid - prev_away_centroid) / dt;
                            
                            obj.coupledMetrics.team_centroid_velocity(t, :) = home_velocity - away_velocity;
                            obj.coupledMetrics.relative_velocity(t) = norm(obj.coupledMetrics.team_centroid_velocity(t, :));
                        end
                    end
                    
                    % 5. Space control ratio
                    home_area = obj.computeTeamArea(home_pos);
                    away_area = obj.computeTeamArea(away_pos);
                    obj.coupledMetrics.space_control_ratio(t) = home_area / (away_area + eps);
                    
                    % 6. Pressure intensity
                    obj.coupledMetrics.pressure_intensity(t) = obj.computePressureIntensity(home_pos, away_pos);
                end
            end
            
            fprintf('Coupled metrics computed for %d time points\n', n_times);
        end
        
        function area = computeTeamArea(obj, positions)
            % Compute the area covered by a team
            if size(positions, 1) < 3
                area = 0;
                return;
            end
            
            try
                % Use convex hull to compute area
                k = convhull(positions(:, 1), positions(:, 2));
                area = polyarea(positions(k, 1), positions(k, 2));
            catch
                % Fallback: use bounding box area
                area = (max(positions(:, 1)) - min(positions(:, 1))) * ...
                       (max(positions(:, 2)) - min(positions(:, 2)));
            end
        end
        
        function pressure = computePressureIntensity(obj, home_pos, away_pos)
            % Compute pressure intensity between teams
            % Based on proximity and relative positioning
            
            % Compute average distance between teams
            distances = pdist2(home_pos, away_pos);
            avg_distance = mean(distances(:));
            
            % Compute pressure based on inverse distance and field position
            pressure = 1 / (avg_distance + 1); % Inverse distance pressure
            
            % Adjust for field position (higher pressure in attacking areas)
            home_centroid = mean(home_pos, 1);
            field_position_factor = home_centroid(1) / obj.parameters.fieldDimensions(1);
            pressure = pressure * (1 + field_position_factor);
            
            pressure = min(pressure, 10); % Cap at reasonable maximum
        end
        
        function identifyAttractorStates(obj)
            % Identify attractor states in the coupled system
            fprintf('Identifying attractor states...\n');
            
            % Create state space from coupled metrics
            state_space = obj.createStateSpace();
            
            % Apply clustering to identify attractors
            obj.attractorStates = obj.clusterAttractorStates(state_space);
            
            % Analyze attractor stability and transitions
            obj.analyzeAttractorTransitions();
            
            fprintf('Identified %d attractor states\n', length(obj.attractorStates.centers));
        end
        
        function state_space = createStateSpace(obj)
            % Create state space from coupled metrics
            n_times = length(obj.coupledMetrics.inter_team_distance);
            
            % Define state vector components
            state_space = zeros(n_times, 6);
            state_space(:, 1) = obj.coupledMetrics.inter_team_distance;
            state_space(:, 2) = obj.coupledMetrics.team_shape_ratio;
            state_space(:, 3) = obj.coupledMetrics.mean_nearest_opponent_distance;
            state_space(:, 4) = obj.coupledMetrics.relative_velocity;
            state_space(:, 5) = obj.coupledMetrics.space_control_ratio;
            state_space(:, 6) = obj.coupledMetrics.pressure_intensity;
            
            % Normalize state space
            for i = 1:size(state_space, 2)
                col = state_space(:, i);
                if std(col) > 0
                    state_space(:, i) = (col - mean(col)) / std(col);
                end
            end
        end
        
        function attractors = clusterAttractorStates(obj, state_space)
            % Cluster state space to identify attractor states
            attractors = struct();
            
            % Use k-means clustering
            n_clusters = min(5, floor(size(state_space, 1) / 20)); % Adaptive number of clusters
            
            if n_clusters > 1
                [cluster_ids, centers] = kmeans(state_space, n_clusters, 'Replicates', 10);
                
                attractors.centers = centers;
                attractors.cluster_ids = cluster_ids;
                attractors.n_clusters = n_clusters;
                
                % Analyze each cluster
                attractors.cluster_stats = cell(n_clusters, 1);
                for i = 1:n_clusters
                    cluster_mask = cluster_ids == i;
                    cluster_times = obj.teamData.timestamps(cluster_mask);
                    
                    stats = struct();
                    stats.duration = max(cluster_times) - min(cluster_times);
                    stats.frequency = sum(cluster_mask) / length(cluster_mask);
                    stats.mean_state = mean(state_space(cluster_mask, :), 1);
                    stats.std_state = std(state_space(cluster_mask, :), 1);
                    stats.time_points = find(cluster_mask);
                    
                    attractors.cluster_stats{i} = stats;
                end
            else
                % Single cluster case
                attractors.centers = mean(state_space, 1);
                attractors.cluster_ids = ones(size(state_space, 1), 1);
                attractors.n_clusters = 1;
                attractors.cluster_stats = {struct('duration', max(obj.teamData.timestamps), 'frequency', 1.0)};
            end
        end
        
        function analyzeAttractorTransitions(obj)
            % Analyze transitions between attractor states
            if obj.attractorStates.n_clusters <= 1
                return;
            end
            
            cluster_ids = obj.attractorStates.cluster_ids;
            n_times = length(cluster_ids);
            
            % Find transition points
            transitions = [];
            for t = 2:n_times
                if cluster_ids(t) ~= cluster_ids(t-1)
                    transitions(end+1) = t;
                end
            end
            
            obj.phaseTransitions = struct();
            obj.phaseTransitions.transition_points = transitions;
            obj.phaseTransitions.transition_times = obj.teamData.timestamps(transitions);
            obj.phaseTransitions.n_transitions = length(transitions);
            
            % Analyze transition patterns
            if length(transitions) > 1
                transition_intervals = diff(transitions);
                obj.phaseTransitions.mean_interval = mean(transition_intervals);
                obj.phaseTransitions.std_interval = std(transition_intervals);
            end
            
            fprintf('Found %d phase transitions\n', length(transitions));
        end
        
        function analyzeSymmetryBreaking(obj)
            % Analyze symmetry breaking in team dynamics
            fprintf('Analyzing symmetry breaking...\n');
            
            n_times = size(obj.teamData.home_positions, 1);
            obj.symmetryAnalysis = struct();
            
            % Initialize symmetry metrics
            obj.symmetryAnalysis.field_symmetry = zeros(n_times, 1);
            obj.symmetryAnalysis.formation_symmetry = zeros(n_times, 1);
            obj.symmetryAnalysis.overload_events = [];
            obj.symmetryAnalysis.symmetry_breaking_events = [];
            
            for t = 1:n_times
                home_pos = squeeze(obj.teamData.home_positions(t, :, 1:2));
                away_pos = squeeze(obj.teamData.away_players(t, :, 1:2));
                
                valid_home = ~isnan(home_pos(:, 1));
                valid_away = ~isnan(away_pos(:, 1));
                
                if sum(valid_home) > 0 && sum(valid_away) > 0
                    home_pos = home_pos(valid_home, :);
                    away_pos = away_pos(valid_away, :);
                    
                    % 1. Field symmetry (players on each side of center line)
                    center_line = obj.parameters.fieldDimensions(1) / 2;
                    home_left = sum(home_pos(:, 1) < center_line);
                    home_right = sum(home_pos(:, 1) >= center_line);
                    away_left = sum(away_pos(:, 1) < center_line);
                    away_right = sum(away_pos(:, 1) >= center_line);
                    
                    obj.symmetryAnalysis.field_symmetry(t) = abs((home_left - home_right) - (away_left - away_right));
                    
                    % 2. Formation symmetry (mirror symmetry)
                    obj.symmetryAnalysis.formation_symmetry(t) = obj.computeFormationSymmetry(home_pos, away_pos);
                    
                    % 3. Detect overload events
                    if obj.symmetryAnalysis.field_symmetry(t) > obj.parameters.symmetryThreshold
                        obj.symmetryAnalysis.overload_events(end+1) = t;
                    end
                    
                    % 4. Detect symmetry breaking events
                    if t > 1 && abs(obj.symmetryAnalysis.field_symmetry(t) - obj.symmetryAnalysis.field_symmetry(t-1)) > obj.parameters.symmetryThreshold
                        obj.symmetryAnalysis.symmetry_breaking_events(end+1) = t;
                    end
                end
            end
            
            fprintf('Symmetry analysis complete. Found %d overload events and %d symmetry breaking events\n', ...
                length(obj.symmetryAnalysis.overload_events), length(obj.symmetryAnalysis.symmetry_breaking_events));
        end
        
        function symmetry = computeFormationSymmetry(obj, home_pos, away_pos)
            % Compute formation symmetry between teams
            % Simplified measure based on relative positioning
            
            if size(home_pos, 1) ~= size(away_pos, 1)
                symmetry = 1; % Maximum asymmetry if different number of players
                return;
            end
            
            % Compute relative positions
            home_centroid = mean(home_pos, 1);
            away_centroid = mean(away_pos, 1);
            
            home_relative = home_pos - home_centroid;
            away_relative = away_pos - away_centroid;
            
            % Compute symmetry as inverse of position difference
            position_diff = mean(abs(home_relative - away_relative), 'all');
            symmetry = 1 / (1 + position_diff);
        end
        
        function analyzeZeroSumDynamics(obj)
            % Analyze zero-sum competition dynamics
            fprintf('Analyzing zero-sum dynamics...\n');
            
            % Compute correlations between opposing team metrics
            obj.analysisResults.zero_sum_analysis = struct();
            
            % Team shape correlation
            home_spread = zeros(size(obj.coupledMetrics.team_shape_ratio));
            away_spread = zeros(size(obj.coupledMetrics.team_shape_ratio));
            
            for t = 1:length(obj.coupledMetrics.team_shape_ratio)
                home_pos = squeeze(obj.teamData.home_positions(t, :, 1:2));
                away_pos = squeeze(obj.teamData.away_positions(t, :, 1:2));
                
                valid_home = ~isnan(home_pos(:, 1));
                valid_away = ~isnan(away_pos(:, 1));
                
                if sum(valid_home) > 0
                    home_spread(t) = std(home_pos(valid_home, :), [], 'all');
                end
                if sum(valid_away) > 0
                    away_spread(t) = std(away_pos(valid_away, :), [], 'all');
                end
            end
            
            % Compute correlation
            valid_indices = home_spread > 0 & away_spread > 0;
            if sum(valid_indices) > 10
                correlation = corrcoef(home_spread(valid_indices), away_spread(valid_indices));
                obj.analysisResults.zero_sum_analysis.shape_correlation = correlation(1, 2);
                obj.analysisResults.zero_sum_analysis.zero_sum_strength = abs(correlation(1, 2));
            else
                obj.analysisResults.zero_sum_analysis.shape_correlation = 0;
                obj.analysisResults.zero_sum_analysis.zero_sum_strength = 0;
            end
            
            % Analyze pressure dynamics
            obj.analysisResults.zero_sum_analysis.pressure_correlation = obj.analyzePressureDynamics();
            
            fprintf('Zero-sum analysis complete. Shape correlation: %.3f\n', ...
                obj.analysisResults.zero_sum_analysis.shape_correlation);
        end
        
        function correlation = analyzePressureDynamics(obj)
            % Analyze pressure dynamics between teams
            % This would involve more complex analysis of how teams respond to each other's pressure
            
            % Simplified version: analyze pressure intensity over time
            pressure = obj.coupledMetrics.pressure_intensity;
            
            % Look for alternating pressure patterns
            if length(pressure) > 20
                % Compute autocorrelation to detect periodic patterns
                [correlation, ~] = xcorr(pressure, pressure, 'coeff');
                correlation = max(correlation);
            else
                correlation = 0;
            end
        end
        
        function visualizeCoupledDynamics(obj)
            % Visualize coupled team dynamics
            figure('Position', [100, 100, 1600, 1200]);
            
            % Plot 1: Inter-team distance and shape ratio
            subplot(3, 4, 1);
            yyaxis left;
            plot(obj.teamData.timestamps, obj.coupledMetrics.inter_team_distance, 'b-', 'LineWidth', 2);
            ylabel('Inter-team Distance (m)');
            yyaxis right;
            plot(obj.teamData.timestamps, obj.coupledMetrics.team_shape_ratio, 'r-', 'LineWidth', 2);
            ylabel('Team Shape Ratio');
            xlabel('Time (s)');
            title('Team Coupling Metrics');
            grid on;
            
            % Plot 2: Nearest opponent distances
            subplot(3, 4, 2);
            plot(obj.teamData.timestamps, obj.coupledMetrics.mean_nearest_opponent_distance, 'g-', 'LineWidth', 2);
            xlabel('Time (s)');
            ylabel('Mean Nearest Opponent Distance (m)');
            title('Marking Intensity');
            grid on;
            
            % Plot 3: Relative velocity
            subplot(3, 4, 3);
            plot(obj.teamData.timestamps, obj.coupledMetrics.relative_velocity, 'm-', 'LineWidth', 2);
            xlabel('Time (s)');
            ylabel('Relative Velocity (m/s)');
            title('Team Movement Dynamics');
            grid on;
            
            % Plot 4: Space control ratio
            subplot(3, 4, 4);
            plot(obj.teamData.timestamps, obj.coupledMetrics.space_control_ratio, 'c-', 'LineWidth', 2);
            xlabel('Time (s)');
            ylabel('Space Control Ratio');
            title('Territorial Control');
            grid on;
            
            % Plot 5: Pressure intensity
            subplot(3, 4, 5);
            plot(obj.teamData.timestamps, obj.coupledMetrics.pressure_intensity, 'k-', 'LineWidth', 2);
            xlabel('Time (s)');
            ylabel('Pressure Intensity');
            title('Pressure Dynamics');
            grid on;
            
            % Plot 6: Attractor states (if available)
            subplot(3, 4, 6);
            if isfield(obj.attractorStates, 'cluster_ids')
                scatter(obj.teamData.timestamps, obj.attractorStates.cluster_ids, 50, obj.attractorStates.cluster_ids, 'filled');
                xlabel('Time (s)');
                ylabel('Attractor State');
                title('Attractor State Evolution');
                colorbar;
            else
                text(0.5, 0.5, 'Run identifyAttractorStates() first', 'HorizontalAlignment', 'center');
                title('Attractor States');
            end
            
            % Plot 7: Symmetry analysis (if available)
            subplot(3, 4, 7);
            if isfield(obj.symmetryAnalysis, 'field_symmetry')
                plot(obj.teamData.timestamps, obj.symmetryAnalysis.field_symmetry, 'b-', 'LineWidth', 2);
                hold on;
                plot(obj.teamData.timestamps, obj.symmetryAnalysis.formation_symmetry, 'r-', 'LineWidth', 2);
                xlabel('Time (s)');
                ylabel('Symmetry Measure');
                title('Symmetry Analysis');
                legend('Field', 'Formation', 'Location', 'best');
                grid on;
            else
                text(0.5, 0.5, 'Run analyzeSymmetryBreaking() first', 'HorizontalAlignment', 'center');
                title('Symmetry Analysis');
            end
            
            % Plot 8: Phase transitions (if available)
            subplot(3, 4, 8);
            if isfield(obj.phaseTransitions, 'transition_times')
                plot(obj.teamData.timestamps, obj.coupledMetrics.inter_team_distance, 'b-', 'LineWidth', 1);
                hold on;
                for i = 1:length(obj.phaseTransitions.transition_times)
                    xline(obj.phaseTransitions.transition_times(i), 'r--', 'LineWidth', 2);
                end
                xlabel('Time (s)');
                ylabel('Inter-team Distance (m)');
                title('Phase Transitions');
                grid on;
            else
                text(0.5, 0.5, 'Run identifyAttractorStates() first', 'HorizontalAlignment', 'center');
                title('Phase Transitions');
            end
            
            % Plot 9: State space (if available)
            subplot(3, 4, 9);
            if isfield(obj.attractorStates, 'cluster_ids')
                state_space = obj.createStateSpace();
                scatter(state_space(:, 1), state_space(:, 2), 50, obj.attractorStates.cluster_ids, 'filled');
                xlabel('Inter-team Distance (normalized)');
                ylabel('Team Shape Ratio (normalized)');
                title('State Space');
                colorbar;
            else
                text(0.5, 0.5, 'Run identifyAttractorStates() first', 'HorizontalAlignment', 'center');
                title('State Space');
            end
            
            % Plot 10: Zero-sum analysis (if available)
            subplot(3, 4, 10);
            if isfield(obj.analysisResults, 'zero_sum_analysis')
                bar([obj.analysisResults.zero_sum_analysis.shape_correlation, ...
                     obj.analysisResults.zero_sum_analysis.zero_sum_strength]);
                set(gca, 'XTickLabel', {'Shape Corr', 'Zero-sum Strength'});
                ylabel('Correlation');
                title('Zero-sum Dynamics');
                grid on;
            else
                text(0.5, 0.5, 'Run analyzeZeroSumDynamics() first', 'HorizontalAlignment', 'center');
                title('Zero-sum Analysis');
            end
            
            % Plot 11: Metric correlations
            subplot(3, 4, 11);
            metrics = [obj.coupledMetrics.inter_team_distance, ...
                      obj.coupledMetrics.team_shape_ratio, ...
                      obj.coupledMetrics.mean_nearest_opponent_distance, ...
                      obj.coupledMetrics.relative_velocity, ...
                      obj.coupledMetrics.space_control_ratio, ...
                      obj.coupledMetrics.pressure_intensity];
            
            correlation_matrix = corrcoef(metrics);
            imagesc(correlation_matrix);
            colorbar;
            title('Metric Correlations');
            set(gca, 'XTickLabel', {'Dist', 'Shape', 'Marking', 'Velocity', 'Space', 'Pressure'});
            set(gca, 'YTickLabel', {'Dist', 'Shape', 'Marking', 'Velocity', 'Space', 'Pressure'});
            
            % Plot 12: Summary statistics
            subplot(3, 4, 12);
            stats = [mean(obj.coupledMetrics.inter_team_distance), ...
                    mean(obj.coupledMetrics.team_shape_ratio), ...
                    mean(obj.coupledMetrics.mean_nearest_opponent_distance), ...
                    mean(obj.coupledMetrics.relative_velocity)];
            bar(stats);
            set(gca, 'XTickLabel', {'Distance', 'Shape', 'Marking', 'Velocity'});
            title('Average Values');
            ylabel('Value');
            grid on;
            
            sgtitle('Coupled Team Dynamics Analysis');
        end
        
        function exportResults(obj, output_dir)
            % Export analysis results
            if ~exist(output_dir, 'dir')
                mkdir(output_dir);
            end
            
            % Export coupled metrics
            coupled_metrics = obj.coupledMetrics;
            save(fullfile(output_dir, 'coupled_metrics.mat'), 'coupled_metrics');
            
            % Export attractor states
            if isfield(obj.attractorStates, 'centers')
                attractor_states = obj.attractorStates;
                save(fullfile(output_dir, 'attractor_states.mat'), 'attractor_states');
            end
            
            % Export phase transitions
            if isfield(obj.phaseTransitions, 'transition_points')
                phase_transitions = obj.phaseTransitions;
                save(fullfile(output_dir, 'phase_transitions.mat'), 'phase_transitions');
            end
            
            % Export symmetry analysis
            if isfield(obj.symmetryAnalysis, 'field_symmetry')
                symmetry_analysis = obj.symmetryAnalysis;
                save(fullfile(output_dir, 'symmetry_analysis.mat'), 'symmetry_analysis');
            end
            
            % Export analysis results
            if isfield(obj.analysisResults, 'zero_sum_analysis')
                analysis_results = obj.analysisResults;
                save(fullfile(output_dir, 'analysis_results.mat'), 'analysis_results');
            end
            
            % Export parameters
            parameters = obj.parameters;
            save(fullfile(output_dir, 'parameters.mat'), 'parameters');
            
            fprintf('Coupled dynamics results exported to: %s\n', output_dir);
        end
    end
end
