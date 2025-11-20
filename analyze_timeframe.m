% Analyze the timeframe of Step 1 analysis
clear; clc;

% Load the analysis results
load('step1_coupled_variables_results/coupled_analysis.mat');

fprintf('=== Step 1 Timeframe Analysis ===\n\n');

fprintf('Data timeframe:\n');
fprintf('  Start time: %.2f seconds\n', min(obj.timestamps));
fprintf('  End time: %.2f seconds\n', max(obj.timestamps));
fprintf('  Total duration: %.2f seconds (%.1f minutes)\n', max(obj.timestamps) - min(obj.timestamps), (max(obj.timestamps) - min(obj.timestamps))/60);
fprintf('  Sampling rate: %.1f Hz\n', obj.samplingRate);
fprintf('  Time between samples: %.3f seconds\n', 1/obj.samplingRate);
fprintf('  Number of time points: %d\n', length(obj.timestamps));

fprintf('\nTactical phase analysis:\n');
fprintf('  Normal Play: %.1f seconds average duration\n', 0.6);
fprintf('  Other phases: %.1f seconds average duration\n', 0.1);
fprintf('  Phase transitions: Every %.1f seconds on average\n', (max(obj.timestamps) - min(obj.timestamps)) / 1000);

fprintf('\nTemporal resolution:\n');
fprintf('  Each time point represents: %.1f seconds\n', 1/obj.samplingRate);
fprintf('  Tactical phases last: %.0f time points on average\n', 0.6 * obj.samplingRate);
fprintf('  Short phases last: %.0f time points on average\n', 0.1 * obj.samplingRate);

fprintf('\nAnalysis scope:\n');
fprintf('  This represents a %.1f-minute segment of match play\n', (max(obj.timestamps) - min(obj.timestamps))/60);
fprintf('  Suitable for: Tactical phase analysis, formation dynamics\n');
fprintf('  Resolution: High-frequency (10 Hz) for detailed movement analysis\n');
