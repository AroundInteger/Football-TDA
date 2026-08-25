% Demo script for CoupledCollectiveVariables - Step 1 Implementation
% This script demonstrates the foundational coupled dynamics analysis

clear; clc; close all;

fprintf('=== Step 1: Coupled Collective Variables Demo ===\n\n');

%% Step 1: Load real data
fprintf('Step 1: Loading real SecondSpectrum data...\n');

% File path
data_file = '/Users/iMacPro/Documents/GitHub/Football-TDA/FieldTest/g2293068_SecondSpectrum_Data copy.txt';

% Load data using our working JSON function
[home_positions, away_positions, timestamps, metadata] = load_secondspectrum_working(data_file, 1000);

fprintf('Data loaded successfully!\n');
fprintf('  Time points: %d\n', metadata.n_times);
fprintf('  Duration: %.1f seconds\n', metadata.duration);
fprintf('  Sampling rate: %.1f Hz\n', metadata.sampling_rate);

%% Step 2: Initialize CoupledCollectiveVariables
fprintf('\nStep 2: Initializing CoupledCollectiveVariables...\n');

% Initialize with real data
coupledVars = CoupledCollectiveVariables(home_positions, away_positions, timestamps, ...
    'fieldDimensions', [105, 68], ...
    'samplingRate', metadata.sampling_rate, ...
    'minPlayers', 8, ...
    'outlierThreshold', 3);

%% Step 3: Compute coupled metrics
fprintf('\nStep 3: Computing coupled collective variables...\n');

% Compute all coupled metrics
coupledVars = coupledVars.computeCoupledMetrics();

%% Step 4: Analyze results
fprintf('\nStep 4: Analyzing coupled dynamics results...\n');

% Display key findings
fprintf('\n--- Key Findings ---\n');

% Inter-team distance analysis
meanInterDist = nanmean(coupledVars.coupledMetrics.InterTeamDistance);
stdInterDist = nanstd(coupledVars.coupledMetrics.InterTeamDistance);
fprintf('Inter-Team Distance:\n');
fprintf('  Mean: %.1f ± %.1f m\n', meanInterDist, stdInterDist);
fprintf('  Range: %.1f - %.1f m\n', nanmin(coupledVars.coupledMetrics.InterTeamDistance), nanmax(coupledVars.coupledMetrics.InterTeamDistance));

% Team area ratio analysis
meanAreaRatio = nanmean(coupledVars.coupledMetrics.TeamAreaRatio);
stdAreaRatio = nanstd(coupledVars.coupledMetrics.TeamAreaRatio);
fprintf('\nTeam Area Ratio (Home/Away):\n');
fprintf('  Mean: %.2f ± %.2f\n', meanAreaRatio, stdAreaRatio);
fprintf('  Range: %.2f - %.2f\n', nanmin(coupledVars.coupledMetrics.TeamAreaRatio), nanmax(coupledVars.coupledMetrics.TeamAreaRatio));

% NOD analysis
meanHomeNOD = nanmean(coupledVars.coupledMetrics.HomeMeanNOD);
meanAwayNOD = nanmean(coupledVars.coupledMetrics.AwayMeanNOD);
fprintf('\nNearest Opponent Distance:\n');
fprintf('  Home team: %.1f ± %.1f m\n', meanHomeNOD, nanstd(coupledVars.coupledMetrics.HomeMeanNOD));
fprintf('  Away team: %.1f ± %.1f m\n', meanAwayNOD, nanstd(coupledVars.coupledMetrics.AwayMeanNOD));

% Shape difference analysis
meanShapeDiff = nanmean(coupledVars.coupledMetrics.ShapeDifference);
fprintf('\nShape Difference (Home - Away):\n');
fprintf('  Mean: %.3f ± %.3f\n', meanShapeDiff, nanstd(coupledVars.coupledMetrics.ShapeDifference));

