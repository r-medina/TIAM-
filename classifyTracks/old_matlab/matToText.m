function matToText()
% This function converts data for TIAM tool and TIAM+ track label
% GUI to text files to be loaded by python

    data = load(fullfile('..','data','020512_hCD8','nveMemDonA_020512_v2_results.mat'));
    % put path to TIAM mat files here
    
    data = data.datacell;
    % when saving .mat files, the data becomes burried one level in
    
    labelFileNames = dir(fullfile('..','labelTracks','classMats','batch*'));
    % use  globbing to catch all the files with track labels
    
    labels = cell(length(labelFileNames),1);
    % set up a cell array to save label data

    for i = 1:length(labelFileNames)
        labels{i} = load(fullfile('..','labelTracks','classMats',labelFileNames(i).name));
        % labelFileName(i).name is the actual name of the file with
        % the labels. You still need to include the path beforehand
        labels{i} = labels{i}.outMat;
    end

    howMany = length(data);
    % how many cells in total
    manyLabeled = 50;
    % manually include the number of tracks labeled
    labelCell = cell(manyLabeled,1);
    % a cell array that holds the labels

    [dataFolder,labelFolder] = makeFolders()

    for i = 1:manyLabeled
        for j = 1:2
            if (~isempty(labels{j}(i)) & isempty(labelCell{i}))
                labelCell{i} = labels{j}(i);
                labelCell{i} =  labelCell{i}{1};
            end
        end
        pos = data{i}(:,3:5);

        trackName = strcat(dataFolder,'/',sprintf('%03d',i),'.csv');
        labelName = strcat(labelFolder,'/',sprintf('%03d',i),'.csv');

        csvwrite(trackName,pos);
        csvwrite(labelName,labelCell{i});
    end

end

function [dataFolder, labelFolder] = makeFolders()

    function chmkdir(name)
       if (~exist(name))
        mkdir(name);
       end
    end 

    chmkdir('../data/txtData/');

    folder = strcat('../data/txtData/','nveMemDonA/');
    % input name of folder where you want to save the data and labels
    
    chmkdir(folder);
    
    dataFolder = strcat(folder,'data');
    labelFolder = strcat(folder,'labels');

    chmkdir(dataFolder);
    chmkdir(labelFolder);

end
