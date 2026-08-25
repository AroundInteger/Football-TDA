%% Figure 3 — Temporal Evolution of H1 Persistence
%  Two-panel figure: individual (top) and tactical (bottom) persistence
%  across analysis windows for the primary match, with half-time marker
%  and smoothed trend lines.
%
%  Data: per_window_persistence.csv from statistical_tests results
%  Usage: run fig3_temporal_evolution from MATLAB

function fig3_temporal_evolution()

figDir = fileparts(mfilename('fullpath'));

%% Load data
T = readtable(fullfile(figDir, 'fig2_temporal.csv'));

primaryID = 'g2293068';
T = T(strcmp(T.match_id, primaryID), :);

ind = sortrows(T(strcmp(T.scale, 'individual'), :), 'window_idx');
tac = sortrows(T(strcmp(T.scale, 'tactical'), :), 'window_idx');

%% Colour definitions
indCol       = [0.20 0.40 0.75];
tacCol       = [0.75 0.15 0.15];
trendCol_ind = [0.10 0.20 0.55];
trendCol_tac = [0.55 0.10 0.10];
halfTimeCol  = [0.4 0.4 0.4];
smoothSpan   = 25;

%% Create figure
fig = figure('Units', 'centimeters', 'Position', [2 2 28 16], ...
             'Color', 'w', 'PaperPositionMode', 'auto');

% ── Panel (a): Individual scale ──
ax1 = subplot(2, 1, 1, 'Parent', fig);
hold(ax1, 'on'); box(ax1, 'on');

stem(ax1, ind.window_idx, ind.mean_persistence, ...
     'Color', [indCol 0.35], 'MarkerSize', 2, ...
     'MarkerFaceColor', indCol, 'MarkerEdgeColor', 'none', 'LineWidth', 0.5);

y_smooth_ind = movmean(ind.mean_persistence, smoothSpan, 'omitnan');
plot(ax1, ind.window_idx, y_smooth_ind, 'Color', trendCol_ind, 'LineWidth', 2.2);

htIdx = floor(max(ind.window_idx) / 2);
xline(ax1, htIdx, '--', 'Color', halfTimeCol, 'LineWidth', 1.2, ...
      'Label', 'Half-time', 'LabelHorizontalAlignment', 'center', 'FontSize', 9);

yl = [0, max(ind.mean_persistence) * 1.1];
fill(ax1, [0 htIdx htIdx 0], [yl(1) yl(1) yl(2) yl(2)], ...
     indCol, 'FaceAlpha', 0.04, 'EdgeColor', 'none');

ylabel(ax1, 'Mean H_1 persistence (m)', 'FontSize', 10);
title(ax1, '(a) Individual scale (\delta = 2.98 m)', ...
      'FontSize', 11, 'FontWeight', 'bold');
ylim(ax1, yl);
set(ax1, 'XTickLabel', [], 'FontSize', 9);

% ── Panel (b): Tactical scale ──
ax2 = subplot(2, 1, 2, 'Parent', fig);
hold(ax2, 'on'); box(ax2, 'on');

stem(ax2, tac.window_idx, tac.mean_persistence, ...
     'Color', [tacCol 0.35], 'MarkerSize', 2, ...
     'MarkerFaceColor', tacCol, 'MarkerEdgeColor', 'none', 'LineWidth', 0.5);

y_smooth_tac = movmean(tac.mean_persistence, smoothSpan, 'omitnan');
plot(ax2, tac.window_idx, y_smooth_tac, 'Color', trendCol_tac, 'LineWidth', 2.2);

htIdx_t = floor(max(tac.window_idx) / 2);
xline(ax2, htIdx_t, '--', 'Color', halfTimeCol, 'LineWidth', 1.2, ...
      'Label', 'Half-time', 'LabelHorizontalAlignment', 'center', 'FontSize', 9);

yl2 = [0, max(tac.mean_persistence) * 1.1];
fill(ax2, [0 htIdx_t htIdx_t 0], [yl2(1) yl2(1) yl2(2) yl2(2)], ...
     tacCol, 'FaceAlpha', 0.04, 'EdgeColor', 'none');

xlabel(ax2, 'Analysis window index', 'FontSize', 10);
ylabel(ax2, 'Mean H_1 persistence (m)', 'FontSize', 10);
title(ax2, '(b) Tactical scale (\delta = 12.0 m)', ...
      'FontSize', 11, 'FontWeight', 'bold');
ylim(ax2, yl2);
set(ax2, 'FontSize', 9);

linkaxes([ax1, ax2], 'x');

%% Export
exportgraphics(fig, fullfile(figDir, 'fig3_temporal_evolution.pdf'), ...
               'ContentType', 'vector', 'Resolution', 300);
exportgraphics(fig, fullfile(figDir, 'fig3_temporal_evolution.png'), ...
               'Resolution', 300);
fprintf('Figure 3 saved to %s\n', figDir);

end
