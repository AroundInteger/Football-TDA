% Create Initial Visualizations for Steps 1 and 2
% This script generates key visualizations to showcase our progress

clear; clc; close all;

fprintf('=== Creating Initial Visualizations for Steps 1 & 2 ===\n\n');

%% Step 1: Load both Step 1 and Step 2 results
fprintf('Loading Step 1 and Step 2 results...\n');

% Load Step 1 results
load('step1_coupled_variables_results/coupled_analysis.mat');
coupledVars = obj;
coupledMetrics = obj.coupledMetrics;
timestamps = obj.timestamps;

% Load Step 2 results
load('step2_state_space_results/state_space_analysis.mat');
stateSpace = obj;

fprintf('Both datasets loaded successfully!\n');

%% Step 2: Create comprehensive overview visualization
fprintf('Creating comprehensive overview visualization...\n');

% Create main overview figure
figure('Position', [100, 100, 1800, 1200]);

% Plot 1: Step 1 - Inter-Team Distance Evolution
subplot(3, 4, 1);
plot(timestamps, coupledMetrics.InterTeamDistance, 'b-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Distance (m)');
title('Step 1: Inter-Team Distance (Field Stretch)');
grid on;
ylim([0, 80]);

% Plot 2: Step 1 - Team Area Ratio
subplot(3, 4, 2);
plot(timestamps, coupledMetrics.TeamAreaRatio, 'r-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Ratio');
title('Step 1: Team Area Ratio (Home/Away)');
yline(1, 'k--', 'LineWidth', 1);
grid on;
ylim([0.8, 1.4]);

% Plot 3: Step 1 - NOD Analysis
subplot(3, 4, 3);
plot(timestamps, coupledMetrics.HomeMeanNOD, 'b-', 'LineWidth', 2);
hold on;
plot(timestamps, coupledMetrics.AwayMeanNOD, 'r-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Distance (m)');
title('Step 1: Nearest Opponent Distance');
legend('Home', 'Away', 'Location', 'best');
grid on;

% Plot 4: Step 1 - Tactical Phases
subplot(3, 4, 4);
% Recreate tactical phase analysis
interDist = coupledMetrics.InterTeamDistance;
areaRatio = coupledMetrics.TeamAreaRatio;
validInterDist = interDist(~isnan(interDist));
validAreaRatio = areaRatio(~isnan(areaRatio));

interDistLow = prctile(validInterDist, 25);
interDistHigh = prctile(validInterDist, 75);
areaRatioLow = prctile(validAreaRatio, 25);
areaRatioHigh = prctile(validAreaRatio, 75);

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

scatter(timestamps, phases, 50, phases, 'filled');
xlabel('Time (s)'); ylabel('Tactical Phase');
title('Step 1: Tactical Phase Identification');
ylim([-0.5, 4.5]);
yticks([0, 1, 2, 3, 4]);
yticklabels({'Unknown', 'Compact', 'High Press', 'Counter', 'Normal'});
colorbar;

% Plot 5: Step 2 - State Vectors Over Time
subplot(3, 4, 5);
stateVars = {'InterTeamDistance', 'TeamAreaRatio', 'HomeMeanNOD', 'AwayMeanNOD'};
colors = {'b', 'r', 'g', 'm'};
for i = 1:length(stateVars)
    if ismember(stateVars{i}, stateSpace.coupledMetrics.Properties.VariableNames)
        values = stateSpace.coupledMetrics.(stateVars{i});
        % Normalize for visualization
        validValues = ~isnan(values);
        if sum(validValues) > 0
            normalizedValues = (values - mean(values(validValues))) / std(values(validValues));
            plot(timestamps, normalizedValues, colors{i}, 'LineWidth', 1.5);
            hold on;
        end
    end
end
xlabel('Time (s)'); ylabel('Normalized Value');
title('Step 2: State Vectors (Normalized)');
legend(stateVars, 'Location', 'best');
grid on;

% Plot 6: Step 2 - 2D State Space Projection
subplot(3, 4, 6);
if size(stateSpace.stateVectors, 2) >= 2
    nStateVectors = size(stateSpace.stateVectors, 1);
    nAttractorLabels = length(stateSpace.attractorLabels);
    minLength = min(nStateVectors, nAttractorLabels);
    
    scatter(stateSpace.stateVectors(1:minLength, 1), stateSpace.stateVectors(1:minLength, 2), ...
            50, stateSpace.attractorLabels(1:minLength), 'filled');
    xlabel('Inter-Team Distance (norm)');
    ylabel('Team Area Ratio (norm)');
    title('Step 2: 2D State Space');
    colorbar;
    grid on;
