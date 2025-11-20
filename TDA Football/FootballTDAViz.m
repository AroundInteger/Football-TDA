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




% classdef FootballTDAViz
%     properties
%         positions % Player positions at each time point
%         timeSteps % Number of time steps
%         nPlayers  % Number of players
%     end
% 
%     methods
%         function obj = FootballTDAViz(positions)
%             obj.positions = positions;
%             [obj.timeSteps, obj.nPlayers, ~] = size(positions);
%         end
% 
%         function visualizeFormationEvolution(obj, timePoints)
%             % Create a figure showing formation evolution with topological features
%             figure('Position', [100 100 1200 800]);
% 
%             for t = 1:length(timePoints)
%                 subplot(2, length(timePoints), t);
%                 obj.plotFormation(timePoints(t));
%                 title(['Formation at t=', num2str(timePoints(t))]);
% 
%                 subplot(2, length(timePoints), t + length(timePoints));
%                 obj.plotPersistenceDiagram(timePoints(t));
%                 title(['Persistence Diagram t=', num2str(timePoints(t))]);
%             end
%             sgtitle('Formation Evolution and Topological Features');
%         end
% 
%         function plotFormation(obj, t)
%             % Plot player positions and connections
%             pos = squeeze(obj.positions(t, :, :));
% 
%             % Plot players
%             scatter(pos(:,1), pos(:,2), 100, 'b', 'filled');
%             hold on;
% 
%             % Plot connections (edges) between players within threshold
%             threshold = 15; % Adjust based on field dimensions
%             for i = 1:obj.nPlayers
%                 for j = i+1:obj.nPlayers
%                     dist = norm(pos(i,:) - pos(j,:));
%                     if dist < threshold
%                         plot([pos(i,1) pos(j,1)], [pos(i,2) pos(j,2)], ...
%                              '-', 'Color',[0,0,0,0.3]);
%                     end
%                 end
%             end
% 
%             % Add tactical units visualization (assuming 4-4-2 formation)
%             obj.highlightTacticalUnits(pos);
% 
%             grid on;
%             axis equal;
%             xlim([0 100]); ylim([0 70]); % Adjust based on field dimensions
%         end
% 
%         function highlightTacticalUnits(~, pos)
%             % Highlight defensive, midfield, and attacking units
%             % Assuming first 4 players are defenders, next 4 midfield, last 2 attackers
%             colors = {'r', 'g', 'b'};
%             unit_sizes = [4, 4, 2]; % 4-4-2 formation
%             start_idx = 1;
% 
%             for u = 1:length(unit_sizes)
%                 unit_pos = pos(start_idx:start_idx+unit_sizes(u)-1, :);
%                 if size(unit_pos, 1) > 2
%                     k = convhull(unit_pos(:,1), unit_pos(:,2));
%                     fill(unit_pos(k,1), unit_pos(k,2), colors{u}, ...
%                          'FaceAlpha', 0.1, 'EdgeColor', colors{u});
%                 end
%                 start_idx = start_idx + unit_sizes(u);
%             end
%         end
% 
%         function plotPersistenceDiagram(obj, t)
%             % Compute and plot persistence diagram
%             pos = squeeze(obj.positions(t, :, :));
%             D = obj.computeDistanceMatrix(pos);
% 
%             % Compute persistence diagram (simplified version)
%             % In practice, use a proper persistence homology library
%             [birth, death] = obj.simplifiedPersistence(D);
% 
%             % Plot persistence diagram
%             scatter(birth, death, 50, 'b', 'filled');
%             hold on;
% 
%             % Add diagonal line
%             max_val = max(max(birth), max(death));
%             plot([0 max_val], [0 max_val], 'k--');
% 
%             xlabel('Birth');
%             ylabel('Death');
%             grid on;
%         end
% 
%         function D = computeDistanceMatrix(~, pos)
%             % Compute pairwise distances between players
%             n = size(pos, 1);
%             D = zeros(n);
%             for i = 1:n
%                 for j = i+1:n
%                     D(i,j) = norm(pos(i,:) - pos(j,:));
%                     D(j,i) = D(i,j);
%                 end
%             end
%         end
% 
%         function visualizeTeamShape(obj, t)
%             % Visualize team shape with multiple metrics
%             figure('Position', [100 100 1200 400]);
% 
%             % Formation plot
%             subplot(1,3,1);
%             obj.plotFormation(t);
%             title('Team Formation');
% 
%             % Centroid and spread
%             subplot(1,3,2);
%             pos = squeeze(obj.positions(t, :, :));
%             centroid = mean(pos);
%             scatter(pos(:,1), pos(:,2), 100, 'b', 'filled');
%             hold on;
%             scatter(centroid(1), centroid(2), 200, 'r', 'filled', 'diamond');
% 
%             % Plot standard deviation ellipse
%             [eigvec, eigval] = eig(cov(pos));
%             theta = linspace(0, 2*pi, 100)';
%             ellipse = [cos(theta), sin(theta)] * sqrt(eigval) * eigvec';
%             plot(ellipse(:,1) + centroid(1), ellipse(:,2) + centroid(2), 'r--');
% 
%             title('Team Centroid and Spread');
%             axis equal;
%             grid on;
% 
%             % Distance matrix heatmap
%             subplot(1,3,3);
%             D = obj.computeDistanceMatrix(pos);
%             imagesc(D);
%             colorbar;
%             title('Inter-player Distances');
%             xlabel('Player');
%             ylabel('Player');
%         end
% 
%         function [birth, death] = simplifiedPersistence(~, D)
%             % Simplified persistence computation for visualization
%             % In practice, use a proper persistence homology library
%             n = size(D,1);
%             birth = zeros(n-1,1);
%             death = zeros(n-1,1);
% 
%             % Simple clustering-based approach for visualization
%             for i = 1:n-1
%                 [min_val, ~] = min(D(i,i+1:end));
%                 birth(i) = min_val;
%                 death(i) = max(min_val * 1.5, min_val + 5);
%             end
%         end
% 
%         function animateFormation(obj, startTime, endTime, frameDelay)
%             % Animate formation evolution over time
%             figure('Position', [100 100 800 600]);
% 
%             for t = startTime:endTime
%                 clf;
%                 obj.plotFormation(t);
%                 title(['Team Formation at t=', num2str(t)]);
%                 drawnow;
%                 pause(frameDelay);
%             end
%         end
%     end
% end
% 
