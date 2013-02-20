function runTrajFeat()
% some of the following code is very specific to how sakellarios named his label files.
% the rest is specific to the the specific TIAM data file i am using.

    % the following lines are manual data processing to be used
    data = load(fullfile('..','data','020512_hCD8','nveMemDonA_020512_v2_results.mat'));
    data = data.datacell;
    labelFileName = dir(fullfile('..','labelTracks','classMats','batch*'));
    labels = cell(length(labelFileName),1);
    for i = 1:length(labelFileName)
        labels{i} = load(fullfile('..','labelTracks','classMats',labelFileName(i).name));
        labels{i} = labels{i}.outMat;
    end

    howMany = length(data);
    manyLabeled = 50;
    labelCell = cell(manyLabeled,1);
    featureCell = cell(manyLabeled,1);
    
    % 50 being how many tracks were labelled
    for i = 1:manyLabeled
        % specific to sakellarios's files
        for j = 1:2
            if (~isempty(labels{j}(i)) & isempty(labelCell{i}))
                labelCell{i} = labels{j}(i);
                labelCell{i} =  labelCell{i}{1};
            end
        end
        
        % load positions in to feed to function that finds features
        pos = data{i}(:,3:4);
        [featureCell{i},featNames] = trajectoryFeatures(pos);
        % filters out empty features
        featureCell{i} = featureCell{i}(:,2:8);
        % featureCell{i} = featureCell{i}(:,3:7);
        featLen = length(featureCell{i});
        %labelCell{i}(1:featLen);
        % add types as last feature;
        featureCell{i} = [featureCell{i},labelCell{i}(1:featLen)];
        
        % stops loop prematurely for run time
        if i == 7
            break;
        end
    end

    % 2nd through 7th features because those are the only ones
    % computed so far
    featNames = featNames(2:8);

    % turn the feature cell into a matrix for easy manipulation
    featureMat = cell2mat(featureCell);
    % sort the matrix on the last column (for the labels)
    featureMat = sortrows(featureMat,8);
    for i = 1:length(featureMat)
        if featureMat(i,8) == 0
            whengood = i;
            break;
        end
    end
    manyPoints = length(featureMat);
    featureMat = featureMat(whengood:manyPoints,:);
    manyPoints = length(featureMat);

    options = statset('maxiter',40000,'display','iter');

    SVMStruct = svmtrain(featureMat(:,1:7),...
                         featureMat(:,8),...
                         'method','SM','options',options);
    Group = svmclassify(SVMStruct,featureMat(:,1:7));
    [conf, sensitivity, specificity] = test(Group,featureMat(:,8))

    %{
    SVMStruct = svmtrain(featureMat(1:2:manyPoints,1:7),...
                         featureMat(1:2:manyPoints,8),...
                         'method','SM','options',options);
    Group = svmclassify(SVMStruct,featureMat(2:2:manyPoints,1:7));
    test(Group,featureMat(2:2:manyPoints,8))

    % following block is for data representation in graphs
    for i = 1:length(featureMat)
        if featureMat(i,8) == 1
            whenchange = i;
            break;
        end
    end
    % type 0 cells
    out0 = featureMat(1:whenchange-1,:);
    % type 1 cells
    out1 = featureMat(whenchange:end,:);
    representations = nchoosek(1:7,3);
    for i = 1:4
        space = representations(i,:);
        figure;
        scatter3([out0(:,space(1));out1(:,space(1))], ...
                 [out0(:,space(2));out1(:,space(2))], ...
                 [out0(:,space(3));out1(:,space(3))],30, ...
        [out0(:,8);out1(:,8)],'filled');
        xlabel(featNames(space(1)));
        ylabel(featNames(space(2)));
        zlabel(featNames(space(3)));
    end
    %}

    for i = 1:length(featureMat)
        if featureMat(i,8) == 1
            whenchange = i;
            break;
        end
    end
    
    %{
    [pc, coords, energies] = princomp(featureMat(:,1:7));
    figure;
    hold all;
    coords = coords';
    plot3(coords(1,1:whenchange-1),coords(2,1:whenchange-1),coords(3,1:whenchange-1),'.');
    plot3(coords(1,whenchange:manyPoints),...
          coords(2,whenchange:manyPoints),...
          coords(3,whenchange:manyPoints),'.');
    figure;
    plot(energies)
    %}

end

% Makes confusion matrix:
% [true positives, false positives; false negatives, true negatives].
%function conf_matrix = test(inout_predic,y)
function [conf_matrix, sens, spec] = test(group,y)
  conf_matrix = zeros(2);

  tp = 0; fn = 0; fp = 0; tn = 0;

  for i = 1:length(y)
      if y(i) == 1
          if group(i) == 1;
              tp = tp + 1;
          else
              fn = fn + 1;
          end
      else
          if group(i) == 1;
              fp = fp + 1;
          else
              tn = tn + 1;
          end
      end
  end

  conf_matrix = [tp fn; fp tn];
  sens = tp/(tp+fn);
  spec = tn/(tn+fp);

end
