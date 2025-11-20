clear; format short g;

% So the rolling average that your program creates. I then (with my crude code)
% calculate per minute columns (AH- AP in the Roll_file tab) and combine the
% contextual data from another file (I haven't go my mac with me that file is on there)

% Ideally want the crude (exponential type) graphs in the comparison tab but
% with individual circles/symbols for the individual data points colour coded
% by position group (defender, midfielder, attacker). With a filter to change
% the Threshold (TH_0, TH_1 etc) but it wont also need to be filtered by the
% variables in columns AH-AP) if that is even possible? Otherwise we would need 9 graphs?


%% load data

T = importfile_DataViz("/Users/iMacPro/Library/CloudStorage/OneDrive-SwanseaUniversity/Research/WIPS/FAW/FAW WCS Womens.xlsx", "Roll_file", [2, Inf]);

GE_id = T.Name == 'Gemma Evans';
GE = T(GE_id,:);
%%
Epoch = (1:10)';
% DpM_wcs = reshape(T.Distance_TH_0,10,[])'./Epoch;

uPG = unique(T.PositionalGroup);
uPG = uPG([1,3,2]);
uPL = unique(T.Name);
%uPL = uPG([1,3,2]);

DpM_mn = zeros(10,3);
DpM_sd = zeros(10,3);
DpM_se = zeros(10,3);

for ii = 1:10
    
    for jj = 1:3



    epoch = 60*ii;
    id = and(T.Epoch == epoch,T.PositionalGroup == uPG(jj));


    S = T(id,:);

    DpM = S.Distance_TH_0/ii;
    DpM = DpM(DpM>0);
    DpM_mn(ii,jj) = mean(DpM,'omitmissing');
    DpM_sd(ii,jj) = std(DpM,'omitmissing');
    DpM_se(ii,jj) = DpM_sd(ii,jj)/sqrt(20);
    %DpM_se(ii,jj) = DpM_sd(ii,jj)/sqrt(numel(DpM));
    end
end
%%
figure(11);%plot(Epoch,DpM_mn,'o-','LineWidth',1.5)
errorbar(Epoch,DpM_mn,DpM_se,DpM_se,'vertical','LineWidth',1.5,'Marker','o')
grid on
xlabel('Epoch (min)',"FontSize",16);
ylabel('Dependent Variable',"FontSize",16)
legend(uPG,'box','off',"FontSize",16)
set(gca,"FontSize",14)

%%
fitP = zeros(3,3);

for jj = 1:3
    y = DpM_mn(:,jj);
    f1 = fit(Epoch,y,'a*exp(b*x)+c',"StartPoint",[0.5,0.5,0.5],"Lower",[0,-10,0],"Upper",[1000,10,1000]);
    figure(jj);errorbar(Epoch,DpM_mn(:,jj),DpM_se(:,jj),DpM_se(:,jj),'vertical','LineWidth',1.5,'Marker','o');hold on
    figure(jj);plot(f1,Epoch,y);hold off
    
    fitP(jj,:) = [f1.a,f1.b,f1.c];
end
%%

xx = reshape(GE.Epoch,10,[])'./60;
yy = reshape(GE.Distance_TH_0,10,[])'./Epoch';

xx = xx(1:70,:);yy = yy(1:70,:);
xx = xx(:);yy = yy(:);

figure(11);
plot(Epoch,DpM_mn,'o-','LineWidth',1.5)
% p = scatter(xx(:),yy(:),'filled');
% % 
% % distfromzero = sqrt((yy-100).^2);
% % %p.AlphaData = distfromzero(:);
% %p.AlphaData = ones(size(xx))*0.01;
% p.MarkerFaceAlpha = 0.2;
% hold on
x = linspace(1,10,1e3)';
y = fitP(:,1)'.*exp(fitP(:,2)'.*x) + fitP(:,3)';
errorbar(Epoch,DpM_mn,DpM_se,DpM_se,'vertical','Marker','o','LineWidth',1.5,'LineStyle','none');
hold on
ax = gca; ax.ColorOrderIndex = 1;
plot(x,y,'--','LineWidth',1.0);hold off
grid on
xlabel('Epoch (min)',"FontSize",16);
ylabel('Dependent Variable',"FontSize",16)
hold on

p = scatter(xx(:),yy(:),'filled');
% 
% distfromzero = sqrt((yy-100).^2);
% %p.AlphaData = distfromzero(:);
%p.AlphaData = ones(size(xx))*0.01;
p.MarkerFaceAlpha = 0.2;
hold off




%s = text("%s a*e^{bt}+c$",uPG(1));
set(gca,"FontSize",16)
legend('',uPG,'box','off',"FontSize",20,"Interpreter","latex")
text(5,137,"$-- a\times e^{bt}+c$","FontSize",18,"Interpreter","latex")
ylim([90 150])
%%
x = linspace(0,10,1e3)';
y = fitP(:,1)'.*exp(fitP(:,2)'.*x) + fitP(:,3)';

Y = log((y - fitP(:,3)')./fitP(:,1)');
X = x.*fitP(:,2)';

figure(12);
plot(X,'-','LineWidth',1.0)
hold off
grid on


% %%
% figure(12);
% plot(x,y(1,:) + abs(cumsum(gradient(y')')),'--','LineWidth',1.0);
% 
% %% 
% figure(10);
% p = waterfall(DpM_mn');view(27,33),p.EdgeColor = 'b';%p.EdgeAlpha = "interp";p.FaceAlpha = "interp";



