% Demo script for ZeroSumSymmetryAnalysis - Step 3 Implementation
% This script demonstrates zero-sum competition and symmetry breaking analysis

clear; clc; close all;

fprintf('=== Step 3: Zero-Sum Competition & Symmetry Breaking Demo ===\n\n');

%% Step 1: Load previous results
fprintf('Step 1: Loading Step 1 and Step 2 results...\n');

% Load Step 1 results
load('step1_coupled_variables_results/coupled_analysis.mat');
coupledVars = obj;
coupledMetrics = obj.coupledMetrics;
timestamps = obj.timestamps;

% Load Step 2 results
load('step2_state_space_results/state_space_analysis.mat');
stateSpace = obj;

fprintf('Previous results loaded successfully!\n');
fprintf('  Step 1: %d time points, %d coupled metrics\n', height(coupledMetrics), width(coupledMetrics));
fprintf('  Step 2: %d attractors, %d state vectors\n', stateSpace.attractorStates.nClusters, size(stateSpace.stateVectors, 1));

%% Step 2: Initialize ZeroSumSymmetryAnalysis
fprintf('\nStep 2: Initializing ZeroSumSymmetryAnalysis...\n');

% Initialize the analysis
zeroSumAnalysis = ZeroSumSymmetryAnalysis(coupledMetrics, stateSpace, timestamps);

%% Step 3: Analyze zero-sum competition
fprintf('\nStep 3: Analyzing zero-sum competition...\n');

% Perform zero-sum competition analysis
zeroSumAnalysis = zeroSumAnalysis.analyzeZeroSumCompetition();

%% Step 4: Analyze symmetry breaking
fprintf('\nStep 4: Analyzing symmetry breaking...\n');

% Perform symmetry breaking analysis
zeroSumAnalysis = zeroSumAnalysis.analyzeSymmetryBreaking();

%% Step 5: Analyze results
fprintf('\nStep 5: Analyzing zero-sum and symmetry results...\n');

% Display key findings
fprintf('\n--- Zero-Sum Competition Analysis Results ---\n');

% Cross-correlations
if isfield(zeroSumAnalysis.crossCorrelations, 'HomeTeamArea')
    fprintf('Cross-Correlations (Home vs Away):\n');
    fprintf('  Team Area: %.3f\n', zeroSumAnalysis.crossCorrelations.HomeTeamArea);
    fprintf('  Mean NOD: %.3f\n', zeroSumAnalysis.crossCorrelations.HomeMeanNOD);
    fprintf('  Std NOD: %.3f\n', zeroSumAnalysis.crossCorrelations.HomeStdNOD);
end

% Zero-sum metrics
if isfield(zeroSumAnalysis.zeroSumMetrics, 'nodZeroSumIndex')
    fprintf('\nZero-Sum Competition Indices:\n');
    fprintf('  NOD Zero-Sum Index: %.3f\n', zeroSumAnalysis.zeroSumMetrics.nodZeroSumIndex(1,2));
    fprintf('  Area Zero-Sum Index: %.3f\n', zeroSumAnalysis.zeroSumMetrics.areaZeroSumIndex(1,2));
    fprintf('  NOD Balance: %.3f\n', zeroSumAnalysis.zeroSumMetrics.nodBalance);
    fprintf('  Area Balance: %.3f\n', zeroSumAnalysis.zeroSumMetrics.areaBalance);
    fprintf('  Area Dominance: %.3f\n', zeroSumAnalysis.zeroSumMetrics.areaDominance);
end

% Competitive balance
if isfield(zeroSumAnalysis.competitiveBalance, 'overallBalance')
    fprintf('\nCompetitive Balance Assessment:\n');
    fprintf('  Area Balance: %.3f\n', zeroSumAnalysis.competitiveBalance.areaBalance);
    fprintf('  NOD Balance: %.3f\n', zeroSumAnalysis.competitiveBalance.nodBalance);
    fprintf('  Overall Balance: %.3f\n', zeroSumAnalysis.competitiveBalance.overallBalance);
    if isfield(zeroSumAnalysis.competitiveBalance, 'attractorBalance')
        fprintf('  Attractor Balance: %.3f\n', zeroSumAnalysis.competitiveBalance.attractorBalance);
    end
end

fprintf('\n--- Symmetry Breaking Analysis Results ---\n');

% Field symmetry
if isfield(zeroSumAnalysis.fieldSymmetry, 'lateralSymmetry')
    fprintf('Field Symmetry Analysis:\n');
    fprintf('  Lateral Symmetry: %.3f\n', zeroSumAnalysis.fieldSymmetry.lateralSymmetry);
    fprintf('  Temporal Symmetry: %.3f\n', zeroSumAnalysis.fieldSymmetry.temporalSymmetry);
    fprintf('  Field Dominance: %.3f\n', zeroSumAnalysis.fieldSymmetry.fieldDominance);
