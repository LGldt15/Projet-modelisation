
import numpy as np
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
from matplotlib.widgets import Button
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
CMAP = cm.get_cmap("hsv")
TWO_PI = 2 * np.pi

FISH_SHAPE = np.array([
    [-0.5,  0.0],
    [-0.45,  0.1],
    [-0.2,  0.25],
    [0.1,  0.15],
    [0.3,  0.05],
    [0.5,  0.35],
    [0.5, -0.35],
    [0.3, -0.05],
    [0.1, -0.15],
    [-0.2, -0.25],
    [-0.45, -0.1],
])

def theta_to_color(theta):
    theta = np.mod(theta, TWO_PI)
    return CMAP(theta / TWO_PI)
   
def plotPoisson(ax, position, angle, lw=0):
    fish = patches.Polygon(
        FISH_SHAPE,
        closed=True,
        facecolor=theta_to_color(angle),
        edgecolor="black",
        linewidth=lw
    )
    
    fish._local_transform = Affine2D()
    fish._full_transform = fish._local_transform + ax.transData
    fish._local_transform.scale(0.4)
    fish._local_transform.rotate(angle + np.pi)
    fish._local_transform.translate(position[0], position[1])
    fish.set_transform(fish._full_transform)
    
    ax.add_patch(fish)

    return fish
    
   
def majPoisson(ax, poissons, positions, angles, L):
    poss = positions % L

    colors = theta_to_color(angles)
    
    scale = 0.4
    
    for fish, pos, angle, col in zip(poissons, poss, angles, colors):
        tr = fish._local_transform
        tr.clear()
        tr.scale(scale)
        tr.rotate(angle + np.pi)
        tr.translate(pos[0], pos[1])
        fish.set_facecolor(col)

def add_stop_button(fig, ani):
    # Ajouter un axe pour le bouton (position et taille sur la figure)
    ax_button = fig.add_axes([0.8, 0.01, 0.1, 0.05])  # [x, y, width, height] en fraction de la figure
    btn = Button(ax_button, 'Stop', color='lightcoral', hovercolor='red')
    
    def on_click(event):
        # arrêter l'animation
        
        if ani is not None:
            ani.event_source.stop()

    btn.on_clicked(on_click)
    return btn
    
def animationBanc(N, L, f, updatefunction, phi = None):
    # Initialise les positions et angles des poissons
    positions = np.random.uniform(0, L, (N, 2))
    angles = np.random.uniform(-np.pi, np.pi, N)
    
    # Génère la figure et fixe les axes
    fig, ax = plt.subplots(figsize = (10, 10))
    ax.set_aspect("equal", adjustable='box') 
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    #fig.tight_layout()

    # Initialisation des poissons sur le graphe
    poissons = [plotPoisson(ax, positions[i], angles[i]) for i in range(N)]
    if phi is not None:
        text_phi = ax.text(
            0.02, 0.98, r"$\Phi$"+" = {}".format(phi(angles)),
            transform=ax.transAxes,
            ha="left", va="top",
            fontsize=12,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none")
        )
    else:
        text_phi = None

    def animate(frame):
        nonlocal positions, angles
        # Appele la fonction update pour déplacer les poissons
        positions, angles = updatefunction(positions, angles, L, f)
        majPoisson(ax, poissons, positions, angles, L)
        
        if text_phi is not None:
            value = phi(angles)
            text_phi.set_text(r"$\Phi$"+ f"= {value:.3f}")
        return poissons

    anim = FuncAnimation(
        fig, animate,
        interval=50,
        blit=False,
        cache_frame_data=False
    )
    btn = add_stop_button(plt.gcf(),  anim)
    return anim, btn

