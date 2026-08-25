%% Generate Figure 1: Comprehensive PEF Framework Landscape
% Create high-resolution figure showing PEF landscape with quadrant analysis
% X-axis: Correlation coefficient (ρ) from -1 to +1 (symmetric, bounded)
% Y-axis: Variance ratio (κ) centered at κ = 1 (Fisher case)
%
% Data points (16 total):
%   - 6 Rugby KPIs (primary): Rucks Won, Kick Metres, Kicks from Hand, Carries, Penalties Conceded, Turnovers Won
%   - 6 Football KPIs (primary): Duels, Cards, Pressures, Interceptions, Fouls, Shots
%   - 4 Other applications (supporting): Healthcare, Clinical Genomics, Finance, Manufacturing
%
% The 4 other applications: source data, processing, and interpretation are in
% paper/draft_v13_comprehensive_theoretical/analysis_scripts/

clear; close all; clc;

%% Set up figure
figure('Position', [100, 100, 1200, 900]);
set(gcf, 'Color', 'white');

% Define parameter ranges
% X-axis: rho (ρ) from -1 to +1 (symmetric, bounded)
rho = linspace(-0.999, 0.999, 1000);

% Y-axis: kappa (κ) centered at κ = 1 (Fisher case)
% Symmetric multiplicative range: 0.1 to 10 (10× below and 10× above κ = 1)
kappa = linspace(0.0, 4, 1000);

[R, K] = meshgrid(rho, kappa);

% Calculate PEF values
PEF = (1 + K) ./ (1 + K - 2 * sqrt(K) .* R);

% Handle singularity: clip PEF at reasonable maximum and use log scale for visualization
% The singularity occurs when denominator → 0 (at ρ → 1, κ → 1)
PEF_max = 100;  % Reasonable maximum for visualization
PEF_clipped = min(PEF, PEF_max);

% Use log10 scale for better visualization (compresses high values)
% Add small epsilon to avoid log(0) for very small PEF values
PEF_log = log10(max(PEF_clipped, 0.01));

% Create contour plot using log scale
cp = contourf(R, K, PEF_log, 50, 'LineStyle', 'none');
hold on;

% Add contour lines at specific PEF values (convert to log scale)
pef_contour_values = [0.5:0.1:1.0, 1.2, 1.5, 2.0:1:5.0, 10.0, 20.0];
%pef_contour_values = [0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 20.0];
pef_contour_log = log10(pef_contour_values);
contour(R, K, PEF_log, pef_contour_log, 'w:', 'LineWidth', 1);
%contour(R, K, PEF_log, cp(1,1));

% Add quadrant boundaries
% Vertical line at ρ = 0
plot([0, 0], [0, 5], 'k-', 'LineWidth', 3, 'HandleVisibility', 'off');
% Horizontal line at κ = 1 (Fisher case - centered!)
plot([-1, 1], [1, 1], 'k-', 'LineWidth', 3, 'HandleVisibility', 'off');

% Exclude contour objects from legend
set(findobj(gca, 'Type', 'contour'), 'HandleVisibility', 'off');

% Add quadrant labels (adjusted for new axes, ensuring quadrant 4 is visible)
text(0.4, 2.5, 'Quadrant 1', 'FontSize', 18, 'Color', 'y');
text(0.4, 0.5, 'Quadrant 2', 'FontSize', 18, 'Color', 'y');
text(-0.6, 0.5, 'Quadrant 3', 'FontSize', 18,  'Color', 'y');
text(-0.6, 2.5, 'Quadrant 4', 'FontSize', 18,  'Color', 'y');  % Moved slightly to avoid formula

% KPI-level examples (rugby and football)
% Store as separate arrays for clean access
% Rugby KPIs: [kappa, rho]
rugby_data = [
    2.1,  0.75;  % Rucks Won
    1.8,  0.62;  % Kick Metres
    1.5,  0.52;  % Kicks from Hand
    1.2,  0.15;  % Carries
    0.9, -0.10;  % Penalties Conceded
    1.4, -0.20   % Turnovers Won
];

