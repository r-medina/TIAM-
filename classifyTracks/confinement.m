function confinement

    close all;
    
    %whichT = 8;
    %whichT = 74;
    %whichT = 63;
    %whichT = 22;
    whichT = 77;
    Sm = 10;

    tiamFile = '../data/020512_hCD8/nveMemDonA_020512_v2_results.mat';
    outMat = load(tiamFile);
    outMat = outMat.datacell;
    
    t_len = length(outMat{whichT}(:,3));
    % x coordinates are the third column
    x_p  = outMat{whichT}(:,3);
    % y coordinates are the fourth column
    y_p  = outMat{whichT}(:,4);
    msdT = getMSD(x_p,y_p,t_len);
    figure;
    hold on;
    plot([1:length(msdT)],msdT);
    diffCoeff = polyfit([1:10],msdT(1:10),1);
    diffCoeff = diffCoeff(1);

    allPsi = zeros(t_len,Sm-4+1);
    avPsi = zeros(1,t_len-Sm);
    allL = zeros(t_len,Sm-4+1);
    avL = zeros(1,t_len-Sm);


    for i = 4:Sm
        for j = 1:t_len-i
            R = 0;
            for k = 2:i
                d = (x_p(k+j)-x_p(j)).^2+(y_p(k+j)-y_p(j)).^2;
                if (d > R)
                    R = d;
                end
            end
            lPsi = 0.2048-2.5117*diffCoeff*i/R;
            allPsi(j,i) = lPsi;
            if (exp(lPsi) <= .1)
                L = -lPsi - 1;
            elseif (exp(lPsi) > .1)
                L = 0;
            end
            allL(j,i) = L;
        end
    end
    
    ep = exp(allPsi);

    for i = 1:t_len-Sm
        avPsi(i) = mean(ep(i,:));
        avL(i) = mean(allL(i,:));
    end
    
    figure;
    hold on;
    plot([1:t_len-Sm],[avPsi]);

    figure;
    hold on;
    plot([1:t_len-Sm],[avL]);


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
    
end