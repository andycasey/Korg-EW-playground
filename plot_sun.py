import matplotlib.pyplot as plt
from astropy.table import Table
import numpy as np

data = Table.read("Sun.dat", format="ascii.csv")
species, Z, A = (data["species"], data["Z"], data["A"])

Z_means = []
A_neutral_means = {}
A_ionized_means = {}
for i, row in enumerate(data):
    Z = int(row["Z"])
    Z_means.append(Z)
    dA = row["A"] - row["Sun"]
    is_ionized = ("II" in row["species"])
    if is_ionized:
        A_ionized_means.setdefault(Z, [])            
        A_ionized_means[Z].append(dA)
    else:
        A_neutral_means.setdefault(Z, [])        
        A_neutral_means[Z].append(dA)
    
    
#for Z in A_ionized_means.keys():
#    A_ionized_means[Z] = np.mean(A_ionized_means[Z])
        
#for Z in A_neutral_means.keys():
#    A_neutral_means[Z] = np.mean(A_neutral_means[Z])
    
x = np.sort(np.unique(Z_means))
y = np.array([np.mean(A_neutral_means[z]) for z in x])
y_err = np.array([np.std(A_neutral_means[z]) / np.sqrt(len(A_neutral_means[z]) - 1) for z in x])

fig, ax = plt.subplots()
ax.axhline(0, c="#666666", ls=':', zorder=-1, lw=0.5)
ax.errorbar(
    x,
    y,
    yerr=y_err,
    fmt='o'
)

#fig, ax = plt.subplots()
#ax.scatter(x, y)