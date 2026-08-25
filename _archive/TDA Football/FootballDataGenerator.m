classdef FootballDataGenerator
    properties
        matchDuration    % Duration in seconds
        samplingRate     % Samples per second
        fieldDimensions  % [length, width] in meters
        formations      % Dictionary of common formations
    end
    
    methods
        function obj = FootballDataGenerator()
            % Initialize with default parameters
            obj.matchDuration = 90 * 60;  % 90 minutes in seconds
            obj.samplingRate = 10;        % 10 Hz sampling
            obj.fieldDimensions = [105, 68]; % Standard field dimensions
            
            % Initialize common formations [x, y] coordinates
            obj.formations = struct();
            obj.formations.f442 = [
                % Defenders (4)
                20 15; 20 30; 20 40; 20 55;
                % Midfielders (4)
                50 15; 50 30; 50 40; 50 55;
                % Forwards (2)
                80 25; 80 45
            ];
            
            obj.formations.f433 = [
                % Defenders (4)
                20 15; 20 30; 20 40; 20 55;
                % Midfielders (3)
                50 20; 50 35; 50 50;
                % Forwards (3)
                80 15; 80 35; 80 55
            ];
            
            obj.formations.f352 = [
                % Defenders (3)
                20 20; 20 35; 20 50;
                % Midfielders (5)
                45 10; 45 25; 45 35; 45 45; 45 60;
                % Forwards (2)
                80 25; 80 45
            ];
        end
        
        function data = generateMatchData(obj, formation, scenario)
            % Generate match data with specific formation and scenario
            nTimeSteps = obj.matchDuration * obj.samplingRate;
            nPlayers = size(obj.formations.(formation), 1);
            
            % Initialize data structure
            data = struct();
            data.positions = zeros(nTimeSteps, nPlayers, 2);
            data.velocities = zeros(nTimeSteps, nPlayers, 2);
            data.accelerations = zeros(nTimeSteps, nPlayers, 2);
            data.events = cell(nTimeSteps, 1);
            data.metadata = struct('formation', formation, 'scenario', scenario);
            
            % Generate base movement based on scenario
            switch scenario
                case 'defensive_press'
                    data = obj.generateDefensivePress(data, formation);
                case 'attacking_buildup'
                    data = obj.generateAttackingBuildup(data, formation);
                case 'possession'
                    data = obj.generatePossessionBased(data, formation);
                otherwise
                    data = obj.generateNormalPlay(data, formation);
            end
            
            % Add natural variation and noise
            data = obj.addVariationAndNoise(data);
            
            % Compute derived metrics
            data = obj.computeDerivedMetrics(data);
        end
        
        function plotTrajectories(~, data, timeWindow)
            % Visualize player trajectories within a time window
            figure('Position', [100 100 1200 800]);
            
            % Plot positions
            subplot(2,2,1);
            positions = data.positions(timeWindow,:,:);
            for p = 1:size(positions,2)
                plot(squeeze(positions(:,p,1)), squeeze(positions(:,p,2)), '-');
                hold on;
            end
            title('Player Trajectories');
            xlabel('X Position (m)');
            ylabel('Y Position (m)');
            grid on;
            
            % Plot team centroid movement
            subplot(2,2,2);
            centroids = squeeze(mean(positions, 2));
            plot(centroids(:,1), centroids(:,2), 'r-', 'LineWidth', 2);
            title('Team Centroid Movement');
            xlabel('X Position (m)');
            ylabel('Y Position (m)');
            grid on;
            
            % Plot velocity magnitudes
            subplot(2,2,3);
            velocities = data.velocities(timeWindow,:,:);
            vel_mag = sqrt(sum(velocities.^2, 3));
            plot(timeWindow, vel_mag);
            title('Player Velocities');
            xlabel('Time Step');
            ylabel('Velocity (m/s)');
            grid on;
            
            % Plot team shape metric
            subplot(2,2,4);
            team_spread = squeeze(std(positions, [], 2));
            plot(timeWindow, sqrt(sum(team_spread.^2, 2)));
            title('Team Spread');
            xlabel('Time Step');
            ylabel('Spread (m)');
            grid on;
        end
        
        function exportData(~, data, filename)
            % Export data in common format (CSV and JSON)
            
            % Save positions to CSV
            positions_table = array2table(reshape(data.positions, [], 2 * size(data.positions, 2)));
            writetable(positions_table, [filename '_positions.csv']);
            
            % Save metadata and events to JSON
            metadata = struct();
            metadata.formation = data.metadata.formation;
            metadata.scenario = data.metadata.scenario;
            metadata.events = data.events;
            
            fid = fopen([filename '_metadata.json'], 'w');
            fprintf(fid, jsonencode(metadata, 'PrettyPrint', true));
            fclose(fid);
        end
        
        % Private helper methods
        function data = generateDefensivePress(obj, data, formation)
            base_positions = obj.formations.(formation);
            nTimeSteps = size(data.positions, 1);
            
            % Simulate pressing movement
            for t = 1:nTimeSteps
                press_intensity = min(t/nTimeSteps * 2, 1);
                forward_press = press_intensity * [20 0];
                data.positions(t,:,:) = base_positions + forward_press;
                
                % Add coordinated pressing movement
                if t > nTimeSteps/2
                    data.positions(t,:,1) = data.positions(t,:,1) + 5 * sin(t/20);
                end
            end
        end
        
        function data = generateAttackingBuildup(obj, data, formation)
            base_positions = obj.formations.(formation);
            nTimeSteps = size(data.positions, 1);
            
            % Simulate build-up play
            for t = 1:nTimeSteps
                progress = t/nTimeSteps;
                forward_movement = progress * [30 0];
                spread = sin(t/30) * [0 5];
                
                data.positions(t,:,:) = base_positions + forward_movement + spread;
                
                % Add wing play
                if t > nTimeSteps/3
                    data.positions(t,[4,7],2) = data.positions(t,[4,7],2) + 10;
                end
            end
        end
        
        function data = generatePossessionBased(obj, data, formation)
            base_positions = obj.formations.(formation);
            nTimeSteps = size(data.positions, 1);
            
            % Simulate possession-based movement
            for t = 1:nTimeSteps
                rotation = [cos(t/50) -sin(t/50); sin(t/50) cos(t/50)];
                shifted_positions = (base_positions - [50 34]) * rotation + [50 34];
                data.positions(t,:,:) = shifted_positions;
                
                % Add positional interchange
                if mod(t, 100) < 50
                    data.positions(t,[6,7],:) = data.positions(t,[7,6],:);
                end
            end
        end
        
        function data = generateNormalPlay(obj, data, formation)
            base_positions = obj.formations.(formation);
            nTimeSteps = size(data.positions, 1);
            
            % Simulate normal match play
            for t = 1:nTimeSteps
                % Add natural movement patterns
                oscillation = sin(t/40) * [5 3];
                drift = (rand(1,2) - 0.5) * 2;
                
                data.positions(t,:,:) = base_positions + oscillation + drift;
            end
        end
        
        function data = addVariationAndNoise(~, data)
            % Add individual player variation and measurement noise
            
            % Player variation
            individual_variation = randn(size(data.positions)) * 0.5;
            data.positions = data.positions + individual_variation;
            
            % Compute velocities and accelerations
            dt = 0.1; % 10 Hz sampling
            data.velocities(2:end,:,:) = diff(data.positions, 1, 1) / dt;
            data.accelerations(2:end,:,:) = diff(data.velocities, 1, 1) / dt;
            
            % Add measurement noise
            data.positions = data.positions + randn(size(data.positions)) * 0.1;
        end
        
        function data = computeDerivedMetrics(~, data)
            % Compute additional metrics
            nTimeSteps = size(data.positions, 1);
            
            % Team centroid
            data.team_centroid = squeeze(mean(data.positions, 2));
            
            % Team spread
            data.team_spread = zeros(nTimeSteps, 1);
            for t = 1:nTimeSteps
                pos = squeeze(data.positions(t,:,:));
                data.team_spread(t) = sqrt(sum(var(pos)));
            end
            
            % Inter-player distances
            nPlayers = size(data.positions, 2);
            data.distance_matrices = zeros(nTimeSteps, nPlayers, nPlayers);
            for t = 1:nTimeSteps
                pos = squeeze(data.positions(t,:,:));
                for i = 1:nPlayers
                    for j = 1:nPlayers
                        data.distance_matrices(t,i,j) = norm(pos(i,:) - pos(j,:));
                    end
                end
            end
        end
    end
end