end

% Plot 7: Step 2 - Attractor Evolution
subplot(3, 4, 7);
plot(timestamps(1:length(stateSpace.attractorLabels)), stateSpace.attractorLabels, 'b-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Attractor State');
title('Step 2: Attractor Evolution');
ylim([0.5, stateSpace.attractorStates.nClusters + 0.5]);
yticks(1:stateSpace.attractorStates.nClusters);
grid on;

% Plot 8: Step 2 - Attractor Frequency
subplot(3, 4, 8);
bar(1:stateSpace.attractorStates.nClusters, stateSpace.attractorMetrics.frequency * 100);
xlabel('Attractor State'); ylabel('Frequency (%)');
title('Step 2: Attractor Frequency');
grid on;

% Plot 9: Step 2 - Transition Matrix
subplot(3, 4, 9);
imagesc(stateSpace.transitionMatrix);
colorbar;
xlabel('To Attractor'); ylabel('From Attractor');
title('Step 2: Transition Matrix');
xticks(1:stateSpace.attractorStates.nClusters);
yticks(1:stateSpace.attractorStates.nClusters);

% Plot 10: Combined Analysis - Coupled Metrics vs Attractors
subplot(3, 4, 10);
yyaxis left;
plot(timestamps, coupledMetrics.InterTeamDistance, 'b-', 'LineWidth', 2);
ylabel('Inter-Team Distance (m)');
yyaxis right;
plot(timestamps(1:length(stateSpace.attractorLabels)), stateSpace.attractorLabels, 'r-', 'LineWidth', 2);
ylabel('Attractor State');
xlabel('Time (s)');
title('Combined: Distance vs Attractors');
grid on;

% Plot 11: Attractor Characteristics Summary
subplot(3, 4, 11);
% Create a summary of attractor characteristics
attractorData = [stateSpace.attractorMetrics.frequency * 100, ...
                 stateSpace.attractorMetrics.duration, ...
                 stateSpace.attractorMetrics.stability * 10]; % Scale stability for visibility

bar(attractorData);
xlabel('Attractor State');
ylabel('Value');
title('Attractor Characteristics');
legend('Frequency (%)', 'Duration (steps)', 'Stability (×10)', 'Location', 'best');
grid on;

% Plot 12: Analysis Summary
subplot(3, 4, 12);
summaryText = {
    sprintf('GPS-TDA Analysis Summary:');
    sprintf('');
    sprintf('Step 1 - Coupled Variables:');
    sprintf('  • Inter-team dynamics');
    sprintf('  • Team shape coupling');
    sprintf('  • NOD analysis');
    sprintf('  • Tactical phases: 5 types');
    sprintf('');
    sprintf('Step 2 - State Space:');
    sprintf('  • Embedding: 3D, delay=2');
    sprintf('  • Attractors: %d states', stateSpace.attractorStates.nClusters);
    sprintf('  • Transitions: %d×%d matrix', size(stateSpace.transitionMatrix, 1), size(stateSpace.transitionMatrix, 2));
    sprintf('');
    sprintf('Next: Step 3 - Zero-Sum &');
    sprintf('      Symmetry Breaking');
};

text(0.05, 0.95, summaryText, 'FontSize', 10, 'VerticalAlignment', 'top', 'FontWeight', 'bold');
axis off;

sgtitle('GPS-TDA Framework: Steps 1 & 2 Analysis Overview', 'FontSize', 16, 'FontWeight', 'bold');

%% Step 3: Save the visualization
fprintf('Saving overview visualization...\n');
saveas(gcf, 'GPS_TDA_Steps1_2_Overview.png');
fprintf('Overview visualization saved as: GPS_TDA_Steps1_2_Overview.png\n');

%% Step 4: Create detailed Step 1 visualization
fprintf('Creating detailed Step 1 visualization...\n');

figure('Position', [200, 200, 1600, 1000]);

% Plot 1: Inter-team distance with tactical phases
subplot(2, 3, 1);
plot(timestamps, coupledMetrics.InterTeamDistance, 'b-', 'LineWidth', 2);
hold on;
% Add phase background colors
phaseColors = [0.9 0.9 0.9; 0.8 0.8 1; 1 0.8 0.8; 0.8 1 0.8; 1 1 0.8];
for i = 1:5
    phaseIndices = find(phases == i-1);
    if ~isempty(phaseIndices)
        for j = 1:length(phaseIndices)
            xline(timestamps(phaseIndices(j)), 'Color', phaseColors(i, :), 'LineWidth', 3, 'Alpha', 0.3);
        end
    end
