=========================
Cygnus OB2 Bayesian Model
=========================

This directory contains the working source code and supporting files used to calculate stellar masses and ages for X-ray detected stars in Cygnus OB2 from optical and near-IR photometry.

Currently the code does:
------------------------
- Uses optical and near-IR magnitudes: r, i, J
- Compares these to Siess isochrones
- Outputs stellar mass and age, distance and extinction
- Current priors:

  + Mass between 0.1 and 10
  + Age between 0.1 and 100 Myr
  + Distance between 1300 and 1500 pc
  + Extinction between A0 = 2 and 12 mags
