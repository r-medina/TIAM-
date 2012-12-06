function newMany(whichExp)

switch whichExp
  case 0
    outputCell = load(['~/other/TC-MAT/data/020512_hCD8/' ...
                       'nveMemDonA_020512_v2_results.mat']);
    outputCSV = csvread('~/other/TC-MAT/data/020512_hCD8/cellDataMemDonA.csv');
  case 1
    outputCell = load(['~/other/TC-MAT/data/020512_hCD8/' ...
                       'nveDonA_020512_v2_results.mat']);
    outputCSV = csvread('~/other/TC-MAT/data/020512_hCD8/cellDataDonA.csv');
end

cellCount = length(outputCell.datacell);
outMat = zeros(1,7);

%{
figure;
hold all;
axis([0 225 0 225])
axis square;
%}

allMSD = cell(1,length(outputCSV));

% For every cell that has been categorized
for i = 1:length(outputCSV)
    % Track length is length of the number of positions for cell
    trackLength = length(outputCell.datacell{i}(:,3));
    % x coordinates are the third column
    x  = outputCell.datacell{i}(1:trackLength,3);
    % y coordinates are the fourth column
    y  = outputCell.datacell{i}(1:trackLength,4);
    % index, cell type, footprint, flur c1, flur c2, arrest coeff, turn angle
    outMat = [outMat;[i outputCSV(i,2) outputCSV(i,8:12)]];
    % MSD things
    [msdTime] = MSD(x,y);
    allMSD{i} = msdTime;
    % Plots positions of all cells during video
    %plot(x,y)
end


% Removes first row because it was a place holder
outMat = outMat(2:end,:);
% Subtracts 1 from type to make random variable {0,1}
outMat(:,2) = outMat(:,2) - 1;
% Sorts by cell type
outMat = sortrows(outMat,2);
% index, cell type, footprint, flur c1, flur c2, arrest coeff, turn angle
out = outMat;

% Number of delta-t points in MSD plot; x-axis
meanLen = 40;
% y-axis
maxDisp = 250;

figure;
hold all;
axis([0 meanLen-1 0 maxDisp]);

switch whichExp
  case 0

    % For breaking up the out matrix into two matrices for the
    % different data types
    for i = 1:length(out)
        if out(i,1) == 1
            whenchange = i;
            break
        end
    end
    % Type 0 cells
    out0 = out(1:whenchange-1,:);
    index0 = out0(:,1);
    msd0 = cell(1,length(index0));
    meanMSD0 = zeros(1,meanLen);
    % Type 1 cells
    out1 = out(whenchange:end,:);
    index1 = out1(:,1);
    msd1 = cell(1,length(index1));
    meanMSD1 = zeros(1,meanLen);

    manyOverLen = 0;
    for i = 1:length(out0)
        msd0{i}(1,:) = allMSD{index0(i)}(1,:);
        %plot([0:length(msd0{i})-1],[msd0{i}(1,:)]);
        if (length(msd0{i}) > meanLen)
            plot([0:length(msd0{i})-1],[msd0{i}(1,:)]);
            for j = 1:meanLen
                meanMSD0(1,j) = meanMSD0(1,j) + msd0{i}(1,j);
            end
            manyOverLen = manyOverLen + 1;
        end
        %{
        if isnan(out0(i,5))
	    out0(i,5) = 0;
        elseif isnan(out0(i,6))
            out0(i,6) = 0;
        end
        %}
    end
    meanMSD0 = meanMSD0/manyOverLen;
    plot([0:meanLen-1],[meanMSD0],'LineWidth',5)
    figure;
    hold all;
    axis([0 meanLen-1 0 maxDisp]);

    manyOverLen = 0;
    for i = 1:length(out1)
        msd1{i}(1,:) = allMSD{index1(i)}(1,:);
        %plot([0:length(msd1{i})-1],[msd1{i}(1,:)]);
        if (length(msd1{i}) > meanLen)
            plot([0:length(msd1{i})-1],[msd1{i}(1,:)]);
            for j = 1:meanLen
                meanMSD1(1,j) = meanMSD1(1,j) + msd1{i}(1,j);
            end
            manyOverLen = manyOverLen + 1;
        end
    end
    meanMSD1 = meanMSD1/manyOverLen;
    plot([0:meanLen-1],[meanMSD1],'LineWidth',5)
    %{
    % One 3D projection
    figure;
    scatter3([out0(1:end-10,2);out1(1:end-10,2)], ...
             [out0(1:end-10,3);out1(1:end-10,3)], ...
             [out0(1:end-10,6);out1(1:end-10,6)],50, ...
             [out0(1:end-10,1);out1(1:end-10,1)],'filled')
    xlabel('MSD per cell');
    ylabel('Contact Area');
    zlabel('Arrest Cooefficient');
    %}

  case 1
    out1 = out;
    meanMSD = zeros(1,meanLen);
    manyOverLen = 0;
    for i = 1:length(allMSD)
        %plot([0:length(allMSD{i})-1],[allMSD{i}(1,:)]);
        if (length(allMSD{i}) > meanLen)
            plot([0:length(allMSD{i})-1],[allMSD{i}(1,:)]);
            for j = 1:meanLen
                meanMSD(1,j) = meanMSD(1,j) + allMSD{i}(1,j);
            end
            manyOverLen = manyOverLen + 1;
        end
    end
    meanMSD = meanMSD/manyOverLen;
    plot([0:meanLen-1],[meanMSD],'LineWidth',5)
    %{
    % testing log shit
    figure;
    for i = 1:length(allMSD)
        if (length(allMSD{i}) > meanLen)
            loglog([0:length(allMSD{i})-1],[allMSD{i}(1,:)]./[0:length(allMSD{i})-1]);
            hold all;
        end
    end
    %}
    %{
    figure;
    scatter3(out1(1:end-10,2),out1(1:end-10,3),out1(1:end-10,6), ...
             50,out1(1:end-10,1).^2,'filled')
    xlabel('MSD per cell');
    ylabel('Contact Area');
    zlabel('Turn Angle');
    %}
end


end
