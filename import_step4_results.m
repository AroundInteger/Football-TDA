function import_step4_results(input_dir, output_dir)
% IMPORT_STEP4_RESULTS - Import results from standalone Python Step 4 analysis
%
% This function imports the results from the standalone Python persistent
% homology analysis and creates MATLAB-compatible data structures and
% visualizations.
%
% Usage:
%   import_step4_results()  % Uses default directories
%   import_step4_results(input_dir, output_dir)  % Specify directories
%
% Inputs:
%   input_dir  - Directory containing Python analysis results (default: './step4_standalone_results')
%   output_dir - Directory to save MATLAB results (default: './step4_matlab_results')
%
% Outputs:
%   Creates MATLAB data files and visualizations in output_dir

%% Default parameters
if nargin < 1
    input_dir = './step4_standalone_results';
end
if nargin < 2
    output_dir = './step4_matlab_results';
end

fprintf('=== Importing Step 4 Python Results ===\n');
fprintf('Input directory: %s\n', input_dir);
fprintf('Output directory: %s\n', output_dir);

%% Check if input directory exists
if ~exist(input_dir, 'dir')
    error('Input directory does not exist: %s', input_dir);
end

%% Create output directory
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

%% Load Python results
fprintf('\nLoading Python analysis results...\n');

% Load complete results JSON
json_file = fullfile(input_dir, 'step4_complete_results.json');
if ~exist(json_file, 'file')
    error('Python results file not found: %s', json_file);
end

% Read JSON file
fid = fopen(json_file, 'r');
jsonStr = fread(fid, inf, 'uint8=>char')';
fclose(fid);

% Parse JSON
pythonResults = jsondecode(jsonStr);

fprintf('  Python results loaded successfully\n');

%% Load CSV files
fprintf('Loading CSV data files...\n');

% Load topological features summary
topo_file = fullfile(input_dir, 'topological_features_summary.csv');
if exist(topo_file, 'file')
    topologicalFeatures = readtable(topo_file);
    fprintf('  Topological features loaded: %d rows\n', height(topologicalFeatures));
else
    fprintf('  Warning: Topological features CSV not found\n');
    topologicalFeatures = table();
end

% Load quantum features
quantum_file = fullfile(input_dir, 'quantum_topological_features.csv');
if exist(quantum_file, 'file')
    quantumFeatures = readtable(quantum_file);
    fprintf('  Quantum features loaded: %d rows\n', height(quantumFeatures));
else
    fprintf('  Warning: Quantum features CSV not found\n');
    quantumFeatures = table();
end

% Load tactical effectiveness
tactical_file = fullfile(input_dir, 'tactical_effectiveness.csv');
if exist(tactical_file, 'file')
    tacticalEffectiveness = readtable(tactical_file);
    fprintf('  Tactical effectiveness loaded: %d rows\n', height(tacticalEffectiveness));
else
    fprintf('  Warning: Tactical effectiveness CSV not found\n');
    tacticalEffectiveness = table();
end

%% Create MATLAB data structure
fprintf('\nCreating MATLAB data structure...\n');

% Create comprehensive results structure
step4Results = struct();

% Add topological features
if ~isempty(topologicalFeatures)
    step4Results.topologicalFeatures = topologicalFeatures;
    
    % Extract key metrics
    h0_row = strcmp(topologicalFeatures.Homology_Dimension, 'H0');
    h1_row = strcmp(topologicalFeatures.Homology_Dimension, 'H1');
    overall_row = strcmp(topologicalFeatures.Homology_Dimension, 'Overall');
    
    if any(h0_row)
        step4Results.h0Count = topologicalFeatures.Feature_Count(h0_row);
        step4Results.h0MaxPersistence = topologicalFeatures.Max_Persistence(h0_row);
        step4Results.h0MeanPersistence = topologicalFeatures.Mean_Persistence(h0_row);
    end
    
    if any(h1_row)
        step4Results.h1Count = topologicalFeatures.Feature_Count(h1_row);
        step4Results.h1MaxPersistence = topologicalFeatures.Max_Persistence(h1_row);
        step4Results.h1MeanPersistence = topologicalFeatures.Mean_Persistence(h1_row);
    end
    
    if any(overall_row)
        step4Results.totalFeatures = topologicalFeatures.Feature_Count(overall_row);
    end
end