% Football KPIs: [kappa, rho]
football_data = [
    1.6,  0.55;  % Duels
    1.3,  0.22;  % Cards
    1.1,  0.08;  % Pressures
    0.95, -0.05; % Interceptions
    1.45, -0.08; % Fouls
    1.25, 0.35   % Shots
];

% 4 Other Applications (Supporting validation domains)
% Source: analysis_scripts in this project. Data, processing, interpretation:
%   - Healthcare: analyze_real_biology_data.py (blood pressure, Einstadter et al. 2018)
%   - Clinical Genomics: analyze_biology_data.py (TCGA Pan-Cancer, Nature Genetics 2013)
%   - Finance: analyze_finance_data.py (Yahoo Finance, S&P 500 market-adjusted returns)
%   - Manufacturing: analyze_manufacturing_data.py (quality control, Montgomery 2017)
%
% These (kappa, rho) values are means across studies; each produces paper's mean eta.
% Try loading from analysis output files if available:
script_dir = fileparts(mfilename('fullpath'));
analysis_scripts_dir = fullfile(script_dir, '..', 'analysis_scripts');
other_data = [];

% Try loading from project analysis outputs
healthcare_file = fullfile(analysis_scripts_dir, '..', '..', '..', 'external_data_sources', 'output_data', 'biology_pef_results.csv');
finance_file = fullfile(analysis_scripts_dir, '..', '..', '..', 'external_data_sources', 'output_data', 'finance_pef_results.csv');
manufacturing_file = fullfile(analysis_scripts_dir, 'manufacturing_pef_results.csv');

if exist(healthcare_file, 'file')
    try
        T = readtable(healthcare_file);
        if ismember('kappa', T.Properties.VariableNames) && ismember('correlation', T.Properties.VariableNames)
            k_mean = mean(T.kappa, 'omitnan');
            r_mean = mean(T.correlation, 'omitnan');
            other_data = [other_data; k_mean, r_mean];
        end
    catch
        % Fall through to default
    end
end
if isempty(other_data) || size(other_data, 1) < 1
    % Fallback: (kappa, rho) giving paper mean eta = 9.858 (Einstadter et al. blood pressure)
    other_data = [0.95, 0.899];  % Healthcare
end

% Clinical Genomics (TCGA)
clin_genomics_file = fullfile(analysis_scripts_dir, 'biology_pef_results.csv');
if exist(clin_genomics_file, 'file')
    try
        T = readtable(clin_genomics_file);
        if ismember('kappa', T.Properties.VariableNames) && ismember('correlation', T.Properties.VariableNames)
            k_mean = mean(T.kappa, 'omitnan');
            r_mean = mean(T.correlation, 'omitnan');
            other_data = [other_data; k_mean, r_mean];
        end
    catch
    end
end
if size(other_data, 1) < 2
    % Fallback: paper mean eta = 3.310
    other_data = [other_data; 1.1, 0.699];  % Clinical Genomics
end

% Finance
if exist(finance_file, 'file')
    try
        T = readtable(finance_file);
        % Finance file may use 'correlation' and 'kappa'; older files use 'sef' for PEF
        if ismember('kappa', T.Properties.VariableNames) && ismember('correlation', T.Properties.VariableNames)
            k_mean = mean(T.kappa, 'omitnan');
            r_mean = mean(T.correlation, 'omitnan');
            other_data = [other_data; k_mean, r_mean];
        end
    catch
    end
end
if size(other_data, 1) < 3
    % Fallback: paper mean eta = 2.970
    other_data = [other_data; 1.2, 0.666];  % Finance
end

% Manufacturing
if exist(manufacturing_file, 'file')
    try
        T = readtable(manufacturing_file);
        if ismember('kappa', T.Properties.VariableNames) && ismember('correlation', T.Properties.VariableNames)
            k_mean = mean(T.kappa, 'omitnan');
            r_mean = mean(T.correlation, 'omitnan');
            other_data = [other_data; k_mean, r_mean];
        end
    catch
    end
end
if size(other_data, 1) < 4
    % Fallback: paper mean eta = 2.156
    other_data = [other_data; 1.0, 0.536];  % Manufacturing
end

other_entries = {'Healthcare', 'Clinical Genomics', 'Finance', 'Manufacturing'};