end
xlabel('Time (s)'); ylabel('Distance (m)');
title('Inter-Team Distance with Tactical Phases');
grid on;

% Plot 2: Team area evolution
subplot(2, 3, 2);
plot(timestamps, coupledMetrics.HomeTeamArea, 'b-', 'LineWidth', 2);
hold on;
plot(timestamps, coupledMetrics.AwayTeamArea, 'r-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Area (m²)');
title('Team Convex Hull Areas');
legend('Home', 'Away', 'Location', 'best');
grid on;

% Plot 3: NOD distribution
subplot(2, 3, 3);
histogram(coupledMetrics.HomeMeanNOD, 20, 'FaceAlpha', 0.7, 'DisplayName', 'Home');
hold on;
histogram(coupledMetrics.AwayMeanNOD, 20, 'FaceAlpha', 0.7, 'DisplayName', 'Away');
xlabel('NOD (m)'); ylabel('Frequency');
title('Nearest Opponent Distance Distribution');
legend('show');
grid on;

% Plot 4: Shape difference over time
subplot(2, 3, 4);
plot(timestamps, coupledMetrics.ShapeDifference, 'g-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Shape Difference');
title('Team Shape Difference (Home - Away)');
yline(0, 'k--', 'LineWidth', 1);
grid on;

% Plot 5: Pressure intensity
subplot(2, 3, 5);
pressure = 1 ./ (coupledMetrics.InterTeamDistance + 1);
plot(timestamps, pressure, 'm-', 'LineWidth', 2);
xlabel('Time (s)'); ylabel('Pressure Intensity');
title('Tactical Pressure Dynamics');
grid on;

% Plot 6: Step 1 summary statistics
subplot(2, 3, 6);
statsText = {
    sprintf('Step 1 Summary Statistics:');
    sprintf('');
    sprintf('Inter-Team Distance:');
    sprintf('  Mean: %.1f ± %.1f m', nanmean(coupledMetrics.InterTeamDistance), nanstd(coupledMetrics.InterTeamDistance));
    sprintf('  Range: %.1f - %.1f m', nanmin(coupledMetrics.InterTeamDistance), nanmax(coupledMetrics.InterTeamDistance));
    sprintf('');
    sprintf('Team Area Ratio:');
    sprintf('  Mean: %.2f ± %.2f', nanmean(coupledMetrics.TeamAreaRatio), nanstd(coupledMetrics.TeamAreaRatio));
    sprintf('');
    sprintf('NOD Analysis:');
    sprintf('  Home: %.1f ± %.1f m', nanmean(coupledMetrics.HomeMeanNOD), nanstd(coupledMetrics.HomeMeanNOD));
    sprintf('  Away: %.1f ± %.1f m', nanmean(coupledMetrics.AwayMeanNOD), nanstd(coupledMetrics.AwayMeanNOD));
    sprintf('');
    sprintf('Tactical Phases:');
};

% Add tactical phase statistics
phaseNames = {'Unknown', 'Compact Defense', 'High Press', 'Counter-Attack', 'Normal Play'};
for i = 1:5
    phaseCount = sum(phases == i-1);
    statsText{end+1} = sprintf('  %s: %d (%.1f%%)', phaseNames{i}, phaseCount, 100*phaseCount/length(phases));
end

text(0.05, 0.95, statsText, 'FontSize', 10, 'VerticalAlignment', 'top');
axis off;

sgtitle('Step 1: Coupled Collective Variables - Detailed Analysis', 'FontSize', 16, 'FontWeight', 'bold');

% Save Step 1 visualization
saveas(gcf, 'GPS_TDA_Step1_Detailed.png');
fprintf('Step 1 detailed visualization saved as: GPS_TDA_Step1_Detailed.png\n');

%% Step 5: Create detailed Step 2 visualization
fprintf('Creating detailed Step 2 visualization...\n');

figure('Position', [300, 300, 1600, 1000]);

% Plot 1: State space trajectory
subplot(2, 3, 1);
if size(stateSpace.stateVectors, 2) >= 2
    nStateVectors = size(stateSpace.stateVectors, 1);
    nAttractorLabels = length(stateSpace.attractorLabels);
    minLength = min(nStateVectors, nAttractorLabels);
    
    scatter(stateSpace.stateVectors(1:minLength, 1), stateSpace.stateVectors(1:minLength, 2), ...
            50, stateSpace.attractorLabels(1:minLength), 'filled');
    xlabel('Inter-Team Distance (norm)');
    ylabel('Team Area Ratio (norm)');
    title('State Space Trajectory');
    colorbar;
    grid on;
end

