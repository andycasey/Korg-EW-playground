from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt

mpl_style = {

    # Lines
    'lines.linewidth': 1.7,
    'lines.antialiased': True,
    'lines.marker': '.',
    'lines.markersize': 5.,

    # Patches
    'patch.linewidth': 1.0,
    'patch.facecolor': '#348ABD',
    'patch.edgecolor': '#CCCCCC',
    'patch.antialiased': True,

    # images
    'image.origin': 'upper',

    # colormap
    'image.cmap': 'viridis',

    # Font
    'font.size': 12.0,
    'text.usetex': True,
    'text.latex.preamble': r'\usepackage{amsmath}',
    'text.latex.preview': True,
    'axes.unicode_minus': False,

    # Axes
    'axes.facecolor': '#FFFFFF',
    'axes.edgecolor': '#333333',
    'axes.linewidth': 1.0,
    'axes.grid': False,
    'axes.titlesize': 'x-large',
    'axes.labelsize': 'large',
    'axes.labelcolor': 'k',
    'axes.axisbelow': True,

    # Ticks
    'xtick.major.size': 8,
    'xtick.minor.size': 4,
    'xtick.major.pad': 6,
    'xtick.minor.pad': 6,
    'xtick.color': '#333333',
    'xtick.direction': 'in',
    'ytick.major.size': 8,
    'ytick.minor.size': 4,
    'ytick.major.pad': 6,
    'ytick.minor.pad': 6,
    'ytick.color': '#333333',
    'ytick.direction': 'in',
    'xtick.labelsize': 'medium',
    'ytick.labelsize': 'medium',

    # Legend
    'legend.fancybox': True,
    'legend.loc': 'best',

    # Figure
    'figure.figsize': [6, 6],
    'figure.facecolor': '1.0',
    'figure.edgecolor': '0.50',
    'figure.subplot.hspace': 0.5,

    # Other
    'savefig.dpi': 300,
}

data = Table.read("Melendez_abundances.csv")

x = data["E_lower"]
y = data["sco_A"] - data["sun_A"]
c = data["charge"]

rew = np.log10((data["sun_ew"] * 1e-3)/data["wl"])

is_neutral = (c == 0)
is_ionized = (c == 1)
fig, (ax_chi, ax_rew) = plt.subplots(2, 1)
ax_chi.scatter(
    x[is_neutral],
    y[is_neutral],
    facecolor="w",
    edgecolor="k",
)
ax_chi.scatter(
    x[is_ionized],
    y[is_ionized],
    marker="s",
    facecolor="#666666",
    edgecolor='k',    
    s=30,
    zorder=10
)
ax_rew.scatter(
    rew[is_neutral],
    y[is_neutral],
    facecolor="w",
    edgecolor="k",    
)
ax_rew.scatter(
    rew[is_ionized],
    y[is_ionized],
    marker="s",
    facecolor="#666666",
    edgecolor='k',
    s=30,
    zorder=10
)
mean_y = np.mean(y)

from matplotlib.ticker import MaxNLocator

for ax in (ax_chi, ax_rew):
    ax.axhline(mean_y, c="#666666", ls=":", lw=0.5, zorder=-1)
    ax.set_ylim(-0.01, 0.12)
    ax.set_ylabel(r"$\mathrm{Differential}$ $\mathrm{[Fe/H]}$ $[\mathrm{dex}]$")
    ax.yaxis.set_major_locator(MaxNLocator(7))

ax_chi.text(0.025, 0.10,
    r"$\langle[\mathrm{{Fe/H}}]\rangle = {0:.3f}$ ($\sigma = {1:.3f},$ $\mathrm{{s.e.}}\,=\,{2:.3f})$".format(mean_y, np.std(y), np.std(y)/np.sqrt(len(y) - 1)),
    transform=ax_chi.transAxes
)
ax_chi.set_xlabel(r"$\chi\,[\mathrm{eV}]$")
ax_rew.set_xlabel(r"$\log_{10}\left(\mathrm{EW}/\lambda\right)$")
ax_chi.set_xlim(-0.25, 5.25)
ax_rew.set_xlim(-5.8, -4.6)
ax_rew.text(
    0.025, 0.20,
    r"$18\,\mathrm{Sco}$",
    transform=ax.transAxes
)
ax_rew.text(
    0.025, 0.10,
    r"$T_\mathrm{eff} = 5823\,\mathrm{K}, \log{g} = 4.45, \mathrm{[Fe/H]} = 0.054\,\,(\mathrm{Melendez\,et\,al.\,2014})$",
    transform=ax.transAxes
)
fig.tight_layout()
fig.savefig("Melendez.pdf", dpi=300)