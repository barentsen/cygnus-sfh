#!/usr/bin/env python
"""Estimates stellar parameters given photometry."""
import numpy as np
import emcee
import triangle
from astropy import log
from astropy.io import fits
from scipy.interpolate.rbf import Rbf

siess = fits.getdata("siess_isochrones.fits", 1)

siess_Mr = Rbf(siess.field("logMass"), siess.field("logAge"),
               siess.field("Mr_iphas"), function="linear")
siess_Mi = Rbf(siess.field("logMass"), siess.field("logAge"),
               siess.field("Mi_iphas"), function="linear")
siess_Mj = Rbf(siess.field("logMass"), siess.field("logAge"),
               siess.field("Mj"), function="linear")


def model_photometry(theta):
    """Returns apparent magnitudes given stellar parameters."""
    log_mass, log_age, dist, a0 = theta
    phot = np.array([siess_Mr(log_mass, log_age),
                     siess_Mi(log_mass, log_age),
                     siess_Mj(log_mass, log_age)])
    dismod = 5.0 * np.log10(dist) - 5.0
    extinction = np.array([0.843*a0, 0.639*a0, 0.276*a0])
    return phot + dismod + extinction

def lnprior(theta):
    """Returns prior prob given stellar parameters."""
    log_mass, log_age, dist, a0 = theta
    if (-1. < log_mass < 1. and 5. < log_age < 8.
        and 1300 < dist < 1500 and 2 < a0 < 12):
        #return 0.0
        return -(dist-1400.)**2 / (10.**2)
    return -np.inf

def lnlike(theta, photom, photom_icov):
    """Returns likelihood prob."""
    diff = photom - model_photometry(theta)
    lnprob = -np.dot(diff, np.dot(photom_icov, diff))/2.
    return lnprob

def lnprob(theta, photom, photom_icov):
    """Returns posterior probability."""
    lp = lnprior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike(theta, photom, photom_icov)

def report(sampler):
    """Prints the result to the screen in human-readable format."""
    log.info('logMass = {0:.2f} +/- {1:.2f}'
                 .format(sampler.flatchain[:,0].mean(),
                         sampler.flatchain[:,0].std()))
    log.info('logAge = {0:.2f} +/- {1:.2f}'
                 .format(sampler.flatchain[:,1].mean(),
                         sampler.flatchain[:,1].std()))
    log.info('dist = {0:.2f} +/- {1:.2f}'
                 .format(sampler.flatchain[:,2].mean(),
                         sampler.flatchain[:,2].std()))
    log.info('a0 = {0:.2f} +/- {1:.2f}'
                 .format(sampler.flatchain[:,3].mean(),
                         sampler.flatchain[:,3].std()))
    log.info("Mean acceptance fraction: {0:.3f}"
                .format(sampler.acceptance_fraction.mean()))


if __name__ == '__main__':
    # Data being fitted:
    photom = np.array([18.583, 16.896, 15.036])  # [r, i, J]
    photom_icov = 1. / 0.05*np.eye(3)  # inverse covariance matrix

    # Setup the sampler
    ndim, nwalkers, nsamples = 4, 100, 10000
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, 
                                    args=([photom, photom_icov]),
                                    threads=10)

    # Create random starting values and sample
    p0 = [np.array([0.0, 6.0, 1500, 6.]) + np.random.rand(ndim)
          for i in range(nwalkers)]
    sampler.run_mcmc(p0, nsamples)

    # Report and plot the results
    report(sampler)
    figure = triangle.corner(sampler.flatchain[1000:], 
                             show_titles=True,
                             quantiles=[0.16, 0.5, 0.84],
                             labels=[r"$\log M$", r"$\log \tau$", r"$d$", r"$A_0$"])
    figure.savefig("triangle.pdf")