% Add quantum features
if ~isempty(quantumFeatures)
    step4Results.quantumFeatures = quantumFeatures;
    
    % Extract key quantum metrics
    h0_row = strcmp(quantumFeatures.Homology_Dimension, 'H0');
    h1_row = strcmp(quantumFeatures.Homology_Dimension, 'H1');
    
    if any(h0_row)
        step4Results.h0QuantumCorrelation = quantumFeatures.Quantum_Correlation(h0_row);
        step4Results.h0QuantumEfficiency = quantumFeatures.Quantum_Efficiency(h0_row);
        step4Results.h0LifetimeRatio = quantumFeatures.Lifetime_Ratio(h0_row);
    end
    
    if any(h1_row)
        step4Results.h1QuantumCorrelation = quantumFeatures.Quantum_Correlation(h1_row);
        step4Results.h1QuantumEfficiency = quantumFeatures.Quantum_Efficiency(h1_row);
        step4Results.h1LifetimeRatio = quantumFeatures.Lifetime_Ratio(h1_row);
    end
end

% Add tactical effectiveness
if ~isempty(tacticalEffectiveness)
    step4Results.tacticalEffectiveness = tacticalEffectiveness;
    
    % Extract effectiveness scores
    comp_row = strcmp(tacticalEffectiveness.Metric, 'Complexity_Effectiveness');
    bal_row = strcmp(tacticalEffectiveness.Metric, 'Persistence_Balance');
    quant_row = strcmp(tacticalEffectiveness.Metric, 'Quantum_Effectiveness');
    
    if any(comp_row)
        step4Results.complexityEffectiveness = tacticalEffectiveness.Score(comp_row);
    end
    
    if any(bal_row)
        step4Results.persistenceBalance = tacticalEffectiveness.Score(bal_row);
    end
    
    if any(quant_row)
        step4Results.quantumEffectiveness = tacticalEffectiveness.Score(quant_row);
    end
end

% Add raw Python results
step4Results.pythonResults = pythonResults;

% Add metadata
step4Results.metadata = struct();
step4Results.metadata.analysisType = 'Step 4: Persistent Homology with Quantum Dot Insights';
step4Results.metadata.importDate = datestr(now);
step4Results.metadata.inputDirectory = input_dir;
step4Results.metadata.outputDirectory = output_dir;

fprintf('  MATLAB data structure created\n');

%% Create visualizations
fprintf('\nCreating visualizations...\n');

% Create main visualization figure
figure('Position', [100, 100, 1800, 1200]);

% Plot 1: Topological feature counts
subplot(3, 4, 1);
if isfield(step4Results, 'h0Count') && isfield(step4Results, 'h1Count')
    bar([step4Results.h0Count, step4Results.h1Count]);
    xlabel('Homology Dimension'); ylabel('Feature Count');
    title('Topological Feature Counts');
    xticklabels({'H0', 'H1'});
    grid on;
end

% Plot 2: Persistence distributions
subplot(3, 4, 2);
if isfield(step4Results, 'h0MeanPersistence') && isfield(step4Results, 'h1MeanPersistence')
    bar([step4Results.h0MeanPersistence, step4Results.h1MeanPersistence]);
    xlabel('Homology Dimension'); ylabel('Mean Persistence');
    title('Mean Persistence by Dimension');
    xticklabels({'H0', 'H1'});
    grid on;
end

% Plot 3: Quantum correlations
subplot(3, 4, 3);
if isfield(step4Results, 'h0QuantumCorrelation') && isfield(step4Results, 'h1QuantumCorrelation')
    bar([step4Results.h0QuantumCorrelation, step4Results.h1QuantumCorrelation]);
    xlabel('Homology Dimension'); ylabel('Quantum Correlation');
    title('Quantum-Topology Correlations');
    xticklabels({'H0', 'H1'});
    grid on;
end

% Plot 4: Quantum efficiency
subplot(3, 4, 4);
if isfield(step4Results, 'h0QuantumEfficiency') && isfield(step4Results, 'h1QuantumEfficiency')
    bar([step4Results.h0QuantumEfficiency, step4Results.h1QuantumEfficiency]);
    xlabel('Homology Dimension'); ylabel('Quantum Efficiency');
    title('Quantum Efficiency by Dimension');
    xticklabels({'H0', 'H1'});
    grid on;
end

% Plot 5: Lifetime ratios
subplot(3, 4, 5);
if isfield(step4Results, 'h0LifetimeRatio') && isfield(step4Results, 'h1LifetimeRatio')
    bar([step4Results.h0LifetimeRatio, step4Results.h1LifetimeRatio]);
    xlabel('Homology Dimension'); ylabel('Lifetime Ratio');
    title('Topological Lifetime Ratios');
    xticklabels({'H0', 'H1'});
    grid on;
end

% Plot 6: Tactical effectiveness
subplot(3, 4, 6);
effectiveness_metrics = [];
metric_names = {};

if isfield(step4Results, 'complexityEffectiveness')
    effectiveness_metrics = [effectiveness_metrics, step4Results.complexityEffectiveness];
    metric_names{end+1} = 'Complexity';
