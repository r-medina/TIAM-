function [msd] = MSD(x_vals,y_vals)
% Everything in this function is also in the trajectoryFeatures
% function. Just need this to run older scripts.
    
    points = length(x_vals) - 1;
    maxdt = floor(points/4);    
    msd = zeros(1,maxdt);
    
    for j = 1:maxdt
        for i = 1:maxdt
            dx = x_vals(i+j) - x_vals(i);
            dy = y_vals(i+j) - y_vals(i);
            disp = norm([dx,dy]).^2;
            msd(j) = msd(j) + disp;
        end
        msd(j) = msd(j)/maxdt;
    end
    
end