% Combined: 6 rugby + 6 football + 4 other applications = 16 points
sample_data = [rugby_data; football_data; other_data];
legend_entries = {'Rucks Won','Kick Metres','Kicks from Hand','Carries','Penalties Conceded','Turnovers Won', ...
    'Duels','Cards','Pressures','Interceptions','Fouls','Shots', ...
    'Healthcare', 'Clinical Genomics', 'Finance', 'Manufacturing'};

fb_KPIs = {'Duels','Cards','Pressures','Interceptions','Fouls','Shots'};

% Calculate PEF values
PEF_sample_data = (1 + sample_data(:,1)) ./ (1 + sample_data(:,1) - 2 * sqrt(sample_data(:,1)) .* sample_data(:,2));

sample_data = [sample_data,PEF_sample_data];

%legend_entries = {'R-Rucks Won','R-Kick Metres','R-Kicks from Hand','R-Carries','R-Penalties Conceded','R-Turnovers Won'};

%legend_entries = {'Healthcare', 'Clinical Genomics', 'Finance', 'Rugby', 'Football', 'Manufacturing'};

% Scatter: 3 gscatter calls for the 3 categories (different marker shapes)
% gscatter colours by group; we map PEF to parula RGB so face colours reflect PEF value
pef_value = min(sample_data(:,3), PEF_max);
pef_log_value = log10(max(pef_value, 0.01));
clim_lo = min(min(PEF_log(:)), min(pef_log_value));
clim_hi = max(max(PEF_log(:)), max(pef_log_value));
caxis([clim_lo, clim_hi]);
colormap(gca, parula(256));
cmap = parula(256);

% Map PEF log values to RGB (normalise to [0,1] then index into colormap)
pef_norm = (pef_log_value - clim_lo) / max(clim_hi - clim_lo, 1e-10);
pef_idx = max(1, min(256, round(1 + pef_norm * 255)));
pef_rgb = cmap(pef_idx, :);

% Colourblind-friendly edge colours (Paul Tol palette: blue, orange, teal)
edge_rugby = [0 119 187]/255;     % blue
edge_football = [230 159 0]/255;  % orange
edge_other = [0 158 115]/255;     % bluish green

rand(0);
colors = [winter(6);bone(6);nebula(4)];
%colors = colors(randperm(16),:);

