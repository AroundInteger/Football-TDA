%% ADVERSARIAL TDA TOY MODEL
% =========================================================================
% Mathematical toy model for EPSRC Small Grant:
% Statistical Topological Data Analysis of Competitive Collective Systems
%
% PI:   Rowan Brown, Zienkiewicz Institute for Modelling, Data and AI
%       Swansea University
% Date: August 2026
%
% DESCRIPTION
%   Implements a hierarchical adversarial point process demonstrating:
%     - Multi-scale H0 persistent homology (ultrametric hierarchy)
%     - Scale-specific adversarial coupling
%     - T1: Frechet mean stability under competitive dependence
%     - T2: CUSUM change-point detection on topological time series
%     - Monte Carlo validation of the T2 localisation bound
%     - H1 encirclement: loops from adversarial embedding, not hierarchy
%     - Framework universality across four competitive domains
%     - The single-scale failure case
%     - Coin-flip vs tug-of-war (independence assumption violation)
%
% REQUIREMENTS
%   MATLAB R2020b or later. No additional toolboxes.
%     matchpairs      (R2019a) - exact optimal matching for Wasserstein
%     exportgraphics  (R2020a) - 300 DPI figure export
%     tiledlayout     (R2019b) - subplot layout with reserved title space
%     subtitle        (R2020b) - layout subtitles
%   Persistent homology is computed from first principles here:
%     H0 via Prim minimum spanning tree (exact, Carlsson-Memoli)
%     H1 via GF(2) reduction of the Vietoris-Rips boundary matrix
%
% OUTPUTS
%   Nine 300 DPI PNG figures saved to OUTPUT_DIR
%   Console output: reference values for verification
%
% KEY REFERENCE VALUES (verify any reimplementation against these)
%   H0(A_WIDE)   = [4.00 x4  4.03 x4  32.56  32.56  60.00]
%   H0(A_NARROW) = [4.00 x4  4.03 x4  12.66  12.66  12.66]
%   H0(A_LINE)   = [4.00 x4  4.03 x4  21.00  26.00  36.00]
%   W1(A_WIDE, A_NARROW) = 76.13   [exact, diagonal matching permitted]
%   W1(A_WIDE, A_LINE)   = 42.12   [single-scale failure]
%   H1(B_RING) = single bar [27.24, 40.00], persistence 12.76
%   H1(B_RING + trapped A cluster) = empty (encirclement penetrated)
%   Pitch diameter = sqrt(120^2 + 80^2) = 144.22   [T1 integrability bound]
%   At delta = 35, A_WIDE and A_LINE both have beta_0 = 2 and beta_1 = 0
%   CUSUM (calibrated at 5% false-alarm): T_hat = 54, error = 4
%
% REVISION NOTES (August 2026 review)
%   Corrected since the previous version:
%     - A_NARROW cluster spacing was 16/20/16, giving deaths 12.66/12.66/16.62
%       rather than the documented flat 12.66 triple. Now spaced 16/16/16.
%     - Wasserstein distance used sorted matching only; it now solves the
%       exact optimal transport problem including matching to the diagonal
%       and handling diagrams of unequal cardinality (e.g. after a red card).
%     - The Frechet mean is the exact W2 barycentre, so the Frechet variance
%       is now measured in W2 as well. Turner et al. (2014) define Frechet
%       means of persistence diagrams with respect to W2, not W1.
%     - Position noise is Gaussian (as specified), previously uniform.
%     - The CUSUM decision interval is calibrated on independent in-control
%       realisations for a 5% false-alarm probability over the monitoring
%       horizon. The previous ad hoc threshold gave a 25% false-alarm rate
%       and needed an arbitrary t >= 30 guard to mask early alarms.
%     - Display scales were delta = [4.5, 22, 66]. Since A_WIDE has no deaths
%       between 4.03 and 32.56, delta = 22 showed exactly the same complex as
%       delta = 4.5. The tactical scale is now delta = 40.
%     - Figure 7 previously compared a series containing a regime change
%       against a time-shuffled copy, so the apparent dependence was
%       non-stationarity rather than adversarial coupling. It now compares a
%       genuinely coupled model (Team B tracks Team A) against an independent
%       model with identical marginals, restricted to the stationary regime.
% =========================================================================

clear; close all; clc;

%% -- CONFIGURATION -------------------------------------------------------
SAVE_FIGS   = true;
OUTPUT_DIR  = fileparts(mfilename('fullpath'));
if isempty(OUTPUT_DIR), OUTPUT_DIR = pwd; end
FIG_DPI     = 300;

NOISE       = 1.5;    % Per-agent Gaussian position noise, s.d. in pitch units
WIN         = 10;     % Frechet mean sliding window (frames)
T_MAX       = 100;    % Total simulation frames
T_STAR      = 50;     % True change-point (phase transition starts here)
T_END       = 56;     % Phase transition completes here
MON_START   = 41;     % CUSUM monitoring begins (frames 0..40 are in-control)
ALPHA_FA    = 0.05;   % Target false-alarm probability over the horizon
N_CAL       = 600;    % In-control realisations used to calibrate the CUSUM
N_MC        = 1000;   % Realisations per condition in the T2 Monte Carlo
SEED_MAIN   = 7;      % Seed for the headline realisation

% Display scales, chosen to fall between the three levels of the hierarchy
DELTA_LOCAL    = 5;    % above 4.03, below 32.56  -> clusters visible
DELTA_TACTICAL = 40;   % above 32.56, below 60.00 -> formations visible
DELTA_GLOBAL   = 66;   % above 60.00              -> whole team connected

% Colour palette (matching grant documents)
CA     = [ 29  78 216]/255;  % Team A: deep blue
CB     = [185  28  28]/255;  % Team B: deep red
CV     = [109  40 217]/255;  % Purple: theory markers
CK     = [217 119   6]/255;  % Amber:  thresholds
CGN    = [ 21 128  61]/255;  % Green:  positive results
CGREY  = [107 114 128]/255;  % Slate:  secondary text
CFAINT = [203 213 225]/255;  % Pale:   de-emphasised elements
CPITCH = [240 253 244]/255;  % Pitch background
CGRASS = [134 239 172]/255;  % Pitch lines
CINK   = [ 15  23  42]/255;  % Near-black for titles

%% -- SECTION 1: AGENT CONFIGURATIONS -------------------------------------
% Three-level ultrametric hierarchy per team:
%   Level 1 (local)    4 clusters x 3 agents, within-cluster deaths 4.00/4.03
%   Level 2 (tactical) 2 formations x 2 clusters, inter-cluster death 32.56
%   Level 3 (global)   1 team, inter-formation death 60.00

R = 2.0;  % Cluster radius

% Team A: 2 formations x 2 clusters x 3 agents = 12 agents
A_WIDE   = [tri_cluster(18,22,R); tri_cluster(18,58,R);
            tri_cluster(82,22,R); tri_cluster(82,58,R)];

% Compressed central column. Spacing is uniform at 16 units so that all three
% upper-level deaths coincide at 12.66, giving the flat post-transition
% signature the specification describes.
A_NARROW = [tri_cluster(47,16,R); tri_cluster(47,32,R);
            tri_cluster(47,48,R); tri_cluster(47,64,R)];

% Team B: encircle A-left with 3 clusters, contest A-right with 1
B_PRESS  = [tri_cluster( 5,22,R); tri_cluster(35, 6,R);
            tri_cluster(35,74,R); tri_cluster(96,40,R)];

B_SPREAD = [tri_cluster(26,26,R); tri_cluster(26,54,R);
            tri_cluster(66,22,R); tri_cluster(66,58,R)];

% Single-scale failure: linear deployment (Figure 6)
A_LINE   = [tri_cluster(10,40,R); tri_cluster(40,40,R);
            tri_cluster(80,40,R); tri_cluster(105,40,R)];

% H1 encirclement (Figure 9): Team B on a ring of radius 22 about (30,40),
% with a single Team A cluster either caught inside the ring or clear of it.
RING_C  = [30 40];  RING_RHO = 22;
B_RING  = ring_clusters(RING_C(1), RING_C(2), RING_RHO, 4, R);
A_TRAP  = tri_cluster(RING_C(1), RING_C(2), R);
A_FREE  = tri_cluster(80, 40, R);

% Generalised domain configurations (Figure 5)
TU_T = [tri_cluster(32,24,R);   tri_cluster(32,56,R);     % Tumour clusters
        tri_cluster(68,24,R);   tri_cluster(68,56,R)];
TU_I = [tri_cluster(22,40,2.2); tri_cluster(54, 6,2.2);   % Immune cells
        tri_cluster(54,74,2.2); tri_cluster(97,40,2.2)];

EC_PREY = [tri_cluster(20,22,2.5); tri_cluster(20,58,2.5);  % Prey herd
           tri_cluster(72,22,2.5); tri_cluster(72,58,2.5)];
EC_PRED = [tri_cluster( 4,22,2.5); tri_cluster(38, 6,2.5);  % Predator pack
           tri_cluster(38,74,2.5); tri_cluster(98,40,2.5)];

AU_A = [tri_cluster(22,28,R);   tri_cluster(22,52,R);      % Fleet A
        tri_cluster(62,28,R);   tri_cluster(62,52,R)];
AU_B = [tri_cluster( 4,40,R);   tri_cluster(44,14,R);      % Fleet B
        tri_cluster(44,66,R);   tri_cluster(95,40,R)];

%% -- SECTION 2: REFERENCE H0 DIAGRAMS ------------------------------------
dA_wide   = compute_h0(A_WIDE);
dA_narrow = compute_h0(A_NARROW);
dB_press  = compute_h0(B_PRESS);
dB_spread = compute_h0(B_SPREAD);
dA_line   = compute_h0(A_LINE);

PITCH_DIAM = hypot(120, 80);

fprintf('\n=== REFERENCE VALUES ===\n');
fprintf('H0(A_WIDE)   : '); fprintf('%.2f  ', dA_wide);   fprintf('\n');
fprintf('H0(A_NARROW) : '); fprintf('%.2f  ', dA_narrow); fprintf('\n');
fprintf('H0(A_LINE)   : '); fprintf('%.2f  ', dA_line);   fprintf('\n');
fprintf('W1(A_WIDE, A_NARROW) = %.2f  (naive sorted matching would give %.2f)\n', ...
        wasserstein_p(dA_wide, dA_narrow, 1), naive_w1(dA_wide, dA_narrow));
fprintf('W1(A_WIDE, A_LINE)   = %.2f\n', wasserstein_p(dA_wide, dA_line, 1));
fprintf('Pitch diameter (T1 integrability bound) = %.2f\n', PITCH_DIAM);

% Single-scale failure is a statement about Betti numbers, so verify both
DFAIL = 35;
[b0w, b1w] = betti_at(A_WIDE, DFAIL);
[b0l, b1l] = betti_at(A_LINE, DFAIL);
fprintf('At delta = %d:  A_WIDE (beta0,beta1) = (%d,%d),  A_LINE = (%d,%d)\n', ...
        DFAIL, b0w, b1w, b0l, b1l);

%% -- SECTION 3: ADVERSARIAL TIME SERIES ----------------------------------
dA_ts = cell(T_MAX+1, 1);
dB_ts = cell(T_MAX+1, 1);
rs_main = RandStream('twister', 'Seed', SEED_MAIN);
for t = 0:T_MAX
    [At, Bt] = get_config(t, NOISE, A_WIDE, A_NARROW, B_PRESS, B_SPREAD, ...
                          T_STAR, T_END, rs_main);
    dA_ts{t+1} = compute_h0(At);
    dB_ts{t+1} = compute_h0(Bt);
end

% Wasserstein-1 between consecutive Team A frames: the detection statistic
wA = zeros(T_MAX+1, 1);
for t = 2:T_MAX+1
    wA(t) = wasserstein_p(dA_ts{t}, dA_ts{t-1}, 1);