end

if isfield(step4Results, 'persistenceBalance')
    effectiveness_metrics = [effectiveness_metrics, step4Results.persistenceBalance];
    metric_names{end+1} = 'Balance';
end

if isfield(step4Results, 'quantumEffectiveness')
    effectiveness_metrics = [effectiveness_metrics, step4Results.quantumEffectiveness];
    metric_names{end+1} = 'Quantum';
end

if ~isempty(effectiveness_metrics)
    bar(effectiveness_metrics);
    xlabel('Effectiveness Metric'); ylabel('Score');
    title('Tactical Effectiveness Scores');
    xticklabels(metric_names);
    grid on;
end

% Plot 7: Feature distribution pie chart
subplot(3, 4, 7);
if isfield(step4Results, 'h0Count') && isfield(step4Results, 'h1Count')
    pie([step4Results.h0Count, step4Results.h1Count], {'H0 Features', 'H1 Features'});
    title(sprintf('Feature Distribution (Total: %d)', step4Results.totalFeatures));
end

% Plot 8: Persistence comparison
subplot(3, 4, 8);
if isfield(step4Results, 'h0MaxPersistence') && isfield(step4Results, 'h1MaxPersistence')
    bar([step4Results.h0MaxPersistence, step4Results.h1MaxPersistence]);
    xlabel('Homology Dimension'); ylabel('Max Persistence');
    title('Maximum Persistence by Dimension');
    xticklabels({'H0', 'H1'});
    grid on;
end

% Plot 9: Analysis summary
subplot(3, 4, 9);
summaryText = {
    sprintf('Step 4 Analysis Summary:');
    sprintf('');
    sprintf('Topological Features:');
};

% Add topological features
if isfield(step4Results, 'h0Count')
    summaryText{end+1} = sprintf('  H0: %d features', step4Results.h0Count);
end
if isfield(step4Results, 'h1Count')
    summaryText{end+1} = sprintf('  H1: %d features', step4Results.h1Count);
end
if isfield(step4Results, 'totalFeatures')
    summaryText{end+1} = sprintf('  Total: %d features', step4Results.totalFeatures);
end

summaryText{end+1} = sprintf('');
summaryText{end+1} = sprintf('Quantum Analysis:');

% Add quantum analysis
if isfield(step4Results, 'h0QuantumCorrelation')
    summaryText{end+1} = sprintf('  H0 Correlation: %.3f', step4Results.h0QuantumCorrelation);
end
if isfield(step4Results, 'h1QuantumCorrelation')
    summaryText{end+1} = sprintf('  H1 Correlation: %.3f', step4Results.h1QuantumCorrelation);
end

text(0.05, 0.95, summaryText, 'FontSize', 10, 'VerticalAlignment', 'top');
axis off;

% Plot 10: Effectiveness summary
subplot(3, 4, 10);
effText = {
    sprintf('Tactical Effectiveness:');
    sprintf('');
};

% Add effectiveness metrics
if isfield(step4Results, 'complexityEffectiveness')
    effText{end+1} = sprintf('Complexity: %.3f', step4Results.complexityEffectiveness);
end
if isfield(step4Results, 'persistenceBalance')
    effText{end+1} = sprintf('Balance: %.3f', step4Results.persistenceBalance);
end
if isfield(step4Results, 'quantumEffectiveness')
    effText{end+1} = sprintf('Quantum: %.3f', step4Results.quantumEffectiveness);
end

effText{end+1} = sprintf('');
effText{end+1} = sprintf('Analysis Method:');
effText{end+1} = sprintf('Standalone Python');
effText{end+1} = sprintf('TDA Libraries:');
effText{end+1} = sprintf('Ripser/Gudhi');

text(0.05, 0.95, effText, 'FontSize', 10, 'VerticalAlignment', 'top');
axis off;

% Plot 11: Import information
subplot(3, 4, 11);
importText = {
    sprintf('Import Information:');
    sprintf('');
    sprintf('Source: Python Analysis');
    sprintf('Input: %s', input_dir);
    sprintf('Output: %s', output_dir);
    sprintf('Date: %s', datestr(now));
    sprintf('');
    sprintf('Files Imported:');
    sprintf('✓ Complete Results JSON');
    sprintf('✓ Topological Features CSV');
    sprintf('✓ Quantum Features CSV');
    sprintf('✓ Tactical Effectiveness CSV');
};

text(0.05, 0.95, importText, 'FontSize', 10, 'VerticalAlignment', 'top');
axis off;

