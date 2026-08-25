classdef QuantumDotAttractorModel
    % QUANTUMDOTATTRACTORMODEL - Models attractor transitions using Gillespie's algorithm
    % 
    % This class implements Gillespie's stochastic simulation algorithm to model
    % attractor state transitions in football dynamics, drawing parallels to
    % quantum dot optical properties with long-lived and short-lived states.
    %
    % Key Features:
    % - Gillespie's algorithm for stochastic transition modeling
    % - Quantum dot-inspired state classification (long-lived vs short-lived)
    % - Transition rate analysis and state lifetime modeling
    % - Comparison with empirical attractor data
    %
    % Based on:
    % - Gillespie (1976) - Exact stochastic simulation of coupled chemical reactions
    % - Quantum dot literature - Long-lived and short-lived state dynamics
    % - Football TDA research - Attractor state transitions
    
    properties
        % Input data
        empiricalTransitionMatrix  % Empirical transition matrix from Step 2
        empiricalAttractorMetrics  % Empirical attractor metrics
        timestamps                % Time vector
        
        % Model parameters
        transitionRates          % Transition rate matrix (per time step)
        stateLifetimes          % Expected lifetimes for each state
        stateClassification     % Classification of states (long-lived vs short-lived)
        
        % Simulation results
        simulatedTrajectory     % Simulated attractor trajectory
        simulatedLifetimes      % Simulated state lifetimes
        simulationParameters    % Parameters used in simulation
        
        % Analysis results
        modelValidation         % Comparison with empirical data
        quantumDotAnalogy      % Quantum dot-inspired analysis
    end
    
    methods
        function obj = QuantumDotAttractorModel(empiricalTransitionMatrix, empiricalAttractorMetrics, timestamps)
            % Constructor for QuantumDotAttractorModel
            
            % Store input data
            obj.empiricalTransitionMatrix = empiricalTransitionMatrix;
            obj.empiricalAttractorMetrics = empiricalAttractorMetrics;
            obj.timestamps = timestamps;
            
            % Initialize model parameters
            obj = obj.initializeModelParameters();
            
            fprintf('QuantumDotAttractorModel initialized\n');
            fprintf('  Number of states: %d\n', size(empiricalTransitionMatrix, 1));
            fprintf('  Time points: %d\n', length(timestamps));
        end
        
        function obj = initializeModelParameters(obj)
            % Initialize model parameters from empirical data
            
            nStates = size(obj.empiricalTransitionMatrix, 1);
            
            % Convert transition probabilities to transition rates
            % For Gillespie's algorithm, we need rates (events per unit time)
            obj.transitionRates = zeros(nStates, nStates);
            
            for i = 1:nStates
                for j = 1:nStates
                    if i ~= j
                        % Convert probability to rate using: rate = -log(1 - prob) / dt
                        % where dt is the time step (assuming 0.1s for 10Hz data)
                        dt = 0.1; % seconds
                        prob = obj.empiricalTransitionMatrix(i, j);
                        if prob > 0
                            obj.transitionRates(i, j) = -log(1 - prob) / dt;
                        end
                    end
                end
            end
            
            % Calculate expected state lifetimes
            obj.stateLifetimes = zeros(nStates, 1);
            for i = 1:nStates
                % Lifetime = 1 / (sum of outgoing rates)
                totalOutgoingRate = sum(obj.transitionRates(i, :));
                if totalOutgoingRate > 0
                    obj.stateLifetimes(i) = 1 / totalOutgoingRate;
                else
                    obj.stateLifetimes(i) = Inf; % Stable state
                end
            end
            
            % Classify states as long-lived or short-lived (quantum dot analogy)
            obj.stateClassification = obj.classifyStates();
            
            fprintf('Model parameters initialized:\n');
            for i = 1:nStates
                fprintf('  State %d: Lifetime = %.2f s, Classification = %s\n', ...
                    i, obj.stateLifetimes(i), obj.stateClassification{i});
            end
        end
        
        function classification = classifyStates(obj)
            % Classify states as long-lived or short-lived (quantum dot analogy)
            
            nStates = length(obj.stateLifetimes);
            classification = cell(nStates, 1);
            
            % Use median lifetime as threshold
            medianLifetime = median(obj.stateLifetimes(obj.stateLifetimes < Inf));
            
            for i = 1:nStates
                if obj.stateLifetimes(i) >= medianLifetime
                    classification{i} = 'Long-lived';
                else
                    classification{i} = 'Short-lived';
                end
            end
        end
        
        function obj = simulateGillespie(obj, simulationTime, initialState)
            % Simulate attractor transitions using Gillespie's algorithm
            
            if nargin < 2
                simulationTime = max(obj.timestamps) - min(obj.timestamps);
            end
            if nargin < 3
                initialState = 1; % Start in state 1
            end
            
            fprintf('Running Gillespie simulation...\n');
            fprintf('  Simulation time: %.1f seconds\n', simulationTime);
            fprintf('  Initial state: %d\n', initialState);
            
            % Initialize simulation
            currentState = initialState;
            currentTime = 0;
            trajectory = [];
            lifetimes = [];
            
            % Gillespie's algorithm
            while currentTime < simulationTime
                % Calculate total transition rate from current state
                totalRate = sum(obj.transitionRates(currentState, :));
                
                if totalRate == 0
                    % No transitions possible, stay in current state
                    trajectory = [trajectory; currentTime, currentState];
                    break;
                end
                
                % Generate exponentially distributed time to next transition
                tau = -log(rand()) / totalRate;
                
                % Update time
                currentTime = currentTime + tau;
                
                % Record current state duration
                if ~isempty(trajectory)
                    stateDuration = currentTime - trajectory(end, 1);
                    lifetimes = [lifetimes; currentState, stateDuration];
                end
                
                % Record state at current time
                trajectory = [trajectory; currentTime, currentState];
                
                % Choose next state based on transition probabilities
                transitionProbs = obj.transitionRates(currentState, :) / totalRate;
                cumulativeProbs = cumsum(transitionProbs);
                randomValue = rand();
                
                nextState = find(cumulativeProbs >= randomValue, 1, 'first');
                if isempty(nextState)
                    nextState = currentState; % Stay in current state
                end
                
                currentState = nextState;
            end
            
            % Store simulation results
            obj.simulatedTrajectory = trajectory;
            obj.simulatedLifetimes = lifetimes;
            obj.simulationParameters.simulationTime = simulationTime;
            obj.simulationParameters.initialState = initialState;
            
            fprintf('Gillespie simulation complete\n');
            fprintf('  Total transitions: %d\n', size(lifetimes, 1));
            fprintf('  Final time: %.2f seconds\n', currentTime);
        end
        
        function obj = validateModel(obj)
            % Validate model against empirical data
            
            if isempty(obj.simulatedTrajectory)
                error('No simulation data available. Run simulateGillespie first.');
            end
            
            fprintf('Validating model against empirical data...\n');
            
            % Initialize validation structure
            obj.modelValidation = struct();
            
            % 1. Compare state frequencies
            empiricalFreq = obj.empiricalAttractorMetrics.frequency;
            simulatedFreq = obj.calculateSimulatedFrequencies();
            
            obj.modelValidation.frequencyCorrelation = corrcoef(empiricalFreq, simulatedFreq);
            obj.modelValidation.frequencyRMSE = sqrt(mean((empiricalFreq - simulatedFreq).^2));
            
            % 2. Compare state lifetimes
            empiricalLifetimes = obj.empiricalAttractorMetrics.duration * 0.1; % Convert to seconds
            simulatedLifetimes = obj.calculateSimulatedLifetimes();
            
            obj.modelValidation.lifetimeCorrelation = corrcoef(empiricalLifetimes, simulatedLifetimes);
            obj.modelValidation.lifetimeRMSE = sqrt(mean((empiricalLifetimes - simulatedLifetimes).^2));
            
            % 3. Compare transition patterns
            empiricalTransitions = obj.empiricalTransitionMatrix;
            simulatedTransitions = obj.calculateSimulatedTransitionMatrix();
            
            obj.modelValidation.transitionCorrelation = corrcoef(empiricalTransitions(:), simulatedTransitions(:));
            obj.modelValidation.transitionRMSE = sqrt(mean((empiricalTransitions(:) - simulatedTransitions(:)).^2));
            
            fprintf('Model validation complete:\n');
            fprintf('  Frequency correlation: %.3f\n', obj.modelValidation.frequencyCorrelation(1,2));
            fprintf('  Lifetime correlation: %.3f\n', obj.modelValidation.lifetimeCorrelation(1,2));
            fprintf('  Transition correlation: %.3f\n', obj.modelValidation.transitionCorrelation(1,2));
        end
        
        function frequencies = calculateSimulatedFrequencies(obj)
            % Calculate state frequencies from simulated trajectory
            
            nStates = size(obj.empiricalTransitionMatrix, 1);
            frequencies = zeros(nStates, 1);
            
            if ~isempty(obj.simulatedTrajectory)
                for i = 1:nStates
                    stateIndices = obj.simulatedTrajectory(:, 2) == i;
                    frequencies(i) = sum(stateIndices) / length(obj.simulatedTrajectory);
                end
            end
        end
        
        function lifetimes = calculateSimulatedLifetimes(obj)
            % Calculate average lifetimes from simulated data
            
            nStates = size(obj.empiricalTransitionMatrix, 1);
            lifetimes = zeros(nStates, 1);
            
            if ~isempty(obj.simulatedLifetimes)
                for i = 1:nStates
                    stateLifetimes = obj.simulatedLifetimes(obj.simulatedLifetimes(:, 1) == i, 2);
                    if ~isempty(stateLifetimes)
                        lifetimes(i) = mean(stateLifetimes);
                    else
                        lifetimes(i) = 0;
                    end
                end
            end
        end
        
        function transitionMatrix = calculateSimulatedTransitionMatrix(obj)
            % Calculate transition matrix from simulated trajectory
            
            nStates = size(obj.empiricalTransitionMatrix, 1);
            transitionMatrix = zeros(nStates, nStates);
            
            if ~isempty(obj.simulatedTrajectory) && size(obj.simulatedTrajectory, 1) > 1
                for i = 1:size(obj.simulatedTrajectory, 1)-1
                    currentState = obj.simulatedTrajectory(i, 2);
                    nextState = obj.simulatedTrajectory(i+1, 2);
                    transitionMatrix(currentState, nextState) = transitionMatrix(currentState, nextState) + 1;
                end
                
                % Normalize rows
                for i = 1:nStates
                    rowSum = sum(transitionMatrix(i, :));
                    if rowSum > 0
                        transitionMatrix(i, :) = transitionMatrix(i, :) / rowSum;
                    end
                end
            end
        end
        
        function obj = analyzeQuantumDotAnalogy(obj)
            % Analyze the quantum dot analogy for attractor states
            
            fprintf('Analyzing quantum dot analogy...\n');
            
            obj.quantumDotAnalogy = struct();
            
            % 1. State lifetime distribution
            obj.quantumDotAnalogy.lifetimeDistribution = obj.stateLifetimes;
            obj.quantumDotAnalogy.longLivedStates = find(strcmp(obj.stateClassification, 'Long-lived'));
            obj.quantumDotAnalogy.shortLivedStates = find(strcmp(obj.stateClassification, 'Short-lived'));
            
            % 2. Quantum dot parameters
            % Long-lived states (like slow quantum dot transitions)
            if ~isempty(obj.quantumDotAnalogy.longLivedStates)
                obj.quantumDotAnalogy.averageLongLifetime = mean(obj.stateLifetimes(obj.quantumDotAnalogy.longLivedStates));
                obj.quantumDotAnalogy.longLivedFrequency = sum(obj.empiricalAttractorMetrics.frequency(obj.quantumDotAnalogy.longLivedStates));
            end
            
            % Short-lived states (like fast quantum dot transitions)
            if ~isempty(obj.quantumDotAnalogy.shortLivedStates)
                obj.quantumDotAnalogy.averageShortLifetime = mean(obj.stateLifetimes(obj.quantumDotAnalogy.shortLivedStates));
                obj.quantumDotAnalogy.shortLivedFrequency = sum(obj.empiricalAttractorMetrics.frequency(obj.quantumDotAnalogy.shortLivedStates));
            end
            
            % 3. Quantum dot efficiency (ratio of long-lived to short-lived)
            if isfield(obj.quantumDotAnalogy, 'averageLongLifetime') && isfield(obj.quantumDotAnalogy, 'averageShortLifetime')
                obj.quantumDotAnalogy.lifetimeRatio = obj.quantumDotAnalogy.averageLongLifetime / obj.quantumDotAnalogy.averageShortLifetime;
            end
            
            % 4. Transition dynamics
            obj.quantumDotAnalogy.transitionRates = obj.transitionRates;
            obj.quantumDotAnalogy.totalTransitionRate = sum(obj.transitionRates(:));
            
            fprintf('Quantum dot analogy analysis complete:\n');
            if isfield(obj.quantumDotAnalogy, 'averageLongLifetime')
                fprintf('  Average long-lived lifetime: %.2f s\n', obj.quantumDotAnalogy.averageLongLifetime);
            end
            if isfield(obj.quantumDotAnalogy, 'averageShortLifetime')
                fprintf('  Average short-lived lifetime: %.2f s\n', obj.quantumDotAnalogy.averageShortLifetime);
            end
            if isfield(obj.quantumDotAnalogy, 'lifetimeRatio')
                fprintf('  Lifetime ratio (long/short): %.2f\n', obj.quantumDotAnalogy.lifetimeRatio);
            end
        end
        
        function visualizeQuantumDotModel(obj)
            % Create comprehensive visualization of quantum dot-inspired model
            
            fprintf('Creating quantum dot model visualizations...\n');
            
            % Create main figure
            figure('Position', [100, 100, 1800, 1200]);
            
            % Plot 1: State lifetime distribution
            subplot(3, 4, 1);
            bar(1:length(obj.stateLifetimes), obj.stateLifetimes);
            xlabel('Attractor State'); ylabel('Lifetime (s)');
            title('State Lifetimes (Quantum Dot Analogy)');
            grid on;
            
            % Color bars based on classification
            hold on;
            for i = 1:length(obj.stateLifetimes)
                if strcmp(obj.stateClassification{i}, 'Long-lived')
                    bar(i, obj.stateLifetimes(i), 'FaceColor', 'r', 'FaceAlpha', 0.7);
                else
                    bar(i, obj.stateLifetimes(i), 'FaceColor', 'b', 'FaceAlpha', 0.7);
                end
            end
            legend('Short-lived', 'Long-lived', 'Location', 'best');
            
            % Plot 2: Transition rate matrix
            subplot(3, 4, 2);
            imagesc(obj.transitionRates);
            colorbar;
            xlabel('To State'); ylabel('From State');
            title('Transition Rate Matrix');
            xticks(1:size(obj.transitionRates, 1));
            yticks(1:size(obj.transitionRates, 1));
            
            % Plot 3: Empirical vs Simulated frequencies
            subplot(3, 4, 3);
            if ~isempty(obj.simulatedTrajectory)
                empiricalFreq = obj.empiricalAttractorMetrics.frequency;
                simulatedFreq = obj.calculateSimulatedFrequencies();
                bar([empiricalFreq, simulatedFreq]);
                xlabel('Attractor State'); ylabel('Frequency');
                title('Empirical vs Simulated Frequencies');
                legend('Empirical', 'Simulated', 'Location', 'best');
                grid on;
            end
            
            % Plot 4: Empirical vs Simulated lifetimes
            subplot(3, 4, 4);
            if ~isempty(obj.simulatedTrajectory)
                empiricalLifetimes = obj.empiricalAttractorMetrics.duration * 0.1;
                simulatedLifetimes = obj.calculateSimulatedLifetimes();
                bar([empiricalLifetimes, simulatedLifetimes]);
                xlabel('Attractor State'); ylabel('Lifetime (s)');
                title('Empirical vs Simulated Lifetimes');
                legend('Empirical', 'Simulated', 'Location', 'best');
                grid on;
            end
            
            % Plot 5: Simulated trajectory
            subplot(3, 4, 5);
            if ~isempty(obj.simulatedTrajectory)
                plot(obj.simulatedTrajectory(:, 1), obj.simulatedTrajectory(:, 2), 'b-', 'LineWidth', 2);
                xlabel('Time (s)'); ylabel('Attractor State');
                title('Simulated Attractor Trajectory');
                ylim([0.5, size(obj.empiricalTransitionMatrix, 1) + 0.5]);
                grid on;
            end
            
            % Plot 6: State duration distribution
            subplot(3, 4, 6);
            if ~isempty(obj.simulatedLifetimes)
                histogram(obj.simulatedLifetimes(:, 2), 20);
                xlabel('State Duration (s)'); ylabel('Frequency');
                title('State Duration Distribution');
                grid on;
            end
            
            % Plot 7: Transition matrix comparison
            subplot(3, 4, 7);
            if ~isempty(obj.simulatedTrajectory)
                empiricalTransitions = obj.empiricalTransitionMatrix;
                simulatedTransitions = obj.calculateSimulatedTransitionMatrix();
                scatter(empiricalTransitions(:), simulatedTransitions(:), 100, 'filled');
                xlabel('Empirical Transition Probability');
                ylabel('Simulated Transition Probability');
                title('Transition Matrix Comparison');
                grid on;
                % Add diagonal line
                hold on;
                plot([0, 1], [0, 1], 'r--', 'LineWidth', 2);
            end
            
            % Plot 8: Quantum dot efficiency
            subplot(3, 4, 8);
            if isfield(obj.quantumDotAnalogy, 'lifetimeRatio')
                bar(1, obj.quantumDotAnalogy.lifetimeRatio);
                ylabel('Lifetime Ratio (Long/Short)');
                title('Quantum Dot Efficiency');
                grid on;
            end
            
            % Plot 9: Model validation metrics
            subplot(3, 4, 9);
            if isfield(obj.modelValidation, 'frequencyCorrelation')
                validationMetrics = [obj.modelValidation.frequencyCorrelation(1,2), ...
                                   obj.modelValidation.lifetimeCorrelation(1,2), ...
                                   obj.modelValidation.transitionCorrelation(1,2)];
                bar(validationMetrics);
                xlabel('Validation Metric'); ylabel('Correlation');
                title('Model Validation');
                xticklabels({'Frequency', 'Lifetime', 'Transition'});
                grid on;
            end
            
            % Plot 10: State classification
            subplot(3, 4, 10);
            longLivedCount = sum(strcmp(obj.stateClassification, 'Long-lived'));
            shortLivedCount = sum(strcmp(obj.stateClassification, 'Short-lived'));
            pie([longLivedCount, shortLivedCount], {'Long-lived', 'Short-lived'});
            title('State Classification');
            
            % Plot 11: Transition dynamics
            subplot(3, 4, 11);
            if ~isempty(obj.simulatedTrajectory)
                % Plot state transitions over time
                stateChanges = diff(obj.simulatedTrajectory(:, 2)) ~= 0;
                transitionTimes = obj.simulatedTrajectory(find(stateChanges) + 1, 1);
                plot(transitionTimes, ones(size(transitionTimes)), 'ro', 'MarkerSize', 8);
                xlabel('Time (s)'); ylabel('Transitions');
                title('State Transitions Over Time');
                grid on;
            end
            
            % Plot 12: Analysis summary
            subplot(3, 4, 12);
            summaryText = {
                sprintf('Quantum Dot Model Summary:');
                sprintf('');
                sprintf('States: %d', length(obj.stateLifetimes));
                sprintf('Long-lived: %d', sum(strcmp(obj.stateClassification, 'Long-lived')));
                sprintf('Short-lived: %d', sum(strcmp(obj.stateClassification, 'Short-lived')));
                sprintf('');
            };
            
            % Add quantum dot analogy metrics
            if isfield(obj.quantumDotAnalogy, 'lifetimeRatio')
                summaryText{end+1} = sprintf('Lifetime Ratio: %.2f', obj.quantumDotAnalogy.lifetimeRatio);
            end
            
            summaryText{end+1} = sprintf('');
            
            % Add model validation metrics
            if isfield(obj.modelValidation, 'frequencyCorrelation')
                summaryText{end+1} = sprintf('Model Validation:');
                summaryText{end+1} = sprintf('  Frequency: %.3f', obj.modelValidation.frequencyCorrelation(1,2));
                summaryText{end+1} = sprintf('  Lifetime: %.3f', obj.modelValidation.lifetimeCorrelation(1,2));
                summaryText{end+1} = sprintf('  Transition: %.3f', obj.modelValidation.transitionCorrelation(1,2));
            end
            
            text(0.05, 0.95, summaryText, 'FontSize', 10, 'VerticalAlignment', 'top');
            axis off;
            
            sgtitle('Quantum Dot-Inspired Attractor Model Analysis', 'FontSize', 16, 'FontWeight', 'bold');
            
            fprintf('Quantum dot model visualization complete\n');
        end
        
        function exportResults(obj, outputDir)
            % Export quantum dot model results
            
            if ~exist(outputDir, 'dir')
                mkdir(outputDir);
            end
            
            fprintf('Exporting quantum dot model results to: %s\n', outputDir);
            
            % Export state lifetimes and classification
            stateTable = table((1:length(obj.stateLifetimes))', obj.stateLifetimes, obj.stateClassification, ...
                             'VariableNames', {'State', 'Lifetime', 'Classification'});
            writetable(stateTable, fullfile(outputDir, 'quantum_dot_states.csv'));
            
            % Export transition rates
            rateTable = array2table(obj.transitionRates, ...
                                  'VariableNames', arrayfun(@(x) sprintf('To_%d', x), 1:size(obj.transitionRates, 1), 'UniformOutput', false), ...
                                  'RowNames', arrayfun(@(x) sprintf('From_%d', x), 1:size(obj.transitionRates, 1), 'UniformOutput', false));
            writetable(rateTable, fullfile(outputDir, 'transition_rates.csv'), 'WriteRowNames', true);
            
            % Export simulation results
            if ~isempty(obj.simulatedTrajectory)
                simTable = array2table(obj.simulatedTrajectory, 'VariableNames', {'Time', 'State'});
                writetable(simTable, fullfile(outputDir, 'simulated_trajectory.csv'));
            end
            
            % Export model validation
            if isfield(obj.modelValidation, 'frequencyCorrelation')
                validationTable = table({'Frequency'; 'Lifetime'; 'Transition'}, ...
                                       [obj.modelValidation.frequencyCorrelation(1,2); ...
                                        obj.modelValidation.lifetimeCorrelation(1,2); ...
                                        obj.modelValidation.transitionCorrelation(1,2)], ...
                                       'VariableNames', {'Metric', 'Correlation'});
                writetable(validationTable, fullfile(outputDir, 'model_validation.csv'));
            end
            
            % Save MATLAB data
            save(fullfile(outputDir, 'quantum_dot_model.mat'), 'obj');
            
            fprintf('Quantum dot model results exported successfully\n');
        end
    end
end
