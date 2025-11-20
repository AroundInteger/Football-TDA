classdef ZeroSumSymmetryAnalysis
    % ZEROSUMSYMMETRYANALYSIS - Implements zero-sum competition and symmetry breaking analysis
    % 
    % This class implements the analysis of zero-sum competition and symmetry breaking
    % in football dynamics, building on the state space reconstruction from Step 2.
    %
    % Key Features:
    % - Zero-sum competition quantification through cross-correlation analysis
    % - Symmetry breaking detection in field positioning and tactical patterns
    % - Overload identification and numerical advantage analysis
    % - Competitive balance assessment and tactical advantage quantification
    %
    % Based on research by:
    % - Fernandez & Bornn (2018) - Spatial dynamics in football
    % - Bialkowski et al. (2014) - Large-scale analysis of soccer matches
    % - Gudmundsson & Horton (2017) - Spatio-temporal analysis of team sports
    
    properties
        % Input data
        coupledMetrics      % Table of coupled collective variables from Step 1
        stateSpace         % StateSpaceReconstruction object from Step 2
        timestamps         % Vector of timestamps
        
        % Zero-sum analysis
        crossCorrelations  % Cross-correlation matrix between opposing team metrics
        zeroSumMetrics     % Quantified zero-sum competition metrics
        competitiveBalance % Competitive balance assessment
        
        % Symmetry breaking analysis
        fieldSymmetry      % Field symmetry analysis
        overloadMetrics    % Numerical overload identification
        tacticalAdvantage  % Tactical advantage quantification
        
        % Analysis results
        analysisComplete   % Boolean flag
        computationTime    % Time taken for analysis
    end
    
    methods
        function obj = ZeroSumSymmetryAnalysis(coupledMetrics, stateSpace, timestamps)
            % Constructor for ZeroSumSymmetryAnalysis
            %
            % Inputs:
            %   coupledMetrics - Table of coupled collective variables from Step 1
            %   stateSpace    - StateSpaceReconstruction object from Step 2
            %   timestamps    - Vector of timestamps
            
            % Store input data
            obj.coupledMetrics = coupledMetrics;
            obj.stateSpace = stateSpace;
            obj.timestamps = timestamps;
            
            % Initialize computed data
            obj.analysisComplete = false;
            obj.computationTime = 0;
            
            fprintf('ZeroSumSymmetryAnalysis initialized\n');
            fprintf('  Time points: %d\n', height(coupledMetrics));
            fprintf('  State space attractors: %d\n', stateSpace.attractorStates.nClusters);
        end
        
        function obj = analyzeZeroSumCompetition(obj)
            % Analyze zero-sum competition between opposing teams
            %
            % This method implements the core zero-sum competition analysis
            % as described in the GPS-TDA framework
            
            fprintf('Analyzing zero-sum competition...\n');
            tic;
            
            % Step 1: Compute cross-correlations between opposing team metrics
            obj = obj.computeCrossCorrelations();
            
            % Step 2: Quantify zero-sum competition
            obj = obj.quantifyZeroSumCompetition();
            
            % Step 3: Assess competitive balance
            obj = obj.assessCompetitiveBalance();
            
            % Mark analysis as complete
            obj.analysisComplete = true;
            obj.computationTime = toc;
            
            fprintf('Zero-sum competition analysis complete (%.2f seconds)\n', obj.computationTime);
        end
        
        function obj = analyzeSymmetryBreaking(obj)
            % Analyze symmetry breaking in field positioning and tactical patterns
            
            fprintf('Analyzing symmetry breaking...\n');
            
            % Step 1: Analyze field symmetry
            obj = obj.analyzeFieldSymmetry();
            
            % Step 2: Identify numerical overloads
            obj = obj.identifyNumericalOverloads();
            
            % Step 3: Quantify tactical advantages
            obj = obj.quantifyTacticalAdvantages();
            
            fprintf('Symmetry breaking analysis complete\n');
        end
        
        function obj = computeCrossCorrelations(obj)
            % Compute cross-correlations between opposing team metrics
            
            fprintf('  Computing cross-correlations...\n');
            
            % Define opposing team metric pairs
            homeMetrics = {'HomeTeamArea', 'HomeMeanNOD', 'HomeStdNOD'};
            awayMetrics = {'AwayTeamArea', 'AwayMeanNOD', 'AwayStdNOD'};
            
            nMetrics = length(homeMetrics);
            obj.crossCorrelations = struct();
            
            % Compute cross-correlations for each metric pair
            for i = 1:nMetrics
                homeMetric = homeMetrics{i};
                awayMetric = awayMetrics{i};
                
                if ismember(homeMetric, obj.coupledMetrics.Properties.VariableNames) && ...
                   ismember(awayMetric, obj.coupledMetrics.Properties.VariableNames)
                    
                    homeValues = obj.coupledMetrics.(homeMetric);
                    awayValues = obj.coupledMetrics.(awayMetric);
                    
                    % Remove NaN values
                    validIndices = ~isnan(homeValues) & ~isnan(awayValues);
                    
                    if sum(validIndices) > 10 % Need sufficient data points
                        % Compute correlation
                        correlation = corrcoef(homeValues(validIndices), awayValues(validIndices));
                        obj.crossCorrelations.(homeMetric) = correlation(1, 2);
                        
                        % Compute cross-correlation with time lags
                        [crossCorr, lags] = xcorr(homeValues(validIndices), awayValues(validIndices), 10, 'normalized');
                        obj.crossCorrelations.([homeMetric '_lags']) = lags;
                        obj.crossCorrelations.([homeMetric '_crosscorr']) = crossCorr;
                    else
                        obj.crossCorrelations.(homeMetric) = NaN;
                    end
                end
            end
            
            fprintf('    Cross-correlations computed for %d metric pairs\n', nMetrics);
        end
        
        function obj = quantifyZeroSumCompetition(obj)
            % Quantify zero-sum competition between teams
            
            fprintf('  Quantifying zero-sum competition...\n');
            
            % Initialize zero-sum metrics structure
            obj.zeroSumMetrics = struct();
            
            % 1. Inter-team distance vs team areas (inverse relationship expected)
            interDist = obj.coupledMetrics.InterTeamDistance;
            homeArea = obj.coupledMetrics.HomeTeamArea;
            awayArea = obj.coupledMetrics.AwayTeamArea;
            
            validIndices = ~isnan(interDist) & ~isnan(homeArea) & ~isnan(awayArea);
            
            if sum(validIndices) > 10
                % Correlation between inter-team distance and team areas
                obj.zeroSumMetrics.interDist_homeArea_corr = corrcoef(interDist(validIndices), homeArea(validIndices));
                obj.zeroSumMetrics.interDist_awayArea_corr = corrcoef(interDist(validIndices), awayArea(validIndices));
                
                % Zero-sum index: how much team areas are inversely related
                teamAreaDiff = homeArea - awayArea;
                obj.zeroSumMetrics.areaZeroSumIndex = corrcoef(interDist(validIndices), teamAreaDiff(validIndices));
            end
            
            % 2. NOD zero-sum analysis
            homeNOD = obj.coupledMetrics.HomeMeanNOD;
            awayNOD = obj.coupledMetrics.AwayMeanNOD;
            
            validNODIndices = ~isnan(homeNOD) & ~isnan(awayNOD);
            
            if sum(validNODIndices) > 10
                % NOD zero-sum index: inverse relationship between home and away NOD
                obj.zeroSumMetrics.nodZeroSumIndex = corrcoef(homeNOD(validNODIndices), awayNOD(validNODIndices));
                
                % NOD balance: how balanced the marking is
                nodBalance = abs(homeNOD - awayNOD) ./ (homeNOD + awayNOD + eps);
                obj.zeroSumMetrics.nodBalance = nanmean(nodBalance(validNODIndices));
            end
            
            % 3. Team area ratio zero-sum analysis
            areaRatio = obj.coupledMetrics.TeamAreaRatio;
            validRatioIndices = ~isnan(areaRatio);
            
            if sum(validRatioIndices) > 10
                % Area ratio balance: how often teams have similar areas
                areaBalance = abs(areaRatio - 1);
                obj.zeroSumMetrics.areaBalance = nanmean(areaBalance(validRatioIndices));
                
                % Area dominance: how often one team has significantly larger area
                areaDominance = sum(areaRatio > 1.2 | areaRatio < 0.8) / sum(validRatioIndices);
                obj.zeroSumMetrics.areaDominance = areaDominance;
            end
            
            fprintf('    Zero-sum competition quantified\n');
        end
        
        function obj = assessCompetitiveBalance(obj)
            % Assess competitive balance between teams
            
            fprintf('  Assessing competitive balance...\n');
            
            % Initialize competitive balance structure
            obj.competitiveBalance = struct();
            
            % 1. Overall competitive balance index
            % Based on variance in team area ratios and NOD differences
            areaRatio = obj.coupledMetrics.TeamAreaRatio;
            homeNOD = obj.coupledMetrics.HomeMeanNOD;
            awayNOD = obj.coupledMetrics.AwayMeanNOD;
            
            validIndices = ~isnan(areaRatio) & ~isnan(homeNOD) & ~isnan(awayNOD);
            
            if sum(validIndices) > 10
                % Competitive balance based on area ratio stability
                areaBalance = 1 - nanstd(areaRatio(validIndices));
                obj.competitiveBalance.areaBalance = areaBalance;
                
                % Competitive balance based on NOD balance
                nodDiff = abs(homeNOD - awayNOD);
                nodBalance = 1 - nanstd(nodDiff(validIndices)) / nanmean(nodDiff(validIndices));
                obj.competitiveBalance.nodBalance = nodBalance;
                
                % Overall competitive balance
                obj.competitiveBalance.overallBalance = (areaBalance + nodBalance) / 2;
            end
            
            % 2. Tactical phase balance
            if isfield(obj.stateSpace, 'attractorLabels') && ~isempty(obj.stateSpace.attractorLabels)
                % Analyze balance in attractor state transitions
                attractorLabels = obj.stateSpace.attractorLabels;
                nClusters = obj.stateSpace.attractorStates.nClusters;
                
                % Compute attractor balance (how evenly distributed the attractors are)
                attractorCounts = zeros(nClusters, 1);
                for i = 1:nClusters
                    attractorCounts(i) = sum(attractorLabels == i);
                end
                
                % Balance index: 1 - coefficient of variation
                if sum(attractorCounts) > 0
                    attractorBalance = 1 - std(attractorCounts) / mean(attractorCounts);
                    obj.competitiveBalance.attractorBalance = attractorBalance;
                end
            end
            
            fprintf('    Competitive balance assessed\n');
        end
        
        function obj = analyzeFieldSymmetry(obj)
            % Analyze field symmetry in team positioning
            
            fprintf('  Analyzing field symmetry...\n');
            
            % Initialize field symmetry structure
            obj.fieldSymmetry = struct();
            
            % 1. Lateral symmetry analysis
            % This would require actual player positions, but we can infer from team areas
            homeArea = obj.coupledMetrics.HomeTeamArea;
            awayArea = obj.coupledMetrics.AwayTeamArea;
            
            validIndices = ~isnan(homeArea) & ~isnan(awayArea);
            
            if sum(validIndices) > 10
                % Lateral symmetry: how similar are team areas (proxy for field coverage)
                areaSimilarity = 1 - abs(homeArea - awayArea) ./ (homeArea + awayArea + eps);
                obj.fieldSymmetry.lateralSymmetry = nanmean(areaSimilarity(validIndices));
                
                % Field dominance: how often one team covers more field
                fieldDominance = sum(abs(homeArea - awayArea) > nanstd(homeArea + awayArea)) / sum(validIndices);
                obj.fieldSymmetry.fieldDominance = fieldDominance;
            end
            
            % 2. Temporal symmetry analysis
            % Analyze how symmetric the dynamics are over time
            interDist = obj.coupledMetrics.InterTeamDistance;
            validTimeIndices = ~isnan(interDist);
            
            if sum(validTimeIndices) > 10
                % Temporal symmetry: how stable is the inter-team distance
                temporalSymmetry = 1 - nanstd(interDist(validTimeIndices)) / nanmean(interDist(validTimeIndices));
                obj.fieldSymmetry.temporalSymmetry = temporalSymmetry;
            end
            
            fprintf('    Field symmetry analyzed\n');
        end
        
        function obj = identifyNumericalOverloads(obj)
            % Identify numerical overloads and tactical advantages
            
            fprintf('  Identifying numerical overloads...\n');
            
            % Initialize overload metrics structure
            obj.overloadMetrics = struct();
            
            % 1. Area-based overload analysis
            areaRatio = obj.coupledMetrics.TeamAreaRatio;
            validIndices = ~isnan(areaRatio);
            
            if sum(validIndices) > 10
                % Home team overload (area ratio > 1.2)
                homeOverload = sum(areaRatio(validIndices) > 1.2) / sum(validIndices);
                obj.overloadMetrics.homeAreaOverload = homeOverload;
                
                % Away team overload (area ratio < 0.8)
                awayOverload = sum(areaRatio(validIndices) < 0.8) / sum(validIndices);
                obj.overloadMetrics.awayAreaOverload = awayOverload;
                
                % Balanced play (area ratio between 0.9 and 1.1)
                balancedPlay = sum(areaRatio(validIndices) >= 0.9 & areaRatio(validIndices) <= 1.1) / sum(validIndices);
                obj.overloadMetrics.balancedPlay = balancedPlay;
            end
            
            % 2. NOD-based overload analysis
            homeNOD = obj.coupledMetrics.HomeMeanNOD;
            awayNOD = obj.coupledMetrics.AwayMeanNOD;
            
            validNODIndices = ~isnan(homeNOD) & ~isnan(awayNOD);
            
            if sum(validNODIndices) > 10
                % Tight marking overload (low NOD for one team)
                homeTightMarking = sum(homeNOD(validNODIndices) < 15) / sum(validNODIndices);
                awayTightMarking = sum(awayNOD(validNODIndices) < 15) / sum(validNODIndices);
                
                obj.overloadMetrics.homeTightMarking = homeTightMarking;
                obj.overloadMetrics.awayTightMarking = awayTightMarking;
                
                % Loose marking (high NOD for one team)
                homeLooseMarking = sum(homeNOD(validNODIndices) > 25) / sum(validNODIndices);
                awayLooseMarking = sum(awayNOD(validNODIndices) > 25) / sum(validNODIndices);
                
                obj.overloadMetrics.homeLooseMarking = homeLooseMarking;
                obj.overloadMetrics.awayLooseMarking = awayLooseMarking;
            end
            
            % 3. Inter-team distance overload analysis
            interDist = obj.coupledMetrics.InterTeamDistance;
            validDistIndices = ~isnan(interDist);
            
            if sum(validDistIndices) > 10
                % High pressure (low inter-team distance)
                highPressure = sum(interDist(validDistIndices) < 30) / sum(validDistIndices);
                obj.overloadMetrics.highPressure = highPressure;
                
                % Low pressure (high inter-team distance)
                lowPressure = sum(interDist(validDistIndices) > 60) / sum(validDistIndices);
                obj.overloadMetrics.lowPressure = lowPressure;
            end
            
            fprintf('    Numerical overloads identified\n');
        end
        
        function obj = quantifyTacticalAdvantages(obj)
            % Quantify tactical advantages and their persistence
            
            fprintf('  Quantifying tactical advantages...\n');
            
            % Initialize tactical advantage structure
            obj.tacticalAdvantage = struct();
            
            % 1. Area advantage persistence
            areaRatio = obj.coupledMetrics.TeamAreaRatio;
            validIndices = ~isnan(areaRatio);
            
            if sum(validIndices) > 10
                % Home area advantage
                homeAdvantage = areaRatio > 1.1;
                homeAdvantagePersistence = obj.computePersistence(homeAdvantage(validIndices));
                obj.tacticalAdvantage.homeAreaPersistence = homeAdvantagePersistence;
                
                % Away area advantage
                awayAdvantage = areaRatio < 0.9;
                awayAdvantagePersistence = obj.computePersistence(awayAdvantage(validIndices));
                obj.tacticalAdvantage.awayAreaPersistence = awayAdvantagePersistence;
            end
            
            % 2. NOD advantage persistence
            homeNOD = obj.coupledMetrics.HomeMeanNOD;
            awayNOD = obj.coupledMetrics.AwayMeanNOD;
            
            validNODIndices = ~isnan(homeNOD) & ~isnan(awayNOD);
            
            if sum(validNODIndices) > 10
                % Home NOD advantage (tighter marking)
                homeNODAdvantage = homeNOD < awayNOD - 5; % 5m difference threshold
                homeNODPersistence = obj.computePersistence(homeNODAdvantage(validNODIndices));
                obj.tacticalAdvantage.homeNODPersistence = homeNODPersistence;
                
                % Away NOD advantage
                awayNODAdvantage = awayNOD < homeNOD - 5;
                awayNODPersistence = obj.computePersistence(awayNODAdvantage(validNODIndices));
                obj.tacticalAdvantage.awayNODPersistence = awayNODPersistence;
            end
            
            % 3. Overall tactical advantage index
            if isfield(obj.tacticalAdvantage, 'homeAreaPersistence') && ...
               isfield(obj.tacticalAdvantage, 'homeNODPersistence')
                obj.tacticalAdvantage.overallHomeAdvantage = ...
                    (obj.tacticalAdvantage.homeAreaPersistence + obj.tacticalAdvantage.homeNODPersistence) / 2;
            end
            
            if isfield(obj.tacticalAdvantage, 'awayAreaPersistence') && ...
               isfield(obj.tacticalAdvantage, 'awayNODPersistence')
                obj.tacticalAdvantage.overallAwayAdvantage = ...
                    (obj.tacticalAdvantage.awayAreaPersistence + obj.tacticalAdvantage.awayNODPersistence) / 2;
            end
            
            fprintf('    Tactical advantages quantified\n');
        end
        
        function persistence = computePersistence(~, binarySequence)
            % Compute persistence of a binary sequence (how long advantages last)
            
            if isempty(binarySequence)
                persistence = 0;
                return;
            end
            
            % Find consecutive sequences of 1s
            diffSequence = diff([0; binarySequence; 0]);
            startIndices = find(diffSequence == 1);
            endIndices = find(diffSequence == -1) - 1;
            
            if isempty(startIndices)
                persistence = 0;
            else
                durations = endIndices - startIndices + 1;
                persistence = mean(durations);
            end
        end
        
        function visualizeZeroSumSymmetry(obj)
            % Create comprehensive visualization of zero-sum and symmetry analysis
            
            if ~obj.analysisComplete
                error('Zero-sum analysis not complete. Run analyzeZeroSumCompetition first.');
            end
            
            fprintf('Creating zero-sum and symmetry visualizations...\n');
            
            % Create main figure
            figure('Position', [100, 100, 1800, 1200]);
            
            % Plot 1: Cross-correlations between opposing team metrics
            subplot(3, 4, 1);
            if isfield(obj.crossCorrelations, 'HomeTeamArea')
                correlations = [obj.crossCorrelations.HomeTeamArea, ...
                               obj.crossCorrelations.HomeMeanNOD, ...
                               obj.crossCorrelations.HomeStdNOD];
                bar(correlations);
                xlabel('Metric Pair'); ylabel('Correlation');
                title('Cross-Correlations: Home vs Away');
                xticklabels({'Area', 'Mean NOD', 'Std NOD'});
                grid on;
            end
            
            % Plot 2: Zero-sum competition metrics
            subplot(3, 4, 2);
            if isfield(obj.zeroSumMetrics, 'nodZeroSumIndex')
                zeroSumIndices = [obj.zeroSumMetrics.nodZeroSumIndex(1,2), ...
                                 obj.zeroSumMetrics.areaZeroSumIndex(1,2)];
                bar(zeroSumIndices);
                xlabel('Metric'); ylabel('Zero-Sum Index');
                title('Zero-Sum Competition Indices');
                xticklabels({'NOD', 'Area'});
                grid on;
            end
            
            % Plot 3: Competitive balance
            subplot(3, 4, 3);
            if isfield(obj.competitiveBalance, 'overallBalance')
                balanceMetrics = [obj.competitiveBalance.areaBalance, ...
                                 obj.competitiveBalance.nodBalance, ...
                                 obj.competitiveBalance.overallBalance];
                bar(balanceMetrics);
                xlabel('Balance Type'); ylabel('Balance Index');
                title('Competitive Balance Assessment');
                xticklabels({'Area', 'NOD', 'Overall'});
                grid on;
            end
            
            % Plot 4: Field symmetry
            subplot(3, 4, 4);
            if isfield(obj.fieldSymmetry, 'lateralSymmetry')
                symmetryMetrics = [obj.fieldSymmetry.lateralSymmetry, ...
                                  obj.fieldSymmetry.temporalSymmetry];
                bar(symmetryMetrics);
                xlabel('Symmetry Type'); ylabel('Symmetry Index');
                title('Field Symmetry Analysis');
                xticklabels({'Lateral', 'Temporal'});
                grid on;
            end
            
            % Plot 5: Numerical overloads
            subplot(3, 4, 5);
            if isfield(obj.overloadMetrics, 'homeAreaOverload')
                overloadData = [obj.overloadMetrics.homeAreaOverload, ...
                               obj.overloadMetrics.awayAreaOverload, ...
                               obj.overloadMetrics.balancedPlay];
                bar(overloadData);
                xlabel('Play Type'); ylabel('Frequency');
                title('Numerical Overload Analysis');
                xticklabels({'Home Overload', 'Away Overload', 'Balanced'});
                grid on;
            end
            
            % Plot 6: Tactical advantage persistence
            subplot(3, 4, 6);
            if isfield(obj.tacticalAdvantage, 'overallHomeAdvantage')
                advantageData = [obj.tacticalAdvantage.overallHomeAdvantage, ...
                                obj.tacticalAdvantage.overallAwayAdvantage];
                bar(advantageData);
                xlabel('Team'); ylabel('Advantage Persistence');
                title('Tactical Advantage Persistence');
                xticklabels({'Home', 'Away'});
                grid on;
            end
            
            % Plot 7: Team area ratio over time with overload zones
            subplot(3, 4, 7);
            areaRatio = obj.coupledMetrics.TeamAreaRatio;
            plot(obj.timestamps, areaRatio, 'b-', 'LineWidth', 2);
            hold on;
            yline(1.2, 'r--', 'LineWidth', 2, 'DisplayName', 'Home Overload');
            yline(0.8, 'r--', 'LineWidth', 2, 'DisplayName', 'Away Overload');
            yline(1, 'k-', 'LineWidth', 1, 'DisplayName', 'Balanced');
            xlabel('Time (s)'); ylabel('Area Ratio');
            title('Team Area Ratio with Overload Zones');
            legend('show');
            grid on;
            
            % Plot 8: NOD difference over time
            subplot(3, 4, 8);
            homeNOD = obj.coupledMetrics.HomeMeanNOD;
            awayNOD = obj.coupledMetrics.AwayMeanNOD;
            nodDiff = homeNOD - awayNOD;
            plot(obj.timestamps, nodDiff, 'g-', 'LineWidth', 2);
            hold on;
            yline(5, 'r--', 'LineWidth', 2, 'DisplayName', 'Home Advantage');
            yline(-5, 'r--', 'LineWidth', 2, 'DisplayName', 'Away Advantage');
            yline(0, 'k-', 'LineWidth', 1, 'DisplayName', 'Balanced');
            xlabel('Time (s)'); ylabel('NOD Difference (m)');
            title('NOD Difference with Advantage Zones');
            legend('show');
            grid on;
            
            % Plot 9: Inter-team distance with pressure zones
            subplot(3, 4, 9);
            interDist = obj.coupledMetrics.InterTeamDistance;
            plot(obj.timestamps, interDist, 'm-', 'LineWidth', 2);
            hold on;
            yline(30, 'r--', 'LineWidth', 2, 'DisplayName', 'High Pressure');
            yline(60, 'b--', 'LineWidth', 2, 'DisplayName', 'Low Pressure');
            xlabel('Time (s)'); ylabel('Distance (m)');
            title('Inter-Team Distance with Pressure Zones');
            legend('show');
            grid on;
            
            % Plot 10: Symmetry breaking events
            subplot(3, 4, 10);
            % Identify symmetry breaking events (large deviations from balance)
            areaRatio = obj.coupledMetrics.TeamAreaRatio;
            symmetryBreaking = abs(areaRatio - 1) > 0.2;
            plot(obj.timestamps, symmetryBreaking, 'r-', 'LineWidth', 2);
            xlabel('Time (s)'); ylabel('Symmetry Breaking');
            title('Symmetry Breaking Events');
            ylim([-0.1, 1.1]);
            grid on;
            
            % Plot 11: Competitive balance over time
            subplot(3, 4, 11);
            % Rolling competitive balance
            windowSize = 50;
            rollingBalance = zeros(length(areaRatio) - windowSize + 1, 1);
            for i = 1:length(rollingBalance)
                windowData = areaRatio(i:i+windowSize-1);
                validData = ~isnan(windowData);
                if sum(validData) > 10
                    rollingBalance(i) = 1 - std(windowData(validData));
                else
                    rollingBalance(i) = NaN;
                end
            end
            plot(obj.timestamps(1:length(rollingBalance)), rollingBalance, 'k-', 'LineWidth', 2);
            xlabel('Time (s)'); ylabel('Competitive Balance');
            title('Rolling Competitive Balance');
            grid on;
            
            % Plot 12: Analysis summary
            subplot(3, 4, 12);
            summaryText = {
                sprintf('Step 3 Analysis Summary:');
                sprintf('');
                sprintf('Zero-Sum Competition:');
            };
            
            % Add zero-sum metrics
            if isfield(obj.zeroSumMetrics, 'nodZeroSumIndex')
                summaryText{end+1} = sprintf('  NOD Zero-Sum: %.3f', obj.zeroSumMetrics.nodZeroSumIndex(1,2));
            end
            if isfield(obj.zeroSumMetrics, 'areaZeroSumIndex')
                summaryText{end+1} = sprintf('  Area Zero-Sum: %.3f', obj.zeroSumMetrics.areaZeroSumIndex(1,2));
            end
            
            summaryText{end+1} = sprintf('');
            summaryText{end+1} = sprintf('Competitive Balance:');
            
            % Add competitive balance
            if isfield(obj.competitiveBalance, 'overallBalance')
                summaryText{end+1} = sprintf('  Overall Balance: %.3f', obj.competitiveBalance.overallBalance);
            end
            
            summaryText{end+1} = sprintf('');
            summaryText{end+1} = sprintf('Field Symmetry:');
            
            % Add field symmetry
            if isfield(obj.fieldSymmetry, 'lateralSymmetry')
                summaryText{end+1} = sprintf('  Lateral Symmetry: %.3f', obj.fieldSymmetry.lateralSymmetry);
            end
            
            summaryText{end+1} = sprintf('');
            summaryText{end+1} = sprintf('Tactical Advantages:');
            
            % Add tactical advantages
            if isfield(obj.tacticalAdvantage, 'overallHomeAdvantage')
                summaryText{end+1} = sprintf('  Home Advantage: %.3f', obj.tacticalAdvantage.overallHomeAdvantage);
            end
            if isfield(obj.tacticalAdvantage, 'overallAwayAdvantage')
                summaryText{end+1} = sprintf('  Away Advantage: %.3f', obj.tacticalAdvantage.overallAwayAdvantage);
            end
            
            text(0.05, 0.95, summaryText, 'FontSize', 10, 'VerticalAlignment', 'top');
            axis off;
            
            sgtitle('Step 3: Zero-Sum Competition & Symmetry Breaking Analysis', 'FontSize', 16, 'FontWeight', 'bold');
            
            fprintf('Zero-sum and symmetry visualization complete\n');
        end
        
        function exportResults(obj, outputDir)
            % Export zero-sum and symmetry analysis results
            
            if ~obj.analysisComplete
                error('Zero-sum analysis not complete. Run analyzeZeroSumCompetition first.');
            end
            
            if ~exist(outputDir, 'dir')
                mkdir(outputDir);
            end
            
            fprintf('Exporting zero-sum and symmetry results to: %s\n', outputDir);
            
            % Export cross-correlations
            if isfield(obj.crossCorrelations, 'HomeTeamArea')
                corrData = [obj.crossCorrelations.HomeTeamArea, ...
                           obj.crossCorrelations.HomeMeanNOD, ...
                           obj.crossCorrelations.HomeStdNOD];
                corrTable = table({'Area'; 'MeanNOD'; 'StdNOD'}, corrData', ...
                                'VariableNames', {'Metric', 'Correlation'});
                writetable(corrTable, fullfile(outputDir, 'cross_correlations.csv'));
            end
            
            % Export zero-sum metrics
            if isfield(obj.zeroSumMetrics, 'nodZeroSumIndex')
                zeroSumData = [obj.zeroSumMetrics.nodZeroSumIndex(1,2), ...
                              obj.zeroSumMetrics.areaZeroSumIndex(1,2), ...
                              obj.zeroSumMetrics.nodBalance, ...
                              obj.zeroSumMetrics.areaBalance];
                zeroSumTable = table({'NOD_ZeroSum'; 'Area_ZeroSum'; 'NOD_Balance'; 'Area_Balance'}, zeroSumData', ...
                                    'VariableNames', {'Metric', 'Value'});
                writetable(zeroSumTable, fullfile(outputDir, 'zero_sum_metrics.csv'));
            end
            
            % Export competitive balance
            if isfield(obj.competitiveBalance, 'overallBalance')
                balanceData = [obj.competitiveBalance.areaBalance, ...
                              obj.competitiveBalance.nodBalance, ...
                              obj.competitiveBalance.overallBalance];
                balanceTable = table({'Area_Balance'; 'NOD_Balance'; 'Overall_Balance'}, balanceData', ...
                                    'VariableNames', {'Metric', 'Value'});
                writetable(balanceTable, fullfile(outputDir, 'competitive_balance.csv'));
            end
            
            % Export overload metrics
            if isfield(obj.overloadMetrics, 'homeAreaOverload')
                overloadData = [obj.overloadMetrics.homeAreaOverload, ...
                               obj.overloadMetrics.awayAreaOverload, ...
                               obj.overloadMetrics.balancedPlay, ...
                               obj.overloadMetrics.highPressure, ...
                               obj.overloadMetrics.lowPressure];
                overloadTable = table({'Home_Area_Overload'; 'Away_Area_Overload'; 'Balanced_Play'; 'High_Pressure'; 'Low_Pressure'}, overloadData', ...
                                      'VariableNames', {'Metric', 'Frequency'});
                writetable(overloadTable, fullfile(outputDir, 'overload_metrics.csv'));
            end
            
            % Save MATLAB data
            save(fullfile(outputDir, 'zero_sum_symmetry_analysis.mat'), 'obj');
            
            fprintf('Zero-sum and symmetry results exported successfully\n');
        end
    end
end
