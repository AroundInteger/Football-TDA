% Demo script for StateSpaceReconstruction - Step 2 Implementation
% This script demonstrates state space reconstruction and attractor identification

clear; clc; close all;

fprintf('=== Step 2: State Space Reconstruction Demo ===\n\n');

%% Step 1: Load Step 1 results
fprintf('Step 1: Loading Step 1 coupled variables results...\n');

% Load the coupled analysis from Step 1
load('step1_coupled_variables_results/coupled_analysis.mat');

% Extract coupled metrics
coupledMetrics = obj.coupledMetrics;
timestamps = obj.timestamps;

fprintf('Step 1 data loaded successfully!\n');
fprintf('  Time points: %d\n', height(coupledMetrics));
fprintf('  Duration: %.1f seconds\n', max(timestamps) - min(timestamps));
fprintf('  Available variables: %s\n', strjoin(coupledMetrics.Properties.VariableNames, ', '));

%% Step 2: Initialize StateSpaceReconstruction
fprintf('\nStep 2: Initializing StateSpaceReconstruction...\n');

% Define state variables for reconstruction
stateVariables = {'InterTeamDistance', 'TeamAreaRatio', 'HomeMeanNOD', 'AwayMeanNOD'};

% Initialize with different embedding parameters
stateSpace = StateSpaceReconstruction(coupledMetrics, timestamps, ...
    'embeddingDimension', 3, ...
    'timeDelay', 2, ...
    'stateVariables', stateVariables);

%% Step 3: Reconstruct state space
fprintf('\nStep 3: Reconstructing state space...\n');

% Perform state space reconstruction
stateSpace = stateSpace.reconstructStateSpace();

%% Step 4: Analyze results
fprintf('\nStep 4: Analyzing state space reconstruction results...\n');

% Display key findings
fprintf('\n--- State Space Analysis Results ---\n');

% Embedding parameters
fprintf('Embedding Parameters:\n');
fprintf('  Embedding dimension: %d\n', stateSpace.embeddingDimension);
fprintf('  Time delay: %d time steps\n', stateSpace.timeDelay);
fprintf('  State variables: %s\n', strjoin(stateSpace.stateVariables, ', '));

% State space dimensions
fprintf('\nState Space Dimensions:\n');
fprintf('  Original state vectors: %d x %d\n', size(stateSpace.stateVectors, 1), size(stateSpace.stateVectors, 2));
fprintf('  Embedded vectors: %d x %d\n', size(stateSpace.embeddedVectors, 1), size(stateSpace.embeddedVectors, 2));

% Attractor analysis
fprintf('\nAttractor Analysis:\n');
fprintf('  Number of attractors identified: %d\n', stateSpace.attractorStates.nClusters);
fprintf('  Attractor labels range: %d - %d\n', min(stateSpace.attractorLabels), max(stateSpace.attractorLabels));

% Attractor characteristics
fprintf('\nAttractor Characteristics:\n');
for i = 1:stateSpace.attractorStates.nClusters
    fprintf('  Attractor %d:\n', i);
    fprintf('    Frequency: %.1f%%\n', 100 * stateSpace.attractorMetrics.frequency(i));
    fprintf('    Duration: %.1f time steps\n', stateSpace.attractorMetrics.duration(i));
    fprintf('    Stability: %.3f\n', stateSpace.attractorMetrics.stability(i));
    fprintf('    Transitions: %d\n', stateSpace.attractorMetrics.transitions(i));
end

%% Step 5: Transition analysis
fprintf('\nStep 5: Analyzing attractor transitions...\n');

% Analyze transition patterns
fprintf('\n--- Transition Analysis ---\n');
fprintf('Transition Matrix:\n');
for i = 1:stateSpace.attractorStates.nClusters
    fprintf('  From Attractor %d:', i);
    for j = 1:stateSpace.attractorStates.nClusters
        fprintf('  %.2f', stateSpace.transitionMatrix(i, j));
    end
    fprintf('\n');
end

% Identify most common transitions
[maxTransitions, maxIndices] = max(stateSpace.transitionMatrix, [], 2);
fprintf('\nMost Common Transitions:\n');
for i = 1:stateSpace.attractorStates.nClusters
    if maxTransitions(i) > 0
        fprintf('  Attractor %d → Attractor %d (%.1f%%)\n', i, maxIndices(i), 100 * maxTransitions(i));
    end
