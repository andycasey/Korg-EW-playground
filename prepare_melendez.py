from astropy.table import Table
import numpy as np

melendez = Table.read("Melendez_et_al.txt", format="ascii.cds")

is_fe = (np.array(melendez["Ion"]).astype(int) == 26)
melendez = melendez[is_fe]

# order the line list.
melendez.sort("Wave")

ews = []
sco_ews = []
linelist = []


for line in melendez:
    ews.append(f"{line['EW-Sun']:.1f},")
    sco_ews.append(f"{line['EW-18S']:.1f},")
    
    linelist.append(
        f"Korg.Line({line['Wave']:.3f} * 1e-8, {line['log(gf)']:.5f}, Korg.Species(\"{line['Ion']}\"), {line['ExPot']}, {line['C6']}),"
    )
sco_ews_as_str = " ".join(sco_ews)    
ews_as_str = " ".join(ews)
linelist_as_str = "[\n" + "\n".join(linelist) + "\n]"

template = f"""
sun_ews = [{ews_as_str}]
sco_ews = [{sco_ews_as_str}]
linelist = {linelist_as_str}
"""

with open("Melendez.jl", "w") as fp:
    fp.write(template)