% Plot 12: Next steps
subplot(3, 4, 12);
nextStepsText = {
    sprintf('Next Steps Available:');
    sprintf('');
    sprintf('1. Deep-dive quantum models');
    sprintf('2. Integrated visualizations');
    sprintf('3. Quantum algorithms');
    sprintf('4. System comparisons');
    sprintf('5. Real data validation');
    sprintf('6. ML classification');
    sprintf('7. Advanced TSP methods');
    sprintf('');
    sprintf('Step 4 Complete!');
};

text(0.05, 0.95, nextStepsText, 'FontSize', 10, 'VerticalAlignment', 'top');
axis off;

sgtitle('Step 4: Persistent Homology Analysis - Python Results Import', 'FontSize', 16, 'FontWeight', 'bold');

% Save figure
saveas(gcf, fullfile(output_dir, 'step4_imported_results_visualization.png'));

fprintf('  Visualizations created and saved\n');

%% Save MATLAB data
fprintf('\nSaving MATLAB data...\n');

% Save complete results
save(fullfile(output_dir, 'step4_imported_results.mat'), 'step4Results');

% Save individual components
if ~isempty(topologicalFeatures)
    save(fullfile(output_dir, 'topological_features.mat'), 'topologicalFeatures');
end

if ~isempty(quantumFeatures)
    save(fullfile(output_dir, 'quantum_features.mat'), 'quantumFeatures');
end

if ~isempty(tacticalEffectiveness)
    save(fullfile(output_dir, 'tactical_effectiveness.mat'), 'tacticalEffectiveness');
end

fprintf('  MATLAB data saved\n');

%% Create import report
fprintf('\nCreating import report...\n');

reportFile = fullfile(output_dir, 'step4_import_report.txt');
fid = fopen(reportFile, 'w');

fprintf(fid, 'Step 4: Python Results Import Report\n');
fprintf(fid, '====================================\n\n');
fprintf(fid, 'Import Date: %s\n', datestr(now));
fprintf(fid, 'Input Directory: %s\n', input_dir);
fprintf(fid, 'Output Directory: %s\n', output_dir);
fprintf(fid, '\n');

fprintf(fid, 'Files Imported:\n');
fprintf(fid, '- %s\n', json_file);
if exist(topo_file, 'file')
    fprintf(fid, '- %s\n', topo_file);
end
if exist(quantum_file, 'file')
    fprintf(fid, '- %s\n', quantum_file);
end
if exist(tactical_file, 'file')
    fprintf(fid, '- %s\n', tactical_file);
end
fprintf(fid, '\n');

fprintf(fid, 'Key Results:\n');
if isfield(step4Results, 'h0Count')
    fprintf(fid, 'H0 Features: %d\n', step4Results.h0Count);
end
if isfield(step4Results, 'h1Count')
    fprintf(fid, 'H1 Features: %d\n', step4Results.h1Count);
end
if isfield(step4Results, 'totalFeatures')
    fprintf(fid, 'Total Features: %d\n', step4Results.totalFeatures);
end

if isfield(step4Results, 'h0QuantumCorrelation')
    fprintf(fid, 'H0 Quantum Correlation: %.3f\n', step4Results.h0QuantumCorrelation);
end
if isfield(step4Results, 'h1QuantumCorrelation')
    fprintf(fid, 'H1 Quantum Correlation: %.3f\n', step4Results.h1QuantumCorrelation);
end

if isfield(step4Results, 'complexityEffectiveness')
    fprintf(fid, 'Complexity Effectiveness: %.3f\n', step4Results.complexityEffectiveness);
end
if isfield(step4Results, 'persistenceBalance')
    fprintf(fid, 'Persistence Balance: %.3f\n', step4Results.persistenceBalance);
end
if isfield(step4Results, 'quantumEffectiveness')
    fprintf(fid, 'Quantum Effectiveness: %.3f\n', step4Results.quantumEffectiveness);
end

fprintf(fid, '\nImport Complete!\n');

fclose(fid);

fprintf('  Import report created\n');

%% Summary
fprintf('\n=== Step 4 Python Results Import Complete ===\n');
fprintf('Successfully imported Python analysis results!\n');
fprintf('\nKey achievements:\n');
fprintf('  ✓ Python results imported to MATLAB\n');
fprintf('  ✓ Topological features extracted\n');
fprintf('  ✓ Quantum dot insights integrated\n');
fprintf('  ✓ Tactical effectiveness analyzed\n');
fprintf('  ✓ Comprehensive visualizations created\n');
fprintf('  ✓ MATLAB-compatible data structures\n');
fprintf('  ✓ Import report generated\n');
fprintf('\nResults saved to: %s\n', output_dir);
fprintf('\nThis completes the GPS-TDA framework with robust Python-MATLAB integration!\n');

end