%% Step 5: Create visualizations
fprintf('\nStep 5: Creating comprehensive visualizations...\n');

% Create coupled metrics visualization
coupledVars.visualizeCoupledMetrics();

%% Step 6: Advanced analysis - Tactical patterns
fprintf('\nStep 6: Identifying tactical patterns...\n');

% Identify different tactical phases based on coupled metrics
tacticalPhases = identifyTacticalPhases(coupledVars);

% Display tactical phase analysis
fprintf('\n--- Tactical Phase Analysis ---\n');
for i = 1:length(tacticalPhases.phaseNames)
    phaseName = tacticalPhases.phaseNames{i};
    phaseCount = tacticalPhases.phaseCounts(i);
    phaseDuration = tacticalPhases.phaseDurations(i);
    fprintf('%s: %d occurrences, avg duration %.1f s\n', phaseName, phaseCount, phaseDuration);
end

%% Step 7: Export results
fprintf('\nStep 7: Exporting results...\n');

% Export to results directory
output_dir = './step1_coupled_variables_results';
coupledVars.exportResults(output_dir);

% Create analysis report
createAnalysisReport(coupledVars, tacticalPhases, output_dir);

%% Step 8: Summary
fprintf('\n=== Step 1 Analysis Complete ===\n');
fprintf('Successfully implemented and analyzed coupled collective variables!\n');
fprintf('\nKey achievements:\n');
fprintf('  ✓ Inter-Team Centroid Vector analysis (field stretch & pressure direction)\n');
fprintf('  ✓ Team Shape Coupling analysis (area ratios & shape dynamics)\n');
fprintf('  ✓ Nearest Opponent Distance (NOD) analysis\n');
fprintf('  ✓ Tactical phase identification\n');
fprintf('  ✓ Comprehensive visualization and reporting\n');
fprintf('\nThis provides the foundation for Steps 2-4 of the GPS-TDA framework!\n');

%% Helper Functions

function tacticalPhases = identifyTacticalPhases(coupledVars)
    % Identify tactical phases based on coupled metrics
    
    % Define phase thresholds based on percentiles
    interDist = coupledVars.coupledMetrics.InterTeamDistance;
    areaRatio = coupledVars.coupledMetrics.TeamAreaRatio;
    
    % Remove NaN values for threshold calculation
    validInterDist = interDist(~isnan(interDist));
    validAreaRatio = areaRatio(~isnan(areaRatio));
    
    % Calculate thresholds
    interDistLow = prctile(validInterDist, 25);
    interDistHigh = prctile(validInterDist, 75);
    areaRatioLow = prctile(validAreaRatio, 25);
    areaRatioHigh = prctile(validAreaRatio, 75);
    
    % Classify phases
    phases = zeros(length(interDist), 1);
    
    for i = 1:length(interDist)
        if isnan(interDist(i)) || isnan(areaRatio(i))
            phases(i) = 0; % Unknown
        elseif interDist(i) < interDistLow && areaRatio(i) < areaRatioLow
            phases(i) = 1; % Compact Defense
        elseif interDist(i) > interDistHigh && areaRatio(i) > areaRatioHigh
            phases(i) = 2; % High Press
        elseif interDist(i) < interDistLow && areaRatio(i) > areaRatioHigh
            phases(i) = 3; % Counter-Attack
        else
            phases(i) = 4; % Normal Play
        end
    end
    
    % Calculate phase statistics
    phaseNames = {'Unknown', 'Compact Defense', 'High Press', 'Counter-Attack', 'Normal Play'};
    phaseCounts = zeros(5, 1);
    phaseDurations = zeros(5, 1);
    
    for i = 1:5
        phaseIndices = find(phases == i-1);
        phaseCounts(i) = length(phaseIndices);
        
        % Calculate average duration
        if ~isempty(phaseIndices)
            % Find consecutive sequences
            diffIndices = diff(phaseIndices);
            breaks = find(diffIndices > 1);
            
            if isempty(breaks)
                durations = length(phaseIndices);
            else
                durations = [breaks(1); diff(breaks); length(phaseIndices) - breaks(end)];
            end
            
            phaseDurations(i) = mean(durations) / coupledVars.samplingRate;
        end
    end
    
    tacticalPhases = struct();
    tacticalPhases.phases = phases;
    tacticalPhases.phaseNames = phaseNames;
    tacticalPhases.phaseCounts = phaseCounts;
    tacticalPhases.phaseDurations = phaseDurations;
    tacticalPhases.thresholds = struct('interDistLow', interDistLow, 'interDistHigh', interDistHigh, ...
                                      'areaRatioLow', areaRatioLow, 'areaRatioHigh', areaRatioHigh);