end

%% Step 6: Create visualizations
fprintf('\nStep 6: Creating state space visualizations...\n');

% Create comprehensive state space visualization
stateSpace.visualizeStateSpace();

%% Step 7: Advanced analysis - Attractor interpretation
fprintf('\nStep 7: Interpreting attractor states...\n');

% Interpret attractors based on coupled metrics
attractorInterpretation = interpretAttractors(stateSpace, coupledMetrics);

% Display interpretation
fprintf('\n--- Attractor Interpretation ---\n');
for i = 1:length(attractorInterpretation.attractorNames)
    fprintf('Attractor %d (%s):\n', i, attractorInterpretation.attractorNames{i});
    fprintf('  Description: %s\n', attractorInterpretation.descriptions{i});
    fprintf('  Key characteristics: %s\n', attractorInterpretation.characteristics{i});
end

%% Step 8: Export results
fprintf('\nStep 8: Exporting results...\n');

% Export to results directory
output_dir = './step2_state_space_results';
stateSpace.exportResults(output_dir);

% Create analysis report
createStateSpaceReport(stateSpace, attractorInterpretation, output_dir);

%% Step 9: Summary
fprintf('\n=== Step 2 Analysis Complete ===\n');
fprintf('Successfully implemented state space reconstruction!\n');
fprintf('\nKey achievements:\n');
fprintf('  ✓ State vector construction from coupled collective variables\n');
fprintf('  ✓ Time-delay embedding using Takens theorem\n');
fprintf('  ✓ Attractor identification using k-means clustering\n');
fprintf('  ✓ Transition matrix computation\n');
fprintf('  ✓ Comprehensive visualization and analysis\n');
fprintf('\nThis provides the foundation for Steps 3-4 of the GPS-TDA framework!\n');

%% Helper Functions

function interpretation = interpretAttractors(stateSpace, coupledMetrics)
    % Interpret attractor states based on coupled metrics
    
    nClusters = stateSpace.attractorStates.nClusters;
    
    % Initialize interpretation structure
    interpretation = struct();
    interpretation.attractorNames = cell(nClusters, 1);
    interpretation.descriptions = cell(nClusters, 1);
    interpretation.characteristics = cell(nClusters, 1);
    
    % Analyze each attractor
    for i = 1:nClusters
        attractorIndices = find(stateSpace.attractorLabels == i);
        
        if ~isempty(attractorIndices)
            % Calculate mean values for this attractor (handle NaN values)
            meanInterDist = nanmean(coupledMetrics.InterTeamDistance(attractorIndices));
            meanAreaRatio = nanmean(coupledMetrics.TeamAreaRatio(attractorIndices));
            meanHomeNOD = nanmean(coupledMetrics.HomeMeanNOD(attractorIndices));
            meanAwayNOD = nanmean(coupledMetrics.AwayMeanNOD(attractorIndices));
            
            % Interpret based on metrics
            if meanInterDist < 30 && meanAreaRatio < 1.0
                interpretation.attractorNames{i} = 'Compact Defense';
                interpretation.descriptions{i} = 'Teams maintain close proximity with compact formations';
                interpretation.characteristics{i} = sprintf('Inter-team distance: %.1fm, Area ratio: %.2f', meanInterDist, meanAreaRatio);
            elseif meanInterDist > 50 && meanAreaRatio > 1.1
                interpretation.attractorNames{i} = 'High Press';
                interpretation.descriptions{i} = 'Teams maintain wide separation with expanded formations';
                interpretation.characteristics{i} = sprintf('Inter-team distance: %.1fm, Area ratio: %.2f', meanInterDist, meanAreaRatio);
            elseif meanHomeNOD < 20 && meanAwayNOD < 20
                interpretation.attractorNames{i} = 'Tight Marking';
                interpretation.descriptions{i} = 'Both teams maintain tight marking schemes';
                interpretation.characteristics{i} = sprintf('Home NOD: %.1fm, Away NOD: %.1fm', meanHomeNOD, meanAwayNOD);
            elseif meanAreaRatio > 1.2
                interpretation.attractorNames{i} = 'Home Advantage';
                interpretation.descriptions{i} = 'Home team maintains larger formation area';
                interpretation.characteristics{i} = sprintf('Area ratio: %.2f, Home NOD: %.1fm', meanAreaRatio, meanHomeNOD);
            else
                interpretation.attractorNames{i} = 'Normal Play';
                interpretation.descriptions{i} = 'Standard tactical configuration';
                interpretation.characteristics{i} = sprintf('Inter-team distance: %.1fm, Area ratio: %.2f', meanInterDist, meanAreaRatio);
            end
        else
            interpretation.attractorNames{i} = 'Unknown';
            interpretation.descriptions{i} = 'Insufficient data for interpretation';
            interpretation.characteristics{i} = 'No data points';
        end
    end
