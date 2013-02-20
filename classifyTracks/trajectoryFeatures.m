function [features,featureNames] = trajectoryFeatures(positions)


    manyFeatures = 9;
    % features: something, straightness, bending, efficiency,
    % asymmetry, point position skewness, point position kurtosis,
    % means square displacement, confinement
    % probability
    featureNames = {'','straigtness','bending','efficiency', ...
                    'asymmetry','skewness','kurtosis','msd', ...
                    'confinement'};

    % arbitrary minimum and maximum trajectory window length
    wMin = 5;
    wMax = 20;

    % length of the whole track 
    trackLength = length(positions);
    
    % store steps (directional vectors) and angles between steps
    steps = getSteps(positions,trackLength);
    angles = getAngle(positions,trackLength);
    % calculate MSD
    msd = getMSD(positions,trackLength);
    % calculate diffusion coefficient as slope of first few points
    % of MSD
    diffCoeff = polyfit([1:10],msd(1:10),1);
    diffCoeff = diffCoeff(1);
    
    % feats is the matrix that will store all the features for each
    % data point in the cell track
    feats = zeros(trackLength,manyFeatures);
    % keeps track of how many times each data point has been summed
    % over
    manyTimes = zeros(trackLength,1);

    % iterates over every starting point
    for i = 1:(trackLength-wMax)
        % iterates from the minnimum to the maximum window length
        for j = wMin:wMax
            %feats(i,1) = feats(i,1) + getSomething(positions(i:i+j,:));
            feats(i:i+j,2) = feats(i:i+j,2) + getStraight(angles(i:i+j-2,:),j);
            feats(i:i+j,3) = feats(i:i+j,3) + getBend(angles(i:i+j-2,:),j);
            feats(i:i+j,4) = feats(i:i+j,4) + ...
                getEff(positions(i:i+j,:),steps(i:i+j-1,:),j);
            
            % the next three lines are required to obtain the
            % asymmetry feature
            gyrationTensor = getGyrationTensor(positions(i:i+j,:));
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
            %feats(i:i+j,8) = feats(i:i+j,8) + getConf(positions(i:i+j,:),j,diffCoeff);
            manyTimes(i:i+j) = manyTimes(i:i+j) + 1;
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

    global epsilon
    epsilon = 0.00001;

end



%{
-------------------------------------------------------------------
Features
-------------------------------------------------------------------
%}

% Helmuth et al.
function straightness = getStraight(windowAngles,windowLength)
    cosb = 0;
    for i = 1:windowLength-2
        cosb = cosb + cos(windowAngles(i));
    end
    straightness = (1/(windowLength-1))*cosb;
end

% Helmuth et al.
function bending = getBend(windowAngles,windowLength)
    sinb = 0;
    for i = 1:windowLength-2
        sinb = sinb + sin(windowAngles(i));
    end
    bending = (1/(windowLength-1))*sinb;
end

% Helmuth et al.
function efficiency = getEff(windowPositions,windowSteps,windowLength)
    global epsilon;
    s2 = 0;
    dispVec = windowSteps(windowLength,:)-windowSteps(1,:);
    disp = dot(dispVec,dispVec);
    for i = 1:windowLength-1
        s2 = s2 + dot(windowSteps(i,:),windowSteps(i,:));
    end
    efficiency = disp.^2/(windowLength*s2+epsilon);
    %efficiency = badFilter(efficiency);
end

% Helmuth et al.
function asymmetry = getAsymm(eig1,eig2)
    global epsilon;
    asymmetry = -log(1-((eig1-eig2).^2/(2*(eig1+eig2).^2+epsilon)));
    %asymmetry = badFilter(asymmetry);
end

% Helmuth et al.
function skewness = getSkew(projection,projMean,trackLength)
    global epsilon;
    num = 0;
    denom = 0;
    for i = 1:trackLength
        num = num + (projection(i)-projMean).^3;
        denom = denom + (projection(i)-projMean).^2;
    end
    denom = denom.^(3/2)+epsilon;
    skewness = (trackLength+1)^.5*(num/denom);
    %skewness = badFilter(skewness);
end

% Helmuth et al.
function kurtosis =  getKurt(projection,projMean,windowLength)
    global epsilon;
    num = 0;
    denom = 0;
    for i = 1:windowLength
        num = num + (projection(i)-projMean).^4;
        denom = denom + (projection(i)-projMean).^2;
    end
    denom = denom.^2+epsilon;
    kurtosis = (windowLength+1).^2*(num/denom);
    %kurtosis = badFilter(kurtosis);
end

function confinement = getConf(windowPositions,windowLength,diffusionCoefficient)
    global epsilon;
    xPos = windowPositions(:,1);
    yPos = windowPositions(:,2);

    R = 0;
    for i = 2:windowLength
        d = (xPos(i)-xPos(1)).^2 + (yPos(i)-yPos(1)).^2;
        if (d > R)
            R = d;
        end
    end

    logPsi = 0.2048-2.5117*diffusionCoefficient*windowLength/(R+epsilon);
    L = -logPsi - 1;

    %    if (exp(lPsi) <= .1)
    %    L = -lPsi - 1;
    %elseif (exp(lPsi) > .1)
    %    L = 0;
    %end
    confinement = L;
end

function [msd] = getMSD(positions,trackLength)
    trackLength = trackLength - 1;
    maxdt = floor(trackLength/4);    
    msd = zeros(1,maxdt);
    xPos = positions(:,1);
    yPos = positions(:,2);
    for j = 1:maxdt
        for i = 1:maxdt
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
    %for i = 1:trackLength-2
    %    v1 = steps(i,:);
    %    v2 = steps(i+1,:);
    %    angles(i,:) = acos(dot(v1,v2)/(norm(v1)*norm(v2)));
    %end
    polar = zeros(size(steps));
    for i = 1:trackLength
        polar(i,1) = norm(steps(i,:));
        polar(i,2) = atan(steps(i,1)/steps(i,2));
        if (steps(i,1) >= 0)
            if (steps(i,2) >= 0)
                polar(i,2) = polar(i,2);
            elseif (steps(i,2) < 0)
                polar(i,2) = polar(i,2) + 2*pi;
            end
        elseif (steps(i,1) < 0)
            if (steps(i,2) >= 0)
                polar(i,2) = polar(i,2) + pi;
            elseif (steps(i,2) < 0)
                polar(i,2) = polar(i,2) + pi;
            end
        end
    end

    for i = 1:trackLength-2    
        angles(i,:) = polar(i+1,2)-polar(i,2);
    end
end

function [gyrationTensor] = getGyrationTensor(windowPositions)
    gyrationTensor = zeros(2,2);
    gyrationTensor(1,1) = mean(windowPositions(:,1).^2) - ...
        mean(windowPositions(:,1)).^2;
    gyrationTensor(1,2) = mean(windowPositions(:,1).*windowPositions(:,2)) - ...
        (mean(windowPositions(:,1))*mean(windowPositions(:,2)));
    gyrationTensor(2,1) = gyrationTensor(1,2);
    gyrationTensor(2,2) = mean(windowPositions(:,2).^2) - ...
        mean(windowPositions(:,2)).^2;
end

function [xProj] = getProjection(windowPositions,domEig,windowLength)
    xProj = zeros(windowLength,1);
    for i = 1:windowLength
        xProj(i) = dot([windowPositions(i,:)],domEig);
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