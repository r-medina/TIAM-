% This function outputs a 10 column array with all the features and
% indices of the cells. See "featStrings"
% Input needs to be the output matlab cell array from the TC-Mat tool
% and the csv formatted to have no text. The last parameter is should
% be either 1 or 2 and denotes how many types of cells there are in
% the datacell and csv
function features = trajectoryFeatures(outMat,outCSV,manyTypes)

%{
class(outMat)
class(outMat{1})
size(outMat{1})
features = 0;
return;
%}

trackCount1 = length(outMat);%(outMat.datacell);
trackCount2 = length(outCSV);%(outCSV);

if (trackCount1 ~= trackCount2)
    %outMat = outMat.datacell(1,1:trackCount2);
    outMat = outMat(1,1:trackCount2);
    trackCount = trackCount2;
end

% Track type has to be either 0 and 1 or 1 and 2
if (any(outCSV(:,2) == 2) & (manyTypes == 2))
    outCSV(:,2) = outCSV(:,2) - 1;
end

numFeatures = 10;

featStrings = {'index' 'net displacement' 'straightness' 'bending' ...
               'efficiency' 'assymetry' 'point position skewness' ...
               'point position kurtosis' 'mean square displacement' ...
               'type'};

featCell = cell(trackCount,numFeatures);

for i = 1:trackCount
    % Track length is length of the number of positions for cell
    t_len = length(outMat{i}(:,3));
    % x coordinates are the third column
    x_p  = outMat{i}(:,3);
    % y coordinates are the fourth column
    y_p  = outMat{i}(:,4);
    % x and y vectors
    x_s = getSteps(x_p,t_len);
    y_s = getSteps(y_p,t_len);
    % index
    featCell{i,1} = outCSV(i,1);
    % net displacement
    featCell{i,2} = getNetDisp(x_p,y_p,t_len);
    % straightness
    featCell{i,3} = getStraight(x_s,y_s,t_len);
    % bending
    featCell{i,4} = getBend(x_s,y_s,t_len);
    % efficiency
    featCell{i,5} = getEff(x_p,y_p,x_s,y_s,featCell{i,2},t_len);
    % gyration tensor and eigenvalues for following features
    gy_ten = getGyrationTensor(x_p,y_p,t_len);
    [eig_vec,eig_vals] = eig(gy_ten);
    eig_vals = [eig_vals(1,1),eig_vals(2,2)]';
    [dom_val,where] = max(eig_vals);
    dom_vec = eig_vec(where,:);
    pos_proj = getProjection(x_p,y_p,dom_vec,t_len);
    pos_proj_mean = mean(pos_proj);
    % assymetry
    featCell{i,6} = getAsymm(eig_vals(1),eig_vals(2));
    % skewness
    featCell{i,7} = getSkew(pos_proj,pos_proj_mean,t_len);
    % kurtosis
    featCell{i,8} = getSkew(pos_proj,pos_proj_mean,t_len);;
    % msd
    featCell{i,9} = getMSD(x_p,y_p,t_len);
    % type
    featCell{i,10} = outCSV(i,2);
end

outMat = cell2mat(featCell);
outMat = sortrows(outMat,10);

features = outMat;

for i = 1:length(outMat)
    if outMat(i,1) == 1
        whenchange = i;
        break
    end
end
% type 0 cells
out0 = outMat(1:whenchange-1,:);
index0 = out0(:,1);
% type 1 cells
out1 = outMat(whenchange:end,:);
index1 = out1(:,1);

SVMStruct = svmtrain(outMat(:,2:9),outMat(:,10));
Group = svmclassify(SVMStruct,outMat(:,2:9));

test(in_or_out(Group),in_or_out(outMat(:,10)))


% The combinations of the feature space that might reveal some
% structure in this space
representations = nchoosek(2:9,3);

%{
for i = 1:4
    space = representations(i,:);
    figure;
    scatter3([out0(:,space(1));out1(:,space(1))], ...
             [out0(:,space(2));out1(:,space(2))], ...
             [out0(:,space(3));out1(:,space(3))],45, ...
             [out0(:,10);out1(:,10)],'filled');
    xlabel(featStrings(space(1)));
    ylabel(featStrings(space(2)));
    zlabel(featStrings(space(3)));
end
%}

end



function [steps] = getSteps(pos,trackLength)
    steps = zeros(trackLength-1,1);
    for i = 1:trackLength-1
        steps(i) = pos(i+1)-pos(i);
    end
end


function [angle] = getAngle(v1,v2);
    angle = acos(dot(v1,v2)/(norm(v1)*norm(v2)));
    %if isnan(angle)
    %    angle = 0;
    %end
end


