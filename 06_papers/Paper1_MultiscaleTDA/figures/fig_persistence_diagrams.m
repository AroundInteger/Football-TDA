%% Figure — Persistence Diagrams at Individual and Tactical Scales
%  Two-panel figure showing (birth, death) for H1 features from representative frames.
%
%  Data: fig_persistence_individual.csv, fig_persistence_tactical.csv
%  Export: run export_data_for_matlab.py first
%  Usage: run fig_persistence_diagrams from MATLAB

function fig_persistence_diagrams()

figDir = fileparts(mfilename('fullpath'));

%% Load data
indFile = fullfile(figDir, 'fig_persistence_individual.csv');
tacFile = fullfile(figDir, 'fig_persistence_tactical.csv');

if ~isfile(indFile) || ~isfile(tacFile)
    error('Run export_data_for_matlab.py first to generate fig_persistence_*.csv');
end

ind = readtable(indFile);
tac = readtable(tacFile);

%% Colours
indCol = [0.13 0.40 0.67];
tacCol = [0.70 0.09 0.17];

%% Create figure
fig = figure('Units', 'centimeters', 'Position', [2 2 22 9], ...
             'Color', 'w', 'PaperPositionMode', 'auto');

% ── Panel (a): Individual scale ──
ax1 = subplot(1, 2, 1, 'Parent', fig);
hold(ax1, 'on'); box(ax1, 'on');

if height(ind) > 0
    maxVal = max(max(ind.birth), max(ind.death)) * 1.1;
    plot(ax1, [0 maxVal], [0 maxVal], 'k--', 'LineWidth', 1, 'Color', [0 0 0 0.4]);
    scatter(ax1, ind.birth, ind.death, 60, indCol, '^', 'filled', ...
            'MarkerEdgeColor', 'k', 'LineWidth', 0.5);
    xlim(ax1, [-0.5 maxVal]);
    ylim(ax1, [-0.5 maxVal]);
else
    text(ax1, 0.5, 0.5, 'No H_1 loops', 'HorizontalAlignment', 'center');
    xlim(ax1, [0 1]);
    ylim(ax1, [0 1]);
end

xlabel(ax1, 'Birth (m)', 'FontSize', 10);
ylabel(ax1, 'Death (m)', 'FontSize', 10);
title(ax1, sprintf('(a) Individual scale (\\delta = 2.98 m)\nn = %d loops', height(ind)), ...
      'FontSize', 11, 'FontWeight', 'bold');
axis(ax1, 'equal');
grid(ax1, 'on');
set(ax1, 'FontSize', 9);

% ── Panel (b): Tactical scale ──
ax2 = subplot(1, 2, 2, 'Parent', fig);
hold(ax2, 'on'); box(ax2, 'on');

if height(tac) > 0
    maxVal = max(max(tac.birth), max(tac.death)) * 1.1;
    plot(ax2, [0 maxVal], [0 maxVal], 'k--', 'LineWidth', 1, 'Color', [0 0 0 0.4]);
    scatter(ax2, tac.birth, tac.death, 60, tacCol, '^', 'filled', ...
            'MarkerEdgeColor', 'k', 'LineWidth', 0.5);
    xlim(ax2, [-0.5 maxVal]);
    ylim(ax2, [-0.5 maxVal]);
else
    text(ax2, 0.5, 0.5, 'No H_1 loops', 'HorizontalAlignment', 'center');
    xlim(ax2, [0 1]);
    ylim(ax2, [0 1]);
end

xlabel(ax2, 'Birth (m)', 'FontSize', 10);
ylabel(ax2, 'Death (m)', 'FontSize', 10);
title(ax2, sprintf('(b) Tactical scale (\\delta = 12.0 m)\nn = %d loops', height(tac)), ...
      'FontSize', 11, 'FontWeight', 'bold');
axis(ax2, 'equal');
grid(ax2, 'on');
set(ax2, 'FontSize', 9);

sgtitle(fig, 'Representative persistence diagrams', 'FontSize', 12, 'FontWeight', 'bold');

%% Export
exportgraphics(fig, fullfile(figDir, 'fig_persistence_diagrams.pdf'), ...
               'ContentType', 'vector', 'Resolution', 300);
exportgraphics(fig, fullfile(figDir, 'fig_persistence_diagrams.png'), ...
               'Resolution', 300);
fprintf('Persistence diagram figure saved to %s\n', figDir);

end
