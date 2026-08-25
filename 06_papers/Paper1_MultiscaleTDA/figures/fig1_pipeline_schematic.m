%% Figure 1 — Multi-Scale TDA Pipeline Schematic
%  Flow diagram: player positions → clustering → VR + persistence diagram
%  → closed cycle identification → geometric realisation.
%
%  No external data required.
%  Usage: run fig1_pipeline_schematic from MATLAB
%  Note: Python fig1_pipeline_schematic.py generates the publication version.

function fig1_pipeline_schematic()

figDir = fileparts(mfilename('fullpath'));

%% Create figure
fig = figure('Units', 'centimeters', 'Position', [2 2 30 8], ...
             'Color', 'w', 'PaperPositionMode', 'auto');
ax = axes(fig);
hold(ax, 'on');
axis(ax, [0 12 0 4]);
axis(ax, 'off');

%% Box positions [x_centre, y_centre, width, height]
boxes = [
    1.5  2  2.2  1.2;
    3.8  2  2.2  1.2;
    6.1  2  2.2  1.2;
    8.4  2  2.2  1.2;
    10.7 2  2.2  1.2;
];

labels = {
    '22 player positions';
    'Hierarchical clustering (\delta)';
    'Vietoris–Rips + persistence diagram';
    'Closed cycle identification';
    'Geometric realisation';
};

boxCol = [0.91 0.96 0.97];
edgeCol = [0.2 0.2 0.2];

for k = 1:size(boxes, 1)
    xc = boxes(k, 1); yc = boxes(k, 2); w = boxes(k, 3); h = boxes(k, 4);
    rectangle(ax, 'Position', [xc - w/2, yc - h/2, w, h], ...
              'FaceColor', boxCol, 'EdgeColor', edgeCol, 'LineWidth', 1.2, ...
              'Curvature', 0.1);
    text(ax, xc, yc, labels{k}, 'HorizontalAlignment', 'center', ...
         'VerticalAlignment', 'middle', 'FontSize', 9);
end

%% Arrows
y = 2;
for k = 1:size(boxes, 1) - 1
    x1 = boxes(k, 1) + boxes(k, 3)/2 + 0.08;
    x2 = boxes(k+1, 1) - boxes(k+1, 3)/2 - 0.08;
    plot(ax, [x1 x2], [y y], '-', 'Color', edgeCol, 'LineWidth', 1.5);
    plot(ax, x2 - 0.12, y, 'v', 'Color', edgeCol, 'MarkerFaceColor', edgeCol, 'MarkerSize', 5);
end

title(ax, 'Multi-scale TDA analysis pipeline', 'FontSize', 12, 'FontWeight', 'bold');

%% Export
exportgraphics(fig, fullfile(figDir, 'fig1_pipeline_schematic.pdf'), ...
               'ContentType', 'vector', 'Resolution', 300);
exportgraphics(fig, fullfile(figDir, 'fig1_pipeline_schematic.png'), ...
               'Resolution', 300);
fprintf('Figure 1 (pipeline schematic) saved to %s\n', figDir);

end