function [gyTen] = getGyrationTensor(xPos,yPos,trackLength)
    gyTen = zeros(2,2);
    gyTen(1,1) = mean(xPos.^2) - mean(xPos).^2;
    gyTen(1,2) = mean(xPos.*yPos) - (mean(xPos)*mean(yPos));
    gyTen(2,1) = gyTen(1,2);
    gyTen(2,2) = mean(yPos.^2) - mean(yPos).^2;
end


function [xProj] = getProjection(xPos,yPos,domEig,trackLength)
    xProj = zeros(trackLength,1);
    for i = 1:trackLength
        xProj(i) = dot([xPos(i),yPos(i)],domEig);
    end
end


function [netDisp] = getNetDisp(xPos,yPos,trackLength)
    netDisp = norm([xPos(trackLength)-xPos(1), ...
                    yPos(trackLength)-yPos(1)]);
end

function [straight]= getStraight(xs,ys,trackLength)
    cosb = 0;
    for i = 1:trackLength-2
        angle = getAngle([xs(i+1),ys(i+1)],[xs(i),ys(i)]);
        j = 1;
        while (isnan(angle) | ~(isreal(angle)))
            if i > j
                angle = getAngle([xs(i+1),ys(i+1)],[xs(i-j),ys(i-j)]);
                j = j + 1;
            else
                angle = 0;
            end
        end
        cosb = cosb + cos(angle);
    end
    straight = (1/(trackLength-1))*cosb;
end


function [bend] = getBend(xs,ys,trackLength)
    sinb = 0;
    for i = 1:trackLength-2
        angle = getAngle([xs(i+1),ys(i+1)],[xs(i),ys(i)]);
        j = 1;
        while (isnan(angle) | ~(isreal(angle)))
            if i > j
                angle = getAngle([xs(i+1),ys(i+1)],[xs(i-j),ys(i-j)]);
                j = j + 1;
            else
                angle = 0;
            end
        end
        sinb = sinb + sin(angle);
    end
    bend = 1/(trackLength-1)*sinb;
end


function [efficiency] = getEff(xPos,yPos,xs,ys,disp,trackLength)
    s2 = 0;
    for i = 1:trackLength-1
        s2 = s2 + dot([xs(i),ys(i)],[xs(i),ys(i)]);
    end
    efficiency = disp.^2/(trackLength*s2);
end


function [asymm] = getAsymm(eig1,eig2)
    asymm = -log(1-((eig1-eig2).^2/(2*(eig1+eig2).^2)));
end


function [skewness] = getSkew(projection,projMean,trackLength)
    num = 0;
    denom = 0;
    for i = 1:trackLength
        num = num + (projection(i)-projMean).^3;
        denom = denom + (projection(i)-projMean).^2;
    end
    denom = denom.^(3/2);
    skewness = (trackLength+1)^.5*(num/denom);
end


function [kurtosis] =  getKurt(projection,projMean,trackLength)
    num = 0;
    denom = 0;
    for i = 1:trackLength
        num = num + (projection(i)-projMean).^4;
        denom = denom + (projection(i)-projMean).^2;
    end
    denom = denom.^2;
    skewness = (trackLength+1).^2*(num/denom);
end

function [msd] = getMSD(xPos,yPos,trackLength)
    trackLength = trackLength - 1;
    maxdt = floor(trackLength/4);    
    msd = zeros(1,maxdt);
    for j = 1:maxdt
        for i = 1:maxdt
            dx = xPos(i+j) - xPos(i);
            dy = yPos(i+j) - yPos(i);
            disp = norm([dx,dy]).^2;
            msd(j) = msd(j) + disp;
        end
        msd(j) = msd(j)/maxdt;
    end
    % temporary output so that it is one number
    msd = msd(j);
end

% Makes confusion matrix:
% [true positives, false positives; false negatives, true negatives].
function conf_matrix = test(inout_predic,y)
  conf_matrix = zeros(2);

  ins = y==1;
  outs = y==-1;
  ins_predic = inout_predic==1;
  outs_predic = inout_predic==-1;

  true_ins = sum(ins);
  true_outs = sum(outs);
  predic_ins = sum(ins_predic);
  predic_outs = sum(outs_predic);
  true_pos = sum((ins==1)&(ins_predic==1));
  false_pos = sum((ins==0)&(ins_predic==1));
  true_neg = sum((outs==1)&(outs_predic==1));
  false_neg = sum((outs==0)&(outs_predic==1));

  conf_matrix(1,:) = [true_pos,false_pos];
  conf_matrix(2,:) = [false_neg,true_neg];
end

% Says whether a probability is in or out.
function in_out = in_or_out(prob)
  in_out = prob > .5;
  in_out = (in_out == 0)*-1 + in_out;
end
