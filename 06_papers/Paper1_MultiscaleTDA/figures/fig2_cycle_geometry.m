%% Figure 2 — Geometric Realisation of H1 Loops
%  Two-panel figure: (a) Individual-scale loop, (b) Tactical-scale loop
%  Plotted on a football pitch with cycle edges and shaded enclosed region.
%
%  Data: exported from h1_loops_full_data.json via export_data_for_matlab.py
%  Usage: run this script from MATLAB (or call fig2_cycle_geometry)

function fig2_cycle_geometry()

figDir = fileparts(mfilename('fullpath'));

%% Load data
ind_pts   = readtable(fullfile(figDir, 'fig1_individual_points.csv'));
ind_cycle = readtable(fullfile(figDir, 'fig1_individual_cycle.csv'));
ind_meta  = readtable(fullfile(figDir, 'fig1_individual_meta.csv'));

tac_pts   = readtable(fullfile(figDir, 'fig1_tactical_points.csv'));
tac_cycle = readtable(fullfile(figDir, 'fig1_tactical_cycle.csv'));
tac_meta  = readtable(fullfile(figDir, 'fig1_tactical_meta.csv'));

%% Colour definitions
cycleEdgeCol  = [0.85 0.15 0.15];
cycleFillCol  = [0.85 0.15 0.15];
fillAlpha     = 0.12;
centroidCol   = [0.15 0.30 0.70];
nonCycleCol   = [0.55 0.55 0.55];

%% Create figure
fig = figure('Units', 'centimeters', 'Position', [2 2 34 15], ...
             'Color', 'w', 'PaperPositionMode', 'auto');

% ── Panel (a): Individual-scale loop ──
ax1 = subplot(2, 1, 1, 'Parent', fig);
draw_pitch(ax1);

isCycle_ind = logical(ind_pts.is_cycle_node);
scatter(ax1, ind_pts.x(~isCycle_ind), ind_pts.y(~isCycle_ind), ...
        40, nonCycleCol, 'filled', 'MarkerEdgeColor', 'w', 'LineWidth', 0.5);
scatter(ax1, ind_pts.x(isCycle_ind), ind_pts.y(isCycle_ind), ...
        60, centroidCol, 'filled', 'MarkerEdgeColor', 'w', 'LineWidth', 0.8);

cycleIdx = ind_cycle.node_idx + 1;
nCycle   = length(cycleIdx);
cx = ind_pts.x(cycleIdx);
cy = ind_pts.y(cycleIdx);

fill(ax1, cx, cy, cycleFillCol, 'FaceAlpha', fillAlpha, 'EdgeColor', 'none');

for k = 1:nCycle
    k2 = mod(k, nCycle) + 1;
    plot(ax1, [cx(k) cx(k2)], [cy(k) cy(k2)], ...
         'Color', cycleEdgeCol, 'LineWidth', 2.2);
end

scatter(ax1, cx, cy, 70, centroidCol, 'filled', ...
        'MarkerEdgeColor', 'w', 'LineWidth', 0.8);

title(ax1, sprintf('(a) Individual scale (\\delta = 2.98 m)\nPersistence = %.2f m', ...
      ind_meta.persistence), 'FontSize', 11, 'FontWeight', 'bold');

% ── Panel (b): Tactical-scale loop ──
ax2 = subplot(2, 1, 2, 'Parent', fig);
draw_pitch(ax2);

isCycle_tac = logical(tac_pts.is_cycle_node);
scatter(ax2, tac_pts.x(~isCycle_tac), tac_pts.y(~isCycle_tac), ...
        50, nonCycleCol, 'filled', 'MarkerEdgeColor', 'w', 'LineWidth', 0.5);
scatter(ax2, tac_pts.x(isCycle_tac), tac_pts.y(isCycle_tac), ...
        80, centroidCol, 'filled', 'MarkerEdgeColor', 'w', 'LineWidth', 0.8, ...
        'Marker', 'd');

cycleIdx_t = tac_cycle.node_idx + 1;
nCycle_t   = length(cycleIdx_t);
tx = tac_pts.x(cycleIdx_t);
ty = tac_pts.y(cycleIdx_t);

fill(ax2, tx, ty, cycleFillCol, 'FaceAlpha', fillAlpha, 'EdgeColor', 'none');

for k = 1:nCycle_t
    k2 = mod(k, nCycle_t) + 1;
    plot(ax2, [tx(k) tx(k2)], [ty(k) ty(k2)], ...
         'Color', cycleEdgeCol, 'LineWidth', 2.5);
end

scatter(ax2, tx, ty, 90, centroidCol, 'filled', ...
        'MarkerEdgeColor', 'w', 'LineWidth', 0.8, 'Marker', 'd');

title(ax2, sprintf('(b) Tactical scale (\\delta = 12.0 m)\nPersistence = %.2f m', ...
      tac_meta.persistence), 'FontSize', 11, 'FontWeight', 'bold');

%% Export
exportgraphics(fig, fullfile(figDir, 'fig2_cycle_geometry.pdf'), ...
               'ContentType', 'vector', 'Resolution', 300);
exportgraphics(fig, fullfile(figDir, 'fig2_cycle_geometry.png'), ...
               'Resolution', 300);
fprintf('Figure 2 saved to %s\n', figDir);

end

%% ── Local functions ──

function draw_pitch(ax)
    hold(ax, 'on');
    pitchCol = [0.22 0.56 0.24];
    lineCol  = [1 1 1];
    lw = 1.0;

    rectangle(ax, 'Position', [-52.5, -34, 105, 68], ...
              'EdgeColor', lineCol, 'LineWidth', lw, ...
              'FaceColor', pitchCol);
    plot(ax, [0 0], [-34 34], 'Color', lineCol, 'LineWidth', lw);
    theta = linspace(0, 2*pi, 100);
    plot(ax, 9.15*cos(theta), 9.15*sin(theta), 'Color', lineCol, 'LineWidth', lw);
    rectangle(ax, 'Position', [-52.5, -20.16, 16.5, 40.32], ...
              'EdgeColor', lineCol, 'LineWidth', lw);
    rectangle(ax, 'Position', [36, -20.16, 16.5, 40.32], ...
              'EdgeColor', lineCol, 'LineWidth', lw);
    rectangle(ax, 'Position', [-52.5, -9.16, 5.5, 18.32], ...
              'EdgeColor', lineCol, 'LineWidth', lw);
    rectangle(ax, 'Position', [47, -9.16, 5.5, 18.32], ...
              'EdgeColor', lineCol, 'LineWidth', lw);

    axis(ax, 'equal');
    xlim(ax, [-55 55]);
    ylim(ax, [-37 37]);
    set(ax, 'Color', pitchCol, 'XColor', 'none', 'YColor', 'none');
end
