classdef StateSpaceReconstruction
    % STATESPACERECONSTRUCTION - Implements state space reconstruction for football dynamics
    % 
    % This class implements state space reconstruction using time-delay embedding
    % to create a multi-dimensional map of game dynamics and identify attractor states.
    %
    % Key Features:
    % - State vector construction from coupled collective variables
    % - Time-delay embedding using Takens' theorem
    % - Attractor identification using clustering algorithms
    % - State space visualization and analysis
    %
    % Based on research by:
    % - Takens (1981) - Time-delay embedding theorem
    % - Kantz & Schreiber (2004) - Nonlinear time series analysis
    % - Broomhead & King (1986) - State space reconstruction methods
    
    properties
        % Input data
        coupledMetrics      % Table of coupled collective variables from Step 1
        timestamps          % Vector of timestamps
        
        % State space parameters
        embeddingDimension  % Dimension of time-delay embedding
        timeDelay          % Time delay parameter (τ)
        stateVariables     % Names of variables to include in state vector
        
        % Computed state space
        stateVectors       % [time, dimension] matrix of state vectors
        embeddedVectors    % [time, embedding_dimension] matrix of embedded vectors
        attractorLabels    % Cluster labels for each time point
        
        % Attractor analysis
        attractorStates    % Structure containing attractor characteristics
        transitionMatrix   % Transition probabilities between attractors
        attractorMetrics   % Metrics for each attractor state
        
        % Analysis results
        reconstructionComplete  % Boolean flag
        computationTime         % Time taken for analysis
    end
    
    methods
        function obj = StateSpaceReconstruction(coupledMetrics, timestamps, varargin)
            % Constructor for StateSpaceReconstruction
            %
            % Inputs:
            %   coupledMetrics - Table of coupled collective variables from Step 1
            %   timestamps    - Vector of timestamps
            %   varargin      - Optional parameters (embeddingDimension, timeDelay, etc.)
            
            % Store input data
            obj.coupledMetrics = coupledMetrics;
            obj.timestamps = timestamps;
            
            % Set default parameters
            obj.embeddingDimension = 3; % Default embedding dimension
            obj.timeDelay = 1; % Default time delay (1 time step)
            obj.stateVariables = {'InterTeamDistance', 'TeamAreaRatio', 'HomeMeanNOD', 'AwayMeanNOD'};
            
            % Parse optional parameters
            if nargin > 2
                for i = 1:2:length(varargin)
                    switch lower(varargin{i})
                        case 'embeddingdimension'
                            obj.embeddingDimension = varargin{i+1};
                        case 'timedelay'
                            obj.timeDelay = varargin{i+1};
                        case 'statevariables'
                            obj.stateVariables = varargin{i+1};
                    end
                end
            end
            
            % Initialize computed data
            obj.reconstructionComplete = false;
            obj.computationTime = 0;
            
            fprintf('StateSpaceReconstruction initialized\n');
            fprintf('  Time points: %d\n', height(coupledMetrics));
            fprintf('  Embedding dimension: %d\n', obj.embeddingDimension);
            fprintf('  Time delay: %d\n', obj.timeDelay);
            fprintf('  State variables: %s\n', strjoin(obj.stateVariables, ', '));
        end
        
        function obj = reconstructStateSpace(obj)
            % Reconstruct state space using time-delay embedding
            %
            % This method implements the core state space reconstruction
            % as described in the GPS-TDA framework
            
            fprintf('Reconstructing state space...\n');
            tic;
            
            % Step 1: Construct state vectors
            obj = obj.constructStateVectors();
            
            % Step 2: Apply time-delay embedding
            obj = obj.applyTimeDelayEmbedding();
            
            % Step 3: Identify attractor states
            obj = obj.identifyAttractorStates();
            
            % Step 4: Analyze attractor characteristics
            obj = obj.analyzeAttractorCharacteristics();
            
            % Step 5: Compute transition matrix
            obj = obj.computeTransitionMatrix();
            
            % Mark reconstruction as complete
            obj.reconstructionComplete = true;
            obj.computationTime = toc;
            
            fprintf('State space reconstruction complete (%.2f seconds)\n', obj.computationTime);
        end
        
        function obj = constructStateVectors(obj)
            % Construct state vectors from coupled collective variables
            %
            % Creates state vectors: State(t) = [InterTeamDistance, TeamAreaRatio, MeanNOD, ...]
            
            fprintf('  Constructing state vectors...\n');
            
            nTimes = height(obj.coupledMetrics);
            nVars = length(obj.stateVariables);
            
            % Initialize state vectors matrix
            obj.stateVectors = zeros(nTimes, nVars);
            
            % Extract variables and normalize
            for i = 1:nVars
                varName = obj.stateVariables{i};
                if ismember(varName, obj.coupledMetrics.Properties.VariableNames)
                    values = obj.coupledMetrics.(varName);
                    
                    % Remove NaN values and normalize
                    validValues = ~isnan(values);
                    if sum(validValues) > 0
                        % Z-score normalization
                        meanVal = mean(values(validValues));
                        stdVal = std(values(validValues));
                        if stdVal > 0
                            obj.stateVectors(:, i) = (values - meanVal) / stdVal;
                        else
                            obj.stateVectors(:, i) = zeros(size(values));
                        end
                    else
                        obj.stateVectors(:, i) = NaN(size(values));
                    end
                else
                    warning('Variable %s not found in coupled metrics', varName);
                    obj.stateVectors(:, i) = NaN(nTimes, 1);
                end
            end
            
            fprintf('    State vectors constructed: %d x %d\n', size(obj.stateVectors, 1), size(obj.stateVectors, 2));
        end
        
        function obj = applyTimeDelayEmbedding(obj)
            % Apply time-delay embedding using Takens' theorem
            %
            % Creates embedded vectors: [State(t), State(t-τ), State(t-2τ), ...]
            
            fprintf('  Applying time-delay embedding...\n');
            
            nTimes = size(obj.stateVectors, 1);
            nVars = size(obj.stateVectors, 2);
            
            % Calculate embedding parameters
            embeddingLength = obj.embeddingDimension * nVars;
            maxTimeIndex = nTimes - (obj.embeddingDimension - 1) * obj.timeDelay;
            
            % Initialize embedded vectors matrix
            obj.embeddedVectors = zeros(maxTimeIndex, embeddingLength);
            
            % Create embedded vectors
            for t = 1:maxTimeIndex
                embeddedVector = [];
                
                % Concatenate state vectors at different time delays
                for d = 0:obj.embeddingDimension-1
                    timeIndex = t + d * obj.timeDelay;
                    if timeIndex <= nTimes
                        embeddedVector = [embeddedVector, obj.stateVectors(timeIndex, :)];
                    else
                        embeddedVector = [embeddedVector, NaN(1, nVars)];
                    end
                end
                
                obj.embeddedVectors(t, :) = embeddedVector;
            end
            
            % Remove rows with NaN values
            validRows = ~any(isnan(obj.embeddedVectors), 2);
            obj.embeddedVectors = obj.embeddedVectors(validRows, :);
            
            fprintf('    Embedded vectors created: %d x %d\n', size(obj.embeddedVectors, 1), size(obj.embeddedVectors, 2));
        end
        
        function obj = identifyAttractorStates(obj)
            % Identify attractor states using clustering algorithms
            %
            % Uses k-means clustering to identify stable patterns in state space
            
            fprintf('  Identifying attractor states...\n');
            
            if isempty(obj.embeddedVectors)
                error('No embedded vectors available. Run applyTimeDelayEmbedding first.');
            end
            
            % Determine optimal number of clusters using elbow method
            maxClusters = min(10, floor(size(obj.embeddedVectors, 1) / 20));
            if maxClusters < 2
                maxClusters = 2;
            end
            
            % Calculate within-cluster sum of squares for different k values
            wcss = zeros(maxClusters, 1);
            for k = 1:maxClusters
                [~, ~, sumd] = kmeans(obj.embeddedVectors, k, 'Replicates', 5);
                wcss(k) = sum(sumd);
            end
            
            % Find elbow point (simplified method)
            if maxClusters >= 3
                % Calculate second derivative to find elbow
                diff1 = diff(wcss);
                diff2 = diff(diff1);
                [~, optimalK] = max(diff2);
                optimalK = optimalK + 2; % Adjust for indexing
            else
                optimalK = 2;
            end
            
            % Perform k-means clustering
            [clusterLabels, centroids] = kmeans(obj.embeddedVectors, optimalK, 'Replicates', 10);
            
            % Store results
            obj.attractorLabels = clusterLabels;
            obj.attractorStates.nClusters = optimalK;
            obj.attractorStates.centroids = centroids;
            obj.attractorStates.wcss = wcss;
            
            fprintf('    Identified %d attractor states\n', optimalK);
        end
        
        function obj = analyzeAttractorCharacteristics(obj)
            % Analyze characteristics of each attractor state
            
            fprintf('  Analyzing attractor characteristics...\n');
            
            if isempty(obj.attractorLabels)
                error('No attractor labels available. Run identifyAttractorStates first.');
            end
            
            nClusters = obj.attractorStates.nClusters;
            
            % Initialize attractor metrics
            obj.attractorMetrics = struct();
            obj.attractorMetrics.frequency = zeros(nClusters, 1);
            obj.attractorMetrics.duration = zeros(nClusters, 1);
            obj.attractorMetrics.stability = zeros(nClusters, 1);
            obj.attractorMetrics.transitions = zeros(nClusters, 1);
            
            % Analyze each attractor
            for i = 1:nClusters
                clusterIndices = find(obj.attractorLabels == i);
                
                % Calculate frequency
                obj.attractorMetrics.frequency(i) = length(clusterIndices) / length(obj.attractorLabels);
                
                % Calculate average duration
                if ~isempty(clusterIndices)
                    % Find consecutive sequences
                    diffIndices = diff(clusterIndices);
                    breaks = find(diffIndices > 1);
                    
                    if isempty(breaks)
                        durations = length(clusterIndices);
                    else
                        durations = [breaks(1); diff(breaks); length(clusterIndices) - breaks(end)];
                    end
                    
                    obj.attractorMetrics.duration(i) = mean(durations);
                end
                
                % Calculate stability (inverse of variance in state space)
                if length(clusterIndices) > 1
                    clusterVectors = obj.embeddedVectors(clusterIndices, :);
                    obj.attractorMetrics.stability(i) = 1 / (mean(var(clusterVectors)) + eps);
                else
                    obj.attractorMetrics.stability(i) = 0;
                end
                
                % Count transitions from this attractor
                if i <= nClusters
                    transitions = 0;
                    for j = 1:length(obj.attractorLabels)-1
                        if obj.attractorLabels(j) == i && obj.attractorLabels(j+1) ~= i
                            transitions = transitions + 1;
                        end
                    end
                    obj.attractorMetrics.transitions(i) = transitions;
                end
            end
            
            fprintf('    Attractor characteristics analyzed\n');
        end
        
        function obj = computeTransitionMatrix(obj)
            % Compute transition matrix between attractor states
            
            fprintf('  Computing transition matrix...\n');
            
            if isempty(obj.attractorLabels)
                error('No attractor labels available. Run identifyAttractorStates first.');
            end
            
            nClusters = obj.attractorStates.nClusters;
            obj.transitionMatrix = zeros(nClusters, nClusters);
            
            % Count transitions
            for i = 1:length(obj.attractorLabels)-1
                currentState = obj.attractorLabels(i);
                nextState = obj.attractorLabels(i+1);
                
                if currentState > 0 && nextState > 0
                    obj.transitionMatrix(currentState, nextState) = obj.transitionMatrix(currentState, nextState) + 1;
                end
            end
            
            % Normalize rows to get probabilities
            rowSums = sum(obj.transitionMatrix, 2);
            for i = 1:nClusters
                if rowSums(i) > 0
                    obj.transitionMatrix(i, :) = obj.transitionMatrix(i, :) / rowSums(i);
                end
            end
            
            fprintf('    Transition matrix computed: %d x %d\n', size(obj.transitionMatrix, 1), size(obj.transitionMatrix, 2));
        end
        
        function visualizeStateSpace(obj)
            % Create comprehensive visualization of state space reconstruction
            
            if ~obj.reconstructionComplete
                error('State space reconstruction not complete. Run reconstructStateSpace first.');
            end
            
            fprintf('Creating state space visualizations...\n');
            
            % Create main figure
            figure('Position', [100, 100, 1600, 1200]);
            
            % Plot 1: State vectors over time
            subplot(3, 3, 1);
            for i = 1:size(obj.stateVectors, 2)
                plot(obj.timestamps(1:size(obj.stateVectors, 1)), obj.stateVectors(:, i), 'LineWidth', 1.5);
                hold on;
            end
            xlabel('Time (s)'); ylabel('Normalized Value');
            title('State Vectors Over Time');
            legend(obj.stateVariables, 'Location', 'best');
            grid on;
            
            % Plot 2: 2D state space projection
            subplot(3, 3, 2);
            if size(obj.stateVectors, 2) >= 2
                % Ensure attractor labels match state vectors length
                nStateVectors = size(obj.stateVectors, 1);
                nAttractorLabels = length(obj.attractorLabels);
                
                if nStateVectors == nAttractorLabels
                    scatter(obj.stateVectors(:, 1), obj.stateVectors(:, 2), 50, obj.attractorLabels, 'filled');
                else
                    % Use only the matching portion
                    minLength = min(nStateVectors, nAttractorLabels);
                    scatter(obj.stateVectors(1:minLength, 1), obj.stateVectors(1:minLength, 2), 50, obj.attractorLabels(1:minLength), 'filled');
                end
                xlabel(obj.stateVariables{1});
                ylabel(obj.stateVariables{2});
                title('2D State Space Projection');
                colorbar;
                grid on;
            end
            
            % Plot 3: Attractor evolution over time
            subplot(3, 3, 3);
            plot(obj.timestamps(1:length(obj.attractorLabels)), obj.attractorLabels, 'b-', 'LineWidth', 2);
            xlabel('Time (s)'); ylabel('Attractor State');
            title('Attractor Evolution');
            ylim([0.5, obj.attractorStates.nClusters + 0.5]);
            grid on;
            
            % Plot 4: Attractor frequency
            subplot(3, 3, 4);
            bar(1:obj.attractorStates.nClusters, obj.attractorMetrics.frequency);
            xlabel('Attractor State'); ylabel('Frequency');
            title('Attractor Frequency');
            grid on;
            
            % Plot 5: Attractor duration
            subplot(3, 3, 5);
            bar(1:obj.attractorStates.nClusters, obj.attractorMetrics.duration);
            xlabel('Attractor State'); ylabel('Average Duration (time steps)');
            title('Attractor Duration');
            grid on;
            
            % Plot 6: Attractor stability
            subplot(3, 3, 6);
            bar(1:obj.attractorStates.nClusters, obj.attractorMetrics.stability);
            xlabel('Attractor State'); ylabel('Stability');
            title('Attractor Stability');
            grid on;
            
            % Plot 7: Transition matrix heatmap
            subplot(3, 3, 7);
            imagesc(obj.transitionMatrix);
            colorbar;
            xlabel('To Attractor'); ylabel('From Attractor');
            title('Transition Matrix');
            xticks(1:obj.attractorStates.nClusters);
            yticks(1:obj.attractorStates.nClusters);
            
            % Plot 8: 3D state space (if available)
            subplot(3, 3, 8);
            if size(obj.stateVectors, 2) >= 3
                % Ensure attractor labels match state vectors length
                nStateVectors = size(obj.stateVectors, 1);
                nAttractorLabels = length(obj.attractorLabels);
                
                if nStateVectors == nAttractorLabels
                    scatter3(obj.stateVectors(:, 1), obj.stateVectors(:, 2), obj.stateVectors(:, 3), ...
                            50, obj.attractorLabels, 'filled');
                else
                    % Use only the matching portion
                    minLength = min(nStateVectors, nAttractorLabels);
                    scatter3(obj.stateVectors(1:minLength, 1), obj.stateVectors(1:minLength, 2), obj.stateVectors(1:minLength, 3), ...
                            50, obj.attractorLabels(1:minLength), 'filled');
                end
                xlabel(obj.stateVariables{1});
                ylabel(obj.stateVariables{2});
                zlabel(obj.stateVariables{3});
                title('3D State Space');
                colorbar;
            else
                text(0.5, 0.5, '3D visualization\nrequires 3+ variables', ...
                     'HorizontalAlignment', 'center', 'FontSize', 12);
                title('3D State Space');
            end
            
            % Plot 9: Summary statistics
            subplot(3, 3, 9);
            summaryText = {
                sprintf('State Space Summary:');
                sprintf('Embedding Dim: %d', obj.embeddingDimension);
                sprintf('Time Delay: %d', obj.timeDelay);
                sprintf('Attractors: %d', obj.attractorStates.nClusters);
                sprintf('State Vectors: %d', size(obj.stateVectors, 1));
                sprintf('Embedded Vectors: %d', size(obj.embeddedVectors, 1));
                sprintf('Computation Time: %.2f s', obj.computationTime);
            };
            
            text(0.1, 0.9, summaryText, 'FontSize', 10, 'VerticalAlignment', 'top');
            axis off;
            
            sgtitle('State Space Reconstruction Analysis', 'FontSize', 16, 'FontWeight', 'bold');
            
            fprintf('State space visualization complete\n');
        end
        
        function exportResults(obj, outputDir)
            % Export state space reconstruction results
            
            if ~obj.reconstructionComplete
                error('State space reconstruction not complete. Run reconstructStateSpace first.');
            end
            
            if ~exist(outputDir, 'dir')
                mkdir(outputDir);
            end
            
            fprintf('Exporting state space results to: %s\n', outputDir);
            
            % Export state vectors
            stateTable = array2table(obj.stateVectors, 'VariableNames', obj.stateVariables);
            stateTable.TimeStep = (1:size(obj.stateVectors, 1))';
            stateTable.Timestamp = obj.timestamps(1:size(obj.stateVectors, 1));
            
            % Handle length mismatch between state vectors and attractor labels
            nStateVectors = size(obj.stateVectors, 1);
            nAttractorLabels = length(obj.attractorLabels);
            
            if nStateVectors == nAttractorLabels
                stateTable.AttractorLabel = obj.attractorLabels;
            else
                % Pad or truncate attractor labels to match state vectors
                if nStateVectors > nAttractorLabels
                    % Pad with NaN
                    paddedLabels = [obj.attractorLabels; NaN(nStateVectors - nAttractorLabels, 1)];
                else
                    % Truncate
                    paddedLabels = obj.attractorLabels(1:nStateVectors);
                end
                stateTable.AttractorLabel = paddedLabels;
            end
            writetable(stateTable, fullfile(outputDir, 'state_vectors.csv'));
            
            % Export attractor metrics
            attractorTable = table((1:obj.attractorStates.nClusters)', ...
                                  obj.attractorMetrics.frequency, ...
                                  obj.attractorMetrics.duration, ...
                                  obj.attractorMetrics.stability, ...
                                  obj.attractorMetrics.transitions, ...
                                  'VariableNames', {'AttractorID', 'Frequency', 'Duration', 'Stability', 'Transitions'});
            writetable(attractorTable, fullfile(outputDir, 'attractor_metrics.csv'));
            
            % Export transition matrix
            transitionTable = array2table(obj.transitionMatrix, ...
                                         'VariableNames', arrayfun(@(x) sprintf('To_%d', x), 1:obj.attractorStates.nClusters, 'UniformOutput', false), ...
                                         'RowNames', arrayfun(@(x) sprintf('From_%d', x), 1:obj.attractorStates.nClusters, 'UniformOutput', false));
            writetable(transitionTable, fullfile(outputDir, 'transition_matrix.csv'), 'WriteRowNames', true);
            
            % Save MATLAB data
            save(fullfile(outputDir, 'state_space_analysis.mat'), 'obj');
            
            fprintf('State space results exported successfully\n');
        end
    end
end
