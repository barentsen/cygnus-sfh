=========================
Cygnus OB2 Bayesian Model
=========================

This directory contains the working source code and supporting files used to calculate stellar masses and ages for X-ray detected stars in Cygnus OB2 from optical and near-IR photometry.

Photometry details
------------------
- There are a total of 5677 sources
- 79% of sources have optical photometry (68% have OSIRIS r,i,z and 40% have IPHAS r,i,Ha)
- 95% of source have near-IR photometry (86% have UKIDSS, 63% have 2MASS)
- Therefore, combining all these:

  + 65% of sources have OSIRIS (and maybe IPHAS) and near-IR photometry (r,i,z,J,H,K)
  + 11% of sources have only IPHAS and near-IR photometry (r,i,J,H,K)
  + 19% of sources have only near-IR photometry (J,H,K)
  + 2% of sources have only OSIRIS (and maybe IPHAS) photometry (r,i,z)
  + 1% of sources have only IPHAS photometry (r,i)
  + 2% of sources have no optical or near-IR photometry


Currently the code does:
------------------------
- Uses optical and near-IR magnitudes: r, i, J
- Compares these to Siess isochrones
- Outputs stellar mass and age, distance and extinction
- Current priors:

  + Mass between 0.1 and 10 Msun
  + Age between 0.1 and 100 Myr
  + Distance between 1300 and 1500 pc
  + Extinction between A0 = 2 and 12 mags

- Uses the emcee code to do the MCMC sampling
- Then outputs means and standard deviations, writes these to the screen and produces a triangle plot


Things to do
------------

- Test the inclusion of H band photometry
- Add in z band photometry
- Create photometric transformations for IPHAS/OSIRIS and 2MASS/UKIDSS data
- Consider including non-detections as upper limits (though must be aware of chip gaps, bad pixels, etc)
- Add in Wright+ 2014 extinction curves to properly account for extinction
- Add in a binarity model that chooses binary companions, adds their fluxes and combines them with the primary to get photometry for the whole system
- Consider a method for flagging and dealing with foreground contaminants


Bonus things to do
------------------

- Take into account Ha photometry to get mass accretion rates
- Take into account K-band or mid-IR photometry to get disk rates
