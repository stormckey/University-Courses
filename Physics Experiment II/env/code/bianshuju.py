import numpy as np
import random
from pylab import meshgrid,  arange
import scipy.io as scio

X,Y,Z,Theta=meshgrid(arange(-0.5,0.5,0.04), arange(-0.5,0.5,0.04), arange(0.05,0.5,0.04),arange(0,2*np.pi,np.pi/20))
R=0.05
I=10000
mu0=4*np.pi*1e-7
C0=mu0/(4*np.pi) * I
Bx = np.zeros((25,25,12))
By = np.zeros((25,25,12))
Bz = np.zeros((25,25,12))
for l in range(-200,201):
    l /= 1000
    r=np.sqrt((l-X)**2+(Y-R*np.cos(Theta))**2+(Z-R*np.sin(Theta))**2)
    dBx=-C0*R*(R-Y*np.cos(Theta)-Z*np.sin(Theta))/(r**3)
    dBy=C0*(l-X)*R*np.cos(Theta)/(r**3)
    dBz=C0*(l-X)*R*np.sin(Theta)/(r**3)
    Bx+=np.trapz(dBx,axis=3)
    By+=np.trapz(dBy,axis=3)
    Bz+=np.trapz(dBz,axis=3)

X,Y,Z=meshgrid(arange(-0.5,0.5,0.04), arange(-0.5,0.5,0.04),arange(0.05,0.5,0.04))
Bx = Bx.flatten()
for x in range(Bx.shape[0]):
    Bx[x] += random.uniform(0,0.12)
Bx = Bx.reshape(25,25,12)
By = By.flatten()
for x in range(By.shape[0]):
    By[x]+=random.uniform(0,0.12)
By = By.reshape(25,25,12)
Bz = Bz.flatten()
for x in range(Bz.shape[0]):
    Bz[x] += random.uniform(0,0.12)
Bz = Bz.reshape(25,25,12)
scio.savemat('Bx.mat', {'data':Bx})
scio.savemat('By.mat', {'data':By})
scio.savemat('Bz.mat', {'data':Bz})
scio.savemat('X.mat', {'data':X})
scio.savemat('Y.mat', {'data':Y})
scio.savemat('Z.mat', {'data':Z})
Bx = Bx.flatten()
By = By.flatten()
Bz = Bz.flatten()
np.savetxt("BX.txt",Bx)
np.savetxt("BY.txt",By)
np.savetxt("BZ.txt",Bz)