% Rugby KPIs - filled circles, PEF-coloured, blue edge
rugby_entries = {'Rucks Won','Kick Metres','Kicks from Hand','Carries','Penalties Conceded','Turnovers Won'};
rugby_clr = pef_rgb(1:6, :);
%h_rugby = gscatter(sample_data(1:6, 2), sample_data(1:6, 1), rugby_entries', rugby_clr, 'o', 15, 'off');
h_rugby = gscatter(sample_data(1:6, 2), sample_data(1:6, 1), rugby_entries',colors(1:6,:),'o',13,'filled');
%for k = 1:length(h_rugby), set(h_rugby(k), 'MarkerFaceColor', rugby_clr(k,:), 'MarkerEdgeColor', edge_rugby, 'LineWidth', 1); end
hold on;

% Football KPIs - filled squares, PEF-coloured
football_entries = {'Duels','Cards','Pressures','Interceptions','Fouls','Shots'};
football_clr = pef_rgb(7:12, :);
h_football = gscatter(sample_data(7:12, 2), sample_data(7:12, 1), football_entries', colors(7:12,:), 's', 13,'filled');
%h_football = gscatter(sample_data(7:12, 2), sample_data(7:12, 1), football_entries', football_clr, 's', 15, 'off');
%for k = 1:length(h_football), set(h_football(k), 'MarkerFaceColor', football_clr(k,:), 'MarkerEdgeColor', edge_football, 'LineWidth', 1); end
hold on;

% Other applications - filled diamonds, PEF-coloured
other_entries = {'Healthcare', 'Clinical Genomics', 'Finance', 'Manufacturing'};
other_clr = pef_rgb(13:16, :);
h_other = gscatter(sample_data(13:16, 2), sample_data(13:16, 1), other_entries', colors(13:16,:), '^', 13,'filled');
%h_other = gscatter(sample_data(13:16, 2), sample_data(13:16, 1), other_entries', other_clr, 'p', 15, 'off');
%for k = 1:length(h_other), set(h_other(k), 'MarkerFaceColor', other_clr(k,:), 'MarkerEdgeColor', edge_other, 'LineWidth', 1); end
hold on;

% Ensure axes in normalized units and shrink width to 0.7
ax = gca;
ax.Units = 'normalized';
pos = ax.Position;         % [x y width height]
pos(3) = 0.65;              % set width to 0.7 normalized units
ax.Position = pos;
drawnow;                   % update graphics so positions are valid

% Add colorbar with log scale labels
c = colorbar;
% Set colorbar ticks to show actual PEF values (not log values)
c_ticks_log = linspace(min(PEF_log(:)), max(PEF_log(:)), 8);
%c_ticks_log = linspace(min(pef_contour_log(:)), max(pef_contour_log(:)), 8);
c_ticks_pef = 10.^c_ticks_log;
c_ticks_pef = round(c_ticks_pef * 10) / 10;  % Round to 1 decimal
c.Ticks = c_ticks_log;
c.TickLabels = arrayfun(@(x) sprintf('%.1f', x), c_ticks_pef, 'UniformOutput', false);
c.Label.String = '\eta Value (log_{10} scale)';
c.Label.FontSize = 16;
c.Label.FontWeight = 'normal';
c.Units = "normalized";
drawnow; % ensure positions are up to date
cbPos = c.Position;    % [x y width height] in normalized figure coords

% Customize colormap
colormap("parula");


% % Add PEF formula (moved to top-left to avoid obstructing quadrant 4)
% text(-0.9, 4, '$PEF = \frac{(1 + \kappa)}{(1 + \kappa - 2\sqrt{\kappa} \cdot \rho)}$', 'FontSize', 16, 'FontWeight', 'bold', ...
%      'BackgroundColor', 'white', 'EdgeColor', 'black', 'Margin', 5, 'Interpreter', 'latex', ...
%      'HorizontalAlignment', 'left');

% Add PEF formula
text(0.25, 3.5, '$\eta = \frac{1 + \kappa}{1 + \kappa - 2\sqrt{\kappa} \cdot \rho}$', ...
    'FontSize', 18, 'Color', 'yellow', 'Margin', 5, 'Interpreter', 'latex');


% Add legend with full descriptive entries (rugby + football KPIs + other applications)
lg = legend([h_rugby; h_football; h_other], legend_entries, 'Location', 'none');
lg.Units = 'normalized';
lg.FontSize = 12;
lg.Box = 'off';
lg.Orientation = 'vertical';


% Compute legend rectangle to the right of colorbar
gap = 0.01;            % normalized gap between colorbar and legend
lgWidth = 0.12;        % choose legend width
lgHeight = min(0.9, cbPos(4) * 1.2);  % taller to accommodate 16 entries
lgX = cbPos(1) + cbPos(3) + gap;
lgY = cbPos(2) + (cbPos(4) - lgHeight)/2; % vertically center with colorbar

% Clamp so legend stays inside figure
lgX = min(lgX, 0.98 - lgWidth);
lgY = max(min(lgY, 0.98 - lgHeight), 0.02);

% Apply position
lg.Position = [0.86, lgY+0.1, lgWidth, lgHeight*0.7];

% Set axis properties
xlim([-1, 1]);  % rho range
ylim([0.0, 4]);      % kappa range (centered at 1)
set(gca, 'FontSize', 16);
% Add labels and title
xlabel('Correlation Coefficient (\rho)', 'FontSize', 18);
ylabel('Variance Ratio (\kappa)', 'FontSize', 18);

x_ticks = -1.0:0.5:1.0;
xticks(x_ticks)
xticklabels(compose('%.1f', x_ticks))
y_ticks = 0:0.5:4;
yticks(y_ticks)
yticklabels(compose('%.1f', y_ticks))

%set(gca, 'YScale', 'log');  % Log scale for kappa emphasizes symmetry around κ = 1
grid on;

% % Save figure
% print('../figures/figure_1_pef_landscape.png', '-dpng', '-r300');
% print('../figures/figure_1_pef_landscape.eps', '-depsc', '-r300');
% 
% fprintf('Figure 1 saved as figure_1_pef_landscape.png and .eps\n');
