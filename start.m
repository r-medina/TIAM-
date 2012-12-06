function start
% This function was the first function I wrote while starting
% this. The only useful bit is the thing about plotting--it plots
% the image under things.

s = load(['~/other/TC-MAT/data/020512_hCD8/' ...
          'nveMemDonA_020512_v2_results.mat']);

c1 = 11;
c2 = 41;

x1 = s.datacell{c1}(1:100,3);
y1 = s.datacell{c1}(1:100,4);

x2 = s.datacell{c2}(1:100,3);
y2 = s.datacell{c2}(1:100,4);

start1pos = [x1(1), y1(1)]
start2pos = [x2(1), y2(1)]

frames1 = s.datacell{c1}(1,1:2)
frames2 = s.datacell{c2}(1,1:2)

%x23 = x23 - (min(x23) - min(x23));
%y23 = y23 - (min(y23) - min(y23));

frame1 = imread('f1.jpg');
frame1 = imresize(frame1, [225 225]);

figure;
imagesc(frame1);
hold on;
axis([0 225 0 225])
axis square;
plot(x1,y1,'b')
plot(x2,y2,'r')

msd1 = MSD(x1,y1)
msd2 = MSD(x2,y2)

end