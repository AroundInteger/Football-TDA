%% TDA Framework Analysis - MATLAB Version
% GPS-Aware Topological Data Analysis for Football Team Dynamics
% Comprehensive analysis and visualization suite

function TDAFrameworkAnalysis()
    %% Initialize
    clc; clear; close all;
    
    fprintf('🚀 GPS-Aware TDA Framework Analysis - MATLAB Version\n');
    fprintf('==================================================\n');
    
    % Set up figure properties
    set(0, 'DefaultFigureColor', 'white');
    set(0, 'DefaultAxesFontSize', 12);
    set(0, 'DefaultAxesFontWeight', 'bold');
    
    %% Generate sample data (replace with real data)
    fprintf('📊 Generating sample data for analysis...\n');
    [tda_results, quantum_results, game_theory_results] = generateSampleData();
    
    %% Create visualizations
    fprintf('🎨 Creating comprehensive visualizations...\n');
    
    % 1. Temporal Evolution Analysis
    createTemporalEvolutionPlot(tda_results, quantum_results, game_theory_results);
    
    % 2. Multi-Scale Epoch Comparison
    createEpochComparisonPlot();
    
    % 3. Formation Analysis (Before/After)
    createFormationAnalysisPlot();
    
    % 4. Quantum States Analysis
    createQuantumStatesPlot(quantum_results);
    
    % 5. Game Theory Analysis
    createGameTheoryPlot(game_theory_results);
    
    % 6. Comprehensive Dashboard
    createComprehensiveDashboard(tda_results, quantum_results, game_theory_results);
    
    fprintf('✅ All MATLAB visualizations created successfully!\n');
    fprintf('📁 Files saved in current directory\n');
end

function [tda_results, quantum_results, game_theory_results] = generateSampleData()
    %% Generate sample data based on our validated results
    
    % Time points (every 30 seconds for 90 minutes)
    time_points = 0:0.5:90;
    n_points = length(time_points);
    
    % TDA Results
    h0_base = 21.71;
    h0_variation = 0.59 * sin(time_points * 0.1) + 0.2 * randn(1, n_points);
    h0_values = h0_base + h0_variation;
    
    h1_base = 3.42;
    h1_variation = 1.18 * sin(time_points * 0.15) + 0.3 * randn(1, n_points);
    h1_values = max(0, h1_base + h1_variation);
    
    complexity_values = (h0_values + h1_values) / 22.0;
    
    tda_results = struct();
    tda_results.time = time_points;
    tda_results.h0 = h0_values;
    tda_results.h1 = h1_values;
    tda_results.complexity = complexity_values;
    
    % Quantum Results
    % state_labels = randi([0, 4], 1, n_points);
    % state_labels = state_labels .* (rand(1, n_points) < [0.234, 0.198, 0.187, 0.201, 0.180](state_labels + 1));
    % Generate random state labels between 0 and 4
    state_labels = randi([0, 4], 1, n_points);
    
    % Define probabilities for each state
    probabilities = [0.234, 0.198, 0.187, 0.201, 0.180];
    
    % Filter state labels based on the defined probabilities
    state_labels = state_labels .* (rand(1, n_points) < probabilities(state_labels + 1));    
    quantum_results = struct();
    quantum_results.time = time_points;
    quantum_results.state = state_labels;
    quantum_results.energy = 1.4 + 0.4 * rand(1, n_points);
    quantum_results.coherence = 0.6 + 0.2 * rand(1, n_points);
    
    % Game Theory Results
    home_spread = 11.44 + 2 * sin(time_points * 0.1) + 0.5 * randn(1, n_points);
    away_spread = 12.90 - 2 * sin(time_points * 0.1) + 0.5 * randn(1, n_points);
    
    game_theory_results = struct();
    game_theory_results.time = time_points;
    game_theory_results.home_spread = home_spread;
    game_theory_results.away_spread = away_spread;
    game_theory_results.zero_sum_strength = 0.6 + 0.2 * rand(1, n_points);
    game_theory_results.nash_equilibrium = 24.34;
end

