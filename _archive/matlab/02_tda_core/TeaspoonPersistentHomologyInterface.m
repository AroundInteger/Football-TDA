classdef TeaspoonPersistentHomologyInterface
    % TEASPOONPERSISTENTHOMOLOGYINTERFACE - MATLAB interface for Teaspoon TSP library
    % 
    % This class provides a MATLAB interface to call the teaspoon library
    % for comprehensive topological signal processing analysis.
    %
    % Teaspoon provides:
    % - Parameter selection for delay coordinate embedding
    % - Signal processing tools for time series analysis
    % - Advanced TDA methods for persistent homology
    % - Machine learning integration for persistence diagrams
    %
    % Key Features:
    % - Calls teaspoon TSP library from MATLAB
    % - Automatic parameter selection using FNN and MI
    % - Delay coordinate embedding optimization
    % - Advanced persistent homology computation
    % - ML feature extraction from persistence diagrams
    % - Quantum dot insights integration
    % - Tactical effectiveness analysis
    
    properties
        % Configuration
        pythonExecutable    % Path to Python executable
        pythonScript        % Path to teaspoon Python script
        tempDir            % Temporary directory for data exchange
        
        % Input data
        coupledMetrics      % Coupled collective variables from Step 1
        stateSpace         % State space reconstruction from Step 2
        zeroSumAnalysis    % Zero-sum analysis from Step 3
        quantumDotModel    % Quantum dot model from quantum analysis
        
        % Results
        teaspoonResults    % Results from teaspoon analysis
        analysisComplete   % Boolean flag
        computationTime    % Time taken for analysis
    end
    
    methods
        function obj = TeaspoonPersistentHomologyInterface(coupledMetrics, stateSpace, zeroSumAnalysis, quantumDotModel, varargin)
            % Constructor for TeaspoonPersistentHomologyInterface
            
            % Store input data
            obj.coupledMetrics = coupledMetrics;
            obj.stateSpace = stateSpace;
            obj.zeroSumAnalysis = zeroSumAnalysis;
            obj.quantumDotModel = quantumDotModel;
            
            % Set default paths
            obj.pythonExecutable = 'python3'; % Default Python executable
            obj.pythonScript = 'persistent_homology_teaspoon.py';
            obj.tempDir = './temp_teaspoon_analysis';
            
            % Parse optional parameters
            if nargin > 4
                for i = 1:2:length(varargin)
                    switch lower(varargin{i})
                        case 'pythonexecutable'
                            obj.pythonExecutable = varargin{i+1};
                        case 'pythonscript'
                            obj.pythonScript = varargin{i+1};
                        case 'tempdir'
                            obj.tempDir = varargin{i+1};
                    end
                end
            end
            
            % Initialize
            obj.analysisComplete = false;
            obj.computationTime = 0;
            
            fprintf('TeaspoonPersistentHomologyInterface initialized\n');
            fprintf('  Python executable: %s\n', obj.pythonExecutable);
            fprintf('  Teaspoon script: %s\n', obj.pythonScript);
            fprintf('  Temp directory: %s\n', obj.tempDir);
        end
        
        function obj = runTeaspoonAnalysis(obj)
            % Run teaspoon persistent homology analysis
            
            fprintf('Running Teaspoon TSP analysis...\n');
            tic;
            
            % Step 1: Check Python and teaspoon availability
            if ~obj.checkTeaspoonAvailability()
                error('Python or teaspoon library not available. Please install teaspoon.');
            end
            
            % Step 2: Export MATLAB data to JSON
            obj.exportDataToJSON();
            
            % Step 3: Run teaspoon script
            obj.runTeaspoonScript();
            
            % Step 4: Import teaspoon results
            obj.importTeaspoonResults();
            
            % Mark analysis as complete
            obj.analysisComplete = true;
            obj.computationTime = toc;
            
            fprintf('Teaspoon TSP analysis complete (%.2f seconds)\n', obj.computationTime);
        end
        
        function isAvailable = checkTeaspoonAvailability(obj)
            % Check if Python and teaspoon are available
            
            fprintf('  Checking teaspoon availability...\n');
            
            % Check Python executable
            [status, ~] = system([obj.pythonExecutable, ' --version']);
            if status ~= 0
                fprintf('    Python executable not found: %s\n', obj.pythonExecutable);
                isAvailable = false;
                return;
            end
            
            % Check if teaspoon script exists
            if ~exist(obj.pythonScript, 'file')
                fprintf('    Teaspoon script not found: %s\n', obj.pythonScript);
                isAvailable = false;
                return;
            end
            
            % Check for teaspoon library
            [status, output] = system([obj.pythonExecutable, ' -c "import teaspoon; print(\"Teaspoon available\")"']);
            if status ~= 0
                fprintf('    Teaspoon library not available\n');
                fprintf('    Install with: pip install teaspoon\n');
                isAvailable = false;
                return;
            end
            
            fprintf('    Python and teaspoon library available\n');
            isAvailable = true;
        end
        
        function exportDataToJSON(obj)
            % Export MATLAB data to JSON for teaspoon processing
            
            fprintf('  Exporting MATLAB data to JSON...\n');
            
            % Create temporary directory
            if ~exist(obj.tempDir, 'dir')
                mkdir(obj.tempDir);
            end
            
            % Prepare data structure
            data = struct();
            
            % Export time series data (state vectors)
            if ~isempty(obj.stateSpace.stateVectors)
                data.stateVectors = obj.stateSpace.stateVectors;
            end
            
            % Export coupled metrics as time series
            if ~isempty(obj.coupledMetrics)
                data.coupledMetrics = struct();
                data.coupledMetrics.InterTeamDistance = obj.coupledMetrics.InterTeamDistance;
                data.coupledMetrics.TeamAreaRatio = obj.coupledMetrics.TeamAreaRatio;
                data.coupledMetrics.HomeMeanNOD = obj.coupledMetrics.HomeMeanNOD;
                data.coupledMetrics.AwayMeanNOD = obj.coupledMetrics.AwayMeanNOD;
            end
            
            % Export quantum dot model
            if ~isempty(obj.quantumDotModel)
                data.quantumDotModel = struct();
                if isfield(obj.quantumDotModel, 'stateLifetimes')
                    data.quantumDotModel.stateLifetimes = obj.quantumDotModel.stateLifetimes;
                end
                if isfield(obj.quantumDotModel, 'quantumDotAnalogy')
                    data.quantumDotModel.quantumDotAnalogy = obj.quantumDotModel.quantumDotAnalogy;
                end
            end
            
            % Export state space information
            if ~isempty(obj.stateSpace)
                data.stateSpace = struct();
                if isfield(obj.stateSpace, 'embeddingDimension')
                    data.stateSpace.embeddingDimension = obj.stateSpace.embeddingDimension;
                end
                if isfield(obj.stateSpace, 'timeDelay')
                    data.stateSpace.timeDelay = obj.stateSpace.timeDelay;
                end
            end
            
            % Export zero-sum analysis
            if ~isempty(obj.zeroSumAnalysis)
                data.zeroSumAnalysis = struct();
                if isfield(obj.zeroSumAnalysis, 'competitiveBalance')
                    data.zeroSumAnalysis.competitiveBalance = obj.zeroSumAnalysis.competitiveBalance;
                end
            end
            
            % Save to JSON file
            inputFile = fullfile(obj.tempDir, 'matlab_data.json');
            jsonStr = jsonencode(data);
            fid = fopen(inputFile, 'w');
            fprintf(fid, '%s', jsonStr);
            fclose(fid);
            
            fprintf('    Data exported to: %s\n', inputFile);
        end
        
        function runTeaspoonScript(obj)
            % Run the teaspoon persistent homology script
            
            fprintf('  Running teaspoon script...\n');
            
            % Prepare file paths
            inputFile = fullfile(obj.tempDir, 'matlab_data.json');
            outputFile = fullfile(obj.tempDir, 'teaspoon_results.json');
            
            % Construct command
            command = sprintf('%s %s %s %s', obj.pythonExecutable, obj.pythonScript, inputFile, outputFile);
            
            % Run command
            [status, output] = system(command);
            
            if status ~= 0
                error('Teaspoon script failed with status %d. Output: %s', status, output);
            end
            
            fprintf('    Teaspoon script completed successfully\n');
        end
        
        function importTeaspoonResults(obj)
            % Import teaspoon results back to MATLAB
            
            fprintf('  Importing teaspoon results...\n');
            
            % Load JSON results
            outputFile = fullfile(obj.tempDir, 'teaspoon_results.json');
            if ~exist(outputFile, 'file')
                error('Teaspoon output file not found: %s', outputFile);
            end
            
            % Read JSON file
            fid = fopen(outputFile, 'r');
            jsonStr = fread(fid, inf, 'uint8=>char')';
            fclose(fid);
            
            % Parse JSON
            obj.teaspoonResults = jsondecode(jsonStr);
            
            fprintf('    Teaspoon results imported successfully\n');
        end
        
        function visualizeTeaspoonResults(obj)
            % Create comprehensive visualization of teaspoon results
            
            if ~obj.analysisComplete
                error('Teaspoon analysis not complete. Run runTeaspoonAnalysis first.');
            end
            
            fprintf('Creating teaspoon TSP visualizations...\n');
            
            % Create main figure
            figure('Position', [100, 100, 2000, 1400]);
            
            % Plot 1: H0 persistence diagram
            subplot(3, 5, 1);
            if isfield(obj.teaspoonResults, 'teaspoon') && isfield(obj.teaspoonResults.teaspoon, 'H0')
                h0_diagram = obj.teaspoonResults.teaspoon.H0;
            elseif isfield(obj.teaspoonResults, 'ripser') && isfield(obj.teaspoonResults.ripser, 'H0')
                h0_diagram = obj.teaspoonResults.ripser.H0;
            else
                h0_diagram = [];
            end
            
            if ~isempty(h0_diagram)
                scatter(h0_diagram(:, 1), h0_diagram(:, 2), 100, 'filled');
                xlabel('Birth'); ylabel('Death');
                title('H0 Persistence Diagram (Teaspoon)');
                grid on;
                axis equal;
            end
            
            % Plot 2: H1 persistence diagram
            subplot(3, 5, 2);
            if isfield(obj.teaspoonResults, 'teaspoon') && isfield(obj.teaspoonResults.teaspoon, 'H1')
                h1_diagram = obj.teaspoonResults.teaspoon.H1;
            elseif isfield(obj.teaspoonResults, 'ripser') && isfield(obj.teaspoonResults.ripser, 'H1')
                h1_diagram = obj.teaspoonResults.ripser.H1;
            else
                h1_diagram = [];
            end
            
            if ~isempty(h1_diagram)
                scatter(h1_diagram(:, 1), h1_diagram(:, 2), 100, 'filled');
                xlabel('Birth'); ylabel('Death');
                title('H1 Persistence Diagram (Teaspoon)');
                grid on;
                axis equal;
            end
            
            % Plot 3: Topological features summary
            subplot(3, 5, 3);
            if isfield(obj.teaspoonResults, 'topological_features')
                h0_count = obj.teaspoonResults.topological_features.H0.count;
                h1_count = obj.teaspoonResults.topological_features.H1.count;
                bar([h0_count, h1_count]);
                xlabel('Homology Dimension'); ylabel('Feature Count');
                title('Topological Feature Counts (Teaspoon)');
                xticklabels({'H0', 'H1'});
                grid on;
            end
            
            % Plot 4: Persistence distributions
            subplot(3, 5, 4);
            if isfield(obj.teaspoonResults, 'topological_features')
                h0_persistence = obj.teaspoonResults.topological_features.H0.persistence_values;
                if ~isempty(h0_persistence)
                    histogram(h0_persistence, 20);
                    xlabel('Persistence'); ylabel('Frequency');
                    title('H0 Persistence Distribution (Teaspoon)');
                    grid on;
                end
            end
            
            % Plot 5: Embedding parameters
            subplot(3, 5, 5);
            if isfield(obj.teaspoonResults, 'metadata')
                metadata = obj.teaspoonResults.metadata;
                embedding_dim = metadata.embedding_dimension;
                time_delay = metadata.time_delay;
                
                bar([embedding_dim, time_delay]);
                xlabel('Parameter Type'); ylabel('Value');
                title('Optimal Embedding Parameters (Teaspoon)');
                xticklabels({'Embedding Dim', 'Time Delay'});
                grid on;
            end
            
            % Plot 6: Quantum topological features
            subplot(3, 5, 6);
            if isfield(obj.teaspoonResults, 'quantum_topological_features')
                quantum_feat = obj.teaspoonResults.quantum_topological_features;
                if isfield(quantum_feat, 'H0') && isfield(quantum_feat.H0, 'quantum_efficiency')
                    h0_eff = quantum_feat.H0.quantum_efficiency;
                    h1_eff = quantum_feat.H1.quantum_efficiency;
                    bar([h0_eff, h1_eff]);
                    xlabel('Homology Dimension'); ylabel('Quantum Efficiency');
                    title('Quantum Topological Features (Teaspoon)');
                    xticklabels({'H0', 'H1'});
                    grid on;
                end
            end
            
            % Plot 7: Tactical effectiveness
            subplot(3, 5, 7);
            if isfield(obj.teaspoonResults, 'tactical_effectiveness')
                tact_eff = obj.teaspoonResults.tactical_effectiveness;
                effectiveness_metrics = [];
                metric_names = {};
                
                if isfield(tact_eff, 'complexity_effectiveness')
                    effectiveness_metrics = [effectiveness_metrics, tact_eff.complexity_effectiveness.effectiveness_score];
                    metric_names{end+1} = 'Complexity';
                end
                if isfield(tact_eff, 'persistence_balance')
                    effectiveness_metrics = [effectiveness_metrics, double(tact_eff.persistence_balance.is_balanced)];
                    metric_names{end+1} = 'Balance';
                end
                if isfield(tact_eff, 'quantum_effectiveness')
                    effectiveness_metrics = [effectiveness_metrics, tact_eff.quantum_effectiveness.quantum_score];
                    metric_names{end+1} = 'Quantum';
                end
                
                if ~isempty(effectiveness_metrics)
                    bar(effectiveness_metrics);
                    xlabel('Effectiveness Metric'); ylabel('Score');
                    title('Tactical Effectiveness (Teaspoon)');
                    xticklabels(metric_names);
                    grid on;
                end
            end
            
            % Plot 8: Complexity evolution
            subplot(3, 5, 8);
            if isfield(obj.teaspoonResults, 'topological_features') && isfield(obj.teaspoonResults.topological_features, 'overall')
                overall = obj.teaspoonResults.topological_features.overall;
                complexity = overall.complexity_index;
                bar(1, complexity);
                xlabel('Analysis'); ylabel('Complexity Index');
                title('Topological Complexity (Teaspoon)');
                grid on;
            end
            
            % Plot 9: Quantum correlation
            subplot(3, 5, 9);
            if isfield(obj.teaspoonResults, 'quantum_topological_features')
                quantum_feat = obj.teaspoonResults.quantum_topological_features;
                correlations = [];
                if isfield(quantum_feat, 'H0') && isfield(quantum_feat.H0, 'quantum_correlation')
                    correlations = [correlations, quantum_feat.H0.quantum_correlation];
                end
                if isfield(quantum_feat, 'H1') && isfield(quantum_feat.H1, 'quantum_correlation')
                    correlations = [correlations, quantum_feat.H1.quantum_correlation];
                end
                
                if ~isempty(correlations)
                    bar(correlations);
                    xlabel('Homology Dimension'); ylabel('Quantum Correlation');
                    title('Quantum-Topology Correlation (Teaspoon)');
                    xticklabels({'H0', 'H1'});
                    grid on;
                end
            end
            
            % Plot 10: ML features
            subplot(3, 5, 10);
            if isfield(obj.teaspoonResults, 'ml_features')
                ml_feat = obj.teaspoonResults.ml_features;
                if isfield(ml_feat, 'H0') && isfield(ml_feat.H0, 'persistence_entropy')
                    h0_entropy = ml_feat.H0.persistence_entropy;
                    h1_entropy = ml_feat.H1.persistence_entropy;
                    bar([h0_entropy, h1_entropy]);
                    xlabel('Homology Dimension'); ylabel('Persistence Entropy');
                    title('ML Features - Persistence Entropy (Teaspoon)');
                    xticklabels({'H0', 'H1'});
                    grid on;
                end
            end
            
            % Plot 11: Lifetime ratios
            subplot(3, 5, 11);
            if isfield(obj.teaspoonResults, 'quantum_topological_features')
                quantum_feat = obj.teaspoonResults.quantum_topological_features;
                lifetime_ratios = [];
                if isfield(quantum_feat, 'H0') && isfield(quantum_feat.H0, 'lifetime_ratio')
                    lifetime_ratios = [lifetime_ratios, quantum_feat.H0.lifetime_ratio];
                end
                if isfield(quantum_feat, 'H1') && isfield(quantum_feat.H1, 'lifetime_ratio')
                    lifetime_ratios = [lifetime_ratios, quantum_feat.H1.lifetime_ratio];
                end
                
                if ~isempty(lifetime_ratios)
                    bar(lifetime_ratios);
                    xlabel('Homology Dimension'); ylabel('Lifetime Ratio');
                    title('Topological Lifetime Ratios (Teaspoon)');
                    xticklabels({'H0', 'H1'});
                    grid on;
                end
            end
            
            % Plot 12: Feature counts comparison
            subplot(3, 5, 12);
            if isfield(obj.teaspoonResults, 'topological_features')
                h0_count = obj.teaspoonResults.topological_features.H0.count;
                h1_count = obj.teaspoonResults.topological_features.H1.count;
                total_features = obj.teaspoonResults.topological_features.overall.total_features;
                
                pie([h0_count, h1_count], {'H0 Features', 'H1 Features'});
                title(sprintf('Feature Distribution (Total: %d)', total_features));
            end
            
            % Plot 13: Analysis summary
            subplot(3, 5, 13);
            if isfield(obj.teaspoonResults, 'metadata')
                metadata = obj.teaspoonResults.metadata;
                summaryText = {
                    sprintf('Teaspoon TSP Analysis Summary:');
                    sprintf('');
                    sprintf('Point Cloud: %dx%d', metadata.point_cloud_shape(1), metadata.point_cloud_shape(2));
                    sprintf('Embedding Dim: %d', metadata.embedding_dimension);
                    sprintf('Time Delay: %d', metadata.time_delay);
                    sprintf('Max Filtration: %.2f', metadata.max_filtration);
                    sprintf('');
                    sprintf('Libraries Used:');
                };
                
                % Add library information
                if metadata.libraries_used.teaspoon
                    summaryText{end+1} = sprintf('  ✓ Teaspoon TSP');
                end
                if metadata.libraries_used.ripser
                    summaryText{end+1} = sprintf('  ✓ Ripser');
                end
                if metadata.libraries_used.gudhi
                    summaryText{end+1} = sprintf('  ✓ Gudhi');
                end
                
                summaryText{end+1} = sprintf('');
                summaryText{end+1} = sprintf('Computation Time: %.2f s', obj.computationTime);
                
                text(0.05, 0.95, summaryText, 'FontSize', 10, 'VerticalAlignment', 'top');
            end
            axis off;
            
            % Plot 14: TSP Pipeline
            subplot(3, 5, 14);
            tspText = {
                sprintf('Teaspoon TSP Pipeline:');
                sprintf('');
                sprintf('1. ✓ Parameter Selection');
                sprintf('   - FNN for embedding dimension');
                sprintf('   - MI for time delay');
                sprintf('');
                sprintf('2. ✓ Signal Processing');
                sprintf('   - Delay coordinate embedding');
                sprintf('   - Time series preprocessing');
                sprintf('');
                sprintf('3. ✓ TDA Analysis');
                sprintf('   - Persistent homology');
                sprintf('   - Feature extraction');
                sprintf('');
                sprintf('4. ✓ ML Integration');
                sprintf('   - Persistence entropy');
                sprintf('   - Betti curves');
            };
            
            text(0.05, 0.95, tspText, 'FontSize', 10, 'VerticalAlignment', 'top');
            axis off;
            
            % Plot 15: Integration benefits
            subplot(3, 5, 15);
            benefitsText = {
                sprintf('Teaspoon TSP Benefits:');
                sprintf('');
                sprintf('✓ Signal Processing Focus');
                sprintf('✓ Optimal Parameter Selection');
                sprintf('✓ Advanced TDA Methods');
                sprintf('✓ ML Feature Integration');
                sprintf('✓ Quantum Dot Insights');
                sprintf('✓ Tactical Effectiveness');
                sprintf('');
                sprintf('Research-Grade Analysis');
                sprintf('for Football TDA');
            };
            
            text(0.05, 0.95, benefitsText, 'FontSize', 10, 'VerticalAlignment', 'top');
            axis off;
            
            sgtitle('Step 4: Teaspoon TSP Persistent Homology Analysis with Quantum Dot Insights', 'FontSize', 16, 'FontWeight', 'bold');
            
            fprintf('Teaspoon TSP visualization complete\n');
        end
        
        function exportResults(obj, outputDir)
            % Export teaspoon results
            
            if ~obj.analysisComplete
                error('Teaspoon analysis not complete. Run runTeaspoonAnalysis first.');
            end
            
            if ~exist(outputDir, 'dir')
                mkdir(outputDir);
            end
            
            fprintf('Exporting teaspoon TSP results to: %s\n', outputDir);
            
            % Export persistence diagrams
            if isfield(obj.teaspoonResults, 'teaspoon')
                diagrams = obj.teaspoonResults.teaspoon;
            elseif isfield(obj.teaspoonResults, 'ripser')
                diagrams = obj.teaspoonResults.ripser;
            else
                diagrams = struct();
            end
            
            for dim = 0:2
                h_key = sprintf('H%d', dim);
                if isfield(diagrams, h_key)
                    diagram = diagrams.(h_key);
                    if ~isempty(diagram)
                        diagramTable = array2table(diagram, 'VariableNames', {'Birth', 'Death'});
                        writetable(diagramTable, fullfile(outputDir, sprintf('teaspoon_persistence_diagram_%s.csv', h_key)));
                    end
                end
            end
            
            % Export topological features
            if isfield(obj.teaspoonResults, 'topological_features')
                features = obj.teaspoonResults.topological_features;
                featureTable = table(features.H0.count, features.H1.count, features.overall.complexity_index, ...
                                   features.overall.embedding_dimension, features.overall.time_delay, ...
                                   'VariableNames', {'H0_Count', 'H1_Count', 'Complexity_Index', 'Embedding_Dimension', 'Time_Delay'});
                writetable(featureTable, fullfile(outputDir, 'teaspoon_topological_features.csv'));
            end
            
            % Export quantum topological features
            if isfield(obj.teaspoonResults, 'quantum_topological_features')
                quantum_feat = obj.teaspoonResults.quantum_topological_features;
                quantumTable = table(quantum_feat.H0.quantum_efficiency, quantum_feat.H1.quantum_efficiency, ...
                                   quantum_feat.H0.quantum_correlation, quantum_feat.H1.quantum_correlation, ...
                                   'VariableNames', {'H0_Quantum_Efficiency', 'H1_Quantum_Efficiency', 'H0_Quantum_Correlation', 'H1_Quantum_Correlation'});
                writetable(quantumTable, fullfile(outputDir, 'teaspoon_quantum_topological_features.csv'));
            end
            
            % Export tactical effectiveness
            if isfield(obj.teaspoonResults, 'tactical_effectiveness')
                tact_eff = obj.teaspoonResults.tactical_effectiveness;
                effectivenessTable = table(tact_eff.complexity_effectiveness.effectiveness_score, ...
                                         double(tact_eff.persistence_balance.is_balanced), ...
                                         tact_eff.quantum_effectiveness.quantum_score, ...
                                         'VariableNames', {'Complexity_Effectiveness', 'Persistence_Balance', 'Quantum_Effectiveness'});
                writetable(effectivenessTable, fullfile(outputDir, 'teaspoon_tactical_effectiveness.csv'));
            end
            
            % Export ML features
            if isfield(obj.teaspoonResults, 'ml_features')
                ml_feat = obj.teaspoonResults.ml_features;
                if isfield(ml_feat.H0, 'persistence_entropy')
                    mlTable = table(ml_feat.H0.persistence_entropy, ml_feat.H1.persistence_entropy, ...
                                   'VariableNames', {'H0_Persistence_Entropy', 'H1_Persistence_Entropy'});
                    writetable(mlTable, fullfile(outputDir, 'teaspoon_ml_features.csv'));
                end
            end
            
            % Save MATLAB data
            save(fullfile(outputDir, 'teaspoon_persistent_homology_analysis.mat'), 'obj');
            
            fprintf('Teaspoon TSP results exported successfully\n');
        end
        
        function cleanup(obj)
            % Clean up temporary files
            
            if exist(obj.tempDir, 'dir')
                rmdir(obj.tempDir, 's');
                fprintf('Temporary directory cleaned up: %s\n', obj.tempDir);
            end
        end
    end
end
