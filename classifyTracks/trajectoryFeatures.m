function [features,featureNames] = trajectoryFeatures(positions)

    manyFeatures = 9;
    % features: something, straightness, bending, efficiency,
    % asymmetry, point position skewness, point position kurtosis,
    % means square displacement, diffusion coefficient, confinement
    % probability
    featureNames = {'','straigtness','bending','efficiency', ...
                    'asymmetry','skewness','kurtosis','msd', ...
                    'confinement'};

    % arbitrary minimum and maximum trajectory segment length
    sMin = 5;
    sMax = 20;

    % length of the whole track 
    trackLength = length(positions);
    
    % store steps (directional vectors) and angles between steps
    steps = getSteps(positions,trackLength);
    angles = getAngle(positions,trackLength);
    
    % feats is the matrix that will store all the features for each
    % data point in the cell track
    feats = zeros(trackLength,manyFeatures);
    % keeps track of how many times each data point has been summed
    % over
    manyTimes = zeros(trackLength,1);

    % iterates over every starting point
    for i = 1:(trackLength-sMax)
        % iterates from the minnimum to the maximum segment length
        for j = sMin:sMax
            %feats(i,1) = feats(i,1) + getSomething(positions(i:i+j,:));
            feats(i:i+j,2) = feats(i:i+j,2) + getStraight(angles(i:i+j-2,:),j);
            feats(i:i+j,3) = feats(i:i+j,3) + getBend(angles(i:i+j-2,:),j);
            feats(i:i+j,4) = feats(i:i+j,4) + getEff(positions(i:i+j,:),steps(i:i+j-1,:),j);
            
            % the next three lines are required to obtain the
            % asymmetry feature
            gyrationTensor = getGyrationTensor(positions(i:i+j,:),j);
            [eig_vec,eig_vals] = eig(gyrationTensor);
            eig_vals = [eig_vals(1,1),eig_vals(2,2)]';
            
            feats(i:i+j,5) = feats(i:i+j,5) + getAsymm(eig_vals(1),eig_vals(2));

            % the next four lines are required for obtaining the
            % skewness and kurtosis
            [dom_val,where] = max(eig_vals);
            dom_vec = eig_vec(where,:);
            pos_proj = getProjection(positions(i:i+j,:),dom_vec,j);
            pos_proj_mean = mean(pos_proj);

            feats(i:i+j,6) = feats(i:i+j,6) + getSkew(pos_proj,pos_proj_mean,j);
            feats(i:i+j,7) = feats(i:i+j,7) + getKurt(pos_proj,pos_proj_mean,j);
            %feats(i:i+j,8) = feats(i:i+j,8) + getMSD(positions(i:i+j,:),j);
            %feats(i:i+j,9) = feats(i:i+j,9) + getConf(positions(i:i+j,:));
            manyTimes(i:i+j) = manyTimes(j) + 1;
        end
    end
    
    % If there's a bug, I think it's here. I'm trying to divide
    % each column of the feats matrix by how many times each of the
    % rows in that column was summed over such that those data
    % points become averages
    for i = 1:(manyFeatures)
        feats(:,i) = feats(:,i) ./ manyTimes;
    end

    features = feats;

end


%{
-------------------------------------------------------------------
Features
-------------------------------------------------------------------
%}

% Helmuth et al.
function straightness = getStraight(segAngles,segLength)
    cosb = 0;
    for i = 1:segLength-2
        cosb = cosb + cos(segAngles(i));
    end
    straightness = (1/(segLength-1))*cosb;
end

% Helmuth et al.
function bending = getBend(segAngles,segLength)
    sinb = 0;
    for i = 1:segLength-2
        sinb = sinb + sin(segAngles(i));
    end
    bending = (1/(segLength-1))*sinb;
end

% Helmuth et al.
function efficiency = getEff(segPositions,segSteps,segLength)
    s2 = 0;
    dispVec = segSteps(segLength,:)-segSteps(1,:);
    disp = dot(dispVec,dispVec);
    for i = 1:segLength-1
        s2 = s2 + dot(segSteps(i,:),segSteps(i,:));
    end
    efficiency = disp.^2/(segLength*s2);
    efficiency = badFilter(efficiency);
end

% Helmuth et al.
function asymmetry = getAsymm(eig1,eig2)
    asymmetry = -log(1-((eig1-eig2).^2/(2*(eig1+eig2).^2)));
    asymmetry = badFilter(asymmetry);
end

% Helmuth et al.
function skewness = getSkew(projection,projMean,trackLength)
    num = 0;
    denom = 0;
    for i = 1:trackLength
        num = num + (projection(i)-projMean).^3;
        denom = denom + (projection(i)-projMean).^2;
    end
    denom = denom.^(3/2);
    skewness = (trackLength+1)^.5*(num/denom);
    skewness = badFilter(skewness);
end

% Helmuth et al.
function kurtosis =  getKurt(projection,projMean,segLength)
    num = 0;
    denom = 0;
    for i = 1:segLength
        num = num + (projection(i)-projMean).^4;
        denom = denom + (projection(i)-projMean).^2;
    end
    denom = denom.^2;
    kurtosis = (segLength+1).^2*(num/denom);
    kurtosis = badFilter(kurtosis);
end

function msd = getMSD(segPositions,segLength)
    xPos = segPositions(:,1);
    yPos = segPositions(:,2);
    maxdt = floor(segLength/4);
    maxdt
    msd = zeros(1,maxdt);
    for j = 1:segLength-maxdt
        for i = 1:maxdt
            dx = xPos(i+j) - xPos(i);
            dx = xPos(i+j) - xPos(i);
            dy = yPos(i+j) - yPos(i);
            disp = norm([dx,dy]).^2;
            msd(j) = msd(j) + disp;
        end
        msd(j) = msd(j)/maxdt;
    end
end


%{
-------------------------------------------------------------------
Intermediate Functions
-------------------------------------------------------------------
%}

function [steps] = getSteps(positions,trackLength)
    steps = zeros(trackLength-1,2);
    for i = 1:trackLength-1
        steps(i,:) = positions(i+1,:)-positions(i,:);
    end
end


function [angles] = getAngle(steps,trackLength)
    angles = zeros(trackLength-2,2);
    for i = 1:trackLength-2
        v1 = steps(i,:);
        v2 = steps(i+1,:);
        angles(i,:) = acos(dot(v1,v2)/(norm(v1)*norm(v2)));
    end
end

function [gyrationTensor] = getGyrationTensor(segPositions,segLength)
    gyrationTensor = zeros(2,2);
    gyrationTensor(1,1) = mean(segPositions(:,1).^2) - ...
        mean(segPositions(:,1)).^2;
    gyrationTensor(1,2) = mean(segPositions(:,1).*segPositions(:,2)) - ...
        (mean(segPositions(:,1))*mean(segPositions(:,2)));
    gyrationTensor(2,1) = gyrationTensor(1,2);
    gyrationTensor(2,2) = mean(segPositions(:,2).^2) - ...
        mean(segPositions(:,2)).^2;
end

function [xProj] = getProjection(segPositions,domEig,segLength)
    xProj = zeros(segLength,1);
    for i = 1:segLength
        xProj(i) = dot([segPositions(i,:)],domEig);
    end
end

% gets rid of un-usable features. Happens when denominators are a
% difference that comes out to 0
function output = badFilter(input)
    if (isnan(input) | ~(isreal(input)) | isinf(input))
        output = 0;
    else
        output = input;
    end
end