% Plot 2: Attractor evolution with transitions
subplot(2, 3, 2);
plot(timestamps(1:length(stateSpace.attractorLabels)), stateSpace.attractorLabels, 'b-', 'LineWidth', 2);
hold on;
% Mark transitions
for i = 1:length(stateSpace.attractorLabels)-1
    if stateSpace.attractorLabels(i) ~= stateSpace.attractorLabels(i+1)
        xline(timestamps(i), 'r--', 'LineWidth', 1, 'Alpha', 0.7);
    end
end
xlabel('Time (s)'); ylabel('Attractor State');
title('Attractor Evolution with Transitions');
ylim([0.5, stateSpace.attractorStates.nClusters + 0.5]);
yticks(1:stateSpace.attractorStates.nClusters);
grid on;

% Plot 3: Attractor stability analysis
subplot(2, 3, 3);
bar(1:stateSpace.attractorStates.nClusters, stateSpace.attractorMetrics.stability);
xlabel('Attractor State'); ylabel('Stability');
title('Attractor Stability');
grid on;

% Plot 4: Transition network
subplot(2, 3, 4);
% Create a simple network visualization
G = digraph(stateSpace.transitionMatrix);
plot(G, 'Layout', 'force', 'NodeLabel', 1:stateSpace.attractorStates.nClusters, ...
     'EdgeLabel', arrayfun(@(x) sprintf('%.2f', x), G.Edges.Weight, 'UniformOutput', false));
title('Attractor Transition Network');
axis off;

% Plot 5: Embedding quality
subplot(2, 3, 5);
% Plot WCSS for different cluster numbers
if isfield(stateSpace.attractorStates, 'wcss')
    plot(1:length(stateSpace.attractorStates.wcss), stateSpace.attractorStates.wcss, 'bo-', 'LineWidth', 2);
    xlabel('Number of Clusters'); ylabel('Within-Cluster Sum of Squares');
    title('Embedding Quality (Elbow Method)');
    grid on;
end

% Plot 6: Step 2 summary statistics
subplot(2, 3, 6);
statsText = {
    sprintf('Step 2 Summary Statistics:');
    sprintf('');
    sprintf('State Space Parameters:');
    sprintf('  Embedding Dimension: %d', stateSpace.embeddingDimension);
    sprintf('  Time Delay: %d steps', stateSpace.timeDelay);
    sprintf('  State Variables: %d', length(stateSpace.stateVariables));
    sprintf('');
    sprintf('Attractor Analysis:');
    sprintf('  Number of Attractors: %d', stateSpace.attractorStates.nClusters);
    sprintf('  State Vectors: %d', size(stateSpace.stateVectors, 1));
    sprintf('  Embedded Vectors: %d', size(stateSpace.embeddedVectors, 1));
    sprintf('');
    sprintf('Attractor Characteristics:');
};

% Add attractor characteristics
for i = 1:stateSpace.attractorStates.nClusters
    statsText{end+1} = sprintf('  Attractor %d: %.1f%% freq, %.1f steps duration', i, ...
            100*stateSpace.attractorMetrics.frequency(i), stateSpace.attractorMetrics.duration(i));
end

statsText{end+1} = sprintf('');
statsText{end+1} = sprintf('Computation Time: %.2f seconds', stateSpace.computationTime);

text(0.05, 0.95, statsText, 'FontSize', 10, 'VerticalAlignment', 'top');
axis off;

sgtitle('Step 2: State Space Reconstruction - Detailed Analysis', 'FontSize', 16, 'FontWeight', 'bold');

% Save Step 2 visualization
saveas(gcf, 'GPS_TDA_Step2_Detailed.png');
fprintf('Step 2 detailed visualization saved as: GPS_TDA_Step2_Detailed.png\n');

%% Step 6: Summary
fprintf('\n=== Initial Visualizations Complete ===\n');
fprintf('Successfully created comprehensive visualizations for Steps 1 & 2!\n');
fprintf('\nGenerated visualizations:\n');
fprintf('  ✓ GPS_TDA_Steps1_2_Overview.png - Comprehensive overview\n');
fprintf('  ✓ GPS_TDA_Step1_Detailed.png - Detailed Step 1 analysis\n');
fprintf('  ✓ GPS_TDA_Step2_Detailed.png - Detailed Step 2 analysis\n');
fprintf('\nThese visualizations showcase:\n');
fprintf('  • Coupled collective variables analysis\n');
fprintf('  • Tactical phase identification\n');
fprintf('  • State space reconstruction\n');
fprintf('  • Attractor identification and dynamics\n');
fprintf('  • Transition analysis\n');
fprintf('\nReady to proceed to Step 3: Zero-Sum Competition & Symmetry Breaking!\n');