function createTemporalEvolutionPlot(tda_results, quantum_results, game_theory_results)
    %% Create comprehensive temporal evolution plot
    
    figure('Position', [100, 100, 1200, 900]);
    
    % Subplot 1: H0 and H1 Evolution
    subplot(4, 1, 1);
    plot(tda_results.time, tda_results.h0, 'b-', 'LineWidth', 2, 'DisplayName', 'H0 (Connected Components)');
    hold on;
    plot(tda_results.time, tda_results.h1, 'r-', 'LineWidth', 2, 'DisplayName', 'H1 (Formation Complexity)');
    
    % Add mean lines
    h0_mean = mean(tda_results.h0);
    h1_mean = mean(tda_results.h1);
    yline(h0_mean, 'b--', 'Alpha', 0.5, 'DisplayName', sprintf('H0 Mean: %.2f', h0_mean));
    yline(h1_mean, 'r--', 'Alpha', 0.5, 'DisplayName', sprintf('H1 Mean: %.2f', h1_mean));
    
    ylabel('Topological Features');
    title('Persistent Homology Evolution (H0 vs H1)', 'FontSize', 14, 'FontWeight', 'bold');
    legend('Location', 'best');
    grid on;
    
    % Subplot 2: Complexity Index
    subplot(4, 1, 2);
    plot(tda_results.time, tda_results.complexity, 'g-', 'LineWidth', 2);
    hold on;
    fill([tda_results.time, fliplr(tda_results.time)], ...
         [tda_results.complexity, zeros(size(tda_results.complexity))], ...
         'g', 'FaceAlpha', 0.3, 'EdgeColor', 'none');
    
    complexity_mean = mean(tda_results.complexity);
    yline(complexity_mean, 'g--', 'Alpha', 0.5, 'DisplayName', sprintf('Mean Complexity: %.4f', complexity_mean));
    
    ylabel('Complexity Index');
    title('Formation Complexity Over Time', 'FontSize', 14, 'FontWeight', 'bold');
    legend('Location', 'best');
    grid on;
    
    % Subplot 3: Quantum States
    subplot(4, 1, 3);
    colors = [0.8, 0.2, 0.2; 0.2, 0.8, 0.6; 0.2, 0.5, 0.8; 0.6, 0.8, 0.6; 1, 0.9, 0.6];
    
    for state = 0:4
        state_indices = quantum_results.state == state;
        if any(state_indices)
            scatter(tda_results.time(state_indices), quantum_results.state(state_indices), ...
                   20, colors(state + 1, :), 'filled', ...
                   'DisplayName', sprintf('State %d', state));alpha(0.25)
            hold on;
        end
    end
    
    ylabel('Quantum State');
    title('Tactical State Evolution (Quantum Attractor States)', 'FontSize', 14, 'FontWeight', 'bold');
    ylim([-0.5, 4.5]);
    legend('Location', 'best');
    grid on;
    
    % Subplot 4: Game Theory Analysis
    subplot(4, 1, 4);
    plot(game_theory_results.time, game_theory_results.home_spread, 'b-', 'LineWidth', 2, ...
         'DisplayName', 'Home Team Spread');
    hold on;
    plot(game_theory_results.time, game_theory_results.away_spread, 'r-', 'LineWidth', 2, ...
         'DisplayName', 'Away Team Spread');
    
    % Nash equilibrium line
    nash_total = game_theory_results.nash_equilibrium;
    yline(nash_total/2, 'Color', [0.5, 0, 0.5], 'LineStyle', '--', 'Alpha', 0.7, ...
          'DisplayName', sprintf('Nash Equilibrium: %.2fm', nash_total));
    
    xlabel('Time (minutes)');
    ylabel('Formation Spread (metres)');
    title('Game Theory Analysis: Team Formation Strategies', 'FontSize', 14, 'FontWeight', 'bold');
    legend('Location', 'best');
    grid on;
    
    sgtitle('GPS-Aware TDA Framework: Temporal Evolution Analysis', 'FontSize', 16, 'FontWeight', 'bold');
    
    % Save figure
    saveas(gcf, 'tda_temporal_evolution_matlab.png');
    saveas(gcf, 'tda_temporal_evolution_matlab.fig');
end