end
ts = (0:T_MAX)';

%% -- SECTION 4: T2 - CALIBRATED CUSUM DETECTION --------------------------
% The decision interval h is calibrated on independent in-control (null)
% realisations of the same generative process, so that the probability of at
% least one alarm during the monitoring horizon is ALPHA_FA. This is the
% sequential-analysis analogue of calibrating on a reference period of
% settled play, and it removes the need for any ad hoc suppression window.

fprintf('\n=== T2: CUSUM CALIBRATION ===\n');
tic;
HORIZON = T_MAX - MON_START + 1;
W_null  = zeros(N_CAL, T_MAX+1);
for s = 1:N_CAL
    W_null(s,:) = w1_series(A_WIDE, A_NARROW, 0.0, NOISE, 900000+s, ...
                            T_MAX, T_STAR, T_END).';
end
pool     = W_null(:, 6:end);
mu_base  = mean(pool(:));
sig_base = std(pool(:));
kappa    = mu_base + 0.5*sig_base;          % standard CUSUM reference value
peaks    = zeros(N_CAL,1);
for s = 1:N_CAL
    peaks(s) = max(cusum_path(W_null(s,:).', kappa, MON_START));
end
peaks_sorted = sort(peaks);
h_thr = peaks_sorted(ceil((1-ALPHA_FA)*N_CAL));
fprintf('mu_0 = %.2f, sigma_0 = %.2f -> kappa = %.2f, h = %.2f  (%.1f s)\n', ...
        mu_base, sig_base, kappa, h_thr, toc);

[det_t, cusum] = run_cusum(wA, kappa, h_thr, MON_START);
fprintf('Headline realisation (seed %d): T_hat = %d, error = %d\n', ...
        SEED_MAIN, det_t, abs(det_t - T_STAR));

% Held-out validation of the false-alarm rate
n_fa = 0;
for s = 1:N_CAL
    w0 = w1_series(A_WIDE, A_NARROW, 0.0, NOISE, 500000+s, T_MAX, T_STAR, T_END);
    if ~isnan(run_cusum(w0, kappa, h_thr, MON_START)), n_fa = n_fa + 1; end
end
fa_rate = n_fa / N_CAL;
fprintf('Held-out false-alarm rate: %.1f%% (nominal %.0f%%)\n', 100*fa_rate, 100*ALPHA_FA);

%% -- SECTION 5: T1 - FRECHET MEAN AND VARIANCE (W2) ----------------------
% For H0 diagrams with all births at zero and equal cardinality, the exact
% W2 barycentre is the componentwise mean of the sorted death vectors. The
% dispersion is therefore measured in W2 as well, following Turner et al.

fm_global = zeros(T_MAX+1, 1);
fm_var    = zeros(T_MAX+1, 1);
for t = 1:T_MAX+1
    s_idx = max(1, t - WIN + 1);
    win_d = dA_ts(s_idx:t);
    m     = frechet_mean(win_d);
    fm_global(t) = m(end);
    fm_var(t)    = mean(cellfun(@(d) wasserstein_p(d, m, 2)^2, win_d));
end
pre_m  = mean(fm_global(6:T_STAR-4));
post_m = mean(fm_global(T_END+WIN+1:end));
fprintf('\n=== T1: FRECHET MEAN ===\n');
fprintf('Global feature, pre-transition  = %.2f delta-units\n', pre_m);
fprintf('Global feature, post-transition = %.2f delta-units\n', post_m);
fprintf('Frechet variance peaks at t = %d\n', find(fm_var == max(fm_var), 1) - 1);

%% -- SECTION 6: MONTE CARLO VALIDATION OF THE T2 BOUND -------------------
% Scale how far Team A reorganises, so the Wasserstein jump varies, and
% measure how accurately the CUSUM localises the change-point.

fprintf('\n=== T2: MONTE CARLO (%d realisations per condition) ===\n', N_MC);
MC_ALPHA = [0.25 0.50 0.75 1.00];
mc_jump  = zeros(size(MC_ALPHA));
mc_err   = zeros(size(MC_ALPHA));
mc_med   = zeros(size(MC_ALPHA));
mc_pow   = zeros(size(MC_ALPHA));
mc_that  = cell(size(MC_ALPHA));
tic;
for a = 1:numel(MC_ALPHA)
    al = MC_ALPHA(a);
    mc_jump(a) = wasserstein_p(dA_wide, compute_h0(A_WIDE + al*(A_NARROW - A_WIDE)), 1);
    hits = nan(N_MC,1);
    for s = 1:N_MC
        w = w1_series(A_WIDE, A_NARROW, al, NOISE, s, T_MAX, T_STAR, T_END);
        hits(s) = run_cusum(w, kappa, h_thr, MON_START);
    end
    mc_that{a} = hits(~isnan(hits));
    mc_err(a)  = mean(abs(mc_that{a} - T_STAR));
    mc_med(a)  = median(abs(mc_that{a} - T_STAR));
    mc_pow(a)  = sum(~isnan(hits)) / N_MC;
    fprintf('  jump W1 = %5.1f -> E|T_hat - T*| = %5.2f, median = %4.1f, power = %5.1f%%\n', ...
            mc_jump(a), mc_err(a), mc_med(a), 100*mc_pow(a));
end
fprintf('  (%.1f s)\n', toc);

%% -- SECTION 7: DEPENDENCE STRUCTURE (COUPLED VS INDEPENDENT) ------------
% Both models have identical marginal distributions for the agent positions.
% They differ only in temporal structure, so any difference in the
% autocorrelation of the topological signal is attributable to dependence
% alone, not to a change in the noise level or to non-stationarity. The
% comparison is restricted to the pre-transition regime for the same reason.

% A dedicated stationary run is used, long enough for the correlation
% estimates to be well resolved. It is separate from the T_MAX = 100 narrative
% series, which contains a change-point and so is not stationary.
DEP_T     = 400;               % frames in the stationary dependence experiment
DEP_SHOW  = 150;               % frames displayed in the time-series panels
DEP_PHI   = 0.85;              % AR(1) persistence of each team's drift
DEP_RHO   = 0.90;              % strength of B's response to A's previous move
DEP_DRIFT = 4.0;               % marginal s.d. of the cluster-centre drift
[wc_A, wc_B] = coupled_series(A_WIDE, B_PRESS, DEP_T, NOISE, DEP_DRIFT, DEP_PHI, DEP_RHO, 2024, true);
[wi_A, wi_B] = coupled_series(A_WIDE, B_PRESS, DEP_T, NOISE, DEP_DRIFT, DEP_PHI, DEP_RHO, 2024, false);

NLAG  = 25;
ac_c  = autocorr_manual(wc_A, NLAG);
ac_i  = autocorr_manual(wi_A, NLAG);
xc_c  = crosscorr_manual(wc_A, wc_B, NLAG);
xc_i  = crosscorr_manual(wi_A, wi_B, NLAG);
ci95  = 1.96 / sqrt(numel(wc_A));

fprintf('\n=== DEPENDENCE (stationary, %d frames) ===\n', DEP_T);
fprintf('Marginal s.d. of the signal:   coupled %.2f, independent %.2f (should agree)\n', ...
        std(wc_A), std(wi_A));
fprintf('Lag-1 autocorrelation:         coupled %+.3f, independent %+.3f (95%% CI +/- %.3f)\n', ...
        ac_c(2), ac_i(2), ci95);
[pk_c, pl_c] = max(xc_c); [pk_i, pl_i] = max(xc_i);
fprintf('Peak A-to-B cross-correlation: coupled %+.3f at lag %d, independent %+.3f at lag %d\n', ...
        pk_c, pl_c-1, pk_i, pl_i-1);

% A single realisation of a 25-lag correlogram will put roughly one bar outside
% a 95% band by chance, and occasionally several. To show that the displayed
% realisation is representative rather than selected, the lag-1 statistic is
% repeated over independent replicates. The independent model should return a
% mean of zero and a band-exceedance rate near the nominal 5%.
DEP_REPS = 200;
r1_c = zeros(DEP_REPS,1); r1_i = zeros(DEP_REPS,1);
for r = 1:DEP_REPS
    rc = coupled_series(A_WIDE, B_PRESS, DEP_T, NOISE, DEP_DRIFT, DEP_PHI, DEP_RHO, 7000+r, true);
    ri = coupled_series(A_WIDE, B_PRESS, DEP_T, NOISE, DEP_DRIFT, DEP_PHI, DEP_RHO, 9000+r, false);
    ac = autocorr_manual(rc, 1); r1_c(r) = ac(2);
    ac = autocorr_manual(ri, 1); r1_i(r) = ac(2);
end
rep_c   = mean(r1_c);              rep_i   = mean(r1_i);
pow_c   = mean(abs(r1_c) > ci95);  fa_i    = mean(abs(r1_i) > ci95);
fprintf(['Over %d replicates, lag-1 rho: coupled %+.3f (sd %.3f), independent %+.3f (sd %.3f)\n' ...
         '  detection rate at the 95%% band: coupled %.0f%%, independent %.0f%% (nominal 5%%)\n'], ...
        DEP_REPS, rep_c, std(r1_c), rep_i, std(r1_i), 100*pow_c, 100*fa_i);

%% =========================================================================
%% FIGURE GENERATION
%% =========================================================================

%% -- Figure 1: Multi-scale framework -------------------------------------
f1 = figure('Position',[50 50 1500 820],'Color','w','Name','Fig1 Multi-Scale');
tl = tiledlayout(f1, 2, 3, 'TileSpacing','compact','Padding','compact');
DELTAS    = [DELTA_LOCAL, DELTA_TACTICAL, DELTA_GLOBAL];
DLABELS   = {sprintf('\\delta_1 = %g  —  Local', DELTA_LOCAL), ...
             sprintf('\\delta_2 = %g  —  Tactical', DELTA_TACTICAL), ...
             sprintf('\\delta_3 = %g  —  Global', DELTA_GLOBAL)};
SUBTITLES = {'Within-cluster groups form', 'Formations emerge', 'Team-wide shape closes'};

for c = 1:3
    ax = nexttile(tl, c);
    setup_pitch(ax, 'football', CPITCH, CGRASS);
    draw_vr(ax, B_PRESS, CB, DELTAS(c), 26, 0.28, 0.85, 0.9);
    draw_vr(ax, A_WIDE,  CA, DELTAS(c), 32, 0.40, 0.92, 1.1);
    nA = 1 + sum(dA_wide  > DELTAS(c));
    nB = 1 + sum(dB_press > DELTAS(c));
    pitch_title(ax, DLABELS{c}, sprintf('%s   (\\beta_0: A = %d, B = %d)', SUBTITLES{c}, nA, nB), CINK);
    panel_label(ax, char('A'+c-1));

    ax2 = nexttile(tl, c+3);
    draw_two_barcodes(ax2, dA_wide, dB_press, CA, CB, DELTAS(c), 92);
    if c == 1, ylabel(ax2, 'Team B    |    Team A', 'FontSize',8.5,'Color',CGREY); end
    if c == 2, xlabel(ax2, 'Scale \delta (pitch units)', 'FontSize',9); end
    panel_label(ax2, char('D'+c-1));
end
title(tl, 'Multi-Scale Topological Structure of Adversarial Collective Systems', ...
      'FontSize',13,'FontWeight','bold','Color',CINK);
subtitle(tl, ['Coloured bars cross the amber threshold, so they are the components still separate ' ...
              'at that scale: their count is \beta_0 - 1.  Note \delta_2 falls between the tactical ' ...
              '(32.6) and global (60.0) deaths, where the previous \delta_2 = 22 did not.'], ...
         'FontSize',9.5,'Color',CGREY);
save_if(SAVE_FIGS, f1, fullfile(OUTPUT_DIR,'fig1_multiscale.png'), FIG_DPI);

%% -- Figure 2: Scale-specific adversarial coupling -----------------------
f2 = figure('Position',[50 50 1250 950],'Color','w','Name','Fig2 Adversarial Coupling');
tl = tiledlayout(f2, 3, 3, 'TileSpacing','compact','Padding','compact');
SCALE_LABELS = {'\delta_1 — Local', '\delta_2 — Tactical', '\delta_3 — Global'};
SCALE_DESC   = {'Clusters contest possession locally', ...
                'Formations contest at the same scale', ...
                'Team-wide shapes contest globally'};

for row = 1:3
    dl = DELTAS(row);

    ax = nexttile(tl, (row-1)*3+1);
    setup_pitch(ax, 'football', CPITCH, CGRASS);
    draw_vr(ax, A_WIDE, CA, dl, 40, 0.45, 0.92, 1.3);
    outline_components(ax, A_WIDE, dl, CA);
    ylabel_pitch(ax, SCALE_LABELS{row}, CINK);
    if row == 1, pitch_title(ax, 'Team A structure','', CA); end
    panel_label(ax, char('A'+row-1));

    ax2 = nexttile(tl, (row-1)*3+2);
    draw_contest_arrow(ax2, SCALE_DESC{row}, ...
                       1 + sum(dA_wide > dl), 1 + sum(dB_press > dl), CB, CGREY);

    ax3 = nexttile(tl, (row-1)*3+3);
    setup_pitch(ax3, 'football', CPITCH, CGRASS);
    draw_vr(ax3, B_PRESS, CB, dl, 40, 0.40, 0.92, 1.2);
    outline_components(ax3, B_PRESS, dl, CB);
    if row == 1, pitch_title(ax3, 'Team B response','', CB); end
    panel_label(ax3, char('D'+row-1));
end
title(tl, 'Scale-Specific Adversarial Coupling in Competitive Collective Systems', ...
      'FontSize',12.5,'FontWeight','bold','Color',CINK);
subtitle(tl, ['At each level of the hierarchy the collective reshapes in response to an ' ...
              'opposing system acting at the equivalent scale.  Dashed outlines mark the ' ...
              'connected components at that \delta.'], 'FontSize',9.5,'Color',CGREY);
save_if(SAVE_FIGS, f2, fullfile(OUTPUT_DIR,'fig2_adversarial_coupling.png'), FIG_DPI);

%% -- Figure 3: Phase transition and T2 detection -------------------------
f3 = figure('Position',[50 50 1320 980],'Color','w','Name','Fig3 Phase Transition');
tl = tiledlayout(f3, 2, 2, 'TileSpacing','compact','Padding','compact');
DELTA_DISPLAY = DELTA_TACTICAL;

ax = nexttile(tl, 1);
setup_pitch(ax, 'football', CPITCH, CGRASS);
draw_vr(ax, B_PRESS, CB, DELTA_DISPLAY, 28, 0.28, 0.85, 0.9);
draw_vr(ax, A_WIDE,  CA, DELTA_DISPLAY, 34, 0.40, 0.92, 1.1);
draw_ellipse(ax, 18, 40, 9, 27, CA, 1.5);
draw_ellipse(ax, 82, 40, 9, 27, CA, 1.5);
text(ax, 18, 76, 'F_1','FontSize',10,'Color',CA,'FontWeight','bold','HorizontalAlignment','center');
text(ax, 82, 76, 'F_2','FontSize',10,'Color',CA,'FontWeight','bold','HorizontalAlignment','center');
pitch_title(ax, sprintf('Pre-transition  (t < %d)', T_STAR),'Two-formation topology', CINK);
panel_label(ax, 'A');

ax = nexttile(tl, 2);
setup_pitch(ax, 'football', CPITCH, CGRASS);
draw_vr(ax, B_SPREAD, CB, DELTA_DISPLAY, 28, 0.28, 0.85, 0.9);
draw_vr(ax, A_NARROW, CA, DELTA_DISPLAY, 34, 0.40, 0.92, 1.1);
draw_ellipse(ax, 47, 40, 7, 32, CA, 1.5);
text(ax, 47, 76, 'F_1 (compressed)','FontSize',9,'Color',CA,'FontWeight','bold','HorizontalAlignment','center');
pitch_title(ax, sprintf('Post-transition  (t > %d)', T_END),'Compressed single-formation topology', CINK);
panel_label(ax, 'B');

% Panel C: paired barcodes before and after
ax = nexttile(tl, 3); hold(ax,'on');
CA_LIGHT = [147 197 253]/255;
sA = sort(dA_wide); sA2 = sort(dA_narrow); nb = numel(sA);
hPre = gobjects(1); hPost = gobjects(1);
for k = 1:nb
    hPre  = barh(ax, k+0.19, sA(k),  0.34,'FaceColor',CA,      'EdgeColor','none','FaceAlpha',0.85);
    hPost = barh(ax, k-0.19, sA2(k), 0.34,'FaceColor',CA_LIGHT,'EdgeColor','none','FaceAlpha',0.9);
end
xlim(ax,[0 92]); ylim(ax,[0.3 nb+1.6]); yticks(ax,[]);
w1_tt = wasserstein_p(dA_wide, dA_narrow, 1);
plot(ax, [sA(end) sA2(end)], [nb+0.19 nb-0.19], '-', 'Color',[0.85 0.1 0.1],'LineWidth',1.4);
plot(ax, sA2(end), nb-0.19, '<', 'Color',[0.85 0.1 0.1],'MarkerFaceColor',[0.85 0.1 0.1],'MarkerSize',5);
text(ax, mean([sA(end) sA2(end)]), nb+0.95, ...
     sprintf('global feature  %.1f \\rightarrow %.1f', sA(end), sA2(end)), ...
     'Color',[0.85 0.1 0.1],'FontSize',8.5,'FontWeight','bold','HorizontalAlignment','center');
xlabel(ax,'Scale \delta (pitch units)','FontSize',9.5);
title(ax,'H_0 persistence barcodes, before and after','FontSize',10,'FontWeight','bold','Color',CINK);
subtitle(ax, sprintf('W_1(D^-, D^+) = %.1f units', w1_tt),'FontSize',8.5,'Color',CGREY,'FontAngle','italic');
legend(ax,[hPre hPost],{sprintf('Pre  (t < %d)',T_STAR),sprintf('Post (t > %d)',T_END)}, ...
       'Location','southeast','FontSize',8.5,'Box','off');
box(ax,'off'); panel_label(ax,'C');

% Panel D: detection statistic and CUSUM
ax = nexttile(tl, 4);
yyaxis(ax,'left'); hold(ax,'on');
ymaxL = max(wA)*1.35;
patch(ax, [0 MON_START-1 MON_START-1 0], [0 0 ymaxL ymaxL], CFAINT, ...
      'FaceAlpha',0.4,'EdgeColor','none','HandleVisibility','off');
hW = plot(ax, ts, wA, 'Color',[CA 0.9],'LineWidth',1.2);
text(ax, (MON_START-1)/2, ymaxL*0.05,'in-control calibration','FontSize',8, ...
     'Color',CGREY,'HorizontalAlignment','center','FontAngle','italic');
ylabel(ax,'W_1(D_t, D_{t-1})   [pitch units]','FontSize',9.5,'Color',CA);
ylim(ax,[0 ymaxL]); ax.YColor = CA;
yyaxis(ax,'right'); hold(ax,'on');
hC = plot(ax, ts, cusum, 'Color',CV,'LineWidth',2.2);
hH = plot(ax, [MON_START-0.5 T_MAX], [h_thr h_thr], '--','Color',CK,'LineWidth',1.5);
ylabel(ax,'CUSUM  C(t)','FontSize',9.5,'Color',CV);
ylim(ax,[0 max([cusum; h_thr],[],'omitnan')*1.35]); ax.YColor = CV;
hT = xline(ax, T_STAR, '--','Color',[0.85 0.1 0.1],'LineWidth',1.6);
hD = xline(ax, det_t, '-','Color',CV,'LineWidth',1.8);
yl = ylim(ax);
text(ax, T_STAR-1.5, yl(2)*0.97, 'T^* = 50','Color',[0.85 0.1 0.1],'FontSize',9, ...
     'FontWeight','bold','HorizontalAlignment','right','VerticalAlignment','top');
text(ax, det_t+1.5, yl(2)*0.97, sprintf('$\\hat{T} = %d$ (error %d)', det_t, abs(det_t-T_STAR)), ...
     'Color',CGN,'FontSize',9.5,'FontWeight','bold','Interpreter','latex','VerticalAlignment','top');
text(ax, T_MAX-1, h_thr, sprintf(' h (%.0f%% false alarm) ', 100*ALPHA_FA), ...
     'Color',CK,'FontSize',8,'HorizontalAlignment','right','VerticalAlignment','bottom');
xlim(ax,[0 T_MAX]); xlabel(ax,'Time t (frames)','FontSize',9.5);
title(ax,'T2 — calibrated CUSUM change-point detection','FontSize',10,'FontWeight','bold','Color',CINK);
subtitle(ax, sprintf('held-out false-alarm rate %.1f%% against a %.0f%% target', ...
         100*fa_rate, 100*ALPHA_FA),'FontSize',8.5,'Color',CGREY,'FontAngle','italic');
legend(ax,[hW hC hH hT hD],{'W_1 signal','CUSUM C(t)','threshold h','true T^*','detected'}, ...
       'Location','northwest','FontSize',8,'Box','off');
panel_label(ax,'D');

title(tl,'Topological Phase Transition and Change-Point Detection', ...
      'FontSize',12.5,'FontWeight','bold','Color',CINK);
subtitle(tl, sprintf(['Team A reorganises from two formations to one at T^* = %d.  ' ...
        'The CUSUM accumulates the Wasserstein signal and fires at t = %d.'], T_STAR, det_t), ...
        'FontSize',9.5,'Color',CGREY);
save_if(SAVE_FIGS, f3, fullfile(OUTPUT_DIR,'fig3_phase_transition.png'), FIG_DPI);

%% -- Figure 4: T1 Frechet mean stability ---------------------------------
f4 = figure('Position',[50 50 1320 570],'Color','w','Name','Fig4 Frechet T1');
tl = tiledlayout(f4, 1, 2, 'TileSpacing','compact','Padding','compact');
SETTLE = T_END + WIN;   % trailing window means the mean settles WIN frames late

ax = nexttile(tl, 1); hold(ax,'on');
ymax = max(fm_global)*1.28;
shade_regimes(ax, T_STAR, SETTLE, T_MAX, ymax, CA, CK);
fill(ax, [ts; flipud(ts)], [fm_global; zeros(T_MAX+1,1)], CA,'FaceAlpha',0.12,'EdgeColor','none');
plot(ax, ts, fm_global, 'Color',CA,'LineWidth',2.4);
xline(ax, T_STAR,'--','Color',[0.85 0.1 0.1],'LineWidth',1.5);
yline(ax, pre_m, ':','Color',CA,'LineWidth',1.2);
yline(ax, post_m,':','Color',CK,'LineWidth',1.2);
text(ax, 24, pre_m+ymax*0.055, sprintf('stable mean  %.1f \\delta-units', pre_m), ...
     'Color',CA,'FontSize',9,'FontWeight','bold','HorizontalAlignment','center');
text(ax, 84, post_m+ymax*0.055, sprintf('new stable mean  %.1f \\delta-units', post_m), ...
     'Color',[146 64 14]/255,'FontSize',9,'FontWeight','bold','HorizontalAlignment','center');
text(ax, T_STAR-1.5, ymax*0.96,'T^* = 50','Color',[0.85 0.1 0.1],'FontSize',9, ...
     'FontWeight','bold','HorizontalAlignment','right');
text(ax, T_MAX-2, ymax*0.96, sprintf('pitch diameter %.0f is the T1 integrability bound', PITCH_DIAM), ...
     'Color',CGREY,'FontSize',7.5,'FontAngle','italic','HorizontalAlignment','right');
xlim(ax,[0 T_MAX]); ylim(ax,[0 ymax]);
xlabel(ax,'Time t (frames)','FontSize',10);
ylabel(ax,'Frechet mean of the global H_0 death (\delta)','FontSize',10);
title(ax,'T1 — Frechet mean trajectory','FontSize',10.5,'FontWeight','bold','Color',CINK);
subtitle(ax,['Bounded domain gives integrability, so the mean is well defined ' ...
             'under adversarial dependence'],'FontSize',8.5,'Color',CGREY,'FontAngle','italic');
panel_label(ax,'A');

ax = nexttile(tl, 2); hold(ax,'on');
vmax = max(fm_var)*1.25;
shade_regimes(ax, T_STAR, SETTLE, T_MAX, vmax, CA, CK);
fill(ax, [ts; flipud(ts)], [fm_var; zeros(T_MAX+1,1)], CV,'FaceAlpha',0.12,'EdgeColor','none');
plot(ax, ts, fm_var,'Color',CV,'LineWidth',2.2);
xline(ax, T_STAR,'--','Color',[0.85 0.1 0.1],'LineWidth',1.5);
[spk_v, spk_i] = max(fm_var);
plot(ax, spk_i-1, spk_v,'o','Color',CV,'MarkerFaceColor',CV,'MarkerSize',7);
text(ax, spk_i+2, spk_v*0.94, sprintf('peak at t = %d\n(window spans both regimes)', spk_i-1), ...
     'Color',CV,'FontSize',8.5,'FontWeight','bold');
xlim(ax,[0 T_MAX]); ylim(ax,[0 vmax]);
xlabel(ax,'Time t (frames)','FontSize',10);
ylabel(ax,'Frechet variance  \sigma^2_F(t)   [W_2^2]','FontSize',10);
title(ax,'T1 — Frechet variance','FontSize',10.5,'FontWeight','bold','Color',CINK);
subtitle(ax,'Spikes at the transition and recovers: the mean is unique in each steady state', ...
         'FontSize',8.5,'Color',CGREY,'FontAngle','italic');
panel_label(ax,'B');

title(tl,'Frechet Mean Stability Under Competitive Dependence  (Theorem T1)', ...
      'FontSize',12.5,'FontWeight','bold','Color',CINK);
subtitle(tl, sprintf(['Sliding window of %d frames.  Because the window is trailing, the mean ' ...
        'settles %d frames after the transition completes (amber band).'], WIN, WIN), ...
        'FontSize',9.5,'Color',CGREY);
save_if(SAVE_FIGS, f4, fullfile(OUTPUT_DIR,'fig4_frechet_diagram_mean.png'), FIG_DPI);

%% -- Figure 5: Framework universality ------------------------------------
f5 = figure('Position',[50 50 1620 980],'Color','w','Name','Fig5 Generalised');
tl = tiledlayout(f5, 2, 4, 'TileSpacing','compact','Padding','compact');
DOM_A     = {A_WIDE,  TU_T,  EC_PREY,  AU_A};
DOM_B     = {B_PRESS, TU_I,  EC_PRED,  AU_B};
DOM_NAMES = {'Professional Football','Tumour-Immune Competition', ...
             'Predator-Prey Ecology','Autonomous Fleet Coordination'};
DOM_SUBS  = {'Established testbed','Cancer biology (Standard Grant)', ...
             'Population dynamics','Contested routing'};
DOM_ALAB  = {'Attacking team','Tumour cells','Prey herd','Fleet A'};
DOM_BLAB  = {'Defending team','Immune cells','Predator pack','Fleet B'};
DOM_ACS   = {CA, [30 64 175]/255, [20 83 45]/255, CA};
DOM_BCS   = {CB, [159 28 56]/255, [120 53 15]/255, CV};
DOM_BG    = {'football','tissue','ecology','corridor'};
DOM_BGC   = {CPITCH, [255 241 242]/255, [254 252 232]/255, [240 249 255]/255};
DOM_BGG   = {CGRASS, [253 164 175]/255, [161 98 7]/255, [125 211 252]/255};

for d = 1:4
    dA_d = compute_h0(DOM_A{d});
    dB_d = compute_h0(DOM_B{d});
    dl_d = tactical_scale(dA_d);   % per-domain scale: formations visible, team not yet whole

    ax = nexttile(tl, d);
    setup_pitch(ax, DOM_BG{d}, DOM_BGC{d}, DOM_BGG{d});
    draw_vr(ax, DOM_B{d}, DOM_BCS{d}, dl_d, 28, 0.28, 0.85, 0.9);
    draw_vr(ax, DOM_A{d}, DOM_ACS{d}, dl_d, 34, 0.40, 0.92, 1.1);
    text(ax, 2, 77, DOM_ALAB{d},'FontSize',8,'Color',DOM_ACS{d},'FontWeight','bold');
    text(ax, 118,77, DOM_BLAB{d},'FontSize',8,'Color',DOM_BCS{d},'FontWeight','bold', ...
         'HorizontalAlignment','right');
    pitch_title(ax, DOM_NAMES{d}, sprintf('%s   (shown at \\delta = %.0f)', DOM_SUBS{d}, dl_d), CINK);
    panel_label(ax, char('A'+d-1));

    ax2 = nexttile(tl, d+4);
    draw_two_barcodes(ax2, dA_d, dB_d, DOM_ACS{d}, DOM_BCS{d}, dl_d, 92, false);
    annotate_levels(ax2, dA_d);
    if d == 1, ylabel(ax2, 'defender    |    attacker','FontSize',8.5,'Color',CGREY); end
    if d == 2, xlabel(ax2,'Scale \delta (domain units)','FontSize',9); end
    panel_label(ax2, char('E'+d-1));
end
title(tl,'Framework Universality: Three-Level Competitive Topology Across Four Domains', ...
      'FontSize',12.5,'FontWeight','bold','Color',CINK);
subtitle(tl, {['The attacking collective carries the same three-level ultrametric hierarchy ' ...
               'in every domain (labelled above each barcode).'], ...
              ['The defending collective is deliberately not hierarchical: it is organised to ' ...
               'contest, which is precisely what the framework has to accommodate.']}, ...
         'FontSize',9.5,'Color',CGREY);
save_if(SAVE_FIGS, f5, fullfile(OUTPUT_DIR,'fig5_generalised.png'), FIG_DPI);

%% -- Figure 6: Single-scale failure --------------------------------------
f6 = figure('Position',[50 50 1420 900],'Color','w','Name','Fig6 Single-Scale Failure');
tl = tiledlayout(f6, 2, 3, 'TileSpacing','compact','Padding','compact');

ax = nexttile(tl, 1);
setup_pitch(ax,'football',CPITCH,CGRASS);
draw_vr(ax, A_WIDE, CA, DFAIL, 36, 0.45, 0.92, 1.3);
draw_ellipse(ax, 18, 40, 9, 27, CA, 1.5);
draw_ellipse(ax, 82, 40, 9, 27, CA, 1.5);
text(ax, 18, 76,'Comp. 1','FontSize',8,'Color',CA,'FontWeight','bold','HorizontalAlignment','center');
text(ax, 82, 76,'Comp. 2','FontSize',8,'Color',CA,'FontWeight','bold','HorizontalAlignment','center');
pitch_title(ax,'Config 1: two-formation layout', ...
            sprintf('at \\delta = %d:  \\beta_0 = %d,  \\beta_1 = %d', DFAIL, b0w, b1w), CINK);
panel_label(ax,'A');

ax = nexttile(tl, 2);
draw_verdict(ax,'SINGLE SCALE', sprintf('indistinguishable at \\delta = %d', DFAIL), ...
             sprintf('(\\beta_0, \\beta_1) = (%d, %d) for both', b0w, b1w), ...
             [0.85 0.1 0.1], [254 226 226]/255);

ax = nexttile(tl, 3);
setup_pitch(ax,'football',CPITCH,CGRASS);
draw_vr(ax, A_LINE, CA, DFAIL, 36, 0.45, 0.92, 1.3);
draw_ellipse(ax, 25,  40, 20, 6, CA, 1.5);
draw_ellipse(ax, 92.5,40, 20, 6, CA, 1.5);
text(ax, 25,  76,'Comp. 1','FontSize',8,'Color',CA,'FontWeight','bold','HorizontalAlignment','center');
text(ax, 92.5,76,'Comp. 2','FontSize',8,'Color',CA,'FontWeight','bold','HorizontalAlignment','center');
pitch_title(ax,'Config 2: linear deployment', ...
            sprintf('at \\delta = %d:  \\beta_0 = %d,  \\beta_1 = %d', DFAIL, b0l, b1l), CINK);
panel_label(ax,'B');

ax = nexttile(tl, 4);
draw_barcode(ax, dA_wide, CA, [], 92,'Config 1 — full H_0 barcode');
annotate_levels(ax, dA_wide);
xlabel(ax,'Scale \delta (pitch units)','FontSize',9.5);
panel_label(ax,'C');

ax = nexttile(tl, 5);
draw_verdict(ax,'MULTI SCALE','clearly distinct across the filtration', ...
             sprintf('W_1(full barcodes) = %.1f units', wasserstein_p(dA_wide,dA_line,1)), ...
             CGN, [220 252 231]/255);

ax = nexttile(tl, 6);
draw_barcode(ax, dA_line, CA, [], 92,'Config 2 — full H_0 barcode');
annotate_levels(ax, dA_line);
gm_w = max(dA_wide); gm_l = max(dA_line);
text(ax, gm_l+3, 7.2, sprintf('global merge at \\delta = %.0f,\nnot \\delta = %.0f', gm_l, gm_w), ...
     'Color',[0.85 0.1 0.1],'FontSize',8.5,'FontWeight','bold');
plot(ax, [gm_l+2.5 gm_l+0.4],[7.0 numel(dA_line)-0.2],'-','Color',[0.85 0.1 0.1],'LineWidth',1.2);
xlabel(ax,'Scale \delta (pitch units)','FontSize',9.5);
panel_label(ax,'D');

title(tl,'The Single-Scale Failure: Tactically Distinct Configurations With Identical Betti Numbers', ...
      'FontSize',12,'FontWeight','bold','Color',CINK);
subtitle(tl, sprintf(['At \\delta = %d both layouts have \\beta_0 = %d and \\beta_1 = %d, so no single ' ...
        'threshold can separate them.  Across the whole filtration they differ by W_1 = %.1f units.'], ...
        DFAIL, b0w, b1w, wasserstein_p(dA_wide,dA_line,1)),'FontSize',9.5,'Color',CGREY);
save_if(SAVE_FIGS, f6, fullfile(OUTPUT_DIR,'fig6_singlescale.png'), FIG_DPI);

%% -- Figure 7: Coin-flip vs tug-of-war -----------------------------------
f7 = figure('Position',[50 50 1300 1050],'Color','w','Name','Fig7 Dependence');
tl = tiledlayout(f7, 3, 2, 'TileSpacing','compact','Padding','compact');
tdep = (0:DEP_SHOW)';
LAGS = (0:NLAG)';

for col = 1:2
    if col == 1
        wa = wc_A; ac = ac_c; xc = xc_c; cc = CA;
        lab = 'Tug-of-war: Team B tracks Team A';
    else
        wa = wi_A; ac = ac_i; xc = xc_i; cc = [100 116 139]/255;
        lab = 'Coin-flip: independent frames';
    end

    ax = nexttile(tl, col); hold(ax,'on');
    wshow = wa(1:DEP_SHOW+1);
    fill(ax,[tdep; flipud(tdep)],[wshow; zeros(numel(tdep),1)],cc,'FaceAlpha',0.15,'EdgeColor','none');
    plot(ax, tdep, wshow,'Color',[cc 0.95],'LineWidth',1.2);
    xlim(ax,[0 DEP_SHOW]); ylim(ax,[0 max([wc_A; wi_A])*1.1]);
    xlabel(ax,'Time t (frames)','FontSize',9);
    ylabel(ax,'W_1(D_t, D_{ref})','FontSize',9);
    title(ax, lab,'FontSize',11,'FontWeight','bold','Color',cc);
    subtitle(ax, sprintf(['stationary throughout, so no change-point is present   ' ...
             '(marginal s.d. %.1f; first %d of %d frames shown)'], std(wa), DEP_SHOW, DEP_T), ...
             'FontSize',8,'Color',CGREY,'FontAngle','italic');
    panel_label(ax, char('A'+col-1));

    % Lag 0 is trivially 1 and is omitted so the scale is set by the lags that
    % actually carry information.
    ax = nexttile(tl, 2+col); hold(ax,'on');
    bar(ax, LAGS(2:end), ac(2:end), 0.8,'FaceColor',cc,'EdgeColor','none','FaceAlpha',0.8);
    yline(ax, 0,'k-','LineWidth',0.8);
    yline(ax, ci95,'--','Color',CFAINT,'LineWidth',1.1);
    yline(ax,-ci95,'--','Color',CFAINT,'LineWidth',1.1);
    xlim(ax,[0.3 NLAG+0.7]); ylim(ax,[-0.25 0.62]);
    xlabel(ax,'Lag (frames)','FontSize',9);
    ylabel(ax,'Autocorrelation  \rho_k','FontSize',9);
    nsig = sum(abs(ac(2:end)) > ci95);
    text(ax, NLAG*0.62, 0.57, sprintf('\\rho_1 = %+.2f;  %d of %d lags\noutside the 95%% band', ...
         ac(2), nsig, NLAG),'Color',cc,'FontSize',8.5,'FontWeight','bold', ...
         'HorizontalAlignment','center','VerticalAlignment','top');
    % One or two bars outside the band is expected in any 25-lag correlogram, so
    % the replicate summary is quoted to show this realisation is typical.
    if col == 1, rmu = rep_c; rdet = pow_c; else, rmu = rep_i; rdet = fa_i; end
    text(ax, NLAG*0.62, 0.40, sprintf('over %d replicates: mean %+.2f,\ndetected %.0f%% of the time', ...
         DEP_REPS, rmu, 100*rdet),'Color',CGREY,'FontSize',7.8,'FontAngle','italic', ...
         'HorizontalAlignment','center','VerticalAlignment','top');
    panel_label(ax, char('C'+col-1));

    ax = nexttile(tl, 4+col); hold(ax,'on');
    bar(ax, LAGS, xc, 0.8,'FaceColor',cc,'EdgeColor','none','FaceAlpha',0.8);
    yline(ax, 0,'k-','LineWidth',0.8);
    yline(ax, ci95,'--','Color',CFAINT,'LineWidth',1.1);
    yline(ax,-ci95,'--','Color',CFAINT,'LineWidth',1.1);
    % A response is only claimed when the peak is both clearly significant and
    % at a short lag; an isolated bar at lag 20 is sampling noise, not tracking.
    [pk, pl] = max(xc);
    if pk > 2*ci95 && LAGS(pl) <= 5
        plot(ax, LAGS(pl), pk,'v','Color',[0.85 0.1 0.1],'MarkerFaceColor',[0.85 0.1 0.1],'MarkerSize',6);
        text(ax, LAGS(pl)+1.2, pk*0.97, sprintf('B responds to A after %d frame', LAGS(pl)), ...
             'Color',[0.85 0.1 0.1],'FontSize',8.5,'FontWeight','bold','VerticalAlignment','top');
    else
        text(ax, NLAG/2, 0.45,'no cross-team structure','HorizontalAlignment','center', ...
             'Color',CGREY,'FontSize',9.5,'FontAngle','italic');
    end
    xlim(ax,[-0.7 NLAG+0.7]); ylim(ax,[-0.25 0.62]);
    xlabel(ax,'Lag (frames), Team A leading','FontSize',9);
    ylabel(ax,'Cross-correlation  A \rightarrow B','FontSize',9);
    panel_label(ax, char('E'+col-1));
end
title(tl,'Coin-Flip vs Tug-of-War: Why Competitive Data Violates the Independence Assumption', ...
      'FontSize',12,'FontWeight','bold','Color',CINK);
subtitle(tl, {['Identical marginal distributions and noise level in both columns, and no ' ...
               'change-point in either: only the dependence structure differs.'], ...
              'Standard statistical topology assumes the left-hand column does not happen.'}, ...
         'FontSize',9.5,'Color',CGREY);
save_if(SAVE_FIGS, f7, fullfile(OUTPUT_DIR,'fig7_dependence.png'), FIG_DPI);

%% -- Figure 8: Monte Carlo validation of T2 ------------------------------
f8 = figure('Position',[50 50 1400 620],'Color','w','Name','Fig8 T2 Monte Carlo');
tl = tiledlayout(f8, 1, 3, 'TileSpacing','compact','Padding','compact');

ax = nexttile(tl, 1); hold(ax,'on');
mc_cols = [0.62 0.76 0.90; 0.36 0.58 0.86; 0.16 0.38 0.78; 0.06 0.15 0.50];
edges  = (MON_START-0.5):1:(T_MAX+0.5);
cmax   = 0;
for a = 1:numel(MC_ALPHA)
    cnt  = histcounts(mc_that{a}, edges) / N_MC;
    cmax = max(cmax, max(cnt));
    stairs(ax, edges(1:end-1)+0.5, cnt,'Color',mc_cols(a,:),'LineWidth',1.8, ...
           'DisplayName',sprintf('W_1 jump = %.0f', mc_jump(a)));
end
ylim(ax,[0 cmax*1.35]);
xline(ax, T_STAR,'--','Color',[0.85 0.1 0.1],'LineWidth',1.5,'HandleVisibility','off');
text(ax, T_STAR+1, cmax*1.05,'T^* = 50','Color',[0.85 0.1 0.1],'FontSize',9.5,'FontWeight','bold', ...
     'HorizontalAlignment','left');
xlim(ax,[MON_START T_MAX]); xlabel(ax,'Detected change-point  T^{\wedge}','FontSize',10);
ylabel(ax,'Proportion of realisations','FontSize',10);
title(ax,'Distribution of the detected change-point','FontSize',10.5,'FontWeight','bold','Color',CINK);
subtitle(ax, sprintf('%d realisations per condition', N_MC),'FontSize',8.5,'Color',CGREY,'FontAngle','italic');
legend(ax,'Location','northeast','FontSize',8.5,'Box','off');
panel_label(ax,'A');

ax = nexttile(tl, 2); hold(ax,'on');
plot(ax, mc_jump, mc_err,'o-','Color',CV,'MarkerFaceColor',CV,'LineWidth',2.2,'MarkerSize',8);
for a = 1:numel(MC_ALPHA)
    text(ax, mc_jump(a), mc_err(a)+0.9, sprintf('%.1f', mc_err(a)), ...
         'Color',CV,'FontSize',8.5,'FontWeight','bold','HorizontalAlignment','center');
end
xlabel(ax,'Wasserstein jump  W_1(D^-, D^+)','FontSize',10);
ylabel(ax,'E| T^{\wedge} - T^* |   (frames)','FontSize',10);
ylim(ax,[0 max(mc_err)*1.25]);
title(ax,'T2 — localisation error falls as the jump grows','FontSize',10.5,'FontWeight','bold','Color',CINK);
subtitle(ax,'the qualitative content of the T2 bound','FontSize',8.5,'Color',CGREY,'FontAngle','italic');
grid(ax,'on'); ax.GridAlpha = 0.12;
panel_label(ax,'B');

ax = nexttile(tl, 3); hold(ax,'on');
plot(ax, mc_jump, 100*mc_pow,'s-','Color',CGN,'MarkerFaceColor',CGN,'LineWidth',2.2,'MarkerSize',8);
yline(ax, 100*fa_rate,'--','Color',CK,'LineWidth',1.5);
text(ax, mc_jump(1), 100*fa_rate+4, sprintf('false-alarm floor %.1f%%', 100*fa_rate), ...
     'Color',CK,'FontSize',8.5,'FontWeight','bold');
xlabel(ax,'Wasserstein jump  W_1(D^-, D^+)','FontSize',10);
ylabel(ax,'Detection rate (%)','FontSize',10);
ylim(ax,[0 105]);
title(ax,'Detection power against jump size','FontSize',10.5,'FontWeight','bold','Color',CINK);
subtitle(ax, sprintf('threshold calibrated for %.0f%% false alarms', 100*ALPHA_FA), ...
         'FontSize',8.5,'Color',CGREY,'FontAngle','italic');
grid(ax,'on'); ax.GridAlpha = 0.12;
panel_label(ax,'C');

title(tl,'Monte Carlo Validation of the T2 Change-Point Localisation Bound', ...
      'FontSize',12.5,'FontWeight','bold','Color',CINK);
subtitle(tl, ['The magnitude of the topological jump controls both how reliably the change is ' ...
              'detected and how tightly it is localised in time.'],'FontSize',9.5,'Color',CGREY);
save_if(SAVE_FIGS, f8, fullfile(OUTPUT_DIR,'fig8_montecarlo_cusum_delay.png'), FIG_DPI);

%% -- Figure 9: H1 encirclement -------------------------------------------
% H1 here is generated by the adversarial embedding, not by the hierarchy:
% Team A alone has no loop, and Team B's ring only carries one because it is
% deployed around an opponent. Compare MacPherson & Schweinhart (2012) and
% Schindler & Barahona (2025).

RING_ONLY   = B_RING;
RING_TRAP   = [B_RING; A_TRAP];
RING_FREE   = [B_RING; A_FREE];
[~, g_only] = vr_persistence(RING_ONLY);
[~, g_trap] = vr_persistence(RING_TRAP);
[~, g_free] = vr_persistence(RING_FREE);

fprintf('\n=== H1 ENCIRCLEMENT ===\n');
report_h1('ring alone            ', g_only);
report_h1('ring + trapped cluster', g_trap);
report_h1('ring + escaped cluster', g_free);

f9 = figure('Position',[50 50 1420 900],'Color','w','Name','Fig9 H1 Encirclement');
tl = tiledlayout(f9, 2, 3, 'TileSpacing','compact','Padding','compact');
H1_SCENES  = {RING_ONLY, RING_TRAP, RING_FREE};
H1_DGMS    = {g_only, g_trap, g_free};
H1_APTS    = {zeros(0,2), A_TRAP, A_FREE};
H1_TITLES  = {'Ring closed, interior empty','Opponent cluster trapped inside','Opponent cluster escaped'};
H1_SUBS    = {'a genuine encirclement','the pocket is occupied','the encirclement is re-formed'};
DELTA_H1   = 30;   % between the birth (27.2) and death (40.0) of the ring loop

for s = 1:3
    ax = nexttile(tl, s);
    setup_pitch(ax,'football',CPITCH,CGRASS);
    draw_vr(ax, B_RING, CB, DELTA_H1, 34, 0.42, 0.92, 1.4);
    if ~isempty(H1_APTS{s})
        % Cross-team edges are drawn first so the agents stay legible on top.
        for i = 1:size(H1_APTS{s},1)
            for j = 1:size(B_RING,1)
                if norm(H1_APTS{s}(i,:) - B_RING(j,:)) <= DELTA_H1
                    plot(ax,[H1_APTS{s}(i,1) B_RING(j,1)],[H1_APTS{s}(i,2) B_RING(j,2)], ...
                         '-','Color',[CV 0.4],'LineWidth',1.0);
                end
            end
        end
        draw_vr(ax, H1_APTS{s}, CA, DELTA_H1, 44, 0.5, 1.0, 1.6);
    end
    if ~isempty(H1_DGMS{s})
        th = linspace(0,2*pi,200);
        plot(ax, RING_C(1)+RING_RHO*0.55*cos(th), RING_C(2)+RING_RHO*0.55*sin(th), ...
             ':','Color',[CGN 0.9],'LineWidth',2.0);
        text(ax, RING_C(1), RING_C(2),'H_1','FontSize',13,'FontWeight','bold','Color',CGN, ...
             'HorizontalAlignment','center');
    end
    pitch_title(ax, H1_TITLES{s}, sprintf('%s   (shown at \\delta = %d)', H1_SUBS{s}, DELTA_H1), CINK);
    panel_label(ax, char('A'+s-1));
end

for s = 1:3
    ax = nexttile(tl, s+3); hold(ax,'on');
    g = H1_DGMS{s};
    d0 = compute_h0(H1_SCENES{s});
    sd = sort(d0);
    for k = 1:numel(sd)
        barh(ax, k, sd(k), 0.6,'FaceColor',CFAINT,'EdgeColor','none','FaceAlpha',0.85);
    end
    ytop = numel(sd) + 2.6;
    yH1 = numel(sd) + 1.6;
    if isempty(g)
        text(ax, 40, yH1,'no H_1 bar','Color',[0.85 0.1 0.1],'FontSize',11, ...
             'FontWeight','bold','HorizontalAlignment','left','VerticalAlignment','middle');
        pers = 0;
    else
        [~, o] = max(g(:,2)-g(:,1)); g = g(o,:);
        pers = g(2) - g(1);
        % Drawn as a thick line rather than a bar: bar objects in one axis
        % share a baseline, so a non-zero BaseValue would shift the H0 bars.
        plot(ax, [g(1) g(2)], [yH1 yH1],'-','Color',CGN,'LineWidth',11);
        text(ax, g(2)+2, yH1, sprintf('H_1  [%.1f, %.1f]', g(1), g(2)), ...
             'Color',CGN,'FontSize',9,'FontWeight','bold','VerticalAlignment','middle');
    end
    xline(ax, DELTA_H1,'-','Color',CK,'LineWidth',1.8);
    xlim(ax,[0 62]); ylim(ax,[0.3 ytop]); yticks(ax,[]);
    box(ax,'off');
    xlabel(ax,'Scale \delta (pitch units)','FontSize',9.5);
    title(ax, sprintf('H_1 persistence = %.2f', pers),'FontSize',10,'FontWeight','bold', ...
          'Color', ternary(pers > 1, CGN, [0.85 0.1 0.1]));
    if s == 1
        subtitle(ax,'grey bars are H_0, green bar is the loop','FontSize',8.5, ...
                 'Color',CGREY,'FontAngle','italic');
    end
    panel_label(ax, char('D'+s-1));
end

title(tl,'H_1 From Adversarial Embedding: Encirclement Is a Loop, Not a Hierarchy', ...
      'FontSize',12.5,'FontWeight','bold','Color',CINK);
subtitle(tl, {'Neither team carries a loop from its own hierarchy.', ...
              ['The H_1 class exists only because Team B is deployed around Team A, and its ' ...
               'persistence collapses to zero the moment an opponent occupies the pocket.']}, ...
         'FontSize',9.5,'Color',CGREY);
save_if(SAVE_FIGS, f9, fullfile(OUTPUT_DIR,'fig9_h1_encirclement.png'), FIG_DPI);

fprintf('\nAll figures generated in %s\n', OUTPUT_DIR);

%% =========================================================================
%% LOCAL FUNCTIONS - GEOMETRY
%% =========================================================================

function pts = tri_cluster(cx, cy, r)
% TRI_CLUSTER  Three agents in an isosceles triangle about (cx, cy).
%   Within-cluster distances are 2r and r*sqrt(4.0625) ~ 2.0156r, so with
%   r = 2 the local H0 deaths are 4.00 and 4.03.
    if nargin < 3, r = 2.0; end
    pts = [cx,     cy - r*1.1;
           cx - r, cy + r*0.65;
           cx + r, cy + r*0.65];
end

function pts = ring_clusters(cx, cy, rho, k, r)
% RING_CLUSTERS  k triangular clusters equally spaced on a circle.
%   Used to build a genuine encirclement that carries an H1 class.
    th  = (0:k-1)' * 2*pi/k;
    pts = zeros(3*k, 2);
    for i = 1:k
        pts(3*i-2:3*i, :) = tri_cluster(cx + rho*cos(th(i)), cy + rho*sin(th(i)), r);
    end
end

%% =========================================================================
%% LOCAL FUNCTIONS - PERSISTENT HOMOLOGY
%% =========================================================================

function deaths = compute_h0(pts)
% COMPUTE_H0  H0 persistent homology via a minimum spanning tree (exact).
%   For the Vietoris-Rips filtration of a finite metric space the H0 death
%   times are exactly the MST edge weights (Carlsson & Memoli 2010). Prim's
%   algorithm on the dense distance matrix is used, which is exact and fast
%   enough to run inside a Monte Carlo loop.
    N = size(pts, 1);
    D = hypot(pts(:,1) - pts(:,1).', pts(:,2) - pts(:,2).');
    inT = false(N,1); inT(1) = true;
    best = D(1,:).'; best(1) = Inf;
    deaths = zeros(N-1, 1);
    for e = 1:N-1
        [wgt, j] = min(best);
        deaths(e) = wgt;
        inT(j) = true; best(j) = Inf;
        upd = ~inT & (D(j,:).' < best);
        best(upd) = D(j,upd).';
    end
    deaths = sort(deaths);
end

function [dgm0, dgm1] = vr_persistence(pts, thresh)
% VR_PERSISTENCE  Vietoris-Rips persistent homology in dimensions 0 and 1.
%   Standard column reduction of the GF(2) boundary matrix over the filtered
%   complex. Simplices are ordered by filtration value then by dimension.
%   Only intended for the small point clouds used here (tens of agents).
    N = size(pts,1);
    D = hypot(pts(:,1) - pts(:,1).', pts(:,2) - pts(:,2).');
    if nargin < 2 || isempty(thresh), thresh = max(D(:)) + 1; end

    nE = 0; E = zeros(N*(N-1)/2, 5);
    for i = 1:N
        for j = i+1:N
            if D(i,j) <= thresh
                nE = nE + 1; E(nE,:) = [D(i,j), 1, i, j, 0];
            end
        end
    end
    E = E(1:nE,:);

    nT = 0; Tr = zeros(N*(N-1)*(N-2)/6, 5);
    for i = 1:N
        for j = i+1:N
            for k = j+1:N
                f = max([D(i,j), D(i,k), D(j,k)]);
                if f <= thresh
                    nT = nT + 1; Tr(nT,:) = [f, 2, i, j, k];
                end
            end
        end
    end
    Tr = Tr(1:nT,:);

    S = [zeros(N,2), (1:N).', zeros(N,2); E; Tr];
    [~, ord] = sortrows(S, [1 2]);
    S = S(ord,:);
    M = size(S,1);

    i1 = zeros(N,1); i2 = zeros(N,N);
    for s = 1:M
        if     S(s,2) == 0, i1(S(s,3)) = s;
        elseif S(s,2) == 1, i2(S(s,3), S(s,4)) = s;
        end
    end

    cols = cell(M,1);
    for s = 1:M
        switch S(s,2)
            case 0
                cols{s} = zeros(0,1);
            case 1
                cols{s} = sort([i1(S(s,3)); i1(S(s,4))]);
            case 2
                a = S(s,3); b = S(s,4); c = S(s,5);
                cols{s} = sort([i2(a,b); i2(a,c); i2(b,c)]);
        end
    end

    lowinv = zeros(M,1); pairs = zeros(M,2); np = 0;
    for j = 1:M
        c = cols{j};
        while ~isempty(c)
            l = c(end);
            if lowinv(l) == 0, break; end
            c = setxor(c, cols{lowinv(l)});
        end
        cols{j} = c;
        if ~isempty(c)
            lowinv(c(end)) = j;
            np = np + 1; pairs(np,:) = [c(end), j];
        end
    end
    pairs = pairs(1:np,:);

    bd = S(pairs(:,1),1); dd = S(pairs(:,2),1); bdim = S(pairs(:,1),2);
    keep = dd > bd + 1e-9;
    dgm0 = [bd(bdim==0 & keep), dd(bdim==0 & keep)];
    dgm1 = [bd(bdim==1 & keep), dd(bdim==1 & keep)];
end

function [b0, b1] = betti_at(pts, delta)
% BETTI_AT  Betti numbers of the Vietoris-Rips complex at a single scale.
%   The full filtration is built, not a truncated one, so that a class born
%   below delta but dying above any truncation cannot be missed.
    [~, g1] = vr_persistence(pts);
    b0 = 1 + sum(compute_h0(pts) > delta);
    if isempty(g1)
        b1 = 0;
    else
        b1 = sum(g1(:,1) <= delta & g1(:,2) > delta);
    end
end

%% =========================================================================
%% LOCAL FUNCTIONS - STATISTICS ON DIAGRAMS
%% =========================================================================

function d = wasserstein_p(a, b, p)
% WASSERSTEIN_P  Exact p-Wasserstein distance between H0 persistence diagrams.
%   Diagrams are given as death-time vectors with all births at zero. The
%   ground metric is L-infinity on the plane, so the cost of matching two
%   points is |d_i - d_j| and the cost of sending a point to the diagonal is
%   d_i / 2. The optimal matching is found exactly by solving a linear
%   assignment problem on the augmented cost matrix, which also handles
%   diagrams of unequal cardinality (for example, a team reduced to ten
%   players). Sorted pairwise matching is only optimal when no point is
%   better served by the diagonal, which is not guaranteed.
    if nargin < 3, p = 1; end
    s1 = sort(a(:)); s2 = sort(b(:));
    n = numel(s1); m = numel(s2);
    if n == 0 && m == 0, d = 0; return; end
    C = inf(n+m, n+m);
    if n > 0 && m > 0, C(1:n, 1:m) = abs(s1 - s2.').^p; end
    for i = 1:n, C(i, m+i) = (s1(i)/2)^p; end
    for j = 1:m, C(n+j, j) = (s2(j)/2)^p; end
    C(n+1:n+m, m+1:m+n) = 0;
    Mt = matchpairs(C, 1e12);
    d  = sum(C(sub2ind(size(C), Mt(:,1), Mt(:,2))))^(1/p);
end

function d = naive_w1(a, b)
% NAIVE_W1  Sorted pairwise matching, retained only to quantify the error
%   it introduces relative to WASSERSTEIN_P.
    s1 = sort(a(:)); s2 = sort(b(:)); n = min(numel(s1), numel(s2));
    d = sum(abs(s1(1:n) - s2(1:n)));
    if numel(s1) > n, d = d + sum(s1(n+1:end)/2);
    elseif numel(s2) > n, d = d + sum(s2(n+1:end)/2); end
end

function m = frechet_mean(diags)
% FRECHET_MEAN  Exact W2 barycentre of H0 persistence diagrams.
%   For diagrams with all births at zero, equal cardinality, and an optimal
%   matching that never uses the diagonal, the minimiser of the Frechet
%   functional sum_i W2(D_i, mu)^2 is the componentwise mean of the sorted
%   death vectors. Turner et al. (2014) define Frechet means of persistence
%   diagrams with respect to W2; the componentwise mean is NOT the minimiser
%   under W1, so dispersion must be measured in W2 to stay consistent.
    if isempty(diags), m = []; return; end
    lens = cellfun(@numel, diags);
    if any(lens ~= lens(1))
        error('frechet_mean:cardinality', ...
              ['Diagrams have unequal cardinality (%d to %d). The componentwise ' ...
               'mean is not the W2 barycentre in that case.'], min(lens), max(lens));
    end
    stacked = zeros(numel(diags), lens(1));
    for i = 1:numel(diags)
        tmp = sort(diags{i}(:));
        stacked(i,:) = tmp.';
    end
    m = sort(mean(stacked, 1)).';
end

function ac = autocorr_manual(x, nlags)
% AUTOCORR_MANUAL  Sample autocorrelation function (no toolbox required).
    x  = (x(:) - mean(x)) / (std(x) + 1e-12);
    n  = numel(x);
    ac = zeros(nlags+1, 1); ac(1) = 1;
    for lag = 1:nlags
        ac(lag+1) = sum(x(1:end-lag) .* x(lag+1:end)) / n;
    end
end

function xc = crosscorr_manual(x, y, nlags)
% CROSSCORR_MANUAL  Cross-correlation of y against x at non-negative lags,
%   so a peak at lag k means y responds to x after k frames.
    x = (x(:) - mean(x)) / (std(x) + 1e-12);
    y = (y(:) - mean(y)) / (std(y) + 1e-12);
    n = numel(x);
    xc = zeros(nlags+1, 1);
    for lag = 0:nlags
        xc(lag+1) = sum(x(1:end-lag) .* y(lag+1:end)) / n;
    end
end

%% =========================================================================
%% LOCAL FUNCTIONS - DYNAMICS
%% =========================================================================

function [A_pts, B_pts] = get_config(t, noise, A0, A1, B0, B1, t_star, t_end, rs)
% GET_CONFIG  Adversarial dynamics: agent positions at frame t.
%   Pre (t < t_star) -> smoothstep transition -> post (t >= t_end).
%   Noise is Gaussian with standard deviation `noise`, drawn from the caller's
%   RandStream so the global random state is left untouched.
    if t < t_star
        A_pts = A0; B_pts = B0;
    elseif t < t_end
        tt = (t - t_star) / (t_end - t_star);
        e  = tt^2 * (3 - 2*tt);          % smoothstep, C1 at both ends
        A_pts = (1-e)*A0 + e*A1;
        B_pts = (1-e)*B0 + e*B1;
    else
        A_pts = A1; B_pts = B1;
    end
    A_pts = A_pts + randn(rs, size(A_pts))*noise;
    B_pts = B_pts + randn(rs, size(B_pts))*noise;
end

function w = w1_series(A0, A1, alpha, noise, seed, T_MAX, t_star, t_end)
% W1_SERIES  Consecutive-frame W1 signal for Team A, with the transition
%   scaled by alpha. alpha = 0 gives a pure in-control realisation, used to
%   calibrate the CUSUM and to measure the false-alarm rate.
    rs  = RandStream('twister','Seed',seed);
    tgt = A0 + alpha*(A1 - A0);
    d   = cell(T_MAX+1,1);
    for t = 0:T_MAX
        if t < t_star
            A = A0;
        elseif t < t_end
            tt = (t - t_star)/(t_end - t_star); e = tt^2*(3-2*tt);
            A  = (1-e)*A0 + e*tgt;
        else
            A = tgt;
        end
        d{t+1} = compute_h0(A + randn(rs, size(A))*noise);
    end
    w = zeros(T_MAX+1,1);
    for t = 2:T_MAX+1
        w(t) = wasserstein_p(d{t}, d{t-1}, 1);
    end
end

function [sA, sB] = coupled_series(A0, B0, T, noise, drift, phi, rho, seed, coupled)
% COUPLED_SERIES  Two dependence structures with identical marginals.
%   In both models each team's cluster centres are displaced by a zero-mean
%   Gaussian field of marginal standard deviation `drift`, and every agent
%   carries i.i.d. N(0, noise^2) jitter on top. The one-frame marginal
%   distribution of every agent position is therefore exactly the same in the
%   two models, so any difference in the topological signal is attributable to
%   dependence alone rather than to a change in scale or noise level.
%
%   coupled = true   Each team's displacement is a stationary AR(1) process
%                    with autoregressive parameter `phi`, scaled to keep the
%                    marginal s.d. at `drift`. Team B's displacement is
%                        U_B(t) = rho*U_A(t-1) + sqrt(1-rho^2)*V(t)
%                    with V an independent AR(1) of the same marginal. Since
%                    U_A(t-1) and V(t) are independent, U_B still has marginal
%                    variance drift^2 exactly, while Team B now tracks Team A
%                    with a one-frame lag: a tug-of-war.
%   coupled = false  Fresh independent displacements every frame, with no
%                    memory and no cross-team term: a sequence of coin flips.
%
%   The returned statistic is per-frame, s(t) = W1(D_t, D_ref) against the
%   undisturbed configuration. A consecutive-frame statistic such as
%   W1(D_t, D_{t-1}) must NOT be used here: successive values share a diagram,
%   which induces lag-1 correlation even when the frames are independent, and
%   would mask the effect being measured.
    rs   = RandStream('twister','Seed',seed);
    nc   = size(A0,1)/3;
    Ac0  = cluster_centres(A0);
    Bc0  = cluster_centres(B0);
    refA = compute_h0(A0);
    refB = compute_h0(B0);

    UA = randn(rs, nc, 2)*drift;      % start in the stationary distribution
    V  = randn(rs, nc, 2)*drift;
    sA = zeros(T+1,1); sB = zeros(T+1,1);
    for t = 0:T
        if coupled
            UA_prev = UA;
            UA = phi*UA + sqrt(1-phi^2)*drift*randn(rs, nc, 2);
            V  = phi*V  + sqrt(1-phi^2)*drift*randn(rs, nc, 2);
            UB = rho*UA_prev + sqrt(1-rho^2)*V;
        else
            UA = drift*randn(rs, nc, 2);
            UB = drift*randn(rs, nc, 2);
        end
        A = displace_clusters(A0, Ac0, Ac0 + UA) + randn(rs, size(A0))*noise;
        B = displace_clusters(B0, Bc0, Bc0 + UB) + randn(rs, size(B0))*noise;
        sA(t+1) = wasserstein_p(compute_h0(A), refA, 1);
        sB(t+1) = wasserstein_p(compute_h0(B), refB, 1);
    end
end

function C = cluster_centres(pts)
% CLUSTER_CENTRES  Centroid of each consecutive triple of agents.
    nc = size(pts,1)/3;
    C  = squeeze(mean(reshape(pts.', 2, 3, nc), 2)).';
end

function pts = displace_clusters(template, base_centres, new_centres)
% DISPLACE_CLUSTERS  Move whole clusters, preserving their internal geometry.
    pts = template;
    for i = 1:size(base_centres,1)
        idx = 3*i-2 : 3*i;
        pts(idx,:) = template(idx,:) + (new_centres(i,:) - base_centres(i,:));
    end
end

%% =========================================================================
%% LOCAL FUNCTIONS - CHANGE-POINT DETECTION
%% =========================================================================

function C = cusum_path(w, kappa, mon0)
% CUSUM_PATH  One-sided CUSUM restricted to the monitoring window.
    T = numel(w) - 1;
    C = zeros(T - mon0 + 1, 1);
    Cv = 0; n = 0;
    for t = mon0:T
        Cv = max(0, Cv + w(t+1) - kappa);
        n = n + 1; C(n) = Cv;
    end
end

function [t_hat, C_full] = run_cusum(w, kappa, h, mon0)
% RUN_CUSUM  First frame at which the CUSUM crosses the decision interval.
%   Returns NaN if no alarm is raised within the series.
    T = numel(w) - 1;
    C_full = nan(T+1, 1);
    Cv = 0; t_hat = NaN;
    for t = mon0:T
        Cv = max(0, Cv + w(t+1) - kappa);
        C_full(t+1) = Cv;
        if isnan(t_hat) && Cv >= h, t_hat = t; end
    end
end

%% =========================================================================
%% LOCAL FUNCTIONS - PLOTTING
%% =========================================================================

function setup_pitch(ax, kind, bg_col, border_col)
% SETUP_PITCH  Draw the domain background for a spatial panel.
%   The vertical limits leave headroom above the domain so that PITCH_TITLE
%   can place the panel heading inside the axes. Titles set with TITLE on an
%   `axis off, axis equal` panel are positioned outside the axes box and are
%   not accounted for by TILEDLAYOUT, which makes them collide with the
%   layout title.
    hold(ax, 'on'); cla(ax);
    axis(ax, 'equal'); axis(ax, 'off');
    set(ax, 'XLim', [-4 124], 'YLim', [-7 105], 'Color', bg_col);
    th = linspace(0, 2*pi, 200);
    switch kind
        case 'football'
            rectangle(ax,'Position',[0 0 120 80],'EdgeColor',border_col,'LineWidth',1.8, ...
                      'FaceColor',bg_col);
            plot(ax,[60 60],[0 80],'Color',[border_col 0.7],'LineWidth',0.9);
            plot(ax, 60+9*cos(th), 40+9*sin(th),'Color',[border_col 0.7],'LineWidth',0.9);
        case 'tissue'
            fill(ax, 60+43*cos(th), 40+43*sin(th), bg_col,'EdgeColor',border_col,'LineWidth',2.0);
            fill(ax, 60+8*cos(th),  40+8*sin(th), [255 228 230]/255,'EdgeColor','none','FaceAlpha',0.5);
        case 'ecology'
            rectangle(ax,'Position',[0 0 120 80],'EdgeColor',border_col,'LineWidth',1.5, ...
                      'FaceColor',bg_col);
            x_arr = linspace(0,120,200);
            for y0 = [25, 55]
                plot(ax, x_arr, y0+3*sin(x_arr*0.08),'Color',[[212 160 23]/255 0.3],'LineWidth',0.6);
            end
        case 'corridor'
            rectangle(ax,'Position',[0 0 120 80],'EdgeColor',border_col,'LineWidth',1.8, ...
                      'FaceColor',bg_col);
            plot(ax,[0 120],[40 40],'--','Color',[border_col 0.55],'LineWidth',1.2);
    end
end

function draw_vr(ax, pts, col, delta, s, alpha_e, alpha_n, lw)
% DRAW_VR  Vietoris-Rips 1-skeleton plus the agent scatter.
    if nargin < 5 || isempty(s),       s = 32;       end
    if nargin < 6 || isempty(alpha_e), alpha_e = 0.35; end
    if nargin < 7 || isempty(alpha_n), alpha_n = 0.92; end
    if nargin < 8 || isempty(lw),      lw = 1.1;     end
    hold(ax,'on');
    N = size(pts,1);
    if ~isempty(delta) && delta > 0
        for i = 1:N
            for j = i+1:N
                if norm(pts(i,:) - pts(j,:)) <= delta
                    plot(ax, [pts(i,1) pts(j,1)], [pts(i,2) pts(j,2)], ...
                         'Color',[col alpha_e],'LineWidth',lw);
                end
            end
        end
    end
    scatter(ax, pts(:,1), pts(:,2), s, col,'filled', ...
            'MarkerEdgeColor','w','LineWidth',1.1,'MarkerFaceAlpha',alpha_n);
end

function outline_components(ax, pts, delta, col)
% OUTLINE_COMPONENTS  Dashed convex hull around each connected component of
%   the Vietoris-Rips graph at scale delta, so the reader can count beta_0.
    N = size(pts,1);
    D = hypot(pts(:,1)-pts(:,1).', pts(:,2)-pts(:,2).');
    Adj = D <= delta;
    lbl = zeros(N,1); nl = 0;
    for i = 1:N
        if lbl(i) == 0
            nl = nl + 1; stack = i; lbl(i) = nl;
            while ~isempty(stack)
                v = stack(end); stack(end) = [];
                nb = find(Adj(v,:) & (lbl.' == 0));
                lbl(nb) = nl; stack = [stack, nb]; %#ok<AGROW>
            end
        end
    end
    for c = 1:nl
        P = pts(lbl == c, :);
        cen = mean(P, 1);
        if size(P,1) < 3 || range(P(:,1)) < 1e-6 || range(P(:,2)) < 1e-6
            draw_ellipse(ax, cen(1), cen(2), 5, 5, col, 1.1);
        else
            H = P(convhull(P(:,1), P(:,2)), :);
            cen = mean(H(1:end-1,:), 1);
            % Scale the hull outwards, with a floor so that a tight cluster
            % still gets an outline large enough to read.
            V   = H - cen;
            pad = 4.5 ./ max(vecnorm(V, 2, 2), 1e-6);
            H   = cen + V .* (1.15 + pad);
            plot(ax, H(:,1), H(:,2), '--','Color',[col 0.65],'LineWidth',1.1);
        end
    end
end

function draw_contest_arrow(ax, desc, nA, nB, col, greycol)
% DRAW_CONTEST_ARROW  Centre panel of Figure 2, drawn in the panel's own data
%   coordinates so it stays aligned when the layout changes.
    hold(ax,'on'); axis(ax,'off');
    xlim(ax,[0 1]); ylim(ax,[0 1]);
    plot(ax,[0.16 0.84],[0.72 0.72],'-','Color',col,'LineWidth',2.4);
    plot(ax, 0.16, 0.72,'<','Color',col,'MarkerFaceColor',col,'MarkerSize',8);
    plot(ax, 0.84, 0.72,'>','Color',col,'MarkerFaceColor',col,'MarkerSize',8);
    text(ax, 0.5, 0.55,'contests','HorizontalAlignment','center','FontSize',11, ...
         'FontWeight','bold','Color',col);
    text(ax, 0.5, 0.42,'at the same scale','HorizontalAlignment','center','FontSize',9, ...
         'Color',greycol,'FontAngle','italic');
    text(ax, 0.5, 0.26, desc,'HorizontalAlignment','center','FontSize',8.5, ...
         'Color',greycol,'FontAngle','italic');
    text(ax, 0.5, 0.10, sprintf('\\beta_0:  A = %d,  B = %d', nA, nB), ...
         'HorizontalAlignment','center','FontSize',9,'FontWeight','bold','Color',greycol);
end

function draw_verdict(ax, headline, line1, line2, col, bgcol)
% DRAW_VERDICT  Centre panel of Figure 6, in the panel's own coordinates.
    hold(ax,'on'); axis(ax,'off');
    xlim(ax,[0 1]); ylim(ax,[0 1]);
    text(ax, 0.5, 0.72, headline,'HorizontalAlignment','center','FontSize',12, ...
         'FontWeight','bold','Color',col,'BackgroundColor',bgcol,'EdgeColor',col,'Margin',6);
    plot(ax,[0.08 0.92],[0.52 0.52],'-','Color',col,'LineWidth',2.4);
    plot(ax, 0.08, 0.52,'<','Color',col,'MarkerFaceColor',col,'MarkerSize',8);
    plot(ax, 0.92, 0.52,'>','Color',col,'MarkerFaceColor',col,'MarkerSize',8);
    text(ax, 0.5, 0.36, line1,'HorizontalAlignment','center','FontSize',10, ...
         'FontWeight','bold','Color',col);
    text(ax, 0.5, 0.24, line2,'HorizontalAlignment','center','FontSize',9,'Color',col);
end

function draw_barcode(ax, deaths, col, delta_line, max_d, ttl)
% DRAW_BARCODE  Horizontal H0 barcode; one bar per connected component.
    if nargin < 4, delta_line = []; end
    if nargin < 5 || isempty(max_d), max_d = 92; end
    if nargin < 6, ttl = ''; end
    hold(ax,'on'); cla(ax);
    s = sort(deaths(:)); n = numel(s);
    for k = 1:n
        fc = col;
        if ~isempty(delta_line) && s(k) > delta_line, fc = [229 231 235]/255; end
        barh(ax, k, s(k), 0.62,'FaceColor',fc,'EdgeColor','none','FaceAlpha',0.78);
    end
    if ~isempty(delta_line)
        xline(ax, delta_line,'Color',[217 119 6]/255,'LineWidth',2.0);
    end
    % Leave headroom so that the most persistent bar is not clipped by the
    % axis and the staggered level labels have somewhere to sit.
    xlim(ax,[0 max_d]); ylim(ax,[0.3 n+2.3]); yticks(ax,[]);
    ax.YAxis.Visible = 'off'; box(ax,'off');
    if ~isempty(ttl)
        title(ax, ttl,'FontSize',9,'FontWeight','bold','Color',col);
    end
end

function draw_two_barcodes(ax, dA, dB, colA, colB, delta_line, max_d, shade)
% DRAW_TWO_BARCODES  Both teams on one axis, attacker above the line and
%   defender below.
%   With shade = true, bars are coloured when they cross the displayed scale,
%   that is when the component is still separate at that delta, and greyed
%   once they have merged. The number of coloured bars is then beta_0 - 1,
%   which is directly readable off the panel.
%   With shade = false the whole barcode is shown in full colour, for panels
%   whose message is the shape of the hierarchy rather than one scale.
    if nargin < 8 || isempty(shade), shade = true; end
    hold(ax,'on'); cla(ax);
    GREY = [214 219 226]/255;
    sA = sort(dA(:)); sB = sort(dB(:));
    for k = 1:numel(sA)
        fc = colA; if shade && ~isempty(delta_line) && sA(k) <= delta_line, fc = GREY; end
        barh(ax, k, sA(k), 0.62,'FaceColor',fc,'EdgeColor','none','FaceAlpha',0.82);
    end
    for k = 1:numel(sB)
        fc = colB; if shade && ~isempty(delta_line) && sB(k) <= delta_line, fc = GREY; end
        barh(ax, -k, sB(k), 0.62,'FaceColor',fc,'EdgeColor','none','FaceAlpha',0.45);
    end
    plot(ax,[0 max_d],[0 0],'-','Color',[148 163 184]/255,'LineWidth',0.8);
    if ~isempty(delta_line)
        xline(ax, delta_line,'Color',[217 119 6]/255,'LineWidth',2.0);
        % Placed below the axis so it cannot collide with the level brackets.
        text(ax, delta_line, -numel(sB)-0.7, sprintf(' \\delta = %g', delta_line), ...
             'Color',[217 119 6]/255,'FontSize',8,'FontWeight','bold','VerticalAlignment','middle');
    end
    xlim(ax,[0 max_d]); ylim(ax,[-numel(sB)-1.6, numel(sA)+2.5]); yticks(ax,[]);
    ax.YAxis.Visible = 'off'; box(ax,'off');
end

function annotate_levels(ax, deaths)
% ANNOTATE_LEVELS  Bracket the levels of the hierarchy, detected from the
%   gaps in the death vector rather than assumed. Labels are staggered over
%   two rows and kept clear of the panel letter so they do not collide when
%   two levels sit close together on the scale axis.
    s = sort(deaths(:)); n = numel(s);
    [~, ord] = sort(diff(s),'descend');
    cuts  = sort(ord(1:min(2,numel(ord))));
    bnds  = [0; cuts(:); n];
    names = {'local','tactical','global'};
    yl = ylim(ax); xl = xlim(ax);
    xmin = xl(1) + 0.16*diff(xl);       % clear of the panel letter
    for g = 1:numel(bnds)-1
        idx = bnds(g)+1 : bnds(g+1);
        if isempty(idx), continue; end
        xc = max(xmin, mean([s(idx(1)), s(idx(end))]));
        yc = yl(2) - 0.25 - 0.85*mod(g-1, 2);
        text(ax, xc, yc, sprintf('%s \\times %d', names{min(g,3)}, numel(idx)), ...
             'FontSize',7.5,'Color',[107 114 128]/255,'FontAngle','italic', ...
             'HorizontalAlignment','center','VerticalAlignment','top');
    end
end

function draw_ellipse(ax, cx, cy, rx, ry, col, lw)
% DRAW_ELLIPSE  Dashed ellipse used to highlight a formation.
    th = linspace(0, 2*pi, 200);
    plot(ax, cx+rx*cos(th), cy+ry*sin(th),'--','Color',[col 0.7],'LineWidth',lw);
end

function shade_regimes(ax, t_star, t_settle, t_max, ymax, col_pre, col_post)
% SHADE_REGIMES  Background bands for the pre-transition, transition and
%   post-transition regimes of a time-series panel.
    patch(ax, [0 t_star t_star 0], [0 0 ymax ymax], col_pre, ...
          'FaceAlpha',0.05,'EdgeColor','none','HandleVisibility','off');
    patch(ax, [t_star t_settle t_settle t_star], [0 0 ymax ymax], [0.85 0.1 0.1], ...
          'FaceAlpha',0.06,'EdgeColor','none','HandleVisibility','off');
    patch(ax, [t_settle t_max t_max t_settle], [0 0 ymax ymax], col_post, ...
          'FaceAlpha',0.05,'EdgeColor','none','HandleVisibility','off');
end

function ylabel_pitch(ax, txt, col)
% YLABEL_PITCH  Row label for an axis that has its decorations switched off.
    text(ax, -2, 40, txt,'Rotation',90,'HorizontalAlignment','center', ...
         'VerticalAlignment','bottom','FontSize',10,'FontWeight','bold','Color',col);
end

function pitch_title(ax, main, sub, col_main)
% PITCH_TITLE  Panel heading drawn inside a decoration-free spatial panel,
%   in the headroom reserved by SETUP_PITCH.
    if nargin < 4 || isempty(col_main), col_main = [15 23 42]/255; end
    text(ax, 60, 100, main,'HorizontalAlignment','center','VerticalAlignment','top', ...
         'FontSize',10,'FontWeight','bold','Color',col_main);
    if ~isempty(sub)
        text(ax, 60, 90, sub,'HorizontalAlignment','center','VerticalAlignment','top', ...
             'FontSize',8.5,'FontAngle','italic','Color',[107 114 128]/255);
    end
end

function panel_label(ax, ch)
% PANEL_LABEL  Bold panel letter in the top-left corner.
    text(ax, 0.015, 0.985, ch,'Units','normalized','FontSize',13,'FontWeight','bold', ...
         'Color',[17 24 39]/255,'VerticalAlignment','top','HorizontalAlignment','left');
end

function report_h1(name, g)
% REPORT_H1  Console summary of the most persistent H1 class.
    if isempty(g)
        fprintf('  %s : no H1 class\n', name);
    else
        [~, o] = max(g(:,2) - g(:,1));
        fprintf('  %s : [%.2f, %.2f], persistence %.2f\n', name, g(o,1), g(o,2), g(o,2)-g(o,1));
    end
end

function dl = tactical_scale(deaths)
% TACTICAL_SCALE  A display scale that reveals the formation level: midway
%   between the largest death below the global feature and the global feature.
    s = sort(deaths(:));
    dl = round(mean(s(end-1:end)));
end

function out = ternary(cond, a, b)
    if cond, out = a; else, out = b; end
end

function save_if(flag, fig, fpath, dpi)
% SAVE_IF  Export the figure as a high-resolution PNG.
    if ~flag, return; end
    exportgraphics(fig, fpath,'Resolution',dpi,'BackgroundColor','white');
    fprintf('Saved: %s\n', fpath);
end
