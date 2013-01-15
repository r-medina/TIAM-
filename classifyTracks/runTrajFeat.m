a = './data/020512_hCD8/nveMemDonA_020512_v2_results.mat';
b = './data/020512_hCD8/cellDataMemDonA.csv';

c = './data/020512_hCD8/nveDonA_020512_v2_results.mat';
d = './data/020512_hCD8/cellDataDonA.csv';

outputCella = load(a);
outputCSVb = csvread(b);

outputCellc = load(c);
outputCSVd = csvread(d);

outputCSVd(:,2) = outputCSVd(:,2) + 2;

a = [outputCella.datacell,outputCellc.datacell];
b = [outputCSVb;outputCSVd];

%class(outputCella.datacell)

%a = outputCella.datacell;
%b = outputCSVb;

memDonA = trajectoryFeatures(a,b,2);
