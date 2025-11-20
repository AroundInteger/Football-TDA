classdef CoupledCollectiveVariables
    % COUPLEDCOLLECTIVEVARIABLES - Implements coupled team dynamics analysis
    % 
    % This class implements the foundational coupled collective variables for
    % football team dynamics analysis, based on established research in
    % sports analytics and collective behavior.
    %
    % Key Features:
    % - Inter-Team Centroid Vector (field stretch & pressure direction)
    % - Team Shape Coupling (area ratios & shape dynamics)
    % - Nearest Opponent Distance (NOD) analysis
    % - Real-time calculation and visualization
    %
    % Based on research by:
    % - Frencken et al. (2011) - Space-time coordination in football
    % - Clemente et al. (2015) - Collective behavior analysis
    % - Memmert et al. (2017) - Tactical analysis frameworks
    
    properties
        % Data properties
        homePositions     % [time, players, coordinates] - Home team positions
        awayPositions     % [time, players, coordinates] - Away team positions
        timestamps        % Vector of timestamps
        fieldDimensions   % [length, width] in meters
        
        % Analysis parameters
        samplingRate      % Data sampling rate (Hz)
        minPlayers        % Minimum players required for analysis
        outlierThreshold  % Threshold for outlier detection
        
        % Computed metrics
        interTeamCentroidVector  % [distance, angle] over time
        teamShapeCoupling        % Area ratios and shape metrics
        nearestOpponentDistance  % NOD analysis results
        coupledMetrics           % Combined metrics table
        
        % Analysis results
        analysisComplete         % Boolean flag
        computationTime          % Time taken for analysis
    end
    
    methods
        function obj = CoupledCollectiveVariables(homePositions, awayPositions, timestamps, varargin)
            % Constructor for CoupledCollectiveVariables
            %
            % Inputs:
            %   homePositions - [time, players, coordinates] matrix
            %   awayPositions - [time, players, coordinates] matrix  
            %   timestamps    - Vector of timestamps
            %   varargin      - Optional parameters (fieldDimensions, samplingRate, etc.)
            
            % Store input data
            obj.homePositions = homePositions;
            obj.awayPositions = awayPositions;
            obj.timestamps = timestamps;
            
            % Set default parameters
            obj.fieldDimensions = [105, 68]; % Standard field dimensions
            obj.samplingRate = 10; % Default 10 Hz
            obj.minPlayers = 8; % Minimum players for reliable analysis
            obj.outlierThreshold = 3; % 3 standard deviations
            
            % Parse optional parameters
            if nargin > 3
                for i = 1:2:length(varargin)
                    switch lower(varargin{i})
                        case 'fielddimensions'
                            obj.fieldDimensions = varargin{i+1};
                        case 'samplingrate'
                            obj.samplingRate = varargin{i+1};
                        case 'minplayers'
                            obj.minPlayers = varargin{i+1};
                        case 'outlierthreshold'
                            obj.outlierThreshold = varargin{i+1};
                    end
                end
            end
            
            % Initialize computed metrics
            obj.analysisComplete = false;
            obj.computationTime = 0;
            
            fprintf('CoupledCollectiveVariables initialized\n');
            fprintf('  Time points: %d\n', size(homePositions, 1));
            fprintf('  Home players: %d\n', size(homePositions, 2));
            fprintf('  Away players: %d\n', size(awayPositions, 2));
            fprintf('  Field dimensions: %.0f x %.0f m\n', obj.fieldDimensions(1), obj.fieldDimensions(2));
        end
        
        function obj = computeCoupledMetrics(obj)
            % Compute all coupled collective variables
            %
            % This method implements the core coupled dynamics analysis
            % as described in the GPS-TDA framework
            
            fprintf('Computing coupled collective variables...\n');
            tic;
            
            nTimes = size(obj.homePositions, 1);
            
            % Initialize results arrays
            obj.interTeamCentroidVector = zeros(nTimes, 2); % [distance, angle]
            obj.teamShapeCoupling = zeros(nTimes, 4); % [homeArea, awayArea, ratio, shapeDiff]
            obj.nearestOpponentDistance = zeros(nTimes, 4); % [homeMean, awayMean, homeStd, awayStd]
            
            % Initialize coupled metrics table
            metricNames = {'TimeStep', 'Timestamp', 'InterTeamDistance', 'InterTeamAngle', ...
                          'HomeTeamArea', 'AwayTeamArea', 'TeamAreaRatio', 'ShapeDifference', ...
                          'HomeMeanNOD', 'AwayMeanNOD', 'HomeStdNOD', 'AwayStdNOD', ...
                          'HomeMinNOD', 'AwayMinNOD', 'HomeMaxNOD', 'AwayMaxNOD'};
            obj.coupledMetrics = table('Size', [nTimes, length(metricNames)], ...
                                      'VariableNames', metricNames, ...
                                      'VariableTypes', repmat({'double'}, 1, length(metricNames)));
            
            % Process each time step
            for t = 1:nTimes
                % Extract positions for current time step
                homePos = squeeze(obj.homePositions(t, :, 1:2));
                awayPos = squeeze(obj.awayPositions(t, :, 1:2));
                
                % Remove invalid positions
                validHome = ~isnan(homePos(:, 1)) & ~isnan(homePos(:, 2));
                validAway = ~isnan(awayPos(:, 1)) & ~isnan(awayPos(:, 2));
                
                if sum(validHome) >= obj.minPlayers && sum(validAway) >= obj.minPlayers
                    % 1. Inter-Team Centroid Vector
                    [interDist, interAngle] = obj.computeInterTeamCentroidVector(homePos(validHome, :), awayPos(validAway, :));
                    obj.interTeamCentroidVector(t, :) = [interDist, interAngle];
                    
                    % 2. Team Shape Coupling
                    [homeArea, awayArea, areaRatio, shapeDiff] = obj.computeTeamShapeCoupling(homePos(validHome, :), awayPos(validAway, :));
                    obj.teamShapeCoupling(t, :) = [homeArea, awayArea, areaRatio, shapeDiff];
                    
                    % 3. Nearest Opponent Distance (NOD)
                    [homeNOD, awayNOD] = obj.computeNearestOpponentDistance(homePos(validHome, :), awayPos(validAway, :));
                    obj.nearestOpponentDistance(t, :) = [mean(homeNOD), mean(awayNOD), std(homeNOD), std(awayNOD)];
                    
                    % Store in table
                    obj.coupledMetrics(t, :) = {t, obj.timestamps(t), interDist, interAngle, ...
                                               homeArea, awayArea, areaRatio, shapeDiff, ...
                                               mean(homeNOD), mean(awayNOD), std(homeNOD), std(awayNOD), ...
                                               min(homeNOD), min(awayNOD), max(homeNOD), max(awayNOD)};
                else
                    % Handle insufficient players
                    obj.interTeamCentroidVector(t, :) = [NaN, NaN];
                    obj.teamShapeCoupling(t, :) = [NaN, NaN, NaN, NaN];
                    obj.nearestOpponentDistance(t, :) = [NaN, NaN, NaN, NaN];
                    
                    obj.coupledMetrics(t, :) = {t, obj.timestamps(t), NaN, NaN, ...
                                               NaN, NaN, NaN, NaN, ...
                                               NaN, NaN, NaN, NaN, ...
                                               NaN, NaN, NaN, NaN};
                end
                
                % Progress indicator
                if mod(t, 100) == 0
                    fprintf('  Processed %d of %d time steps\n', t, nTimes);
                end
            end
            
            % Remove outliers
            obj = obj.removeOutliers();
            
            % Mark analysis as complete
            obj.analysisComplete = true;
            obj.computationTime = toc;
            
            fprintf('Coupled metrics computation complete (%.2f seconds)\n', obj.computationTime);
        end
        
        function [distance, angle] = computeInterTeamCentroidVector(obj, homePos, awayPos)
            % Compute inter-team centroid vector
            %
            % This implements the "field stretch" and "pressure direction" metrics
            % from the GPS-TDA framework
            %
            % Inputs:
            %   homePos - [n_players, 2] home team positions
            %   awayPos - [n_players, 2] away team positions
            %
            % Outputs:
            %   distance - Magnitude of inter-team centroid vector (field stretch)
            %   angle    - Direction of vector in radians (pressure direction)
            
            % Calculate team centroids
            homeCentroid = mean(homePos, 1);
            awayCentroid = mean(awayPos, 1);
            
            % Compute inter-team vector
            interTeamVector = homeCentroid - awayCentroid;
            
            % Extract distance (field stretch) and angle (pressure direction)
            distance = norm(interTeamVector);
            angle = atan2(interTeamVector(2), interTeamVector(1));
        end
        
        function [homeArea, awayArea, areaRatio, shapeDifference] = computeTeamShapeCoupling(obj, homePos, awayPos)
            % Compute team shape coupling metrics
            %
            % This implements the team shape coupling analysis from the GPS-TDA framework
            % including area ratios and shape differences
            %
            % Inputs:
            %   homePos - [n_players, 2] home team positions
            %   awayPos - [n_players, 2] away team positions
            %
            % Outputs:
            %   homeArea        - Convex hull area of home team
            %   awayArea        - Convex hull area of away team
            %   areaRatio       - Home area / Away area
            %   shapeDifference - Difference in shape compactness
            
            % Calculate convex hull areas
            homeArea = obj.computeConvexHullArea(homePos);
            awayArea = obj.computeConvexHullArea(awayPos);
            
            % Calculate area ratio (avoid division by zero)
            if awayArea > 0
                areaRatio = homeArea / awayArea;
            else
                areaRatio = NaN;
            end
            
            % Calculate shape difference (compactness difference)
            homeCompactness = obj.computeShapeCompactness(homePos);
            awayCompactness = obj.computeShapeCompactness(awayPos);
            shapeDifference = homeCompactness - awayCompactness;
        end
        
        function [homeNOD, awayNOD] = computeNearestOpponentDistance(obj, homePos, awayPos)
            % Compute Nearest Opponent Distance (NOD) for both teams
            %
            % This implements the NOD analysis from the GPS-TDA framework
            % which characterizes marking schemes and defensive organization
            %
            % Inputs:
            %   homePos - [n_players, 2] home team positions
            %   awayPos - [n_players, 2] away team positions
            %
            % Outputs:
            %   homeNOD - [n_home_players, 1] NOD for each home player
            %   awayNOD - [n_away_players, 1] NOD for each away player
            
            % Calculate pairwise distances between teams
            distances = pdist2(homePos, awayPos);
            
            % Find nearest opponent for each home player
            homeNOD = min(distances, [], 2);
            
            % Find nearest opponent for each away player
            awayNOD = min(distances, [], 1)';
        end
        
        function area = computeConvexHullArea(obj, positions)
            % Compute convex hull area of player positions
            %
            % Inputs:
            %   positions - [n_players, 2] player positions
            %
            % Outputs:
            %   area - Area of convex hull
            
            if size(positions, 1) < 3
                area = 0;
                return;
            end
            
            try
                % Compute convex hull
                k = convhull(positions(:, 1), positions(:, 2));
                area = polyarea(positions(k, 1), positions(k, 2));
            catch
                area = NaN;
            end
        end
        
        function compactness = computeShapeCompactness(obj, positions)
            % Compute shape compactness metric
            %
            % Compactness = Area / Perimeter^2 (normalized)
            % Higher values indicate more compact formations
            %
            % Inputs:
            %   positions - [n_players, 2] player positions
            %
            % Outputs:
            %   compactness - Shape compactness metric
            
            if size(positions, 1) < 3
                compactness = 0;
                return;
            end
            
            try
                % Compute convex hull
                k = convhull(positions(:, 1), positions(:, 2));
                hullPositions = positions(k, :);
                
                % Calculate area
                area = polyarea(hullPositions(:, 1), hullPositions(:, 2));
                
                % Calculate perimeter
                perimeter = 0;
                for i = 1:size(hullPositions, 1)-1
                    perimeter = perimeter + norm(hullPositions(i+1, :) - hullPositions(i, :));
                end
                perimeter = perimeter + norm(hullPositions(1, :) - hullPositions(end, :));
                
                % Calculate compactness (normalized)
                if perimeter > 0
                    compactness = 4 * pi * area / (perimeter^2);
                else
                    compactness = 0;
                end
            catch
                compactness = NaN;
            end
        end
        
        function obj = removeOutliers(obj)
            % Remove outliers from computed metrics
            %
            % Uses statistical outlier detection to clean the data
            
            if ~obj.analysisComplete
                return;
            end
            
            fprintf('Removing outliers from coupled metrics...\n');
            
            % Define metrics to clean
            metricsToClean = {'InterTeamDistance', 'TeamAreaRatio', 'HomeMeanNOD', 'AwayMeanNOD'};
            
            for i = 1:length(metricsToClean)
                metric = metricsToClean{i};
                values = obj.coupledMetrics.(metric);
                validValues = ~isnan(values);
                
                if sum(validValues) > 10
                    % Calculate outlier threshold
                    meanVal = mean(values(validValues));
                    stdVal = std(values(validValues));
                    threshold = obj.outlierThreshold * stdVal;
                    
                    % Identify outliers
                    outliers = abs(values - meanVal) > threshold;
                    
                    % Replace outliers with NaN
                    obj.coupledMetrics.(metric)(outliers) = NaN;
                    
                    fprintf('  %s: Removed %d outliers\n', metric, sum(outliers));
                end
            end
        end
        
        function visualizeCoupledMetrics(obj)
            % Create comprehensive visualization of coupled metrics
            %
            % Generates publication-quality plots of all coupled dynamics
            
            if ~obj.analysisComplete
                error('Analysis not complete. Run computeCoupledMetrics first.');
            end
            
            fprintf('Creating coupled metrics visualizations...\n');
            
            % Create main figure
            figure('Position', [100, 100, 1600, 1200]);
            
            % Plot 1: Inter-Team Centroid Vector
            subplot(3, 3, 1);
            plot(obj.timestamps, obj.coupledMetrics.InterTeamDistance, 'b-', 'LineWidth', 2);
            xlabel('Time (s)'); ylabel('Distance (m)');
            title('Inter-Team Distance (Field Stretch)');
            grid on;
            
            subplot(3, 3, 2);
            plot(obj.timestamps, rad2deg(obj.coupledMetrics.InterTeamAngle), 'r-', 'LineWidth', 2);
            xlabel('Time (s)'); ylabel('Angle (degrees)');
            title('Pressure Direction');
            grid on;
            
            % Plot 2: Team Shape Coupling
            subplot(3, 3, 3);
            plot(obj.timestamps, obj.coupledMetrics.HomeTeamArea, 'b-', 'LineWidth', 2);
            hold on;
            plot(obj.timestamps, obj.coupledMetrics.AwayTeamArea, 'r-', 'LineWidth', 2);
            xlabel('Time (s)'); ylabel('Area (m²)');
            title('Team Convex Hull Areas');
            legend('Home', 'Away', 'Location', 'best');
            grid on;
            
            subplot(3, 3, 4);
            plot(obj.timestamps, obj.coupledMetrics.TeamAreaRatio, 'g-', 'LineWidth', 2);
            xlabel('Time (s)'); ylabel('Ratio');
            title('Team Area Ratio (Home/Away)');
            yline(1, 'k--', 'LineWidth', 1);
            grid on;
            
            subplot(3, 3, 5);
            plot(obj.timestamps, obj.coupledMetrics.ShapeDifference, 'm-', 'LineWidth', 2);
            xlabel('Time (s)'); ylabel('Compactness Difference');
            title('Shape Difference (Home - Away)');
            yline(0, 'k--', 'LineWidth', 1);
            grid on;
            
            % Plot 3: Nearest Opponent Distance
            subplot(3, 3, 6);
            plot(obj.timestamps, obj.coupledMetrics.HomeMeanNOD, 'b-', 'LineWidth', 2);
            hold on;
            plot(obj.timestamps, obj.coupledMetrics.AwayMeanNOD, 'r-', 'LineWidth', 2);
            xlabel('Time (s)'); ylabel('Distance (m)');
            title('Mean Nearest Opponent Distance');
            legend('Home', 'Away', 'Location', 'best');
            grid on;
            
            subplot(3, 3, 7);
            plot(obj.timestamps, obj.coupledMetrics.HomeStdNOD, 'b-', 'LineWidth', 2);
            hold on;
            plot(obj.timestamps, obj.coupledMetrics.AwayStdNOD, 'r-', 'LineWidth', 2);
            xlabel('Time (s)'); ylabel('Standard Deviation (m)');
            title('NOD Variability');
            legend('Home', 'Away', 'Location', 'best');
            grid on;
            
            % Plot 4: Combined Analysis
            subplot(3, 3, 8);
            yyaxis left;
            plot(obj.timestamps, obj.coupledMetrics.InterTeamDistance, 'b-', 'LineWidth', 2);
            ylabel('Inter-Team Distance (m)');
            yyaxis right;
            plot(obj.timestamps, obj.coupledMetrics.TeamAreaRatio, 'r-', 'LineWidth', 2);
            ylabel('Area Ratio');
            xlabel('Time (s)');
            title('Coupled Dynamics');
            grid on;
            
            % Plot 5: Summary Statistics
            subplot(3, 3, 9);
            % Create summary text
            summaryText = {
                sprintf('Analysis Summary:');
                sprintf('Time Points: %d', height(obj.coupledMetrics));
                sprintf('Duration: %.1f s', max(obj.timestamps) - min(obj.timestamps));
                sprintf('Mean Inter-Team Dist: %.1f m', nanmean(obj.coupledMetrics.InterTeamDistance));
                sprintf('Mean Area Ratio: %.2f', nanmean(obj.coupledMetrics.TeamAreaRatio));
                sprintf('Mean Home NOD: %.1f m', nanmean(obj.coupledMetrics.HomeMeanNOD));
                sprintf('Mean Away NOD: %.1f m', nanmean(obj.coupledMetrics.AwayMeanNOD));
                sprintf('Computation Time: %.2f s', obj.computationTime);
            };
            
            text(0.1, 0.9, summaryText, 'FontSize', 10, 'VerticalAlignment', 'top');
            axis off;
            
            sgtitle('Coupled Collective Variables Analysis', 'FontSize', 16, 'FontWeight', 'bold');
            
            fprintf('Coupled metrics visualization complete\n');
        end
        
        function exportResults(obj, outputDir)
            % Export analysis results to files
            %
            % Inputs:
            %   outputDir - Directory to save results
            
            if ~obj.analysisComplete
                error('Analysis not complete. Run computeCoupledMetrics first.');
            end
            
            if ~exist(outputDir, 'dir')
                mkdir(outputDir);
            end
            
            fprintf('Exporting coupled metrics results to: %s\n', outputDir);
            
            % Export metrics table
            writetable(obj.coupledMetrics, fullfile(outputDir, 'coupled_metrics.csv'));
            
            % Export summary statistics
            summaryStats = obj.computeSummaryStatistics();
            writetable(summaryStats, fullfile(outputDir, 'summary_statistics.csv'));
            
            % Save MATLAB data
            save(fullfile(outputDir, 'coupled_analysis.mat'), 'obj');
            
            fprintf('Results exported successfully\n');
        end
        
        function summaryStats = computeSummaryStatistics(obj)
            % Compute summary statistics for all metrics
            
            if ~obj.analysisComplete
                error('Analysis not complete. Run computeCoupledMetrics first.');
            end
            
            % Define metrics to summarize
            metrics = {'InterTeamDistance', 'InterTeamAngle', 'HomeTeamArea', 'AwayTeamArea', ...
                      'TeamAreaRatio', 'ShapeDifference', 'HomeMeanNOD', 'AwayMeanNOD', ...
                      'HomeStdNOD', 'AwayStdNOD'};
            
            % Initialize summary table
            summaryStats = table('Size', [length(metrics), 6], ...
                                'VariableNames', {'Metric', 'Mean', 'Std', 'Min', 'Max', 'ValidPoints'}, ...
                                'VariableTypes', {'string', 'double', 'double', 'double', 'double', 'double'});
            
            % Calculate statistics for each metric
            for i = 1:length(metrics)
                metric = metrics{i};
                values = obj.coupledMetrics.(metric);
                validValues = ~isnan(values);
                
                summaryStats.Metric(i) = metric;
                summaryStats.Mean(i) = mean(values(validValues));
                summaryStats.Std(i) = std(values(validValues));
                summaryStats.Min(i) = min(values(validValues));
                summaryStats.Max(i) = max(values(validValues));
                summaryStats.ValidPoints(i) = sum(validValues);
            end
        end
    end
end
