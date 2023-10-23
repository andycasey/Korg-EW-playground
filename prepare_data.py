'''
with open("ews.dat", "r") as fp:
    content = fp.readlines()

# separate ews by star name
ews_by_star = {}
o = -1
for line in content:
    name = line[o+1:o+9+1]
    hfs_used = (line[o+11] == '-')
    wl_rest = line[o+12:o+19+1]
    source_flag = ('M' == line[o+21])
    species = line[o+23:o+27+1]
    chi = line[o+29:o+34+1]
    loggf = line[o+36:o+42+1]
    ew = line[o+44:o+50+1]

    name = name.strip()
    ews_by_star.setdefault(name, [])
    row = dict(
        wl_rest=float(wl_rest),
        hfs_used=hfs_used,
        source_flag=source_flag,
        species=species.strip(),
        chi=float(chi.strip()),
        loggf=float(loggf.strip()),
        ew=float(ew.strip())
    )
    ews_by_star[name].append(row)


# Load abundances
with open("table2.dat", "r") as fp:
    content = fp.readlines()
'''


from astropy.table import Table

bedell_2015_ews = Table.read("data/Bedell_2015_table2.dat", format='ascii.cds')
keep = (
    (bedell_2015_ews["Vesta1"] > 0)
#&   (bedell_2015_ews["Species"].astype(int) == 26) # Only Fe for now
)
bedell_2015_ews = bedell_2015_ews[keep]
bedell_2015_ews.sort("Wave")
ews = []
linelist = []
# order the line list.
for line in bedell_2015_ews:
    ews.append(f"{line['Vesta1']:.1f},")
    linelist.append(
        f"Korg.Line({line['Wave']:.3f} * 1e-8, {line['log(gf)']:.5f}, Korg.Species(\"{line['Species']}\"), {line['ExPot']}),"
    )
ews_as_str = " ".join(ews)
linelist_as_str = "[\n" + "\n".join(linelist) + "\n]"

sun_params = {
    "Teff": 5777,
    "logg": 4.44,
    "[Fe/H]": 0.0,
    "Xi": 1.0,
}

template = f"""
Teff, logg, Fe_H, vmic = ({sun_params['Teff']}, {sun_params['logg']}, {sun_params['[Fe/H]']}, {sun_params['Xi']})
A_X = Korg.format_A_X(Fe_H)
atm = Korg.interpolate_marcs(Teff, logg, Fe_H)  
ews = [{ews_as_str}]
linelist = {linelist_as_str}
"""
with open("Sun.jl", "w") as fp:
    fp.write(template)
    
print(f"Created Sun.jl")




ews = Table.read("data/ews.dat", format="ascii.cds")



params = Table.read("data/Spina_table2.dat", format="ascii.cds")
abundances = Table.read("data/table2.dat", format="ascii.cds")

params_by_hip = {}
for group in params.group_by(["HIP"]).groups:
    params_by_hip[group["HIP"][0]] = dict(zip(group.dtype.names, group[0]))

params_by_hip["Sun"] = {
    "Teff": 5777,
    "logg": 4.44,
    "[Fe/H]": 0.0,
    "Xi": 1.0,
}

# need: ews by star
# need: mean abundances by star
# need: stellar parameters by star

ews_by_star = {}
for group in ews.group_by(["Name"]).groups:
    name = group["Name"][0]
    keep = (
        (group["n_lambda"] != "-") # exclude HFS lines
    &   (group["EW"] > 0) # exclude lines not measured
    &   (group["Ion"] < 100) # exclude molecules
    )
    if name != "Sun":
        name = int(name.lstrip("HIP ")) # HIP
    ews_by_star[name] = group[keep]

abundances_by_star = {}
for group in abundances.group_by(["Name"]).groups:
    name = group["Name"][0]
    if name != "Sun":
        name = int(name.lstrip("HIP ")) # HIP    
    abundances_by_star[name] = dict(zip(group.dtype.names, group[0]))


# Now prepare for Korg.
for name, params in params_by_hip.items():
    
    ews_as_str = " ".join([f"{ew:.1f}," for ew in ews_by_star[name]["EW"]])
    linelist = []
    for line in ews_by_star[name]:
        linelist.append(
            f"Korg.Line({line['lambda']:.3f} * 1e-8, {line['log(gf)']:.5f}, Korg.Species(\"{line['Ion']}\"), {line})"
        )

    template = f"""
    Teff, logg, Fe_H = ({params['Teff']}, {params['logg']}, {params['[Fe/H]']})
    A_X = Korg.format_A_X(Fe_H)
    atm = Korg.interpolate_marcs(Teff, logg, Fe_H)  
    ews = [{ews_as_str}]
    linelist = [{linelist_as_str}]
    """
    print(template)
    raise a
'''
linelist_and_ews = [
    [Korg.Line(4365.90 * 1e-8, -2.25, Korg.Species("26.0"), 2.99),   51.0, 7.3911195],
    [Korg.Line(4389.25 * 1e-8, -4.58, Korg.Species("26.0"), 0.05),   72.2, 7.3351083],
    [Korg.Line(4445.47 * 1e-8, -5.44, Korg.Species("26.0"), 0.09),   40.6, 7.373839 ],
    [Korg.Line(4602.00 * 1e-8, -3.15, Korg.Species("26.0"), 1.61),   69.2, 7.39661  ],
    [Korg.Line(4788.76 * 1e-8, -1.73, Korg.Species("26.0"), 3.24),   64.3, 7.370553 ],
    [Korg.Line(4950.10 * 1e-8, -1.56, Korg.Species("26.0"), 3.42),   72.3, 7.51876  ],
    [Korg.Line(4994.13 * 1e-8, -3.08, Korg.Species("26.0"), 0.92),  103.1, 7.4076533],
    [Korg.Line(5044.21 * 1e-8, -2.06, Korg.Species("26.0"), 2.85),   73.7, 7.4127636],
    [Korg.Line(5054.64 * 1e-8, -1.92, Korg.Species("26.0"), 3.64),   38.5, 7.31961  ],
    [Korg.Line(5127.36 * 1e-8, -3.31, Korg.Species("26.0"), 0.92),   95.2, 7.4004474],
'''



