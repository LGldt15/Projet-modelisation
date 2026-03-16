%matplotlib widget

from plotPoisson import plotPoisson
def plotPoissons(positions, angles):
    """
    Appele la fonction plotPoisson sur un ensemble de positions et d'orientations
    pour afficher un banc.
    La couleur de chaque poisson correspond à son orientation de sorte
    que des poissons qui se déplacent dans la même direction seront de la même couleur
    """
    # Création de la figure
    fig, ax = plt.subplots()
    # Liste qui contient les polygones de chaque poisson
    poissons = []
    for i in range(len(positions)):
        poissons += [plotPoisson(ax, positions[i], angles[i])]
    plt.xlim(0, L)
    plt.ylim(0, L)
    return poissons




import numpy as np
import math
import matplotlib.pyplot as plt
# Nombre de poissons
N = 100
# Largeur du carré de la boite
L = 20
# Tableau de dimension (N, 2) contenant les positions de chaque poisson
positions = np.random.uniform(0,L,(N,2))
# Orientation de chaque poisson, tableau de dimension N
angles = np.random.uniform(0,6.28,N)

#for i in range(N):
#    positions.append([random.randint(0,L),random.randint(0,L)])
#    angles.append(random.randint(0,360))

#print(positions)
#print(angles)

plotPoissons(positions,angles)

def moyenneAngle(angles):
    return np.angle(np.mean(np.exp(1j*angles)))

angles1 = np.array([np.pi/2, -np.pi/2, 0])
print("Premier test:", abs(np.mod(moyenneAngle(angles1), 2*np.pi) - 0) < 0.01) 
angles2 = np.array([np.pi, -np.pi])
print("Second test:", abs(np.mod(moyenneAngle(angles2), 2*np.pi) - np.pi) < 0.01)
angles3 = np.array([5*np.pi/2, 0])
print("Troisième test:", abs(np.mod(moyenneAngle(angles3), 2*np.pi) - np.pi/4) < 0.01)



def distancePeriodique(point1, point2, L):
    dx=point1[0]-point2[0]
    dy=point1[1]-point2[1]
    return np.sqrt((dx-L*np.round(dx/L))*(dx-L*np.round(dx/L))+(dy-L*np.round(dy/L))*(dy-L*np.round(dy/L)))

print(distancePeriodique([1,1],[51,51],50))



def update(positions, angles, L, f, R = 0.5, v = 0.4, dt = 1):
    
    N = len(positions)
    anglesSave=angles
    #  Pour chaque poisson calculer la nouvelle orientation
    # à partir de la moyenne de celle de ses voisins
    # Ajouter à ces nouvelles orientations les fluctuations aléatoires d'amplitude $f$
    # Mettre à jour les nouvelles positions à partir des nouvelles orientations
    for i in range(N):
        anglesVoisin=[]
        tailleModif=0
        for j in range(N):
            if (distancePeriodique(positions[i],positions[j],L)<R):
                anglesVoisin.append(anglesSave[j])
        angles[i]=moyenneAngle(np.array(anglesVoisin))
    angles=angles+np.random.uniform(-np.pi*f,np.pi*f,N)
    
    for i in range (N):
        positions[i,1]=positions[i,1]+math.sin(angles[i])*v*dt
        positions[i,0]=positions[i,0]+math.cos(angles[i])*v*dt
    return positions, angles


from plotPoisson import animationBanc
N = 200
L = 10
f = 0.2

# Arrête la potentielle animation déja existante
plt.close("all")

try:
    ani.event_source.stop()
except NameError:
    pass
ani, btn = animationBanc(N, L, f, update)
import time
L=20
f=0.1

temps=np.zeros((10))
NBp=np.zeros((10))

for i in range(10):
    N=(i+1)*50
    NBp[i]=N
    positions = np.random.uniform(0,L,(N,2))
    angles = np.random.uniform(0,6.28,N)
    t=time.time()
    for j in range(10):
        update(positions,angles,L,f)
    temps[i]=(time.time()-t)/50



plt.close("all")
plt.plot(NBp,temps)
plt.show()

def calcGrille(positions, L):
    grille = [[[] for i in range(L)] for j in range(L)]
    # remplir la grille des indices
    for i in range(len(positions)):
        k=positions[i]
        x=int(np.floor(k[0]))%L
        y=int(np.floor(k[1]))%L
        grille[x][y].append(i)
    #print (positions)
    #print(grille)
        
    return grille


