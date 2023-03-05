Bx =load("/Users/chenhaogao/cidian/code/Bx.mat").data;
By =load("/Users/chenhaogao/cidian/code/By.mat").data;
Bz =load("/Users/chenhaogao/cidian/code/Bz.mat").data;
[X,Y,Z] = meshgrid(-0.5:0.04:0.49,-0.5:0.04:0.49,0.05:0.04:0.5)
[startX,startY,startZ] = meshgrid(-0.5:0.15:0.5,-0.5:0.15:0.5,-0.5:0.15:0.5);
verts = stream3(X,Y,Z,Bx,By,Bz,startX,startY,startZ);
streamline(verts);
view(3)
hold on
quiver3(X,Y,Z,Bx,By,Bz);






% Bx = load('Ix.txt');
% By = load('Iy.txt');
% Bz = load('Iz.txt');
% Bx = reshape(Bx,25*25*12,1)
% By = reshape(By,25*25*12,1)
% Bz = reshape(Bz,25*25*12,1)
% Bx = Bx.*134*2e-3 + pi/4
% By = By.*134*2e-3 + pi/4
% Bz = Bz.*134*2e-3 + pi/4
% Bx = cos(Bx).^2
% By = cos(By).^2
% Bz = cos(Bz).^2
% Ix0 = 5112, Iy0 = 6890,Iz0 = 1960,V=134,L=2e-3
% Bx = Bx.*Ix0
% By = By.*Iy0
% Bz = Bz.*Iz0
% Bx = round(Bx,7)
% By = round(By,7)
% Bz = round(Bz,7)
% writematrix(Bx,"Ix.txt")
% writematrix(By,"Iy.txt")
% writematrix(Bz,"Iz.txt")
% Bx = sqrt(Bx./Ix0)
% Bx = acos(Bx)
% Bx = Bx - pi/4
% Bx = Bx./(V*L)
% By = sqrt(By./Ix0)
% By = acos(By)
% By = By - pi/4
% By = By./(V*L)
% Bz = sqrt(Bz./Ix0)
% Bz = acos(Bz)
% Bz = Bz - pi/4
% Bz = Bz./(V*L)
% Bx = reshape(Bx,25,25,12)
% By = reshape(By,25,25,12)
% Bz = reshape(Bz,25,25,12)




% Bx =load("/Users/chenhaogao/cidian/code/Bx.mat").data;
% By =load("/Users/chenhaogao/cidian/code/By.mat").data;
% Bz =load("/Users/chenhaogao/cidian/code/Bz.mat").data;