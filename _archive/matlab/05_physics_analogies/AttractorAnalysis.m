classdef AttractorAnalysis < handle
    % AttractorAnalysis - Advanced attractor state identification and analysis
    % Implements sophisticated methods for identifying and analyzing team attractor states
    
    properties
        stateSpace
        attractors
        transitions
        stability
        analysisResults
        parameters
    end
    
    methods
        function obj = AttractorAnalysis()
            % Initialize the attractor analyzer
            obj.stateSpace = struct();
            obj.attractors = struct();
            obj.transitions = struct();
            obj.stability = struct();
            obj.analysisResults = struct();
            
            % Set default parameters
            obj.parameters = struct();
            obj.parameters.minAttractorDuration = 5.0;      % Minimum duration for stable attractor (seconds)
            obj.parameters.attractorThreshold = 0.1;        % Distance threshold for attractor identification
            obj.parameters.transitionThreshold = 0.2;       % Threshold for phase transitions
            obj.parameters.stabilityWindow = 10;            % Window for stability analysis (time points)
            obj.parameters.maxAttractors = 10;              % Maximum number of attractors to identify
            obj.parameters.clusteringMethod = 'kmeans';     % Clustering method: 'kmeans', 'dbscan', 'hierarchical'
            obj.parameters.distanceMetric = 'euclidean';    % Distance metric for clustering
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
        
        function loadStateSpace(obj, state_data, timestamps, metadata)
            % Load state space data for attractor analysis
            obj.stateSpace = struct();
            obj.stateSpace.data = state_data;           % [time, features] matrix
            obj.stateSpace.timestamps = timestamps;
            obj.stateSpace.metadata = metadata;
            obj.stateSpace.n_features = size(state_data, 2);
            obj.stateSpace.n_times = size(state_data, 1);
            
            fprintf('Loaded state space: %d time points, %d features\n', ...
                obj.stateSpace.n_times, obj.stateSpace.n_features);
        end
        
        function identifyAttractors(obj)
            % Identify attractor states using multiple methods
            fprintf('Identifying attractor states...\n');
            
            % Normalize state space
            normalized_data = obj.normalizeStateSpace();
            
            % Apply clustering method
            switch obj.parameters.clusteringMethod
                case 'kmeans'
                    obj.attractors = obj.kmeansClustering(normalized_data);
                case 'dbscan'
                    obj.attractors = obj.dbscanClustering(normalized_data);
                case 'hierarchical'
                    obj.attractors = obj.hierarchicalClustering(normalized_data);
                otherwise
                    error('Unknown clustering method: %s', obj.parameters.clusteringMethod);
            end
            
            % Analyze attractor properties
            obj.analyzeAttractorProperties();
            
            % Identify phase transitions
            obj.identifyPhaseTransitions();
            
            % Analyze attractor stability
            obj.analyzeAttractorStability();
            
            fprintf('Identified %d attractor states\n', obj.attractors.n_attractors);
        end
        
        function normalized_data = normalizeStateSpace(obj)
            % Normalize state space data
            data = obj.stateSpace.data;
            normalized_data = zeros(size(data));
            
            for i = 1:size(data, 2)
                col = data(:, i);
                if std(col) > 0
                    normalized_data(:, i) = (col - mean(col)) / std(col);
                else
                    normalized_data(:, i) = col;
                end
            end
        end
        
        function attractors = kmeansClustering(obj, data)
            % K-means clustering for attractor identification
            attractors = struct();
            
            % Determine optimal number of clusters
            n_clusters = obj.estimateOptimalClusters(data);
            n_clusters = min(n_clusters, obj.parameters.maxAttractors);
            
            % Perform k-means clustering
            [cluster_ids, centers, sumd] = kmeans(data, n_clusters, 'Replicates', 10, 'MaxIter', 1000);
            
            attractors.method = 'kmeans';
            attractors.n_attractors = n_clusters;
            attractors.centers = centers;
            attractors.cluster_ids = cluster_ids;
            attractors.sum_squared_distances = sumd;
            attractors.silhouette_score = obj.computeSilhouetteScore(data, cluster_ids);
            
            % Analyze each attractor
            attractors.attractor_stats = cell(n_clusters, 1);
            for i = 1:n_clusters
                stats = obj.analyzeAttractorCluster(data, cluster_ids, i);
                attractors.attractor_stats{i} = stats;
            end
        end
        
        function attractors = dbscanClustering(obj, data)
            % DBSCAN clustering for attractor identification
            attractors = struct();
            
            % Set DBSCAN parameters
            epsilon = obj.estimateDBSCANEpsilon(data);
            min_points = max(3, floor(size(data, 1) / 50));
            
            % Perform DBSCAN clustering
            cluster_ids = dbscan(data, epsilon, min_points);
            
            % Remove noise points (cluster_id = -1)
            valid_indices = cluster_ids ~= -1;
            if sum(valid_indices) < size(data, 1) * 0.5
                warning('DBSCAN identified too many noise points. Consider adjusting parameters.');
            end
            
            % Reassign noise points to nearest cluster
            if sum(~valid_indices) > 0
                cluster_ids = obj.reassignNoisePoints(data, cluster_ids);
            end
            
            n_clusters = max(cluster_ids);
            
            attractors.method = 'dbscan';
            attractors.n_attractors = n_clusters;
            attractors.cluster_ids = cluster_ids;
            attractors.epsilon = epsilon;
            attractors.min_points = min_points;
            
            % Compute cluster centers
            centers = zeros(n_clusters, size(data, 2));
            for i = 1:n_clusters
                cluster_mask = cluster_ids == i;
                centers(i, :) = mean(data(cluster_mask, :), 1);
            end
            attractors.centers = centers;
            
            % Analyze each attractor
            attractors.attractor_stats = cell(n_clusters, 1);
            for i = 1:n_clusters
                stats = obj.analyzeAttractorCluster(data, cluster_ids, i);
                attractors.attractor_stats{i} = stats;
            end
        end
        
        function attractors = hierarchicalClustering(obj, data)
            % Hierarchical clustering for attractor identification
            attractors = struct();
            
            % Compute distance matrix
            distances = pdist(data, obj.parameters.distanceMetric);
            
            % Perform hierarchical clustering
            linkage_tree = linkage(distances, 'ward');
            
            % Determine optimal number of clusters
            n_clusters = obj.estimateOptimalClusters(data);
            n_clusters = min(n_clusters, obj.parameters.maxAttractors);
            
            % Cut the dendrogram
            cluster_ids = cluster(linkage_tree, 'MaxClust', n_clusters);
            
            attractors.method = 'hierarchical';
            attractors.n_attractors = n_clusters;
            attractors.cluster_ids = cluster_ids;
            attractors.linkage_tree = linkage_tree;
            
            % Compute cluster centers
            centers = zeros(n_clusters, size(data, 2));
            for i = 1:n_clusters
                cluster_mask = cluster_ids == i;
                centers(i, :) = mean(data(cluster_mask, :), 1);
            end
            attractors.centers = centers;
            
            % Analyze each attractor
            attractors.attractor_stats = cell(n_clusters, 1);
            for i = 1:n_clusters
                stats = obj.analyzeAttractorCluster(data, cluster_ids, i);
                attractors.attractor_stats{i} = stats;
            end
        end
        
        function n_clusters = estimateOptimalClusters(obj, data)
            % Estimate optimal number of clusters using elbow method and silhouette analysis
            max_clusters = min(10, floor(size(data, 1) / 20));
            if max_clusters < 2
                n_clusters = 2;
                return;
            end
            
            % Elbow method
            inertias = zeros(max_clusters, 1);
            silhouette_scores = zeros(max_clusters, 1);
            
            for k = 2:max_clusters
                [~, ~, sumd] = kmeans(data, k, 'Replicates', 5);
                inertias(k) = sum(sumd);
                silhouette_scores(k) = obj.computeSilhouetteScore(data, kmeans(data, k, 'Replicates', 5));
            end
            
            % Find elbow point
            if length(inertias) > 2
                % Compute second derivative to find elbow
                second_deriv = diff(diff(inertias(2:end)));
                [~, elbow_idx] = max(second_deriv);
                elbow_k = elbow_idx + 2;
            else
                elbow_k = 2;
            end
            
            % Find best silhouette score
            [~, silhouette_idx] = max(silhouette_scores(2:end));
            silhouette_k = silhouette_idx + 1;
            
            % Choose the smaller of the two (more conservative)
            n_clusters = min(elbow_k, silhouette_k);
            n_clusters = max(2, n_clusters); % At least 2 clusters
        end
        
        function epsilon = estimateDBSCANEpsilon(obj, data)
            % Estimate optimal epsilon for DBSCAN using k-distance graph
            k = 4; % k-nearest neighbors
            distances = pdist(data);
            sorted_distances = sort(distances);
            
            % Use k-distance heuristic
            k_distances = sorted_distances(1:k:end);
            epsilon = median(k_distances);
        end
        
        function cluster_ids = reassignNoisePoints(obj, data, cluster_ids)
            % Reassign noise points to nearest cluster
            noise_indices = find(cluster_ids == -1);
            valid_clusters = unique(cluster_ids(cluster_ids ~= -1));
            
            for i = 1:length(noise_indices)
                idx = noise_indices(i);
                point = data(idx, :);
                
                % Find nearest cluster center
                min_distance = inf;
                nearest_cluster = valid_clusters(1);
                
                for j = 1:length(valid_clusters)
                    cluster_mask = cluster_ids == valid_clusters(j);
                    cluster_center = mean(data(cluster_mask, :), 1);
                    distance = norm(point - cluster_center);
                    
                    if distance < min_distance
                        min_distance = distance;
                        nearest_cluster = valid_clusters(j);
                    end
                end
                
                cluster_ids(idx) = nearest_cluster;
            end
        end
        
        function score = computeSilhouetteScore(obj, data, cluster_ids)
            % Compute silhouette score for clustering quality
            try
                score = mean(silhouette(data, cluster_ids));
            catch
                score = 0; % Fallback if silhouette computation fails
            end
        end
        
        function stats = analyzeAttractorCluster(obj, data, cluster_ids, cluster_id)
            % Analyze properties of a specific attractor cluster
            cluster_mask = cluster_ids == cluster_id;
            cluster_data = data(cluster_mask, :);
            cluster_times = obj.stateSpace.timestamps(cluster_mask);
            
            stats = struct();
            stats.cluster_id = cluster_id;
            stats.size = sum(cluster_mask);
            stats.frequency = stats.size / length(cluster_ids);
            stats.duration = max(cluster_times) - min(cluster_times);
            stats.mean_state = mean(cluster_data, 1);
            stats.std_state = std(cluster_data, 1);
            stats.coefficient_of_variation = stats.std_state ./ (abs(stats.mean_state) + eps);
            stats.time_points = find(cluster_mask);
            stats.timestamps = cluster_times;
            
            % Compute cluster compactness
            if stats.size > 1
                center = stats.mean_state;
                distances = sqrt(sum((cluster_data - center).^2, 2));
                stats.compactness = mean(distances);
                stats.max_radius = max(distances);
            else
                stats.compactness = 0;
                stats.max_radius = 0;
            end
            
            % Analyze temporal patterns
            if length(cluster_times) > 1
                time_intervals = diff(sort(cluster_times));
                stats.mean_interval = mean(time_intervals);
                stats.std_interval = std(time_intervals);
                stats.continuity = obj.computeContinuity(cluster_times);
            else
                stats.mean_interval = 0;
                stats.std_interval = 0;
                stats.continuity = 0;
            end
        end
        
        function continuity = computeContinuity(obj, timestamps)
            % Compute continuity measure for attractor persistence
            if length(timestamps) < 2
                continuity = 0;
                return;
            end
            
            sorted_times = sort(timestamps);
            intervals = diff(sorted_times);
            expected_interval = 1 / obj.stateSpace.metadata.sampling_rate;
            
            % Continuity is inverse of interval variability
            continuity = 1 / (1 + std(intervals) / expected_interval);
        end
        
        function analyzeAttractorProperties(obj)
            % Analyze properties of identified attractors
            fprintf('Analyzing attractor properties...\n');
            
            obj.analysisResults = struct();
            obj.analysisResults.attractor_summary = struct();
            
            % Summary statistics
            obj.analysisResults.attractor_summary.n_attractors = obj.attractors.n_attractors;
            obj.analysisResults.attractor_summary.total_duration = max(obj.stateSpace.timestamps) - min(obj.stateSpace.timestamps);
            
            % Analyze attractor dominance
            frequencies = zeros(obj.attractors.n_attractors, 1);
            durations = zeros(obj.attractors.n_attractors, 1);
            compactnesses = zeros(obj.attractors.n_attractors, 1);
            
            for i = 1:obj.attractors.n_attractors
                stats = obj.attractors.attractor_stats{i};
                frequencies(i) = stats.frequency;
                durations(i) = stats.duration;
                compactnesses(i) = stats.compactness;
            end
            
            obj.analysisResults.attractor_summary.dominant_attractor = find(frequencies == max(frequencies), 1);
            obj.analysisResults.attractor_summary.most_stable_attractor = find(compactnesses == min(compactnesses), 1);
            obj.analysisResults.attractor_summary.longest_attractor = find(durations == max(durations), 1);
            
            % Compute attractor diversity
            obj.analysisResults.attractor_summary.diversity = obj.computeAttractorDiversity();
            
            % Analyze attractor transitions
            obj.analysisResults.attractor_summary.transition_matrix = obj.computeTransitionMatrix();
        end
        
        function diversity = computeAttractorDiversity(obj)
            % Compute diversity measure for attractor states
            frequencies = zeros(obj.attractors.n_attractors, 1);
            for i = 1:obj.attractors.n_attractors
                frequencies(i) = obj.attractors.attractor_stats{i}.frequency;
            end
            
            % Shannon entropy
            frequencies = frequencies(frequencies > 0);
            if length(frequencies) > 1
                diversity = -sum(frequencies .* log2(frequencies + eps));
            else
                diversity = 0;
            end
        end
        
        function transition_matrix = computeTransitionMatrix(obj)
            % Compute transition matrix between attractor states
            cluster_ids = obj.attractors.cluster_ids;
            n_attractors = obj.attractors.n_attractors;
            
            transition_matrix = zeros(n_attractors, n_attractors);
            
            for t = 2:length(cluster_ids)
                from_state = cluster_ids(t-1);
                to_state = cluster_ids(t);
                if from_state ~= to_state
                    transition_matrix(from_state, to_state) = transition_matrix(from_state, to_state) + 1;
                end
            end
            
            % Normalize by row sums
            row_sums = sum(transition_matrix, 2);
            for i = 1:n_attractors
                if row_sums(i) > 0
                    transition_matrix(i, :) = transition_matrix(i, :) / row_sums(i);
                end
            end
        end
        
        function identifyPhaseTransitions(obj)
            % Identify phase transitions between attractor states
            fprintf('Identifying phase transitions...\n');
            
            cluster_ids = obj.attractors.cluster_ids;
            timestamps = obj.stateSpace.timestamps;
            
            obj.transitions = struct();
            obj.transitions.transition_points = [];
            obj.transitions.transition_times = [];
            obj.transitions.from_states = [];
            obj.transitions.to_states = [];
            obj.transitions.transition_durations = [];
            
            for t = 2:length(cluster_ids)
                if cluster_ids(t) ~= cluster_ids(t-1)
                    obj.transitions.transition_points(end+1) = t;
                    obj.transitions.transition_times(end+1) = timestamps(t);
                    obj.transitions.from_states(end+1) = cluster_ids(t-1);
                    obj.transitions.to_states(end+1) = cluster_ids(t);
                    
                    % Compute transition duration
                    if t > 1
                        duration = timestamps(t) - timestamps(t-1);
                        obj.transitions.transition_durations(end+1) = duration;
                    end
                end
            end
            
            obj.transitions.n_transitions = length(obj.transitions.transition_points);
            
            if obj.transitions.n_transitions > 0
                obj.transitions.mean_interval = mean(diff(obj.transitions.transition_times));
                obj.transitions.std_interval = std(diff(obj.transitions.transition_times));
            else
                obj.transitions.mean_interval = 0;
                obj.transitions.std_interval = 0;
            end
            
            fprintf('Found %d phase transitions\n', obj.transitions.n_transitions);
        end
        
        function analyzeAttractorStability(obj)
            % Analyze stability of attractor states
            fprintf('Analyzing attractor stability...\n');
            
            obj.stability = struct();
            obj.stability.stability_scores = zeros(obj.attractors.n_attractors, 1);
            obj.stability.return_times = cell(obj.attractors.n_attractors, 1);
            obj.stability.persistence_times = zeros(obj.attractors.n_attractors, 1);
            
            for i = 1:obj.attractors.n_attractors
                stats = obj.attractors.attractor_stats{i};
                
                % Stability score based on compactness and continuity
                obj.stability.stability_scores(i) = stats.continuity / (1 + stats.compactness);
                
                % Analyze return times
                obj.stability.return_times{i} = obj.computeReturnTimes(i);
                
                % Persistence time
                obj.stability.persistence_times(i) = stats.duration;
            end
            
            % Overall system stability
            obj.stability.system_stability = mean(obj.stability.stability_scores);
            obj.stability.stability_variance = var(obj.stability.stability_scores);
        end
        
        function return_times = computeReturnTimes(obj, attractor_id)
            % Compute return times to a specific attractor
            cluster_ids = obj.attractors.cluster_ids;
            timestamps = obj.stateSpace.timestamps;
            
            attractor_times = timestamps(cluster_ids == attractor_id);
            return_times = [];
            
            if length(attractor_times) > 1
                sorted_times = sort(attractor_times);
                for i = 2:length(sorted_times)
                    return_times(end+1) = sorted_times(i) - sorted_times(i-1);
                end
            end
        end
        
        function visualizeAttractors(obj)
            % Visualize attractor analysis results
            figure('Position', [100, 100, 1600, 1200]);
            
            % Plot 1: State space with attractor centers
            subplot(3, 4, 1);
            if obj.stateSpace.n_features >= 2
                scatter(obj.stateSpace.data(:, 1), obj.stateSpace.data(:, 2), 50, obj.attractors.cluster_ids, 'filled');
                hold on;
                scatter(obj.attractors.centers(:, 1), obj.attractors.centers(:, 2), 200, 'k', 'filled', 'diamond');
                xlabel('Feature 1'); ylabel('Feature 2');
                title('State Space with Attractors');
                colorbar;
            else
                text(0.5, 0.5, 'Need at least 2 features for 2D visualization', 'HorizontalAlignment', 'center');
                title('State Space');
            end
            
            % Plot 2: Attractor evolution over time
            subplot(3, 4, 2);
            scatter(obj.stateSpace.timestamps, obj.attractors.cluster_ids, 50, obj.attractors.cluster_ids, 'filled');
            xlabel('Time (s)'); ylabel('Attractor State');
            title('Attractor Evolution');
            colorbar;
            
            % Plot 3: Attractor frequencies
            subplot(3, 4, 3);
            frequencies = zeros(obj.attractors.n_attractors, 1);
            for i = 1:obj.attractors.n_attractors
                frequencies(i) = obj.attractors.attractor_stats{i}.frequency;
            end
            bar(frequencies);
            xlabel('Attractor ID'); ylabel('Frequency');
            title('Attractor Frequencies');
            grid on;
            
            % Plot 4: Attractor durations
            subplot(3, 4, 4);
            durations = zeros(obj.attractors.n_attractors, 1);
            for i = 1:obj.attractors.n_attractors
                durations(i) = obj.attractors.attractor_stats{i}.duration;
            end
            bar(durations);
            xlabel('Attractor ID'); ylabel('Duration (s)');
            title('Attractor Durations');
            grid on;
            
            % Plot 5: Attractor compactness
            subplot(3, 4, 5);
            compactnesses = zeros(obj.attractors.n_attractors, 1);
            for i = 1:obj.attractors.n_attractors
                compactnesses(i) = obj.attractors.attractor_stats{i}.compactness;
            end
            bar(compactnesses);
            xlabel('Attractor ID'); ylabel('Compactness');
            title('Attractor Compactness');
            grid on;
            
            % Plot 6: Transition matrix
            subplot(3, 4, 6);
            if isfield(obj.analysisResults, 'attractor_summary') && isfield(obj.analysisResults.attractor_summary, 'transition_matrix')
                imagesc(obj.analysisResults.attractor_summary.transition_matrix);
                colorbar;
                xlabel('To State'); ylabel('From State');
                title('Transition Matrix');
            else
                text(0.5, 0.5, 'No transition matrix available', 'HorizontalAlignment', 'center');
                title('Transition Matrix');
            end
            
            % Plot 7: Phase transitions
            subplot(3, 4, 7);
            plot(obj.stateSpace.timestamps, obj.attractors.cluster_ids, 'b-', 'LineWidth', 1);
            hold on;
            if obj.transitions.n_transitions > 0
                for i = 1:length(obj.transitions.transition_times)
                    xline(obj.transitions.transition_times(i), 'r--', 'LineWidth', 2);
                end
            end
            xlabel('Time (s)'); ylabel('Attractor State');
            title('Phase Transitions');
            grid on;
            
            % Plot 8: Stability scores
            subplot(3, 4, 8);
            if isfield(obj.stability, 'stability_scores')
                bar(obj.stability.stability_scores);
                xlabel('Attractor ID'); ylabel('Stability Score');
                title('Attractor Stability');
                grid on;
            else
                text(0.5, 0.5, 'No stability data available', 'HorizontalAlignment', 'center');
                title('Attractor Stability');
            end
            
            % Plot 9: Return time analysis
            subplot(3, 4, 9);
            if isfield(obj.stability, 'return_times')
                all_return_times = [];
                for i = 1:length(obj.stability.return_times)
                    all_return_times = [all_return_times; obj.stability.return_times{i}];
                end
                if ~isempty(all_return_times)
                    histogram(all_return_times, 20);
                    xlabel('Return Time (s)'); ylabel('Frequency');
                    title('Return Time Distribution');
                    grid on;
                else
                    text(0.5, 0.5, 'No return time data', 'HorizontalAlignment', 'center');
                    title('Return Time Distribution');
                end
            else
                text(0.5, 0.5, 'No return time data available', 'HorizontalAlignment', 'center');
                title('Return Time Distribution');
            end
            
            % Plot 10: Attractor diversity
            subplot(3, 4, 10);
            if isfield(obj.analysisResults, 'attractor_summary') && isfield(obj.analysisResults.attractor_summary, 'diversity')
                bar(obj.analysisResults.attractor_summary.diversity);
                ylabel('Diversity (bits)');
                title('Attractor Diversity');
                grid on;
            else
                text(0.5, 0.5, 'No diversity data available', 'HorizontalAlignment', 'center');
                title('Attractor Diversity');
            end
            
            % Plot 11: Feature importance
            subplot(3, 4, 11);
            if obj.stateSpace.n_features > 1
                feature_variance = var(obj.stateSpace.data, [], 1);
                bar(feature_variance);
                xlabel('Feature Index'); ylabel('Variance');
                title('Feature Importance');
                grid on;
            else
                text(0.5, 0.5, 'Single feature analysis', 'HorizontalAlignment', 'center');
                title('Feature Importance');
            end
            
            % Plot 12: Summary statistics
            subplot(3, 4, 12);
            if isfield(obj.analysisResults, 'attractor_summary')
                summary = obj.analysisResults.attractor_summary;
                text(0.1, 0.8, sprintf('Analysis Summary:'), 'FontSize', 12, 'FontWeight', 'bold');
                text(0.1, 0.7, sprintf('Attractors: %d', summary.n_attractors), 'FontSize', 10);
                text(0.1, 0.6, sprintf('Duration: %.1f s', summary.total_duration), 'FontSize', 10);
                if isfield(summary, 'dominant_attractor')
                    text(0.1, 0.5, sprintf('Dominant: %d', summary.dominant_attractor), 'FontSize', 10);
                end
                if isfield(summary, 'diversity')
                    text(0.1, 0.4, sprintf('Diversity: %.2f', summary.diversity), 'FontSize', 10);
                end
                if isfield(obj.stability, 'system_stability')
                    text(0.1, 0.3, sprintf('Stability: %.2f', obj.stability.system_stability), 'FontSize', 10);
                end
            else
                text(0.5, 0.5, 'No summary data available', 'HorizontalAlignment', 'center');
            end
            axis off;
            
            sgtitle('Attractor Analysis Results');
        end
        
        function exportResults(obj, output_dir)
            % Export attractor analysis results
            if ~exist(output_dir, 'dir')
                mkdir(output_dir);
            end
            
            % Export attractors
            attractors = obj.attractors;
            save(fullfile(output_dir, 'attractors.mat'), 'attractors');
            
            % Export transitions
            transitions = obj.transitions;
            save(fullfile(output_dir, 'transitions.mat'), 'transitions');
            
            % Export stability analysis
            stability = obj.stability;
            save(fullfile(output_dir, 'stability.mat'), 'stability');
            
            % Export analysis results
            analysis_results = obj.analysisResults;
            save(fullfile(output_dir, 'analysis_results.mat'), 'analysis_results');
            
            % Export parameters
            parameters = obj.parameters;
            save(fullfile(output_dir, 'parameters.mat'), 'parameters');
            
            % Export state space
            state_space = obj.stateSpace;
            save(fullfile(output_dir, 'state_space.mat'), 'state_space');
            
            fprintf('Attractor analysis results exported to: %s\n', output_dir);
        end
    end
end