def calcVoisins(i, positions, grille, L, R = 1):
    x=int(np.floor(positions[i,0]))%L
    y=int(np.floor(positions[i,1]))%L
    voisins=[]
    voisins=grille[x][y]
    #print (voisins)

    return voisins



def updateGrille(positions, angles, L, f, R = 1, v = 0.4, dt = 1):
    N = len(positions)
    grille = calcGrille(positions,L)
    anglesSave=angles
    for i in range(N):
        anglesMoy=[]
        voisins=calcVoisins(i,positions,grille,L,R)
        for j in range(len(voisins)):
            anglesMoy.append(anglesSave[voisins[j]])
        angles[i]=moyenneAngle(np.array(anglesMoy))
        
    angles=angles+np.random.uniform(-np.pi*f,np.pi*f,N)
    
    for i in range (N):
        positions[i,1]=positions[i,1]+math.sin(angles[i])*v*dt
        positions[i,0]=positions[i,0]+math.cos(angles[i])*v*dt
    return positions, angles


N = 1000
L = 20
f = 0.1

# Arrête la potentielle animation déja existante
plt.close("all")
try:
    ani.event_source.stop()
except NameError:
    pass
ani, btn = animationBanc(N, L, f, updateGrille)



import time
L=20
f=0.1

temps=np.zeros((10))
NBp=np.zeros((10))

for i in range(10):
    N=(i+1)*50
    NBp[i]=N
    positions = np.random.uniform(0,L,(N,2))
    angles = np.random.uniform(0,6.28,N)
    t=time.time()
    for j in range(50):
        updateGrille(positions,angles,L,f)
    temps[i]=(time.time()-t)/50


plt.close("all")
plt.plot(NBp,temps)
plt.show()


def phi(angles):
    Phi=0
    Phix=0
    Phiy=0
    for i in angles:
        Phix=Phix+np.cos(i)
        Phiy=Phiy+np.sin(i)
    Phi=np.sqrt(Phix*Phix+Phiy*Phiy)/len(angles)
    return Phi



N = 1000
L = 20
f = 0.1

# Arrête la potentielle animation déja existante
plt.close("all")

try:
    ani.event_source.stop()
except NameError:
    pass
ani, btn = animationBanc(N, L, f, updateGrille, phi)

rho = 2
L = 10
N = rho * L * L
listef = [0, 0.2, 0.4, 0.6, 0.8]
listePhi = [[],[],[],[],[]]
# pour chaque amplitude de bruit calculer phi sur environ 300 iterations et le stocker dans une liste
for f in range(len(listef)):
    positions = np.random.uniform(0,L,(N,2))
    angles = np.random.uniform(0,6.28,N)
    for i in range(300):
        positions,angles=updateGrille(positions, angles, L, listef[f])
        listePhi[f].append(phi(angles))
    
        
def saveSimulation(angles,positions,L,f):
    listePhi = []
    for i in range(100):
        positions,angles=updateGrille(positions, angles, L, f)
    for i in range(100):
        positions,angles=updateGrille(positions, angles, L, f)
        listePhi.append(phi(angles))
    np.savetxt("./data/output"+str(f),listePhi)



listef = [0, 0.2,0.3,0.4,0.45,0.5, 0.6, 0.8]
for i in listef:
    positions = np.random.uniform(0,L,(N,2))
    angles = np.random.uniform(0,6.28,N)
    saveSimulation(angles,positions,10,i)

def moyennePhi(nomFichier):
    tabPhi=np.loadtxt(nomFichier)
    return np.mean(tabPhi)


plt.close()
listef = [0, 0.2,0.3,0.4,0.45,0.5, 0.6, 0.8]
listePhi=[]
for i in listef:
    listePhi.append(moyennePhi("./data/output"+str(i)))
plt.plot(listef,listePhi)
plt.show()



listef = [0, 0.2,0.3,0.4,0.45,0.5, 0.6, 0.8]
listeN =[100,200,300,400,500,600,700,800]
listePhi=[[],[],[],[],[],[],[],[]]
for n in range(len(listeN)):
    for i in listef:
        positions = np.random.uniform(0,L,(listeN[n],2))
        angles = np.random.uniform(0,6.28,listeN[n])
        saveSimulation(angles,positions,L,i)
    for i in listef:
        listePhi[n].append(moyennePhi("./data/output"+str(i)))


plt.close()
for i in range(len(listeN)):
    plt.plot(listef,listePhi[i], label= listeN[i]/(L*L))
plt.legend()
plt.show()
