import datetime

import numpy as np
from astropy.table import Table
from scipy import signal
from scipy.interpolate import interp1d

from laspec.binning import wave_log10


def Gaussian_kernel(dRV_sampling=0.1, dRV_Gk=2.3548200450309493, n_sigma_Gk=5.):
    # FWHM --> sigma
    sigma = dRV_Gk/dRV_sampling/(2*np.sqrt(2*np.log(2)))
    
    # determine X
    npix_half = np.int(sigma*n_sigma_Gk)
    # npix = 2 * npix_half + 1
    x = np.arange(-npix_half, npix_half+1)
        
    # normalized Gaussian kernel
    kernel = np.exp(-.5*(x/sigma)**2.)
    kernel /= np.sum(kernel)
    return kernel


def Rotation_kernel(dRV_sampling=0.3, vsini=100, epsilon=0.6, cushion=10):
    
    # determine X
    npix_half = np.int(np.floor(vsini/dRV_sampling))# + cushion
    # npix = 2 * npix_half + 1
    vvl = np.arange(-npix_half, npix_half+1)*dRV_sampling/vsini
    
    # rotation kernel
    denominator = np.pi * vsini * (1.0 - epsilon / 3.0)
    c1 = 2.0 * (1.0 - epsilon) / denominator
    c2 = 0.5 * np.pi * epsilon / denominator
    kernel = c1 * np.sqrt(1.0 - vvl**2) + c2 * (1.0 - vvl**2)
    kernel /= np.sum(kernel)
    return kernel


def conv_spec_Gaussian(wave, flux, dRV_Gk=None,
                       R_hi=3e5, R_lo=2000., n_sigma_Gk=5., 
                       interp=True, osr_ext=3., wave_new=None):
    """ to convolve instrumental broadening (high-R spectrum to low-R spectrum)

    Parameters
    ----------
    wave: array
        wavelength
    flux: array
        flux array
    dRV_Gk: float
        the FWHM of the Gaussian kernel (km/s)
        if None, determined by R_hi and R_lo
    R_hi: float
        higher resolution
    R_lo: float
        lower resolution
    n_sigma_Gk: float
        the gaussian kernel width in terms of sigma
    interp: bool
        if True, interpolate to log10 wavelength
    osr_ext:
        the extra oversampling rate if interp is True.
    wave_new:
        if not None, return convolved spectrum at wave_new
        if None, return log10 spectrum

    Returns
    -------
    wave_new, flux_new

    """
    if interp:
        wave_interp = wave_log10(wave, osr_ext=osr_ext)
        flux_interp = np.interp(wave_interp, wave, flux) # 10 times faster
        # flux_interp = interp1d(wave, flux, kind="linear", bounds_error=False)(wave_interp)
    else:
        wave_interp = np.copy(wave)
        flux_interp = np.copy(flux)
    assert np.all(np.isfinite(flux_interp))
    
    # evaluate the RV sampling rate via log10(wave) sampling rate
    # d(log10(wave)) = z / ln(10) = d(RV)/(c*ln(10))
    # --> d(RV) = c*ln(10)*d(log10(wave))
    dRV_sampling = 299792.458 * np.log(10) * (np.log10(wave_interp[1])-np.log10(wave_interp[0]))
    if dRV_Gk is None:
        R_Gk = R_hi*R_lo / np.sqrt(R_hi**2-R_lo**2) # Gaussian kernel resolution
        dRV_Gk = 299792.458 / R_Gk # Gaussian kernel resolution (FWHM) --> RV resolution
    # generate Gaussian kernel
    Gk = Gaussian_kernel(dRV_sampling, dRV_Gk, n_sigma_Gk=n_sigma_Gk)
    
    # convolution
    # fftconvolve is the most efficient ...currently
    flux_conv = signal.fftconvolve(flux_interp, Gk, mode="same")
    # flux_conv = np.convolve(flux_interp, Gk, mode="same")
    # flux_conv = signal.convolve(flux_interp, Gk, mode="same")
    
    # interpolate to new wavelength grid if necessary
    if wave_new is None:
        return wave_interp, flux_conv
    else:
        flux_conv_interp = np.interp(wave_new, wave_interp, flux_conv)
        return wave_interp, flux_conv_interp
    