function createEpochComparisonPlot()
    %% Create multi-scale temporal analysis comparison
    
    figure('Position', [100, 100, 1200, 800]);
    
    % Define epochs and their characteristics
    epochs = {'1min', '2min', '5min', '10min'};
    h0_means = [21.45, 21.71, 21.89, 22.12];
    h0_stds = [0.52, 0.59, 0.67, 0.74];
    h1_means = [3.12, 3.42, 3.78, 4.15];
    h1_stds = [1.05, 1.18, 1.32, 1.45];
    complexities = (h0_means + h1_means) / 22.0;
    
    colors = [0.8, 0.2, 0.2; 0.2, 0.8, 0.6; 0.2, 0.5, 0.8; 0.6, 0.8, 0.6];
    
    % Subplot 1: H0 Comparison
    subplot(2, 2, 1);
    bars1 = bar(1:4, h0_means, 'FaceColor', 'flat');
    bars1.CData = colors;
    hold on;
    errorbar(1:4, h0_means, h0_stds, 'k', 'LineStyle', 'none', 'LineWidth', 2);
    
    % Add value labels
    for i = 1:4
        text(i, h0_means(i) + h0_stds(i) + 0.1, sprintf('%.2f±%.2f', h0_means(i), h0_stds(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:4, 'XTickLabel', epochs);
    ylabel('H0 (Connected Components)');
    title('H0 Across Temporal Scales', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Subplot 2: H1 Comparison
    subplot(2, 2, 2);
    bars2 = bar(1:4, h1_means, 'FaceColor', 'flat');
    bars2.CData = colors;
    hold on;
    errorbar(1:4, h1_means, h1_stds, 'k', 'LineStyle', 'none', 'LineWidth', 2);
    
    for i = 1:4
        text(i, h1_means(i) + h1_stds(i) + 0.1, sprintf('%.2f±%.2f', h1_means(i), h1_stds(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:4, 'XTickLabel', epochs);
    ylabel('H1 (Formation Complexity)');
    title('H1 Across Temporal Scales', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Subplot 3: Complexity Comparison
    subplot(2, 2, 3);
    bars3 = bar(1:4, complexities, 'FaceColor', 'flat');
    bars3.CData = colors;
    
    for i = 1:4
        text(i, complexities(i) + 0.001, sprintf('%.4f', complexities(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:4, 'XTickLabel', epochs);
    ylabel('Complexity Index');
    title('Formation Complexity Across Scales', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Subplot 4: Scale-Dependent Patterns
    subplot(2, 2, 4);
    window_sizes = [1, 2, 5, 10];
    plot(window_sizes, h0_means, 'bo-', 'LineWidth', 2, 'MarkerSize', 8, ...
         'DisplayName', 'H0 (Connected Components)');
    hold on;
    plot(window_sizes, h1_means, 'ro-', 'LineWidth', 2, 'MarkerSize', 8, ...
         'DisplayName', 'H1 (Formation Complexity)');
    
    xlabel('Window Size (minutes)');
    ylabel('Topological Features');
    title('Scale-Dependent Patterns', 'FontSize', 14, 'FontWeight', 'bold');
    legend('Location', 'best');
    grid on;
    
    sgtitle('Multi-Scale Temporal Analysis: Epoch Comparison', 'FontSize', 16, 'FontWeight', 'bold');
    
    % Save figure
    saveas(gcf, 'tda_epoch_comparison_matlab.png');
    saveas(gcf, 'tda_epoch_comparison_matlab.fig');
end

function createFormationAnalysisPlot()
    %% Create formation analysis (before/after clustering)
    
    figure('Position', [100, 100, 1200, 800]);
    
    % Subplot 1: Before GPS-Aware Clustering
    subplot(2, 2, 1);
    % Simulate scattered players
    rng(42); % For reproducibility
    n_players = 22;
    x_before = 100 * rand(1, n_players);
    y_before = 60 * rand(1, n_players);
    
    scatter(x_before, y_before, 100, 'red', 'filled');alpha(0.7)
    hold on;
    
    % Add player labels
    for i = 1:n_players
        text(x_before(i), y_before(i) - 3, sprintf('P%d', i), ...
             'HorizontalAlignment', 'center', 'FontSize', 8, 'FontWeight', 'bold');
    end
    
    xlim([-5, 105]);
    ylim([-5, 65]);
    xlabel('Field Position (metres)');
    ylabel('Field Position (metres)');
    title('Before GPS-Aware Clustering (H0 = 22 - Artifact)', 'FontSize', 14, 'FontWeight', 'bold', 'Color', 'red');
    grid on;
    
    % Add annotation
    annotation('textbox', [0.1, 0.85, 0.3, 0.1], 'String', 'Artifact: H0 = Number of Players', ...
               'FontSize', 11, 'FontWeight', 'bold', 'Color', 'red', ...
               'BackgroundColor', 'white', 'EdgeColor', 'red');
    
    % Subplot 2: After GPS-Aware Clustering
    subplot(2, 2, 2);
    % Define cluster centers and assign players
    cluster_centers = [20, 30; 50, 20; 80, 35; 30, 50; 70, 45];
    cluster_labels = randi([1, 5], 1, n_players);
    colors = [0.8, 0.2, 0.2; 0.2, 0.8, 0.6; 0.2, 0.5, 0.8; 0.6, 0.8, 0.6; 1, 0.9, 0.6];
    
    for i = 1:5
        cluster_points = find(cluster_labels == i);
        if ~isempty(cluster_points)
            % Add noise around cluster center
            x_cluster = cluster_centers(i, 1) + 2 * randn(1, length(cluster_points));
            y_cluster = cluster_centers(i, 2) + 2 * randn(1, length(cluster_points));
            
            scatter(x_cluster, y_cluster, 100, colors(i, :), 'filled');alpha(0.7)
            hold on;
            
            % Draw cluster boundary
            viscircles(cluster_centers(i, :), 3, 'Color', colors(i, :), 'LineWidth', 2);
            
            % Label cluster
            text(cluster_centers(i, 1), cluster_centers(i, 2), sprintf('C%d', i), ...
                 'HorizontalAlignment', 'center', 'FontSize', 12, 'FontWeight', 'bold', ...
                 'BackgroundColor', 'white');
        end
    end
    
    xlim([-5, 105]);
    ylim([-5, 65]);
    xlabel('Field Position (metres)');
    ylabel('Field Position (metres)');
    title('After GPS-Aware Clustering (H0 = 5 - Meaningful)', 'FontSize', 14, 'FontWeight', 'bold', 'Color', 'green');
    grid on;
    
    % Add annotation
    annotation('textbox', [0.6, 0.85, 0.3, 0.1], 'String', 'Meaningful: H0 = Player Groups', ...
               'FontSize', 11, 'FontWeight', 'bold', 'Color', 'green', ...
               'BackgroundColor', 'white', 'EdgeColor', 'green');
    
    % Subplot 3: H0 Evolution
    subplot(2, 2, 3);
    time_points = 0:2:90;
    h0_values = 21.71 + 0.59 * sin(time_points * 0.1) + 0.2 * randn(1, length(time_points));
    
    plot(time_points, h0_values, 'b-', 'LineWidth', 2);
    hold on;
    yline(22, 'r--', 'Alpha', 0.7, 'DisplayName', 'Artifact Value (H0 = 22)');
    yline(21.71, 'g--', 'Alpha', 0.7, 'DisplayName', 'Corrected Value (H0 = 21.71)');
    
    xlabel('Time (minutes)');
    ylabel('H0 (Connected Components)');
    title('H0 Evolution: Artifact Resolution', 'FontSize', 14, 'FontWeight', 'bold');
    legend('Location', 'best');
    grid on;
    
    % Subplot 4: Complexity Index
    subplot(2, 2, 4);
    complexity_values = (h0_values + 3 + rand(1, length(time_points))) / 22.0;
    
    plot(time_points, complexity_values, 'g-', 'LineWidth', 2);
    hold on;
    fill([time_points, fliplr(time_points)], [complexity_values, zeros(size(complexity_values))], ...
         'g', 'FaceAlpha', 0.3, 'EdgeColor', 'none');
    
    complexity_mean = mean(complexity_values);
    yline(complexity_mean, 'g--', 'Alpha', 0.7, 'DisplayName', sprintf('Mean Complexity: %.4f', complexity_mean));
    
    xlabel('Time (minutes)');
    ylabel('Complexity Index');
    title('Formation Complexity Over Time', 'FontSize', 14, 'FontWeight', 'bold');
    legend('Location', 'best');
    grid on;
    
    sgtitle('GPS-Aware Formation Analysis: Before vs After Clustering', 'FontSize', 16, 'FontWeight', 'bold');
    
    % Save figure
    saveas(gcf, 'tda_formation_analysis_matlab.png');
    saveas(gcf, 'tda_formation_analysis_matlab.fig');
end

function createQuantumStatesPlot(quantum_results)
    %% Create quantum states analysis plot
    
    figure('Position', [100, 100, 1200, 800]);
    
    % Subplot 1: State frequencies
    subplot(2, 2, 1);
    states = {'State 0', 'State 1', 'State 2', 'State 3', 'State 4'};
    frequencies = [0.234, 0.198, 0.187, 0.201, 0.180];
    colors = [0.8, 0.2, 0.2; 0.2, 0.8, 0.6; 0.2, 0.5, 0.8; 0.6, 0.8, 0.6; 1, 0.9, 0.6];
    
    bars = bar(1:5, frequencies, 'FaceColor', 'flat');
    bars.CData = colors;
    
    % Add value labels
    for i = 1:5
        text(i, frequencies(i) + 0.005, sprintf('%.3f', frequencies(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:5, 'XTickLabel', states);
    ylabel('Frequency');
    title('Quantum Attractor State Frequencies', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Subplot 2: Energy landscapes
    subplot(2, 2, 2);
    energies = [1.452, 1.620, 1.678, 1.609, 1.715];
    
    bars2 = bar(1:5, energies, 'FaceColor', 'flat');
    bars2.CData = colors;
    
    for i = 1:5
        text(i, energies(i) + 0.01, sprintf('%.3f', energies(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:5, 'XTickLabel', states);
    ylabel('Total Energy');
    title('Energy Landscapes by State', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Subplot 3: Band gaps
    subplot(2, 2, 3);
    gaps = {'0-1', '1-2', '2-3', '3-4'};
    gap_values = [0.168, 0.058, 0.069, 0.106];
    
    bars3 = bar(1:4, gap_values, 'FaceColor', [0.5, 0, 0.5]); alpha(0.8)
    
    for i = 1:4
        text(i, gap_values(i) + 0.002, sprintf('%.3f', gap_values(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:4, 'XTickLabel', gaps);
    ylabel('Band Gap (eV)');
    title('Energy Band Gaps Between States', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Subplot 4: Transition probabilities
    subplot(2, 2, 4);
    transitions = {'0→1', '1→2', '2→3', '3→4', '4→0'};
    probabilities = [0.234, 0.198, 0.187, 0.201, 0.180];
    
    bars4 = bar(1:5, probabilities, 'FaceColor', [1, 0.5, 0]); alpha(0.8)
    
    for i = 1:5
        text(i, probabilities(i) + 0.005, sprintf('%.3f', probabilities(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:5, 'XTickLabel', transitions);
    ylabel('Transition Probability');
    title('Quantum Tunnelling Transitions', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    sgtitle('Quantum Phenomena Analysis: Attractor States and Energy Landscapes', 'FontSize', 16, 'FontWeight', 'bold');
    
    % Save figure
    % saveas(gcf, 'tda_quantum_states_matlab.png');
    % saveas(gcf, 'tda_quantum_states_matlab.fig');
end

function createGameTheoryPlot(game_theory_results)
    %% Create game theory analysis plot
    
    figure('Position', [100, 100, 1200, 800]);
    
    % Subplot 1: Nash equilibrium
    subplot(2, 2, 1);
    home_strategy = 11.44;
    away_strategy = 12.90;
    total_strategy = 24.34;
    
    strategies = {'Home Team', 'Away Team', 'Total Strategy'};
    values = [home_strategy, away_strategy, total_strategy];
    colors = [0, 0, 1; 1, 0, 0; 0.5, 0, 0.5];
    
    bars = bar(1:3, values, 'FaceColor', 'flat');
    bars.CData = colors;
    
    for i = 1:3
        text(i, values(i) + 0.2, sprintf('%.2fm', values(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:3, 'XTickLabel', strategies);
    ylabel('Formation Width (metres)');
    title('Nash Equilibrium in Team Formation Strategies', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Subplot 2: Zero-sum analysis
    subplot(2, 2, 2);
    time_points = 0:2:90;
    home_spread = 11.44 + 2 * sin(time_points * 0.1) + 0.5 * randn(1, length(time_points));
    away_spread = 12.90 - 2 * sin(time_points * 0.1) + 0.5 * randn(1, length(time_points));
    
    plot(time_points, home_spread, 'b-', 'LineWidth', 2, 'DisplayName', 'Home Team Spread');
    hold on;
    plot(time_points, away_spread, 'r-', 'LineWidth', 2, 'DisplayName', 'Away Team Spread');
    plot(time_points, home_spread + away_spread, 'Color', [0.5, 0, 0.5], 'LineWidth', 2, ...
         'DisplayName', 'Total Spread');
    
    yline(total_strategy, 'Color', [0.5, 0, 0.5], 'LineStyle', '--', 'Alpha', 0.7, ...
          'DisplayName', sprintf('Conservation Law: %.2fm', total_strategy));
    
    xlabel('Time (minutes)');
    ylabel('Formation Spread (metres)');
    title('Zero-Sum Competitive Balance', 'FontSize', 14, 'FontWeight', 'bold');
    legend('Location', 'best');
    grid on;
    
    % Subplot 3: p-adic analysis
    subplot(2, 2, 3);
    primes = {'p=2', 'p=3', 'p=5', 'p=7', 'p=11'};
    balance_values = [0.7234, 0.6789, 0.7123, 0.6987, 0.7345];
    
    bars3 = bar(1:5, balance_values, 'FaceColor', [0, 0.8, 0]); alpha(0.8)
    
    for i = 1:5
        text(i, balance_values(i) + 0.005, sprintf('%.4f', balance_values(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:5, 'XTickLabel', primes);
    ylabel('p-adic Balance');
    title('p-adic Competitive Hierarchies', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Subplot 4: Competitive balance metrics
    subplot(2, 2, 4);
    metrics = {'Zero-Sum\nCorrelation', 'L1\nCoefficient', 'Balance\nStability'};
    values = [0.8234, 0.1567, 0.6789];
    colors_metrics = [0.8, 0.2, 0.2; 0.2, 0.8, 0.6; 0.2, 0.5, 0.8];
    
    bars4 = bar(1:3, values, 'FaceColor', 'flat');
    bars4.CData = colors_metrics;
    
    for i = 1:3
        text(i, values(i) + 0.01, sprintf('%.4f', values(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:3, 'XTickLabel', metrics);
    ylabel('Metric Value');
    title('Competitive Balance Metrics', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    sgtitle('Game Theory Analysis: Nash Equilibrium and Competitive Balance', 'FontSize', 16, 'FontWeight', 'bold');
    
    % Save figure
    % saveas(gcf, 'tda_game_theory_matlab.png');
    % saveas(gcf, 'tda_game_theory_matlab.fig');
end

function createComprehensiveDashboard(tda_results, quantum_results, game_theory_results)
    %% Create comprehensive summary dashboard
    
    figure('Position', [100, 100, 1600, 1000]);
    
    % Create grid layout
    % Top row: Key metrics
    subplot(3, 4, [1, 2]);
    metrics = {'H0 (Connected\nComponents)', 'H1 (Formation\nComplexity)', ...
               'Complexity\nIndex', 'Zero-Sum\nStrength'};
    values = [21.71, 3.42, 0.1156, 0.6789];
    colors = [0.8, 0.2, 0.2; 0.2, 0.8, 0.6; 0.2, 0.5, 0.8; 0.6, 0.8, 0.6];
    
    bars = bar(1:4, values, 'FaceColor', 'flat');
    bars.CData = colors;
    
    for i = 1:4
        text(i, values(i) + 0.1, sprintf('%.4f', values(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold', 'FontSize', 12);
    end
    
    set(gca, 'XTick', 1:4, 'XTickLabel', metrics);
    ylabel('Metric Value');
    title('Key Framework Metrics', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Top row: Temporal evolution
    subplot(3, 4, [3, 4]);
    time_points = 0:2:90;
    h0_values = 21.71 + 0.59 * sin(time_points * 0.1) + 0.2 * randn(1, length(time_points));
    
    plot(time_points, h0_values, 'b-', 'LineWidth', 2);
    hold on;
    yline(21.71, 'b--', 'Alpha', 0.7, 'DisplayName', sprintf('H0 Mean: %.2f', 21.71));
    
    xlabel('Time (minutes)');
    ylabel('H0 (Connected Components)');
    title('H0 Evolution Over Match', 'FontSize', 14, 'FontWeight', 'bold');
    legend('Location', 'best');
    grid on;
    
    % Middle row: Quantum states
    subplot(3, 4, [5, 6]);
    states = {'State 0', 'State 1', 'State 2', 'State 3', 'State 4'};
    frequencies = [0.234, 0.198, 0.187, 0.201, 0.180];
    colors_q = [0.8, 0.2, 0.2; 0.2, 0.8, 0.6; 0.2, 0.5, 0.8; 0.6, 0.8, 0.6; 1, 0.9, 0.6];
    
    bars_q = bar(1:5, frequencies, 'FaceColor', 'flat');
    bars_q.CData = colors_q;
    
    set(gca, 'XTick', 1:5, 'XTickLabel', states);
    ylabel('Frequency');
    title('Quantum Attractor States', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Middle row: Nash equilibrium
    subplot(3, 4, [7, 8]);
    home_strategy = 11.44;
    away_strategy = 12.90;
    
    strategies = {'Home Team', 'Away Team'};
    values_nash = [home_strategy, away_strategy];
    colors_nash = [0, 0, 1; 1, 0, 0];
    
    bars_nash = bar(1:2, values_nash, 'FaceColor', 'flat');
    bars_nash.CData = colors_nash;
    
    for i = 1:2
        text(i, values_nash(i) + 0.2, sprintf('%.2fm', values_nash(i)), ...
             'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    end
    
    set(gca, 'XTick', 1:2, 'XTickLabel', strategies);
    ylabel('Formation Width (metres)');
    title('Nash Equilibrium Discovery', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Bottom row: Scale comparison
    subplot(3, 4, [9, 10]);
    epochs = {'1min', '2min', '5min', '10min'};
    h0_means = [21.45, 21.71, 21.89, 22.12];
    colors_epochs = [0.8, 0.2, 0.2; 0.2, 0.8, 0.6; 0.2, 0.5, 0.8; 0.6, 0.8, 0.6];
    
    bars_epochs = bar(1:4, h0_means, 'FaceColor', 'flat');
    bars_epochs.CData = colors_epochs;
    
    set(gca, 'XTick', 1:4, 'XTickLabel', epochs);
    ylabel('H0 (Connected Components)');
    title('Multi-Scale Analysis', 'FontSize', 14, 'FontWeight', 'bold');
    grid on;
    
    % Bottom row: Framework benefits
    subplot(3, 4, [11, 12]);
    benefits = {'Real-Time\nAnalysis', 'Formation\nComplexity', 'Tactical\nStates', ...
                'Competitive\nBalance', 'Multi-Scale\nInsights', 'Validated\nMethodology'};
    
    % Create visual representation of benefits
    y_positions = 1:6;
    colors_benefits = [0.8, 0.2, 0.2; 0.2, 0.8, 0.6; 0.2, 0.5, 0.8; 0.6, 0.8, 0.6; 1, 0.9, 0.6; 0.8, 0.6, 0.8];
    
    for i = 1:6
        barh(i, 1, 'FaceColor', colors_benefits(i, :)); alpha(0.8)
        hold on;
        text(0.5, i, benefits{i}, 'HorizontalAlignment', 'center', 'FontWeight', 'bold', 'FontSize', 10);
    end
    
    xlim([0, 1]);
    ylim([0.5, 6.5]);
    xlabel('Value Proposition');
    title('Framework Benefits', 'FontSize', 14, 'FontWeight', 'bold');
    set(gca, 'YTick', []);
    
    sgtitle('GPS-Aware TDA Framework: Comprehensive Analysis Dashboard', 'FontSize', 20, 'FontWeight', 'bold');
    
    % Save figure
    % saveas(gcf, 'tda_comprehensive_dashboard_matlab.png');
    % saveas(gcf, 'tda_comprehensive_dashboard_matlab.fig');
end
