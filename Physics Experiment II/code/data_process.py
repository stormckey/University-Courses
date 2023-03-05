import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import meshgrid , arange ,streamplot ,show
import scipy.io as scio

xlsx = pd.ExcelFile('~/Desktop/data.xlsx')
data = pd.read_excel(xlsx, 'Sheet1').to_numpy(dtype=np.str_)
data = np.char.replace(data, ' /1', '')#remove the label
data = np.char.replace(data, ' /2', '')
data = np.char.replace(data, ' /3', '')
data = np.char.replace(data, '\xa0', '')
data = np.char.split(data, sep='/')#split the data
Ix,Iy,Iz = np.zeros(75),np.zeros(75),np.zeros(75)#``
for i in range(len(data)):#convert the data to float store them in Ix,Iy,Iz
    for j in range(len(data[i])):
        Ix[i*5+j] = data[i][j][0]
        Iy[i*5+j] = data[i][j][1]
        Iz[i*5+j] = data[i][j][2]
x0,y0,z0= 2556,3445,980#the initial value
Ix = Ix.reshape(5,3,5)
Iy = Iy.reshape(5,3,5)
Iz = Iz.reshape(5,3,5)
#calculate the magnetic field
Ix /= 2*x0
Iy /= 2*y0
Iz /= 2*z0
Ix = np.sqrt(Ix)
Iy = np.sqrt(Iy)
Iz = np.sqrt(Iz)
anglex = np.arccos(Ix)
angley = np.arccos(Iy)
anglez = np.arccos(Iz)
anglex -= np.pi/4
angley -= np.pi/4
anglez -= np.pi/4
Bx = anglex/(134*2e-3)
By = angley/(134*2e-3)
Bz = anglez/(134*2e-3)
Bx *= 3
By *= 3
Bz *= 3
#plot the magnetic field
X,Y,Z = meshgrid(arange(-0.5,0.5,0.34),arange(-0.5,0.5,0.2),arange(-0.5,0.5,0.2))

# print(X.shape)
ax = plt.figure().add_subplot(projection='3d')
ax.quiver(X,Y,Z,Bx,By,Bz)
show()