def conv_spec_Rotation(wave, flux, vsini=100., epsilon=0.6,
                       interp=True, osr_ext=3., wave_new=None):
    """ to convolve instrumental broadening (high-R spectrum to low-R spectrum)

    Parameters
    ----------
    wave: array
        wavelength
    flux: array
        flux array
    vsini: float
        the projected stellar rotational velocity (km/s)
    epsilon: float
        0 to 1, the limb-darkening coefficient, default 0.6.
    interp: bool
        if True, interpolate to log10 wavelength
    osr_ext:
        the extra oversampling rate if interp is True.
    wave_new:
        if not None, return convolved spectrum at wave_new
        if None, return log10 spectrum

    Returns
    -------
    wave_new, flux_new OR Table([wave, flux])

    """
    if interp:
        wave_interp = wave_log10(wave, osr_ext=osr_ext)
        flux_interp = np.interp(wave_interp, wave, flux) # 10 times faster
        # flux_interp = interp1d(wave, flux, kind="linear", bounds_error=False)(wave_interp)
    else:
        wave_interp = np.copy(wave)
        flux_interp = np.copy(flux)
    assert np.all(np.isfinite(flux_interp))
    
    # evaluate the RV sampling rate via log10(wave) sampling rate
    # d(log10(wave)) = z / ln(10) = d(RV)/(c*ln(10))
    # --> d(RV) = c*ln(10)*d(log10(wave))
    dRV_sampling = 299792.458 * np.log(10) * (np.log10(wave_interp[1])-np.log10(wave_interp[0]))

    # generate rotation kernel
    Rk = Rotation_kernel(dRV_sampling, vsini, epsilon=epsilon)

    # convolution
    # fftconvolve is the most efficient ...currently
    flux_conv = signal.fftconvolve(flux_interp, Rk, mode="same")
    # flux_conv = np.convolve(flux_interp, Gk, mode="same")
    # flux_conv = signal.convolve(flux_interp, Gk, mode="same")
    
    # interpolate to new wavelength grid if necessary
    if wave_new is None:
        return wave_interp, flux_conv
    else:
        flux_conv_interp = np.interp(wave_new, wave_interp, flux_conv)
        return wave_interp, flux_conv_interp    

def read_phoenix_sun():
    """ read PHOENIX synthetic spectrum for the Sun """
    import laspec
    from astropy.io import fits
    flux_sun = fits.open(laspec.__path__[0] + "/data/phoenix/lte05800-4.50-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits")[0].data
    wave_sun = fits.open(laspec.__path__[0] + "/data/phoenix/WAVE_PHOENIX-ACES-AGSS-COND-2011.fits")[0].data
    return wave_sun, flux_sun


def test_convolution():
    """ testing convolving PHOENIX synthetic spectrum for the Sun """
    import matplotlib.pyplot as plt
    from laspec.convolution import conv_spec
    wave_sun, flux_sun = read_phoenix_sun()
    ind_optical = (wave_sun > 4000) & (wave_sun < 7000)
    wave = wave_sun[ind_optical]
    flux = flux_sun[ind_optical]
    
    print("testing laspec.convolution.conv_spec ...  ")
    t0 = datetime.datetime.now()    
    wave_conv1, flux_conv1 = conv_spec(wave, flux, R_hi=3e5, R_lo=2000, verbose=False)
    print("time spent: ", datetime.datetime.now() - t0)
    
    print("testing laspec.qconv.conv_spec_Gaussian ...  ")
    t0 = datetime.datetime.now()    
    wave_conv2, flux_conv2 = conv_spec_Gaussian(wave, flux, R_hi=3e5, R_lo=2000)
    print("time spent: ", datetime.datetime.now() - t0)
    
    print("testing laspec.qconv.conv_spec_Rotation ...  ")
    t0 = datetime.datetime.now()    
    wave_conv3, flux_conv3 = conv_spec_Rotation(wave_conv2, flux_conv2, vsini=0.1, epsilon=0.6)
    print("time spent: ", datetime.datetime.now() - t0)
    
    plt.figure()
    plt.plot(wave, flux)
    plt.plot(wave_conv1, flux_conv1)
    plt.plot(wave_conv2, flux_conv2)
    plt.plot(wave_conv3, flux_conv3)
    return
    

if __name__ == '__main__':
    test_convolution()
