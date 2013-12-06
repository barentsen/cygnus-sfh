from matplotlib import rc
rc("font", family="serif", size=10)
rc("text", usetex=True)

import matplotlib
matplotlib.use('Agg')
matplotlib.interactive(False)

import daft



# Instantiate the PGM.
pgm = daft.PGM([3.0, 5.0], origin=[0.15, 0.3])

# Hierarchical parameters.
#pgm.add_node(daft.Node("alpha", r"$\alpha$", 0.5, 2, fixed=True))


pgm.add_node(daft.Node("sfh", r"$\rm SFH$", 1.0, 5))
pgm.add_node(daft.Node("clustermass", r"$\rm M_{tot}$", 0.5, 4))
pgm.add_node(daft.Node("imf", r"$\rm IMF$", 1.5, 4, fixed=True))
pgm.add_node(daft.Node("binarity", r"$\rm Binarity$", 2.5, 4, fixed=True))
pgm.add_node(daft.Node("d", r"$d$", 3.0, 3, fixed=True))

# Latent variable.
pgm.add_node(daft.Node("mass", r"$\rm M_n$", 0.8, 3))
pgm.add_node(daft.Node("age", r"$\rm \tau_n$", 1.35, 3))
pgm.add_node(daft.Node("ext", r"$\rm A_{V,n}$", 1.9, 3, fixed=True))
pgm.add_node(daft.Node("bin", r"$\rm B_n$", 2.45, 3))

pgm.add_node(daft.Node("sed", r"$\rm SED_n$", 1.7, 2))

# Data.
pgm.add_node(daft.Node("spec", r"$\rm Spec_n$", 1.4, 1, observed=True))
pgm.add_node(daft.Node("phot", r"$\rm Phot_n$", 2.0, 1, observed=True))

# Add in the edges.
pgm.add_edge("sfh", "mass")
pgm.add_edge("sfh", "age")
pgm.add_edge("binarity", "bin")
pgm.add_edge("clustermass", "mass")
pgm.add_edge("imf", "mass")

pgm.add_edge("d", "sed")
pgm.add_edge("mass", "sed")
pgm.add_edge("age", "sed")
pgm.add_edge("ext", "sed")
pgm.add_edge("bin", "sed")


pgm.add_edge("sed", "spec")
pgm.add_edge("sed", "phot")


# And a plate.
pgm.add_plate(daft.Plate([0.5, 0.5, 2.25, 3], label=r"$n = 1, \cdots, N$",
    shift=-0.1))

# Render and save.
pgm.render()
pgm.figure.savefig("sfh-model.pdf")
pgm.figure.savefig("sfh-model.png", dpi=150)
