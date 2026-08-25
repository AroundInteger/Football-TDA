%% TDA Metrics Schematic Guide - MATLAB Version
% Visual explanations of TDA concepts for non-technical audiences
% Professional schematics explaining H0, H1, Complexity Index, Quantum States, and Nash Equilibrium

function TDAMetricsSchematicGuide()
    %% Initialize
    clc; clear; close all;
    
    fprintf('🚀 TDA Metrics Schematic Guide - MATLAB Version\n');
    fprintf('==============================================\n');
    
    % Set up figure properties
    set(0, 'DefaultFigureColor', 'white');
    set(0, 'DefaultAxesFontSize', 12);
    set(0, 'DefaultAxesFontWeight', 'bold');
    
    %% Create all schematic explanations
    fprintf('🎨 Generating metric explanation schematics...\n');
    
    % 1. H0 Explanation Schematic
    createH0ExplanationSchematic();
    
    % 2. H1 Explanation Schematic
    createH1ExplanationSchematic();
    
    % 3. Complexity Index Explanation
    createComplexityIndexExplanation();
    
    % 4. Quantum States Explanation
    createQuantumStatesExplanation();
    
    % 5. Nash Equilibrium Explanation
    createNashEquilibriumExplanation();
    
    fprintf('✅ All MATLAB schematic explanations created successfully!\n');
    fprintf('📁 Files saved in current directory\n');
end

