import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
        "opacity",
        choices=["scattering", "absorption"],
        help="Opacity type to plot",
)

args = parser.parse_args()

data = {
    1: [],
    2: [],
    3: []
}

reading = False

with open("point_output.txt") as f:
    for line in f:
        if "Example of a single point call with returning all emissivity" in line:
            reading = True
            continue
        if reading:
            parts = line.split()

            if len(parts) != 7:
                if any(data.values()):
                    break
                continue

            species = int(parts[0])
            energy = float(parts[2])
            absorption = float(parts[4])
            scattering = float(parts[5])

            data[species].append((energy, absorption, scattering))

for species in [1, 2, 3]:
    print(species, len(data[species]))

labels = {
    1: r"$\nu_e$",
    2: r"$\bar{\nu}_e$",
    3: r"$\nu_x$",
}

for species in [1, 2, 3]:
    energy = [x[0] for x in data[species]]

    if args.opacity == "scattering":
        opacity = [x[2] for x in data[species]]
    else:
        opacity = [x[1] for x in data[species]]

    plt.plot(energy, opacity, marker="o", label=labels[species])

plt.xlabel(r"Neutrino energy $E_\nu$ [MeV]")

if args.opacity == "scattering":
    plt.ylabel(r"Scattering opacity $\kappa_{\rm scat}$ [cm$^{-1}$]")
else:
    plt.ylabel(r"Absorption opacity $\kappa_{\rm abs}$ [cm$^{-1}$]")

plt.xscale("log")
plt.yscale("log")

plt.legend()
plt.grid()

plt.title(
    r"LS220: $\rho=10^{12}$ g cm$^{-3}$, "
    r"$T=1.5$ MeV, $Y_e=0.35$"
)

plt.show()