end

function createStateSpaceReport(stateSpace, interpretation, outputDir)
    % Create detailed state space analysis report
    
    reportFile = fullfile(outputDir, 'step2_analysis_report.txt');
    fid = fopen(reportFile, 'w');
    
    fprintf(fid, 'Step 2: State Space Reconstruction Analysis Report\n');
    fprintf(fid, '==================================================\n\n');
    fprintf(fid, 'Analysis Date: %s\n', datestr(now));
    fprintf(fid, '\n');
    
    fprintf(fid, 'State Space Parameters:\n');
    fprintf(fid, '  Embedding Dimension: %d\n', stateSpace.embeddingDimension);
    fprintf(fid, '  Time Delay: %d time steps\n', stateSpace.timeDelay);
    fprintf(fid, '  State Variables: %s\n', strjoin(stateSpace.stateVariables, ', '));
    fprintf(fid, '\n');
    
    fprintf(fid, 'State Space Dimensions:\n');
    fprintf(fid, '  Original State Vectors: %d x %d\n', size(stateSpace.stateVectors, 1), size(stateSpace.stateVectors, 2));
    fprintf(fid, '  Embedded Vectors: %d x %d\n', size(stateSpace.embeddedVectors, 1), size(stateSpace.embeddedVectors, 2));
    fprintf(fid, '  Total Embedding Dimension: %d\n', size(stateSpace.embeddedVectors, 2));
    fprintf(fid, '\n');
    
    fprintf(fid, 'Attractor Analysis:\n');
    fprintf(fid, '  Number of Attractors: %d\n', stateSpace.attractorStates.nClusters);
    for i = 1:stateSpace.attractorStates.nClusters
        fprintf(fid, '  Attractor %d (%s):\n', i, interpretation.attractorNames{i});
        fprintf(fid, '    Frequency: %.1f%%\n', 100 * stateSpace.attractorMetrics.frequency(i));
        fprintf(fid, '    Duration: %.1f time steps\n', stateSpace.attractorMetrics.duration(i));
        fprintf(fid, '    Stability: %.3f\n', stateSpace.attractorMetrics.stability(i));
        fprintf(fid, '    Transitions: %d\n', stateSpace.attractorMetrics.transitions(i));
        fprintf(fid, '    Description: %s\n', interpretation.descriptions{i});
        fprintf(fid, '\n');
    end
    
    fprintf(fid, 'Transition Analysis:\n');
    fprintf(fid, '  Transition Matrix:\n');
    for i = 1:stateSpace.attractorStates.nClusters
        fprintf(fid, '    From %d:', i);
        for j = 1:stateSpace.attractorStates.nClusters
            fprintf(fid, '  %.2f', stateSpace.transitionMatrix(i, j));
        end
        fprintf(fid, '\n');
    end
    fprintf(fid, '\n');
    
    fprintf(fid, 'Key Insights:\n');
    fprintf(fid, '  - State space reconstruction successfully identified %d attractor states\n', stateSpace.attractorStates.nClusters);
    fprintf(fid, '  - Time-delay embedding captured temporal dynamics\n');
    fprintf(fid, '  - Attractor states represent distinct tactical configurations\n');
    fprintf(fid, '  - Transition matrix reveals tactical evolution patterns\n');
    fprintf(fid, '\n');
    
    fprintf(fid, 'Methodological Notes:\n');
    fprintf(fid, '  - Based on Takens theorem for time-delay embedding\n');
    fprintf(fid, '  - K-means clustering for attractor identification\n');
    fprintf(fid, '  - Provides foundation for zero-sum analysis (Step 3)\n');
    fprintf(fid, '  - Ready for topological analysis (Step 4)\n');
    
    fclose(fid);
    
    fprintf('State space analysis report saved to: %s\n', reportFile);
end
