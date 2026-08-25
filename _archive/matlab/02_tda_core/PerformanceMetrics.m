classdef PerformanceMetrics < handle
    % PerformanceMetrics - Link topological features to football performance metrics
    % Implements methods to correlate TDA results with actual football performance
    
    properties
        topologicalFeatures
        coupledMetrics
        performanceData
        correlations
        predictiveModels
        analysisResults
        parameters
    end
    
    methods
        function obj = PerformanceMetrics()
            % Initialize the performance metrics analyzer
            obj.topologicalFeatures = struct();
            obj.coupledMetrics = struct();
            obj.performanceData = struct();
            obj.correlations = struct();
            obj.predictiveModels = struct();
            obj.analysisResults = struct();
            
            % Set default parameters
            obj.parameters = struct();
            obj.parameters.correlationThreshold = 0.3;        % Minimum correlation for significance
            obj.parameters.pValueThreshold = 0.05;           % Statistical significance threshold
            obj.parameters.lagWindow = 5;                    % Time window for lagged correlations
            obj.parameters.predictionWindow = 10;            % Window for predictive analysis
            obj.parameters.crossValidationFolds = 5;         % Cross-validation folds
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
        
        function loadTopologicalData(obj, topological_features, coupled_metrics, timestamps)
            % Load topological and coupled dynamics data
            obj.topologicalFeatures = topological_features;
            obj.coupledMetrics = coupled_metrics;
            obj.performanceData.timestamps = timestamps;
            
            fprintf('Loaded topological data: %d time points\n', length(timestamps));
        end
        
        function generatePerformanceMetrics(obj, match_events, team_positions)
            % Generate performance metrics from match events and positions
            fprintf('Generating performance metrics...\n');
            
            n_times = length(obj.performanceData.timestamps);
            
            % Initialize performance metrics
            obj.performanceData = struct();
            obj.performanceData.timestamps = obj.performanceData.timestamps;
            obj.performanceData.shots = zeros(n_times, 1);
            obj.performanceData.goals = zeros(n_times, 1);
            obj.performanceData.passes = zeros(n_times, 1);
            obj.performanceData.successful_passes = zeros(n_times, 1);
            obj.performanceData.tackles = zeros(n_times, 1);
            obj.performanceData.interceptions = zeros(n_times, 1);
            obj.performanceData.ball_possession = zeros(n_times, 1);
            obj.performanceData.field_control = zeros(n_times, 1);
            obj.performanceData.attacking_threat = zeros(n_times, 1);
            obj.performanceData.defensive_stability = zeros(n_times, 1);
            
            % Generate synthetic performance metrics based on team positions
            obj.generateSyntheticPerformanceMetrics(team_positions);
            
            fprintf('Performance metrics generated for %d time points\n', n_times);
        end
        
        function generateSyntheticPerformanceMetrics(obj, team_positions)
            % Generate synthetic performance metrics based on team positions
            n_times = length(obj.performanceData.timestamps);
            
            for t = 1:n_times
                if t <= size(team_positions, 1)
                    home_pos = squeeze(team_positions(t, :, 1:2));
                    
                    % Ball possession (based on field position)
                    avg_x_position = mean(home_pos(:, 1));
                    obj.performanceData.ball_possession(t) = min(1, max(0, avg_x_position / 105));
                    
                    % Field control (based on spread and position)
                    team_spread = std(home_pos, [], 'all');
                    obj.performanceData.field_control(t) = min(1, team_spread / 50);
                    
                    % Attacking threat (based on forward position and compactness)
                    forward_players = sum(home_pos(:, 1) > 70);
                    compactness = 1 / (1 + team_spread);
                    obj.performanceData.attacking_threat(t) = (forward_players / 10) * compactness;
                    
                    % Defensive stability (based on back position and organization)
                    back_players = sum(home_pos(:, 1) < 40);
                    organization = 1 / (1 + std(home_pos(:, 2)));
                    obj.performanceData.defensive_stability(t) = (back_players / 10) * organization;
                    
                    % Shots (based on attacking threat and field control)
                    if obj.performanceData.attacking_threat(t) > 0.6 && obj.performanceData.field_control(t) > 0.4
                        obj.performanceData.shots(t) = rand() < 0.1;
                    end
                    
                    % Goals (based on shots and attacking threat)
                    if obj.performanceData.shots(t) && obj.performanceData.attacking_threat(t) > 0.8
                        obj.performanceData.goals(t) = rand() < 0.2;
                    end
                    
                    % Passes (based on field control and ball possession)
                    if obj.performanceData.field_control(t) > 0.3
                        obj.performanceData.passes(t) = rand() < 0.3;
                        if obj.performanceData.passes(t)
                            obj.performanceData.successful_passes(t) = rand() < 0.8;
                        end
                    end
                    
                    % Tackles (based on defensive stability and low ball possession)
                    if obj.performanceData.defensive_stability(t) > 0.5 && obj.performanceData.ball_possession(t) < 0.4
                        obj.performanceData.tackles(t) = rand() < 0.2;
                    end
                    
                    % Interceptions (based on defensive stability and field control)
                    if obj.performanceData.defensive_stability(t) > 0.6 && obj.performanceData.field_control(t) > 0.5
                        obj.performanceData.interceptions(t) = rand() < 0.15;
                    end
                end
            end
        end
        
        function computeCorrelations(obj)
            % Compute correlations between topological features and performance metrics
            fprintf('Computing correlations between topological features and performance metrics...\n');
            
            obj.correlations = struct();
            
            % Get feature names
            feature_names = fieldnames(obj.topologicalFeatures);
            performance_names = fieldnames(obj.performanceData);
            
            % Remove timestamps from performance names
            performance_names = performance_names(~strcmp(performance_names, 'timestamps'));
            
            % Initialize correlation matrices
            n_features = length(feature_names);
            n_performance = length(performance_names);
            
            obj.correlations.correlation_matrix = zeros(n_features, n_performance);
            obj.correlations.p_value_matrix = zeros(n_features, n_performance);
            obj.correlations.significant_correlations = [];
            
            % Compute correlations
            for i = 1:n_features
                feature_name = feature_names{i};
                feature_data = obj.topologicalFeatures.(feature_name);
                
                for j = 1:n_performance
                    performance_name = performance_names{j};
                    performance_data = obj.performanceData.(performance_name);
                    
                    % Ensure same length
                    min_length = min(length(feature_data), length(performance_data));
                    if min_length > 10
                        feature_subset = feature_data(1:min_length);
                        performance_subset = performance_data(1:min_length);
                        
                        % Compute correlation
                        [correlation, p_value] = corrcoef(feature_subset, performance_subset);
                        
                        if size(correlation, 1) > 1
                            obj.correlations.correlation_matrix(i, j) = correlation(1, 2);
                            obj.correlations.p_value_matrix(i, j) = p_value(1, 2);
                            
                            % Check significance
                            if abs(correlation(1, 2)) > obj.parameters.correlationThreshold && p_value(1, 2) < obj.parameters.pValueThreshold
                                obj.correlations.significant_correlations(end+1, :) = [i, j, correlation(1, 2), p_value(1, 2)];
                            end
                        end
                    end
                end
            end
            
            % Store feature and performance names
            obj.correlations.feature_names = feature_names;
            obj.correlations.performance_names = performance_names;
            
            fprintf('Found %d significant correlations\n', size(obj.correlations.significant_correlations, 1));
        end
        
        function computeLaggedCorrelations(obj)
            % Compute lagged correlations to identify predictive relationships
            fprintf('Computing lagged correlations...\n');
            
            obj.correlations.lagged_correlations = struct();
            
            feature_names = obj.correlations.feature_names;
            performance_names = obj.correlations.performance_names;
            
            for i = 1:length(feature_names)
                feature_name = feature_names{i};
                feature_data = obj.topologicalFeatures.(feature_name);
                
                for j = 1:length(performance_names)
                    performance_name = performance_names{j};
                    performance_data = obj.performanceData.(performance_name);
                    
                    % Compute lagged correlations
                    max_lag = obj.parameters.lagWindow;
                    lagged_corrs = zeros(max_lag * 2 + 1, 1);
                    lagged_pvals = zeros(max_lag * 2 + 1, 1);
                    
                    for lag = -max_lag:max_lag
                        if lag < 0
                            % Feature leads performance
                            feature_lead = feature_data(1:end+lag);
                            performance_lag = performance_data(-lag+1:end);
                        elseif lag > 0
                            % Performance leads feature
                            feature_lag = feature_data(lag+1:end);
                            performance_lead = performance_data(1:end-lag);
                        else
                            % No lag
                            feature_lead = feature_data;
                            performance_lag = performance_data;
                        end
                        
                        if lag ~= 0
                            min_length = min(length(feature_lead), length(performance_lag));
                            if min_length > 10
                                feature_subset = feature_lead(1:min_length);
                                performance_subset = performance_lag(1:min_length);
                                
                                [correlation, p_value] = corrcoef(feature_subset, performance_subset);
                                if size(correlation, 1) > 1
                                    lagged_corrs(lag + max_lag + 1) = correlation(1, 2);
                                    lagged_pvals(lag + max_lag + 1) = p_value(1, 2);
                                end
                            end
                        end
                    end
                    
                    % Store lagged correlations
                    obj.correlations.lagged_correlations.(feature_name).(performance_name) = struct();
                    obj.correlations.lagged_correlations.(feature_name).(performance_name).correlations = lagged_corrs;
                    obj.correlations.lagged_correlations.(feature_name).(performance_name).p_values = lagged_pvals;
                    obj.correlations.lagged_correlations.(feature_name).(performance_name).lags = -max_lag:max_lag;
                end
            end
            
            fprintf('Lagged correlations computed\n');
        end
        
        function buildPredictiveModels(obj)
            % Build predictive models for performance metrics
            fprintf('Building predictive models...\n');
            
            obj.predictiveModels = struct();
            
            feature_names = obj.correlations.feature_names;
            performance_names = obj.correlations.performance_names;
            
            % Prepare feature matrix
            n_features = length(feature_names);
            n_times = length(obj.performanceData.timestamps);
            
            feature_matrix = zeros(n_times, n_features);
            for i = 1:n_features
                feature_data = obj.topologicalFeatures.(feature_names{i});
                min_length = min(length(feature_data), n_times);
                feature_matrix(1:min_length, i) = feature_data(1:min_length);
            end
            
            % Build models for each performance metric
            for j = 1:length(performance_names)
                performance_name = performance_names{j};
                performance_data = obj.performanceData.(performance_name);
                
                % Prepare target data
                min_length = min(length(performance_data), n_times);
                target_data = performance_data(1:min_length);
                feature_subset = feature_matrix(1:min_length, :);
                
                % Skip if insufficient data
                if min_length < 20
                    continue;
                end
                
                % Build linear regression model
                try
                    model = fitlm(feature_subset, target_data);
                    obj.predictiveModels.(performance_name) = struct();
                    obj.predictiveModels.(performance_name).model = model;
                    obj.predictiveModels.(performance_name).r_squared = model.Rsquared.Ordinary;
                    obj.predictiveModels.(performance_name).p_value = model.Coefficients.pValue(2:end);
                    obj.predictiveModels.(performance_name).coefficients = model.Coefficients.Estimate(2:end);
                    obj.predictiveModels.(performance_name).feature_names = feature_names;
                    
                    % Cross-validation
                    cv_results = obj.performCrossValidation(feature_subset, target_data);
                    obj.predictiveModels.(performance_name).cv_results = cv_results;
                    
                catch ME
                    warning('Failed to build model for %s: %s', performance_name, ME.message);
                end
            end
            
            fprintf('Predictive models built for %d performance metrics\n', length(fieldnames(obj.predictiveModels)));
        end
        
        function cv_results = performCrossValidation(obj, features, targets)
            % Perform cross-validation for model evaluation
            n_folds = obj.parameters.crossValidationFolds;
            n_samples = size(features, 1);
            
            % Create fold indices
            fold_size = floor(n_samples / n_folds);
            cv_results = struct();
            cv_results.r_squared_scores = zeros(n_folds, 1);
            cv_results.rmse_scores = zeros(n_folds, 1);
            
            for fold = 1:n_folds
                % Create train/test split
                test_start = (fold - 1) * fold_size + 1;
                test_end = min(fold * fold_size, n_samples);
                test_indices = test_start:test_end;
                train_indices = setdiff(1:n_samples, test_indices);
                
                % Train model
                try
                    train_features = features(train_indices, :);
                    train_targets = targets(train_indices);
                    test_features = features(test_indices, :);
                    test_targets = targets(test_indices);
                    
                    model = fitlm(train_features, train_targets);
                    
                    % Test model
                    predictions = predict(model, test_features);
                    
                    % Compute metrics
                    cv_results.r_squared_scores(fold) = 1 - sum((test_targets - predictions).^2) / sum((test_targets - mean(test_targets)).^2);
                    cv_results.rmse_scores(fold) = sqrt(mean((test_targets - predictions).^2));
                    
                catch ME
                    warning('Cross-validation fold %d failed: %s', fold, ME.message);
                    cv_results.r_squared_scores(fold) = 0;
                    cv_results.rmse_scores(fold) = inf;
                end
            end
            
            % Summary statistics
            cv_results.mean_r_squared = mean(cv_results.r_squared_scores);
            cv_results.std_r_squared = std(cv_results.r_squared_scores);
            cv_results.mean_rmse = mean(cv_results.rmse_scores);
            cv_results.std_rmse = std(cv_results.rmse_scores);
        end
        
        function analyzePerformancePatterns(obj)
            % Analyze patterns in performance metrics
            fprintf('Analyzing performance patterns...\n');
            
            obj.analysisResults = struct();
            obj.analysisResults.performance_summary = struct();
            obj.analysisResults.pattern_analysis = struct();
            
            % Performance summary
            performance_names = obj.correlations.performance_names;
            for i = 1:length(performance_names)
                name = performance_names{i};
                data = obj.performanceData.(name);
                
                obj.analysisResults.performance_summary.(name) = struct();
                obj.analysisResults.performance_summary.(name).mean = mean(data);
                obj.analysisResults.performance_summary.(name).std = std(data);
                obj.analysisResults.performance_summary.(name).max = max(data);
                obj.analysisResults.performance_summary.(name).min = min(data);
                obj.analysisResults.performance_summary.(name).total = sum(data);
            end
            
            % Pattern analysis
            obj.analysisResults.pattern_analysis = obj.identifyPerformancePatterns();
            
            fprintf('Performance pattern analysis complete\n');
        end
        
        function patterns = identifyPerformancePatterns(obj)
            % Identify patterns in performance metrics
            patterns = struct();
            
            % Analyze temporal patterns
            patterns.temporal_patterns = obj.analyzeTemporalPatterns();
            
            % Analyze correlation patterns
            patterns.correlation_patterns = obj.analyzeCorrelationPatterns();
            
            % Analyze predictive patterns
            patterns.predictive_patterns = obj.analyzePredictivePatterns();
        end
        
        function temporal_patterns = analyzeTemporalPatterns(obj)
            % Analyze temporal patterns in performance metrics
            temporal_patterns = struct();
            
            performance_names = obj.correlations.performance_names;
            
            for i = 1:length(performance_names)
                name = performance_names{i};
                data = obj.performanceData.(name);
                
                % Compute autocorrelation
                if length(data) > 20
                    [autocorr, lags] = xcorr(data, data, 'coeff');
                    [max_autocorr, max_lag_idx] = max(autocorr);
                    max_lag = lags(max_lag_idx);
                    
                    temporal_patterns.(name) = struct();
                    temporal_patterns.(name).max_autocorrelation = max_autocorr;
                    temporal_patterns.(name).max_lag = max_lag;
                    temporal_patterns.(name).periodicity = max_lag > 0;
                end
            end
        end
        
        function correlation_patterns = analyzeCorrelationPatterns(obj)
            % Analyze patterns in correlations
            correlation_patterns = struct();
            
            % Find strongest correlations
            if ~isempty(obj.correlations.significant_correlations)
                [~, strongest_idx] = max(abs(obj.correlations.significant_correlations(:, 3)));
                strongest_corr = obj.correlations.significant_correlations(strongest_idx, :);
                
                correlation_patterns.strongest_correlation = struct();
                correlation_patterns.strongest_correlation.feature_idx = strongest_corr(1);
                correlation_patterns.strongest_correlation.performance_idx = strongest_corr(2);
                correlation_patterns.strongest_correlation.correlation = strongest_corr(3);
                correlation_patterns.strongest_correlation.p_value = strongest_corr(4);
                correlation_patterns.strongest_correlation.feature_name = obj.correlations.feature_names{strongest_corr(1)};
                correlation_patterns.strongest_correlation.performance_name = obj.correlations.performance_names{strongest_corr(2)};
            end
            
            % Analyze correlation clusters
            correlation_patterns.correlation_clusters = obj.identifyCorrelationClusters();
        end
        
        function clusters = identifyCorrelationClusters(obj)
            % Identify clusters of correlated features
            clusters = struct();
            
            if isempty(obj.correlations.correlation_matrix)
                return;
            end
            
            % Use hierarchical clustering on correlation matrix
            try
                distances = 1 - abs(obj.correlations.correlation_matrix);
                linkage_tree = linkage(distances(:), 'ward');
                cluster_ids = cluster(linkage_tree, 'MaxClust', 3);
                
                clusters.cluster_ids = cluster_ids;
                clusters.n_clusters = max(cluster_ids);
                
                % Analyze each cluster
                for i = 1:clusters.n_clusters
                    cluster_mask = cluster_ids == i;
                    clusters.cluster_stats(i) = struct();
                    clusters.cluster_stats(i).size = sum(cluster_mask);
                    clusters.cluster_stats(i).mean_correlation = mean(abs(obj.correlations.correlation_matrix(cluster_mask)));
                end
                
            catch ME
                warning('Failed to identify correlation clusters: %s', ME.message);
                clusters = struct();
            end
        end
        
        function predictive_patterns = analyzePredictivePatterns(obj)
            % Analyze predictive patterns
            predictive_patterns = struct();
            
            model_names = fieldnames(obj.predictiveModels);
            
            for i = 1:length(model_names)
                name = model_names{i};
                model = obj.predictiveModels.(name);
                
                predictive_patterns.(name) = struct();
                predictive_patterns.(name).r_squared = model.r_squared;
                predictive_patterns.(name).cv_r_squared = model.cv_results.mean_r_squared;
                predictive_patterns.(name).cv_rmse = model.cv_results.mean_rmse;
                predictive_patterns.(name).predictive_power = model.cv_results.mean_r_squared > 0.3;
                
                % Identify most important features
                [~, important_idx] = max(abs(model.coefficients));
                predictive_patterns.(name).most_important_feature = model.feature_names{important_idx};
                predictive_patterns.(name).most_important_coefficient = model.coefficients(important_idx);
            end
        end
        
        function visualizeResults(obj)
            % Visualize performance metrics analysis results
            figure('Position', [100, 100, 1600, 1200]);
            
            % Plot 1: Performance metrics over time
            subplot(3, 4, 1);
            performance_names = obj.correlations.performance_names;
            colors = lines(length(performance_names));
            
            for i = 1:length(performance_names)
                name = performance_names{i};
                data = obj.performanceData.(name);
                plot(obj.performanceData.timestamps, data, 'Color', colors(i, :), 'LineWidth', 2);
                hold on;
            end
            
            xlabel('Time (s)'); ylabel('Value');
            title('Performance Metrics Over Time');
            legend(performance_names, 'Location', 'best');
            grid on;
            
            % Plot 2: Correlation matrix
            subplot(3, 4, 2);
            if ~isempty(obj.correlations.correlation_matrix)
                imagesc(obj.correlations.correlation_matrix);
                colorbar;
                xlabel('Performance Metrics');
                ylabel('Topological Features');
                title('Correlation Matrix');
                set(gca, 'XTickLabel', obj.correlations.performance_names);
                set(gca, 'YTickLabel', obj.correlations.feature_names);
            else
                text(0.5, 0.5, 'No correlation data', 'HorizontalAlignment', 'center');
                title('Correlation Matrix');
            end
            
            % Plot 3: Significant correlations
            subplot(3, 4, 3);
            if ~isempty(obj.correlations.significant_correlations)
                scatter(obj.correlations.significant_correlations(:, 3), ...
                       obj.correlations.significant_correlations(:, 4), 100, 'b', 'filled');
                xlabel('Correlation'); ylabel('P-value');
                title('Significant Correlations');
                grid on;
            else
                text(0.5, 0.5, 'No significant correlations', 'HorizontalAlignment', 'center');
                title('Significant Correlations');
            end
            
            % Plot 4: Model performance
            subplot(3, 4, 4);
            model_names = fieldnames(obj.predictiveModels);
            if ~isempty(model_names)
                r_squared_scores = zeros(length(model_names), 1);
                for i = 1:length(model_names)
                    r_squared_scores(i) = obj.predictiveModels.(model_names{i}).r_squared;
                end
                bar(r_squared_scores);
                xlabel('Performance Metric'); ylabel('R²');
                title('Model Performance');
                set(gca, 'XTickLabel', model_names);
                grid on;
            else
                text(0.5, 0.5, 'No predictive models', 'HorizontalAlignment', 'center');
                title('Model Performance');
            end
            
            % Plot 5: Cross-validation results
            subplot(3, 4, 5);
            if ~isempty(model_names)
                cv_r_squared = zeros(length(model_names), 1);
                for i = 1:length(model_names)
                    cv_r_squared(i) = obj.predictiveModels.(model_names{i}).cv_results.mean_r_squared;
                end
                bar(cv_r_squared);
                xlabel('Performance Metric'); ylabel('CV R²');
                title('Cross-Validation Performance');
                set(gca, 'XTickLabel', model_names);
                grid on;
            else
                text(0.5, 0.5, 'No CV results', 'HorizontalAlignment', 'center');
                title('Cross-Validation Performance');
            end
            
            % Plot 6: Feature importance
            subplot(3, 4, 6);
            if ~isempty(model_names)
                % Use first model for feature importance
                first_model = obj.predictiveModels.(model_names{1});
                bar(abs(first_model.coefficients));
                xlabel('Feature Index'); ylabel('Coefficient Magnitude');
                title('Feature Importance');
                grid on;
            else
                text(0.5, 0.5, 'No feature data', 'HorizontalAlignment', 'center');
                title('Feature Importance');
            end
            
            % Plot 7: Lagged correlations
            subplot(3, 4, 7);
            if isfield(obj.correlations, 'lagged_correlations')
                feature_names = obj.correlations.feature_names;
                performance_names = obj.correlations.performance_names;
                
                if ~isempty(feature_names) && ~isempty(performance_names)
                    lagged_data = obj.correlations.lagged_correlations.(feature_names{1}).(performance_names{1});
                    plot(lagged_data.lags, lagged_data.correlations, 'b-', 'LineWidth', 2);
                    xlabel('Lag'); ylabel('Correlation');
                    title('Lagged Correlations');
                    grid on;
                else
                    text(0.5, 0.5, 'No lagged data', 'HorizontalAlignment', 'center');
                    title('Lagged Correlations');
                end
            else
                text(0.5, 0.5, 'No lagged correlations', 'HorizontalAlignment', 'center');
                title('Lagged Correlations');
            end
            
            % Plot 8: Performance summary
            subplot(3, 4, 8);
            if isfield(obj.analysisResults, 'performance_summary')
                summary = obj.analysisResults.performance_summary;
                summary_names = fieldnames(summary);
                means = zeros(length(summary_names), 1);
                for i = 1:length(summary_names)
                    means(i) = summary.(summary_names{i}).mean;
                end
                bar(means);
                xlabel('Performance Metric'); ylabel('Mean Value');
                title('Performance Summary');
                set(gca, 'XTickLabel', summary_names);
                grid on;
            else
                text(0.5, 0.5, 'No summary data', 'HorizontalAlignment', 'center');
                title('Performance Summary');
            end
            
            % Plot 9: Temporal patterns
            subplot(3, 4, 9);
            if isfield(obj.analysisResults, 'pattern_analysis') && isfield(obj.analysisResults.pattern_analysis, 'temporal_patterns')
                temporal = obj.analysisResults.pattern_analysis.temporal_patterns;
                temporal_names = fieldnames(temporal);
                autocorrs = zeros(length(temporal_names), 1);
                for i = 1:length(temporal_names)
                    autocorrs(i) = temporal.(temporal_names{i}).max_autocorrelation;
                end
                bar(autocorrs);
                xlabel('Performance Metric'); ylabel('Max Autocorrelation');
                title('Temporal Patterns');
                set(gca, 'XTickLabel', temporal_names);
                grid on;
            else
                text(0.5, 0.5, 'No temporal patterns', 'HorizontalAlignment', 'center');
                title('Temporal Patterns');
            end
            
            % Plot 10: Correlation clusters
            subplot(3, 4, 10);
            if isfield(obj.analysisResults, 'pattern_analysis') && isfield(obj.analysisResults.pattern_analysis, 'correlation_patterns')
                corr_patterns = obj.analysisResults.pattern_analysis.correlation_patterns;
                if isfield(corr_patterns, 'correlation_clusters') && isfield(corr_patterns.correlation_clusters, 'cluster_ids')
                    scatter(1:length(corr_patterns.correlation_clusters.cluster_ids), ...
                           corr_patterns.correlation_clusters.cluster_ids, 100, 'b', 'filled');
                    xlabel('Feature Index'); ylabel('Cluster ID');
                    title('Correlation Clusters');
                    grid on;
                else
                    text(0.5, 0.5, 'No cluster data', 'HorizontalAlignment', 'center');
                    title('Correlation Clusters');
                end
            else
                text(0.5, 0.5, 'No correlation patterns', 'HorizontalAlignment', 'center');
                title('Correlation Clusters');
            end
            
            % Plot 11: Predictive patterns
            subplot(3, 4, 11);
            if isfield(obj.analysisResults, 'pattern_analysis') && isfield(obj.analysisResults.pattern_analysis, 'predictive_patterns')
                pred_patterns = obj.analysisResults.pattern_analysis.predictive_patterns;
                pred_names = fieldnames(pred_patterns);
                predictive_powers = zeros(length(pred_names), 1);
                for i = 1:length(pred_names)
                    predictive_powers(i) = pred_patterns.(pred_names{i}).predictive_power;
                end
                bar(predictive_powers);
                xlabel('Performance Metric'); ylabel('Predictive Power');
                title('Predictive Patterns');
                set(gca, 'XTickLabel', pred_names);
                grid on;
            else
                text(0.5, 0.5, 'No predictive patterns', 'HorizontalAlignment', 'center');
                title('Predictive Patterns');
            end
            
            % Plot 12: Analysis summary
            subplot(3, 4, 12);
            text(0.1, 0.8, sprintf('Analysis Summary:'), 'FontSize', 12, 'FontWeight', 'bold');
            text(0.1, 0.7, sprintf('Features: %d', length(obj.correlations.feature_names)), 'FontSize', 10);
            text(0.1, 0.6, sprintf('Performance Metrics: %d', length(obj.correlations.performance_names)), 'FontSize', 10);
            text(0.1, 0.5, sprintf('Significant Correlations: %d', size(obj.correlations.significant_correlations, 1)), 'FontSize', 10);
            text(0.1, 0.4, sprintf('Predictive Models: %d', length(fieldnames(obj.predictiveModels))), 'FontSize', 10);
            if isfield(obj.analysisResults, 'pattern_analysis') && isfield(obj.analysisResults.pattern_analysis, 'correlation_patterns')
                corr_patterns = obj.analysisResults.pattern_analysis.correlation_patterns;
                if isfield(corr_patterns, 'strongest_correlation')
                    text(0.1, 0.3, sprintf('Strongest Corr: %.3f', corr_patterns.strongest_correlation.correlation), 'FontSize', 10);
                end
            end
            axis off;
            
            sgtitle('Performance Metrics Analysis Results');
        end
        
        function exportResults(obj, output_dir)
            % Export performance metrics analysis results
            if ~exist(output_dir, 'dir')
                mkdir(output_dir);
            end
            
            % Export correlations
            correlations = obj.correlations;
            save(fullfile(output_dir, 'correlations.mat'), 'correlations');
            
            % Export predictive models
            predictive_models = obj.predictiveModels;
            save(fullfile(output_dir, 'predictive_models.mat'), 'predictive_models');
            
            % Export analysis results
            analysis_results = obj.analysisResults;
            save(fullfile(output_dir, 'analysis_results.mat'), 'analysis_results');
            
            % Export performance data
            performance_data = obj.performanceData;
            save(fullfile(output_dir, 'performance_data.mat'), 'performance_data');
            
            % Export parameters
            parameters = obj.parameters;
            save(fullfile(output_dir, 'parameters.mat'), 'parameters');
            
            fprintf('Performance metrics results exported to: %s\n', output_dir);
        end
    end
end