function createH0ExplanationSchematic()
    %% Create schematic explaining H0 (Connected Components)
    
    figure('Position', [100, 100, 1200, 900]);
    
    % Panel 1: Individual Players (Before Clustering)
    subplot(2, 2, 1);
    % Draw individual players as dots
    player_positions = [2, 8; 3, 7; 4, 6; 6, 8; 7, 7; 8, 6; ...
                       2, 3; 3, 2; 4, 1; 6, 3; 7, 2; 8, 1];
    
    scatter(player_positions(:, 1), player_positions(:, 2), 100, [0.8, 0.2, 0.2], 'filled', 'Alpha', 0.8);
    hold on;
    
    % Add player labels
    for i = 1:size(player_positions, 1)
        text(player_positions(i, 1), player_positions(i, 2) - 0.6, sprintf('P%d', i), ...
             'HorizontalAlignment', 'center', 'FontSize', 8, 'FontWeight', 'bold');
    end
    
    xlim([0, 10]);
    ylim([0, 10]);
    xlabel('Field Position');
    ylabel('Field Position');
    title('Individual Players (22 separate points)', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Add annotation
    annotation('textbox', [0.1, 0.85, 0.3, 0.1], 'String', 'H0 = 22 (Artifact: Just counting players)', ...
               'FontSize', 11, 'FontWeight', 'bold', 'Color', 'red', ...
               'BackgroundColor', 'white', 'EdgeColor', 'red');
    
    % Panel 2: Clustered Players (After GPS-Aware Clustering)
    subplot(2, 2, 2);
    % Define clusters
    cluster_centers = [2.5, 7; 7, 7; 2.5, 2; 7, 2; 5, 5];
    cluster_labels = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4];
    colors = [0.8, 0.2, 0.2; 0.2, 0.8, 0.6; 0.2, 0.5, 0.8; 0.6, 0.8, 0.6; 1, 0.9, 0.6];
    
    for i = 1:5
        cluster_points = find(cluster_labels == i);
        if ~isempty(cluster_points)
            % Add noise around cluster center
            x_cluster = cluster_centers(i, 1) + 0.5 * randn(1, length(cluster_points));
            y_cluster = cluster_centers(i, 2) + 0.5 * randn(1, length(cluster_points));
            
            scatter(x_cluster, y_cluster, 100, colors(i, :), 'filled', 'Alpha', 0.8);
            hold on;
            
            % Draw cluster boundary
            viscircles(cluster_centers(i, :), 1.2, 'Color', colors(i, :), 'LineWidth', 3);
            
            % Label cluster
            text(cluster_centers(i, 1), cluster_centers(i, 2), sprintf('C%d', i), ...
                 'HorizontalAlignment', 'center', 'FontSize', 12, 'FontWeight', 'bold', ...
                 'BackgroundColor', 'white');
        end
    end
    
    xlim([0, 10]);
    ylim([0, 10]);
    xlabel('Field Position');
    ylabel('Field Position');
    title('GPS-Aware Clustering (5 distinct groups)', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Add annotation
    annotation('textbox', [0.6, 0.85, 0.3, 0.1], 'String', 'H0 = 5 (Meaningful: Number of player groups)', ...
               'FontSize', 11, 'FontWeight', 'bold', 'Color', 'green', ...
               'BackgroundColor', 'white', 'EdgeColor', 'green');
    
    % Panel 3: Real Football Example
    subplot(2, 2, 3);
    % Draw football field
    rectangle('Position', [1, 1, 8, 8], 'EdgeColor', 'black', 'LineWidth', 2);
    
    % Draw goal areas
    rectangle('Position', [0.5, 3, 0.5, 4], 'EdgeColor', 'black', 'LineWidth', 2);
    rectangle('Position', [9, 3, 0.5, 4], 'EdgeColor', 'black', 'LineWidth', 2);
    
    % Draw player formations
    % Home team (blue)
    home_positions = [2, 2; 2.5, 3; 2, 4; 2.5, 5; 2, 6; 2.5, 7; 2, 8];
    scatter(home_positions(:, 1), home_positions(:, 2), 50, [0, 0, 1], 'filled', 'Alpha', 0.8);
    hold on;
    
    % Away team (red)
    away_positions = [8, 2; 7.5, 3; 8, 4; 7.5, 5; 8, 6; 7.5, 7; 8, 8];
    scatter(away_positions(:, 1), away_positions(:, 2), 50, [1, 0, 0], 'filled', 'Alpha', 0.8);
    
    % Draw cluster boundaries
    viscircles([2.25, 5], 1.5, 'Color', [0, 0, 1], 'LineWidth', 2, 'Alpha', 0.6);
    viscircles([7.75, 5], 1.5, 'Color', [1, 0, 0], 'LineWidth', 2, 'Alpha', 0.6);
    
    xlim([0, 10]);
    ylim([0, 10]);
    xlabel('Field Position');
    ylabel('Field Position');
    title('Real Football Example: H0 = 2 (Home vs Away formations)', 'FontSize', 14, 'FontWeight', 'bold');
    
    % Add annotation
    annotation('textbox', [0.1, 0.35, 0.8, 0.1], 'String', 'H0 tells us how many distinct team formations exist', ...
               'FontSize', 11, 'FontWeight', 'bold', 'BackgroundColor', 'lightblue');
    
    % Panel 4: Interpretation Guide
    subplot(2, 2, 4);
    interpretations = {
        'H0 = 1: Single formation (All players together)', 'lightgreen';
        'H0 = 2-3: Few formations (Simple tactics)', 'lightblue';
        'H0 = 4-6: Multiple formations (Complex tactics)', 'lightyellow';
        'H0 = 7+: Many formations (Very complex tactics)', 'lightcoral'
    };
    
    y_positions = [8, 6, 4, 2];
    
    for i = 1:4
        rectangle('Position', [1, y_positions(i)-0.5, 8, 1], ...
                  'FaceColor', interpretations{i, 2}, 'Alpha', 0.7, 'EdgeColor', 'black');
        text(5, y_positions(i), interpretations{i, 1}, 'HorizontalAlignment', 'center', ...
             'FontSize', 11, 'FontWeight', 'bold');
    end
    
    xlim([0, 10]);
    ylim([0, 10]);
    title('H0 Interpretation Guide: What the numbers mean', 'FontSize', 14, 'FontWeight', 'bold');
    set(gca, 'XTick', [], 'YTick', []);
    
    sgtitle('H0 (Connected Components): What Does It Mean?', 'FontSize', 18, 'FontWeight', 'bold');
    
    % Save figure
    saveas(gcf, 'h0_explanation_schematic_matlab.png');
    saveas(gcf, 'h0_explanation_schematic_matlab.fig');
end

function createH1ExplanationSchematic()
    %% Create schematic explaining H1 (Formation Complexity)
    
    figure('Position', [100, 100, 1200, 900]);
    
    % Panel 1: Simple Formation (H1 = 0)
    subplot(2, 2, 1);
    % Draw simple line formation
    positions = [2, 5; 3, 5; 4, 5; 5, 5; 6, 5; 7, 5];
    
    scatter(positions(:, 1), positions(:, 2), 100, [0.8, 0.2, 0.2], 'filled', 'Alpha', 0.8);
    hold on;
    
    % Add player labels
    for i = 1:size(positions, 1)
        text(positions(i, 1), positions(i, 2) - 0.6, sprintf('P%d', i), ...
             'HorizontalAlignment', 'center', 'FontSize', 8, 'FontWeight', 'bold');
    end
    
    % Draw connections
    for i = 1:size(positions, 1)-1
        plot([positions(i, 1), positions(i+1, 1)], [positions(i, 2), positions(i+1, 2)], ...
             'k-', 'LineWidth', 2, 'Alpha', 0.6);
    end
    
    xlim([0, 10]);
    ylim([0, 10]);
    xlabel('Field Position');
    ylabel('Field Position');
    title('Simple Formation (Straight line)', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Add annotation
    annotation('textbox', [0.1, 0.85, 0.3, 0.1], 'String', 'H1 = 0 (No holes or loops)', ...
               'FontSize', 11, 'FontWeight', 'bold', 'Color', 'green', ...
               'BackgroundColor', 'white', 'EdgeColor', 'green');
    
    % Panel 2: Complex Formation (H1 = 1)
    subplot(2, 2, 2);
    % Draw triangular formation
    positions = [3, 7; 5, 5; 7, 7; 4, 3; 6, 3];
    
    scatter(positions(:, 1), positions(:, 2), 100, [0.8, 0.2, 0.2], 'filled', 'Alpha', 0.8);
    hold on;
    
    % Add player labels
    for i = 1:size(positions, 1)
        text(positions(i, 1), positions(i, 2) - 0.6, sprintf('P%d', i), ...
             'HorizontalAlignment', 'center', 'FontSize', 8, 'FontWeight', 'bold');
    end
    
    % Draw triangular connections
    triangle_edges = [1, 2; 2, 3; 3, 1; 2, 4; 4, 5; 5, 2];
    for i = 1:size(triangle_edges, 1)
        start_idx = triangle_edges(i, 1);
        end_idx = triangle_edges(i, 2);
        plot([positions(start_idx, 1), positions(end_idx, 1)], ...
             [positions(start_idx, 2), positions(end_idx, 2)], ...
             'k-', 'LineWidth', 2, 'Alpha', 0.6);
    end
    
    % Highlight the hole
    viscircles([5, 5.5], 0.8, 'Color', 'red', 'LineWidth', 3);
    text(5, 5.5, 'HOLE', 'HorizontalAlignment', 'center', 'FontSize', 10, ...
         'Color', 'red', 'FontWeight', 'bold');
    
    xlim([0, 10]);
    ylim([0, 10]);
    xlabel('Field Position');
    ylabel('Field Position');
    title('Complex Formation (Triangular with hole)', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Add annotation
    annotation('textbox', [0.6, 0.85, 0.3, 0.1], 'String', 'H1 = 1 (1 hole in formation)', ...
               'FontSize', 11, 'FontWeight', 'bold', 'Color', 'orange', ...
               'BackgroundColor', 'white', 'EdgeColor', 'orange');
    
    % Panel 3: Football Formation Examples
    subplot(2, 2, 3);
    % Draw football field
    rectangle('Position', [1, 1, 8, 8], 'EdgeColor', 'black', 'LineWidth', 2);
    
    % Draw 4-4-2 formation
    % Back line
    back_line = [2, 2; 3, 2; 4, 2; 5, 2];
    % Midfield
    midfield = [2, 4; 3, 4; 4, 4; 5, 4];
    % Forwards
    forwards = [3, 6; 4, 6];
    
    all_positions = [back_line; midfield; forwards];
    
    scatter(all_positions(:, 1), all_positions(:, 2), 50, [0, 0, 1], 'filled', 'Alpha', 0.8);
    hold on;
    
    % Draw formation lines
    plot([2, 5], [2, 2], 'b-', 'LineWidth', 2, 'Alpha', 0.6); % Back line
    plot([2, 5], [4, 4], 'b-', 'LineWidth', 2, 'Alpha', 0.6); % Midfield
    plot([3, 4], [6, 6], 'b-', 'LineWidth', 2, 'Alpha', 0.6); % Forwards
    
    xlim([0, 10]);
    ylim([0, 10]);
    xlabel('Field Position');
    ylabel('Field Position');
    title('4-4-2 Formation: H1 = 2 (2 holes between lines)', 'FontSize', 14, 'FontWeight', 'bold');
    
    % Add annotation
    annotation('textbox', [0.1, 0.35, 0.8, 0.1], 'String', 'H1 measures formation structural complexity', ...
               'FontSize', 11, 'FontWeight', 'bold', 'BackgroundColor', 'lightblue');
    
    % Panel 4: H1 Interpretation Guide
    subplot(2, 2, 4);
    interpretations = {
        'H1 = 0: Simple formations (Straight lines)', 'lightgreen';
        'H1 = 1-2: Moderate complexity (Basic shapes)', 'lightblue';
        'H1 = 3-4: Complex formations (Multiple holes)', 'lightyellow';
        'H1 = 5+: Very complex (Many structural holes)', 'lightcoral'
    };
    
    y_positions = [8, 6, 4, 2];
    
    for i = 1:4
        rectangle('Position', [1, y_positions(i)-0.5, 8, 1], ...
                  'FaceColor', interpretations{i, 2}, 'Alpha', 0.7, 'EdgeColor', 'black');
        text(5, y_positions(i), interpretations{i, 1}, 'HorizontalAlignment', 'center', ...
             'FontSize', 11, 'FontWeight', 'bold');
    end
    
    xlim([0, 10]);
    ylim([0, 10]);
    title('H1 Interpretation Guide: Formation complexity levels', 'FontSize', 14, 'FontWeight', 'bold');
    set(gca, 'XTick', [], 'YTick', []);
    
    sgtitle('H1 (Formation Complexity): What Does It Mean?', 'FontSize', 18, 'FontWeight', 'bold');
    
    % Save figure
    saveas(gcf, 'h1_explanation_schematic_matlab.png');
    saveas(gcf, 'h1_explanation_schematic_matlab.fig');
end

function createComplexityIndexExplanation()
    %% Create schematic explaining Complexity Index
    
    figure('Position', [100, 100, 1200, 900]);
    
    % Panel 1: Formula Explanation
    subplot(2, 2, 1);
    % Draw formula
    text(5, 8, 'Complexity Index =', 'HorizontalAlignment', 'center', 'FontSize', 16, 'FontWeight', 'bold');
    text(5, 6.5, 'H0 + H1', 'HorizontalAlignment', 'center', 'FontSize', 20, 'FontWeight', 'bold', 'Color', 'blue');
    text(5, 5, 'Point Cloud Size', 'HorizontalAlignment', 'center', 'FontSize', 16, 'FontWeight', 'bold');
    
    % Draw division line
    plot([2, 8], [5.5, 5.5], 'k-', 'LineWidth', 3);
    
    % Add explanation
    annotation('textbox', [0.1, 0.25, 0.8, 0.15], 'String', 'Measures overall tactical complexity per player in the formation', ...
               'FontSize', 12, 'FontWeight', 'bold', 'BackgroundColor', 'lightblue');
    
    xlim([0, 10]);
    ylim([0, 10]);
    title('Complexity Index Formula', 'FontSize', 14, 'FontWeight', 'bold');
    set(gca, 'XTick', [], 'YTick', []);
    
    % Panel 2: Example Calculation
    subplot(2, 2, 2);
    % Example values
    h0_example = 5;
    h1_example = 3;
    point_cloud_size = 22;
    
    complexity = (h0_example + h1_example) / point_cloud_size;
    
    text(5, 8, 'Example Calculation:', 'HorizontalAlignment', 'center', 'FontSize', 14, 'FontWeight', 'bold');
    text(5, 6.5, sprintf('H0 = %d', h0_example), 'HorizontalAlignment', 'center', 'FontSize', 16, 'FontWeight', 'bold', 'Color', 'green');
    text(5, 5.5, sprintf('H1 = %d', h1_example), 'HorizontalAlignment', 'center', 'FontSize', 16, 'FontWeight', 'bold', 'Color', 'orange');
    text(5, 4.5, sprintf('Point Cloud Size = %d', point_cloud_size), 'HorizontalAlignment', 'center', 'FontSize', 16, 'FontWeight', 'bold', 'Color', 'blue');
    
    % Draw division line
    plot([2, 8], [4, 4], 'k-', 'LineWidth', 3);
    
    text(5, 3, sprintf('Complexity = %.4f', complexity), 'HorizontalAlignment', 'center', ...
         'FontSize', 18, 'FontWeight', 'bold', 'Color', 'red', ...
         'BackgroundColor', 'lightcoral');
    
    xlim([0, 10]);
    ylim([0, 10]);
    title('Example Calculation', 'FontSize', 14, 'FontWeight', 'bold');
    set(gca, 'XTick', [], 'YTick', []);
    
    % Panel 3: Complexity Levels
    subplot(2, 2, 3);
    complexity_levels = {
        '0.00 - 0.05: Very Simple (Basic formations)', 'lightgreen';
        '0.05 - 0.10: Simple (Standard tactics)', 'lightblue';
        '0.10 - 0.15: Moderate (Complex tactics)', 'lightyellow';
        '0.15 - 0.20: Complex (Advanced tactics)', 'lightcoral';
        '0.20+: Very Complex (Elite tactics)', 'lightpink'
    };
    
    y_positions = [8, 6.5, 5, 3.5, 2];
    
    for i = 1:5
        rectangle('Position', [1, y_positions(i)-0.4, 8, 0.8], ...
                  'FaceColor', complexity_levels{i, 2}, 'Alpha', 0.7, 'EdgeColor', 'black');
        text(5, y_positions(i), complexity_levels{i, 1}, 'HorizontalAlignment', 'center', ...
             'FontSize', 11, 'FontWeight', 'bold');
    end
    
    xlim([0, 10]);
    ylim([0, 10]);
    title('Complexity Index Levels', 'FontSize', 14, 'FontWeight', 'bold');
    set(gca, 'XTick', [], 'YTick', []);
    
    % Panel 4: Real-World Example
    subplot(2, 2, 4);
    % Draw football field
    rectangle('Position', [1, 1, 8, 8], 'EdgeColor', 'black', 'LineWidth', 2);
    
    % Draw formation with complexity
    % Multiple clusters (H0 = 4)
    clusters = [2, 2; 5, 4; 3, 6; 7, 6];
    colors = [0, 0, 1; 0, 0, 1; 0, 0, 1; 0, 0, 1];
    
    for i = 1:4
        scatter(clusters(i, 1), clusters(i, 2), 100, colors(i, :), 'filled', 'Alpha', 0.8);
        hold on;
        text(clusters(i, 1), clusters(i, 2)-0.6, sprintf('C%d', i), ...
             'HorizontalAlignment', 'center', 'FontSize', 10, 'FontWeight', 'bold');
    end
    
    % Draw connections (H1 = 2)
    connections = [1, 2; 2, 3; 2, 4];
    for i = 1:size(connections, 1)
        start_idx = connections(i, 1);
        end_idx = connections(i, 2);
        plot([clusters(start_idx, 1), clusters(end_idx, 1)], ...
             [clusters(start_idx, 2), clusters(end_idx, 2)], ...
             'k-', 'LineWidth', 2, 'Alpha', 0.6);
    end
    
    xlim([0, 10]);
    ylim([0, 10]);
    xlabel('Field Position');
    ylabel('Field Position');
    title('Real Formation Example: H0=4, H1=2, Complexity=0.27', 'FontSize', 14, 'FontWeight', 'bold');
    
    % Add annotation
    annotation('textbox', [0.1, 0.25, 0.8, 0.1], 'String', 'High complexity formation with multiple tactical elements', ...
               'FontSize', 11, 'FontWeight', 'bold', 'BackgroundColor', 'lightcoral');
    
    sgtitle('Complexity Index: Combining H0 and H1', 'FontSize', 18, 'FontWeight', 'bold');
    
    % Save figure
    saveas(gcf, 'complexity_index_explanation_matlab.png');
    saveas(gcf, 'complexity_index_explanation_matlab.fig');
end

function createQuantumStatesExplanation()
    %% Create schematic explaining Quantum States (Tactical States)
    
    figure('Position', [100, 100, 1200, 900]);
    
    % Panel 1: State Concept
    subplot(2, 2, 1);
    % Draw state diagram
    states = {
        'State 0\nDefensive', [2, 8], [0.8, 0.2, 0.2];
        'State 1\nCounter-Attack', [8, 8], [0.2, 0.8, 0.6];
        'State 2\nPossession', [2, 2], [0.2, 0.5, 0.8];
        'State 3\nHigh Press', [8, 2], [0.6, 0.8, 0.6];
        'State 4\nTransition', [5, 5], [1, 0.9, 0.6]
    };
    
    for i = 1:5
        state_name = states{i, 1};
        state_pos = states{i, 2};
        state_color = states{i, 3};
        
        viscircles(state_pos, 0.8, 'Color', state_color, 'LineWidth', 2);
        text(state_pos(1), state_pos(2), state_name, 'HorizontalAlignment', 'center', ...
             'FontSize', 10, 'FontWeight', 'bold');
    end
    
    % Draw transitions
    transitions = [1, 5; 2, 5; 3, 5; 4, 5; 5, 1; 5, 2; 5, 3; 5, 4];
    for i = 1:size(transitions, 1)
        start_pos = states{transitions(i, 1), 2};
        end_pos = states{transitions(i, 2), 2};
        plot([start_pos(1), end_pos(1)], [start_pos(2), end_pos(2)], ...
             'k--', 'LineWidth', 1, 'Alpha', 0.5);
    end
    
    xlim([0, 10]);
    ylim([0, 10]);
    xlabel('Tactical Configuration');
    ylabel('Tactical Configuration');
    title('Tactical States (Team formation patterns)', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Add annotation
    annotation('textbox', [0.1, 0.25, 0.8, 0.1], 'String', 'Teams switch between different tactical states during matches', ...
               'FontSize', 11, 'FontWeight', 'bold', 'BackgroundColor', 'lightblue');
    
    % Panel 2: State Frequencies
    subplot(2, 2, 2);
    state_names = {'Defensive', 'Counter\nAttack', 'Possession', 'High Press', 'Transition'};
    frequencies = [0.234, 0.198, 0.187, 0.201, 0.180];
    colors = [0.8, 0.2, 0.2; 0.2, 0.8, 0.6; 0.2, 0.5, 0.8; 0.6, 0.8, 0.6; 1, 0.9, 0.6];
    
    bars = bar(1:5, frequencies, 'FaceColor', 'flat');
    bars.CData = colors;
    
    % Add value labels
    for i = 1:5
        text(i, frequencies(i) + 0.005, sprintf('%.3f', frequencies(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:5, 'XTickLabel', state_names);
    ylabel('Frequency');
    title('State Frequencies (How often each state occurs)', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Panel 3: Energy Landscapes
    subplot(2, 2, 3);
    % Draw energy landscape
    x = linspace(0, 10, 100);
    y = 5 + 2 * sin(x * 0.8) + 0.5 * sin(x * 2.5);
    
    plot(x, y, 'b-', 'LineWidth', 3, 'Alpha', 0.8);
    hold on;
    fill([x, fliplr(x)], [y, zeros(size(y))], 'b', 'FaceAlpha', 0.3, 'EdgeColor', 'none');
    
    % Mark state positions
    state_x = [2, 4, 6, 8, 5];
    state_y = 5 + 2 * sin(state_x * 0.8) + 0.5 * sin(state_x * 2.5);
    
    for i = 1:5
        scatter(state_x(i), state_y(i), 100, colors(i, :), 'filled', 'Alpha', 0.8);
        text(state_x(i), state_y(i)-0.5, sprintf('S%d', i-1), 'HorizontalAlignment', 'center', ...
             'FontSize', 10, 'FontWeight', 'bold');
    end
    
    xlabel('Tactical Configuration');
    ylabel('Energy Level');
    title('Energy Landscapes (State stability)', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Panel 4: Transition Probabilities
    subplot(2, 2, 4);
    % Draw transition matrix visualization
    transitions = {
        'Defensive', 'Counter', 0.234, [0.8, 0.2, 0.2];
        'Counter', 'Possession', 0.198, [0.2, 0.8, 0.6];
        'Possession', 'High Press', 0.187, [0.2, 0.5, 0.8];
        'High Press', 'Transition', 0.201, [0.6, 0.8, 0.6];
        'Transition', 'Defensive', 0.180, [1, 0.9, 0.6]
    };
    
    y_positions = [8, 6.5, 5, 3.5, 2];
    
    for i = 1:5
        % Draw transition arrow
        arrow_start = [2, y_positions(i)];
        arrow_end = [6, y_positions(i)];
        annotation('arrow', [0.2, 0.6], [y_positions(i)/10, y_positions(i)/10], ...
                  'Color', transitions{i, 4}, 'LineWidth', 2);
        
        % Draw probability bar
        bar_width = transitions{i, 3} * 3;
        rectangle('Position', [6.5, y_positions(i)-0.2, bar_width, 0.4], ...
                  'FaceColor', transitions{i, 4}, 'Alpha', 0.8, 'EdgeColor', 'black');
        
        % Labels
        text(1, y_positions(i), sprintf('%s →', transitions{i, 1}), ...
             'HorizontalAlignment', 'right', 'FontSize', 9, 'FontWeight', 'bold');
        text(6.5 + bar_width + 0.2, y_positions(i), sprintf('%.3f', transitions{i, 3}), ...
             'HorizontalAlignment', 'left', 'FontSize', 9, 'FontWeight', 'bold');
    end
    
    xlim([0, 10]);
    ylim([0, 10]);
    xlabel('Transition Type');
    ylabel('Probability');
    title('Transition Probabilities (How states change)', 'FontSize', 14, 'FontWeight', 'bold');
    set(gca, 'XTick', [], 'YTick', []);
    
    sgtitle('Tactical States: What Are They?', 'FontSize', 18, 'FontWeight', 'bold');
    
    % Save figure
    saveas(gcf, 'quantum_states_explanation_matlab.png');
    saveas(gcf, 'quantum_states_explanation_matlab.fig');
end

function createNashEquilibriumExplanation()
    %% Create schematic explaining Nash Equilibrium
    
    figure('Position', [100, 100, 1200, 900]);
    
    % Panel 1: Game Theory Concept
    subplot(2, 2, 1);
    % Draw payoff matrix
    text(5, 9, 'Game Theory: Team Formation Strategies', ...
         'HorizontalAlignment', 'center', 'FontSize', 14, 'FontWeight', 'bold');
    
    % Draw matrix
    matrix_x = 2;
    matrix_y = 6;
    matrix_width = 6;
    matrix_height = 3;
    
    % Matrix background
    rectangle('Position', [matrix_x, matrix_y, matrix_width, matrix_height], ...
              'FaceColor', 'lightblue', 'Alpha', 0.3, 'EdgeColor', 'black', 'LineWidth', 2);
    
    % Matrix labels
    text(matrix_x + 1, matrix_y + 2.5, 'Home Team', 'HorizontalAlignment', 'center', ...
         'FontSize', 12, 'FontWeight', 'bold');
    text(matrix_x + 3, matrix_y + 2.5, 'Narrow\n(11.44m)', 'HorizontalAlignment', 'center', ...
         'FontSize', 10, 'FontWeight', 'bold');
    text(matrix_x + 5, matrix_y + 2.5, 'Wide\n(12.90m)', 'HorizontalAlignment', 'center', ...
         'FontSize', 10, 'FontWeight', 'bold');
    
    text(matrix_x + 0.5, matrix_y + 1.5, 'Away\nTeam', 'HorizontalAlignment', 'center', ...
         'FontSize', 12, 'FontWeight', 'bold');
    text(matrix_x + 0.5, matrix_y + 0.5, 'Narrow', 'HorizontalAlignment', 'center', ...
         'FontSize', 10, 'FontWeight', 'bold');
    
    % Payoff values
    text(matrix_x + 3, matrix_y + 1.5, '3, 3', 'HorizontalAlignment', 'center', ...
         'FontSize', 12, 'FontWeight', 'bold', 'Color', 'green');
    text(matrix_x + 5, matrix_y + 1.5, '1, 4', 'HorizontalAlignment', 'center', ...
         'FontSize', 12, 'FontWeight', 'bold');
    text(matrix_x + 3, matrix_y + 0.5, '4, 1', 'HorizontalAlignment', 'center', ...
         'FontSize', 12, 'FontWeight', 'bold');
    text(matrix_x + 5, matrix_y + 0.5, '2, 2', 'HorizontalAlignment', 'center', ...
         'FontSize', 12, 'FontWeight', 'bold');
    
    % Highlight Nash equilibrium
    rectangle('Position', [matrix_x + 2.5, matrix_y + 1, 1, 1], ...
              'EdgeColor', 'red', 'LineWidth', 3);
    
    text(5, 3, 'Nash Equilibrium: Both teams choose optimal strategies (11.44m vs 12.90m formation width)', ...
         'HorizontalAlignment', 'center', 'FontSize', 11, 'FontWeight', 'bold', ...
         'BackgroundColor', 'lightgreen');
    
    xlim([0, 10]);
    ylim([0, 10]);
    title('Game Theory Matrix', 'FontSize', 14, 'FontWeight', 'bold');
    set(gca, 'XTick', [], 'YTick', []);
    
    % Panel 2: Formation Width Visualization
    subplot(2, 2, 2);
    % Draw football field
    rectangle('Position', [1, 1, 8, 8], 'EdgeColor', 'black', 'LineWidth', 2);
    
    % Draw goal areas
    rectangle('Position', [0.5, 3, 0.5, 4], 'EdgeColor', 'black', 'LineWidth', 2);
    rectangle('Position', [9, 3, 0.5, 4], 'EdgeColor', 'black', 'LineWidth', 2);
    
    % Draw home team formation (narrow)
    home_positions = [2, 2; 2, 3; 2, 4; 2, 5; 2, 6; 2, 7; 2, 8];
    scatter(home_positions(:, 1), home_positions(:, 2), 50, [0, 0, 1], 'filled', 'Alpha', 0.8);
    hold on;
    
    % Draw away team formation (wide)
    away_positions = [8, 2; 8, 3; 8, 4; 8, 5; 8, 6; 8, 7; 8, 8];
    scatter(away_positions(:, 1), away_positions(:, 2), 50, [1, 0, 0], 'filled', 'Alpha', 0.8);
    
    % Draw formation width lines
    plot([1.5, 1.5], [1, 9], 'b-', 'LineWidth', 3, 'Alpha', 0.6);
    plot([8.5, 8.5], [1, 9], 'r-', 'LineWidth', 3, 'Alpha', 0.6);
    
    xlim([0, 10]);
    ylim([0, 10]);
    xlabel('Field Position');
    ylabel('Field Position');
    title('Nash Equilibrium Formations (Optimal strategies)', 'FontSize', 14, 'FontWeight', 'bold');
    
    % Add legend
    legend('Home: 11.44m', 'Away: 12.90m', 'Location', 'best');
    
    % Add annotation
    annotation('textbox', [0.1, 0.35, 0.8, 0.1], 'String', 'Each team chooses the formation width that maximizes their advantage', ...
               'FontSize', 11, 'FontWeight', 'bold', 'BackgroundColor', 'lightblue');
    
    % Panel 3: Zero-Sum Relationship
    subplot(2, 2, 3);
    % Draw zero-sum relationship
    time_points = linspace(0, 10, 50);
    home_spread = 11.44 + 2 * sin(time_points * 0.5);
    away_spread = 12.90 - 2 * sin(time_points * 0.5);
    total_spread = home_spread + away_spread;
    
    plot(time_points, home_spread, 'b-', 'LineWidth', 3, 'DisplayName', 'Home Team Spread');
    hold on;
    plot(time_points, away_spread, 'r-', 'LineWidth', 3, 'DisplayName', 'Away Team Spread');
    plot(time_points, total_spread, 'Color', [0.5, 0, 0.5], 'LineWidth', 3, 'DisplayName', 'Total Strategy');
    
    yline(24.34, 'Color', [0.5, 0, 0.5], 'LineStyle', '--', 'Alpha', 0.7, ...
          'DisplayName', 'Conservation Law: 24.34m');
    
    xlabel('Time (minutes)');
    ylabel('Formation Width (metres)');
    title('Zero-Sum Relationship (Competitive balance)', 'FontSize', 14, 'FontWeight', 'bold');
    legend('Location', 'best');
    grid on;
    
    % Panel 4: Competitive Balance
    subplot(2, 2, 4);
    % Draw balance scale
    scale_center = [5, 7];
    scale_arm_length = 3;
    
    % Draw scale
    plot([scale_center(1) - scale_arm_length, scale_center(1) + scale_arm_length], ...
         [scale_center(2), scale_center(2)], 'k-', 'LineWidth', 4);
    plot([scale_center(1), scale_center(1)], [scale_center(2), scale_center(2) - 2], ...
         'k-', 'LineWidth', 4);
    
    % Draw pans
    viscircles([scale_center(1) - scale_arm_length, scale_center(2) - 0.5], 0.8, ...
               'Color', 'blue', 'LineWidth', 3);
    viscircles([scale_center(1) + scale_arm_length, scale_center(2) - 0.5], 0.8, ...
               'Color', 'red', 'LineWidth', 3);
    
    % Add weights
    text(scale_center(1) - scale_arm_length, scale_center(2) - 1.5, '11.44m', ...
         'HorizontalAlignment', 'center', 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'blue');
    text(scale_center(1) + scale_arm_length, scale_center(2) - 1.5, '12.90m', ...
         'HorizontalAlignment', 'center', 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'red');
    
    xlim([0, 10]);
    ylim([0, 10]);
    title('Competitive Balance (Zero-sum equilibrium)', 'FontSize', 14, 'FontWeight', 'bold');
    
    % Add annotation
    annotation('textbox', [0.1, 0.25, 0.8, 0.1], 'String', 'Teams maintain competitive balance through optimal strategy choices', ...
               'FontSize', 11, 'FontWeight', 'bold', 'BackgroundColor', 'lightgreen');
    
    set(gca, 'XTick', [], 'YTick', []);
    
    sgtitle('Nash Equilibrium: What Does It Mean?', 'FontSize', 18, 'FontWeight', 'bold');
    
    % Save figure
    saveas(gcf, 'nash_equilibrium_explanation_matlab.png');
    saveas(gcf, 'nash_equilibrium_explanation_matlab.fig');
end
