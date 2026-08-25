% Example usage script
%function demoFootballTDA()
    % Generate sample data (replace with real tracking data)
    nTimeSteps = 100;
    nPlayers = 10;
    
    % Simulate 4-4-2 formation with some movement
    base_formation = [
        % Defenders
        20 15; 20 30; 20 40; 20 55;
        % Midfielders
        50 15; 50 30; 50 40; 50 55;
        % Forwards
        80 25; 80 45
    ];
    
    % Add some movement over time
    positions = zeros(nTimeSteps, nPlayers, 2);
    for t = 1:nTimeSteps
        % Add random movement + some systematic tactical shift
        movement = randn(nPlayers, 2) * 2;
        tactical_shift = sin(t/10) * [ones(nPlayers,1) zeros(nPlayers,1)];
        positions(t,:,:) = base_formation + movement + tactical_shift;
    end
    
    % Create visualization object
    viz = FootballTDAViz(positions);
    
    % Generate visualizations
    % 1. Formation evolution
    viz.visualizeFormationEvolution([1 25 50 75]);
    
    % 2. Team shape analysis
    viz.visualizeTeamShape(1);
    
    % 3. Animate formation
    viz.animateFormation(1, 50, 0.1);
%end

%%

% Example usage script
% function demoDataGeneration()
    % Create generator
    generator = FootballDataGenerator();
    
    % Generate different scenarios
    scenarios = {'defensive_press', 'attacking_buildup', 'possession'};
    formations = {'f442', 'f433', 'f352'};
    
    % Generate and visualize data for each scenario
    for i = 1:length(scenarios)
        data = generator.generateMatchData(formations{1}, scenarios{i});
        
        % Plot trajectories for a 30-second window
        timeWindow = 1:300; % 30 seconds at 10 Hz
        generator.plotTrajectories(data, timeWindow);
        sgtitle(['Scenario: ' scenarios{i}]);
        
        % Export data
        generator.exportData(data, ['match_data_' scenarios{i}]);
    end
% end
