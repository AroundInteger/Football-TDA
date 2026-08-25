%% Figure 4 — Event Correlation: Persistence Change by Event Type
%  Grouped horizontal bar chart showing mean persistence delta for each
%  significant event type at individual and tactical scales.
%
%  Data: event_correlation_summary.json via export_data_for_matlab.py
%  Usage: run fig4_event_correlation from MATLAB

function fig4_event_correlation()

figDir = fileparts(mfilename('fullpath'));

%% Load data
T = readtable(fullfile(figDir, 'fig3_event_correlation.csv'));

% Filter to significant associations only
T = T(T.significant == 1, :);

ind = T(strcmp(T.scale, 'individual'), :);
tac = T(strcmp(T.scale, 'tactical'), :);

% Event types significant in either scale
allEvents = union(ind.event_type, tac.event_type);
nEvents   = length(allEvents);

%% Build data matrix
deltas = nan(nEvents, 2);
pvals  = nan(nEvents, 2);
counts = nan(nEvents, 2);

for k = 1:nEvents
    ev = allEvents{k};
    idx_i = find(strcmp(ind.event_type, ev));
    idx_t = find(strcmp(tac.event_type, ev));
    if ~isempty(idx_i)
        deltas(k, 1) = ind.mean_delta(idx_i);
        pvals(k, 1)  = ind.p_value(idx_i);
        counts(k, 1) = ind.n_events(idx_i);
    end
    if ~isempty(idx_t)
        deltas(k, 2) = tac.mean_delta(idx_t);
        pvals(k, 2)  = tac.p_value(idx_t);
        counts(k, 2) = tac.n_events(idx_t);
    end
end

% Sort by individual-scale delta (most negative first)
sortVal = deltas(:, 1);
sortVal(isnan(sortVal)) = deltas(isnan(sortVal), 2);
[~, sortIdx] = sort(sortVal, 'ascend');
deltas    = deltas(sortIdx, :);
pvals     = pvals(sortIdx, :);
counts    = counts(sortIdx, :);
allEvents = allEvents(sortIdx);

% Clean labels
labels = strrep(allEvents, '_', ' ');
for k = 1:length(labels)
    labels{k} = [upper(labels{k}(1)), labels{k}(2:end)];
end

%% Colour definitions
indCol = [0.20 0.40 0.75];
tacCol = [0.75 0.15 0.15];

%% Create figure
fig = figure('Units', 'centimeters', 'Position', [2 2 22 14], ...
             'Color', 'w', 'PaperPositionMode', 'auto');
ax = axes(fig);
hold(ax, 'on'); box(ax, 'on');

barWidth = 0.35;
y = 1:nEvents;

% Individual scale bars
for k = 1:nEvents
    if ~isnan(deltas(k, 1))
        barh(ax, y(k) + barWidth/2, deltas(k, 1), barWidth, ...
             'FaceColor', indCol, 'EdgeColor', 'none', 'FaceAlpha', 0.85);
    end
end

% Tactical scale bars
for k = 1:nEvents
    if ~isnan(deltas(k, 2))
        barh(ax, y(k) - barWidth/2, deltas(k, 2), barWidth, ...
             'FaceColor', tacCol, 'EdgeColor', 'none', 'FaceAlpha', 0.85);
    end
end

% Significance stars
for k = 1:nEvents
    for s = 1:2
        if ~isnan(pvals(k, s))
            offset = (2 - s) * barWidth - barWidth/2;
            xpos = deltas(k, s);
            if isnan(xpos); continue; end
            if pvals(k, s) < 0.001
                star = '***';
            elseif pvals(k, s) < 0.01
                star = '**';
            elseif pvals(k, s) < 0.05
                star = '*';
            else
                star = '';
            end
            if ~isempty(star)
                if xpos < 0
                    ha = 'right'; nudge = -0.02;
                else
                    ha = 'left'; nudge = 0.02;
                end
                text(ax, xpos + nudge, y(k) + offset, star, ...
                     'FontSize', 8, 'HorizontalAlignment', ha, ...
                     'VerticalAlignment', 'middle', 'FontWeight', 'bold');
            end
        end
    end
end

% Zero line
xline(ax, 0, '-', 'Color', [0.3 0.3 0.3], 'LineWidth', 1);

% Axis labels
set(ax, 'YTick', y, 'YTickLabel', labels, 'FontSize', 9);
xlabel(ax, 'Mean persistence change (\Delta, metres)', 'FontSize', 10);
ylim(ax, [0.3, nEvents + 0.7]);
set(ax, 'YDir', 'reverse');

% Zone annotations
xl = xlim(ax);
text(ax, xl(1) * 0.6, nEvents + 0.55, '\leftarrow Disruption', ...
     'FontSize', 8, 'Color', [0.4 0.4 0.4], 'HorizontalAlignment', 'center');
text(ax, xl(2) * 0.6, nEvents + 0.55, 'Organisation \rightarrow', ...
     'FontSize', 8, 'Color', [0.4 0.4 0.4], 'HorizontalAlignment', 'center');

% Legend
h1 = patch(ax, NaN, NaN, indCol, 'FaceAlpha', 0.85, 'EdgeColor', 'none');
h2 = patch(ax, NaN, NaN, tacCol, 'FaceAlpha', 0.85, 'EdgeColor', 'none');
legend(ax, [h1 h2], {'Individual scale', 'Tactical scale'}, ...
       'Location', 'southeast', 'FontSize', 9, 'Box', 'off');

title(ax, 'Persistence change by match event type', ...
      'FontSize', 11, 'FontWeight', 'bold');

% Sample size annotations
for k = 1:nEvents
    n_val = max(counts(k, :), [], 'omitnan');
    if ~isnan(n_val)
        text(ax, xl(2) * 0.98, y(k), sprintf('n = %d', n_val), ...
             'FontSize', 7, 'Color', [0.5 0.5 0.5], ...
             'HorizontalAlignment', 'right', 'VerticalAlignment', 'middle');
    end
end

%% Export
exportgraphics(fig, fullfile(figDir, 'fig4_event_correlation.pdf'), ...
               'ContentType', 'vector', 'Resolution', 300);
exportgraphics(fig, fullfile(figDir, 'fig4_event_correlation.png'), ...
               'Resolution', 300);
fprintf('Figure 4 saved to %s\n', figDir);

end