end

function createAnalysisReport(coupledVars, tacticalPhases, outputDir)
    % Create detailed analysis report
    
    reportFile = fullfile(outputDir, 'step1_analysis_report.txt');
    fid = fopen(reportFile, 'w');
    
    fprintf(fid, 'Step 1: Coupled Collective Variables Analysis Report\n');
    fprintf(fid, '====================================================\n\n');
    fprintf(fid, 'Analysis Date: %s\n', datestr(now));
    fprintf(fid, 'Data Source: %s\n', coupledVars.coupledMetrics.Properties.Description);
    fprintf(fid, '\n');
    
    fprintf(fid, 'Data Summary:\n');
    fprintf(fid, '  Time Points: %d\n', height(coupledVars.coupledMetrics));
    fprintf(fid, '  Duration: %.1f seconds\n', max(coupledVars.timestamps) - min(coupledVars.timestamps));
    fprintf(fid, '  Sampling Rate: %.1f Hz\n', coupledVars.samplingRate);
    fprintf(fid, '  Field Dimensions: %.0f x %.0f m\n', coupledVars.fieldDimensions(1), coupledVars.fieldDimensions(2));
    fprintf(fid, '\n');
    
    fprintf(fid, 'Coupled Metrics Summary:\n');
    summaryStats = coupledVars.computeSummaryStatistics();
    for i = 1:height(summaryStats)
        fprintf(fid, '  %s: %.3f ± %.3f (range: %.3f - %.3f)\n', ...
                summaryStats.Metric(i), summaryStats.Mean(i), summaryStats.Std(i), ...
                summaryStats.Min(i), summaryStats.Max(i));
    end
    fprintf(fid, '\n');
    
    fprintf(fid, 'Tactical Phase Analysis:\n');
    for i = 1:length(tacticalPhases.phaseNames)
        fprintf(fid, '  %s: %d occurrences (%.1f%%), avg duration %.1f s\n', ...
                tacticalPhases.phaseNames{i}, tacticalPhases.phaseCounts(i), ...
                100 * tacticalPhases.phaseCounts(i) / sum(tacticalPhases.phaseCounts), ...
                tacticalPhases.phaseDurations(i));
    end
    fprintf(fid, '\n');
    
    fprintf(fid, 'Key Insights:\n');
    fprintf(fid, '  - Inter-team distance shows field stretch dynamics\n');
    fprintf(fid, '  - Team area ratios reveal shape coupling patterns\n');
    fprintf(fid, '  - NOD analysis characterizes marking schemes\n');
    fprintf(fid, '  - Tactical phases identified based on coupled metrics\n');
    fprintf(fid, '\n');
    
    fprintf(fid, 'Methodological Notes:\n');
    fprintf(fid, '  - Based on established research in sports analytics\n');
    fprintf(fid, '  - Implements coupled collective variables framework\n');
    fprintf(fid, '  - Provides foundation for advanced TDA analysis\n');
    fprintf(fid, '  - Ready for state space reconstruction (Step 2)\n');
    
    fclose(fid);
    
    fprintf('Analysis report saved to: %s\n', reportFile);
end