end

% Numerical overloads
if isfield(zeroSumAnalysis.overloadMetrics, 'homeAreaOverload')
    fprintf('\nNumerical Overload Analysis:\n');
    fprintf('  Home Area Overload: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.homeAreaOverload);
    fprintf('  Away Area Overload: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.awayAreaOverload);
    fprintf('  Balanced Play: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.balancedPlay);
    fprintf('  High Pressure: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.highPressure);
    fprintf('  Low Pressure: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.lowPressure);
    fprintf('  Home Tight Marking: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.homeTightMarking);
    fprintf('  Away Tight Marking: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.awayTightMarking);
end

% Tactical advantages
if isfield(zeroSumAnalysis.tacticalAdvantage, 'overallHomeAdvantage')
    fprintf('\nTactical Advantage Analysis:\n');
    fprintf('  Home Area Persistence: %.3f\n', zeroSumAnalysis.tacticalAdvantage.homeAreaPersistence);
    fprintf('  Away Area Persistence: %.3f\n', zeroSumAnalysis.tacticalAdvantage.awayAreaPersistence);
    fprintf('  Home NOD Persistence: %.3f\n', zeroSumAnalysis.tacticalAdvantage.homeNODPersistence);
    fprintf('  Away NOD Persistence: %.3f\n', zeroSumAnalysis.tacticalAdvantage.awayNODPersistence);
    fprintf('  Overall Home Advantage: %.3f\n', zeroSumAnalysis.tacticalAdvantage.overallHomeAdvantage);
    fprintf('  Overall Away Advantage: %.3f\n', zeroSumAnalysis.tacticalAdvantage.overallAwayAdvantage);
end

%% Step 6: Create visualizations
fprintf('\nStep 6: Creating zero-sum and symmetry visualizations...\n');

% Create comprehensive visualization
zeroSumAnalysis.visualizeZeroSumSymmetry();

%% Step 7: Advanced analysis - Competitive dynamics
fprintf('\nStep 7: Analyzing competitive dynamics...\n');

% Analyze competitive dynamics over time
competitiveDynamics = analyzeCompetitiveDynamics(zeroSumAnalysis, coupledMetrics, timestamps);

% Display competitive dynamics insights
fprintf('\n--- Competitive Dynamics Analysis ---\n');
fprintf('Competitive Intensity:\n');
fprintf('  High Competition Periods: %.1f%%\n', 100 * competitiveDynamics.highCompetitionPeriods);
fprintf('  Low Competition Periods: %.1f%%\n', 100 * competitiveDynamics.lowCompetitionPeriods);
fprintf('  Average Competition Level: %.3f\n', competitiveDynamics.averageCompetitionLevel);

fprintf('\nTactical Evolution:\n');
fprintf('  Tactical Changes: %d\n', competitiveDynamics.tacticalChanges);
fprintf('  Average Change Interval: %.1f seconds\n', competitiveDynamics.averageChangeInterval);
fprintf('  Tactical Stability: %.3f\n', competitiveDynamics.tacticalStability);

%% Step 8: Export results
fprintf('\nStep 8: Exporting results...\n');

% Export to results directory
output_dir = './step3_zero_sum_symmetry_results';
zeroSumAnalysis.exportResults(output_dir);

% Create analysis report
createZeroSumSymmetryReport(zeroSumAnalysis, competitiveDynamics, output_dir);

%% Step 9: Summary
fprintf('\n=== Step 3 Analysis Complete ===\n');
fprintf('Successfully implemented zero-sum competition and symmetry breaking analysis!\n');
fprintf('\nKey achievements:\n');
fprintf('  ✓ Cross-correlation analysis between opposing team metrics\n');
fprintf('  ✓ Zero-sum competition quantification\n');
fprintf('  ✓ Competitive balance assessment\n');
fprintf('  ✓ Field symmetry analysis\n');
fprintf('  ✓ Numerical overload identification\n');
fprintf('  ✓ Tactical advantage quantification\n');
fprintf('  ✓ Comprehensive visualization and analysis\n');
fprintf('\nThis provides the foundation for Step 4: Homology for Deeper Structural Insights!\n');

%% Helper Functions

function competitiveDynamics = analyzeCompetitiveDynamics(zeroSumAnalysis, coupledMetrics, timestamps)
    % Analyze competitive dynamics over time
    
    competitiveDynamics = struct();
    
    % 1. Competitive intensity analysis
    areaRatio = coupledMetrics.TeamAreaRatio;
    interDist = coupledMetrics.InterTeamDistance;
    
    % Define high competition periods (balanced play with moderate pressure)
    highCompetition = (areaRatio >= 0.9 & areaRatio <= 1.1) & (interDist >= 30 & interDist <= 60);
    lowCompetition = (areaRatio < 0.8 | areaRatio > 1.2) | (interDist < 20 | interDist > 70);
    
    competitiveDynamics.highCompetitionPeriods = sum(highCompetition) / length(highCompetition);
    competitiveDynamics.lowCompetitionPeriods = sum(lowCompetition) / length(lowCompetition);
    
    % Average competition level (inverse of area ratio deviation from 1)
    areaDeviation = abs(areaRatio - 1);
    competitiveDynamics.averageCompetitionLevel = 1 - nanmean(areaDeviation);
    
    % 2. Tactical evolution analysis
    if isfield(zeroSumAnalysis.stateSpace, 'attractorLabels') && ~isempty(zeroSumAnalysis.stateSpace.attractorLabels)
        attractorLabels = zeroSumAnalysis.stateSpace.attractorLabels;
        
        % Count tactical changes (attractor transitions)
        tacticalChanges = sum(diff(attractorLabels) ~= 0);
        competitiveDynamics.tacticalChanges = tacticalChanges;
        
        % Average change interval
        if tacticalChanges > 0
            competitiveDynamics.averageChangeInterval = (timestamps(end) - timestamps(1)) / tacticalChanges;
        else
            competitiveDynamics.averageChangeInterval = Inf;
        end
        
        % Tactical stability (inverse of change frequency)
        competitiveDynamics.tacticalStability = 1 - (tacticalChanges / length(attractorLabels));
    else
        competitiveDynamics.tacticalChanges = 0;
        competitiveDynamics.averageChangeInterval = Inf;
        competitiveDynamics.tacticalStability = 1;
    end
end

function createZeroSumSymmetryReport(zeroSumAnalysis, competitiveDynamics, outputDir)
    % Create detailed zero-sum and symmetry analysis report
    
    reportFile = fullfile(outputDir, 'step3_analysis_report.txt');
    fid = fopen(reportFile, 'w');
    
    fprintf(fid, 'Step 3: Zero-Sum Competition & Symmetry Breaking Analysis Report\n');
    fprintf(fid, '================================================================\n\n');
    fprintf(fid, 'Analysis Date: %s\n', datestr(now));
    fprintf(fid, '\n');
    
    fprintf(fid, 'Zero-Sum Competition Analysis:\n');
    if isfield(zeroSumAnalysis.crossCorrelations, 'HomeTeamArea')
        fprintf(fid, '  Cross-Correlations (Home vs Away):\n');
        fprintf(fid, '    Team Area: %.3f\n', zeroSumAnalysis.crossCorrelations.HomeTeamArea);
        fprintf(fid, '    Mean NOD: %.3f\n', zeroSumAnalysis.crossCorrelations.HomeMeanNOD);
        fprintf(fid, '    Std NOD: %.3f\n', zeroSumAnalysis.crossCorrelations.HomeStdNOD);
    end
    
    if isfield(zeroSumAnalysis.zeroSumMetrics, 'nodZeroSumIndex')
        fprintf(fid, '  Zero-Sum Competition Indices:\n');
        fprintf(fid, '    NOD Zero-Sum Index: %.3f\n', zeroSumAnalysis.zeroSumMetrics.nodZeroSumIndex(1,2));
        fprintf(fid, '    Area Zero-Sum Index: %.3f\n', zeroSumAnalysis.zeroSumMetrics.areaZeroSumIndex(1,2));
        fprintf(fid, '    NOD Balance: %.3f\n', zeroSumAnalysis.zeroSumMetrics.nodBalance);
        fprintf(fid, '    Area Balance: %.3f\n', zeroSumAnalysis.zeroSumMetrics.areaBalance);
        fprintf(fid, '    Area Dominance: %.3f\n', zeroSumAnalysis.zeroSumMetrics.areaDominance);
    end
    fprintf(fid, '\n');
    
    fprintf(fid, 'Competitive Balance Assessment:\n');
    if isfield(zeroSumAnalysis.competitiveBalance, 'overallBalance')
        fprintf(fid, '  Area Balance: %.3f\n', zeroSumAnalysis.competitiveBalance.areaBalance);
        fprintf(fid, '  NOD Balance: %.3f\n', zeroSumAnalysis.competitiveBalance.nodBalance);
        fprintf(fid, '  Overall Balance: %.3f\n', zeroSumAnalysis.competitiveBalance.overallBalance);
        if isfield(zeroSumAnalysis.competitiveBalance, 'attractorBalance')
            fprintf(fid, '  Attractor Balance: %.3f\n', zeroSumAnalysis.competitiveBalance.attractorBalance);
        end
    end
    fprintf(fid, '\n');
    
    fprintf(fid, 'Symmetry Breaking Analysis:\n');
    if isfield(zeroSumAnalysis.fieldSymmetry, 'lateralSymmetry')
        fprintf(fid, '  Field Symmetry:\n');
        fprintf(fid, '    Lateral Symmetry: %.3f\n', zeroSumAnalysis.fieldSymmetry.lateralSymmetry);
        fprintf(fid, '    Temporal Symmetry: %.3f\n', zeroSumAnalysis.fieldSymmetry.temporalSymmetry);
        fprintf(fid, '    Field Dominance: %.3f\n', zeroSumAnalysis.fieldSymmetry.fieldDominance);
    end
    
    if isfield(zeroSumAnalysis.overloadMetrics, 'homeAreaOverload')
        fprintf(fid, '  Numerical Overloads:\n');
        fprintf(fid, '    Home Area Overload: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.homeAreaOverload);
        fprintf(fid, '    Away Area Overload: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.awayAreaOverload);
        fprintf(fid, '    Balanced Play: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.balancedPlay);
        fprintf(fid, '    High Pressure: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.highPressure);
        fprintf(fid, '    Low Pressure: %.1f%%\n', 100 * zeroSumAnalysis.overloadMetrics.lowPressure);
    end
    
    if isfield(zeroSumAnalysis.tacticalAdvantage, 'overallHomeAdvantage')
        fprintf(fid, '  Tactical Advantages:\n');
        fprintf(fid, '    Home Area Persistence: %.3f\n', zeroSumAnalysis.tacticalAdvantage.homeAreaPersistence);
        fprintf(fid, '    Away Area Persistence: %.3f\n', zeroSumAnalysis.tacticalAdvantage.awayAreaPersistence);
        fprintf(fid, '    Home NOD Persistence: %.3f\n', zeroSumAnalysis.tacticalAdvantage.homeNODPersistence);
        fprintf(fid, '    Away NOD Persistence: %.3f\n', zeroSumAnalysis.tacticalAdvantage.awayNODPersistence);
        fprintf(fid, '    Overall Home Advantage: %.3f\n', zeroSumAnalysis.tacticalAdvantage.overallHomeAdvantage);
        fprintf(fid, '    Overall Away Advantage: %.3f\n', zeroSumAnalysis.tacticalAdvantage.overallAwayAdvantage);
    end
    fprintf(fid, '\n');
    
    fprintf(fid, 'Competitive Dynamics Analysis:\n');
    fprintf(fid, '  High Competition Periods: %.1f%%\n', 100 * competitiveDynamics.highCompetitionPeriods);
    fprintf(fid, '  Low Competition Periods: %.1f%%\n', 100 * competitiveDynamics.lowCompetitionPeriods);
    fprintf(fid, '  Average Competition Level: %.3f\n', competitiveDynamics.averageCompetitionLevel);
    fprintf(fid, '  Tactical Changes: %d\n', competitiveDynamics.tacticalChanges);
    fprintf(fid, '  Average Change Interval: %.1f seconds\n', competitiveDynamics.averageChangeInterval);
    fprintf(fid, '  Tactical Stability: %.3f\n', competitiveDynamics.tacticalStability);
    fprintf(fid, '\n');
    
    fprintf(fid, 'Key Insights:\n');
    fprintf(fid, '  - Zero-sum competition reveals inverse relationships between opposing team metrics\n');
    fprintf(fid, '  - Symmetry breaking identifies tactical advantages and numerical overloads\n');
    fprintf(fid, '  - Competitive balance assessment quantifies game equilibrium\n');
    fprintf(fid, '  - Tactical advantage persistence indicates strategic effectiveness\n');
    fprintf(fid, '\n');
    
    fprintf(fid, 'Methodological Notes:\n');
    fprintf(fid, '  - Based on cross-correlation analysis and symmetry breaking detection\n');
    fprintf(fid, '  - Implements competitive balance assessment framework\n');
    fprintf(fid, '  - Provides foundation for topological analysis (Step 4)\n');
    fprintf(fid, '  - Ready for homology-based structural insights\n');
    
    fclose(fid);
    
    fprintf('Zero-sum and symmetry analysis report saved to: %s\n', reportFile);
end
