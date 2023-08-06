#############################################################################################
#                                                                                           #
# Author:   GeoPy Team                                                                      #
# Date:     September 2018                                                                  #
#                                                                                           #
#############################################################################################

# seismic attribute analysis functions

from PyQt5 import QtCore
import sys
import numpy as np
from scipy.signal.signaltools import hilbert


def calcPowerSpectrum(seis3dmat, zstep):
    """
    Calculate the power spectrum of a seismic cube
    Args:
        seis3dmat: seismic data in 3D matrix [Z/XL/IL]
        zstep: z sampling rate in ms
    Return:
        spec: 2D matrix of two columns, [frequency, spectrum]
    """
    if np.ndim(seis3dmat) != 3:
        print('ERROR in calcPowerSpectrum: 3D seismic matrix expected')
        sys.exit()
    #
    znum = np.shape(seis3dmat)[0]
    #
    spec = np.zeros([int((znum+1)/2), 2])
    #
    freq = np.fft.fft(seis3dmat, axis=0)
    freq = np.abs(freq)
    freq = np.mean(freq, axis=1)
    freq = np.mean(freq, axis=1)
    #
    spec[:, 0] = np.linspace(0, 500.0/np.abs(zstep), int((znum+1)/2))
    spec[:, 1] = freq[0:int((znum+1)/2)]
    #
    return spec


def calcCumulativeSum(seis3dmat):
    """
    Calculate cusum attribute
    Args:
        seis3dmat: seismic data in 3D matrix [Z/XL/IL]
    Return:
    """
    if np.ndim(seis3dmat) != 3:
        print('ERROR in calcCumulativeSum: 3D seismic matrix expected')
        sys.exit()
    #
    return np.cumsum(seis3dmat, axis=0)

def calcFirstDerivative(seis3dmat):
    """
    Calculate first derivative attribute
    Args:
        seis3dmat: seismic data in 3D matrix [Z/XL/IL]
    Return:
    """
    if np.ndim(seis3dmat) != 3:
        print('ERROR in calcFirstDerivative: 3D seismic matrix expected')
        sys.exit()
    #
    attrib = seis3dmat.copy()
    if np.shape(seis3dmat)[0] > 1:
        attrib[1:, :, :] -= seis3dmat[0:-1, :, :]
        # attrib[0, :, :] *= 0
    #
    return attrib

def calcInstanEnvelop(seis3dmat):
    """
    Calculate instantaneous envelop attribute
    Args:
        seis3dmat: seismic data in 3D matrix [Z/XL/IL]
    Return:
    """
    if np.ndim(seis3dmat) != 3:
        print('ERROR in calcInstanEnvelop: 3D seismic matrix expected')
        sys.exit()
    #
    attrib = np.abs(hilbert(seis3dmat, axis=0))
    #
    return attrib

def calcInstanQuadrature(seis3dmat):
    """
    Calculate instantaneous quadrature attribute
    Args:
        seis3dmat: seismic data in 3D matrix [Z/XL/IL]
    Return:
    """
    if np.ndim(seis3dmat) != 3:
        print('ERROR in calcInstanEnvelop: 3D seismic matrix expected')
        sys.exit()
    #
    attrib = np.imag(hilbert(seis3dmat, axis=0))
    #
    return attrib

def calcInstanPhase(seis3dmat):
    """
    Calculate instantaneous phase attribute
    Args:
        seis3dmat: seismic data in 3D matrix [Z/XL/IL]
    Return:
    """
    if np.ndim(seis3dmat) != 3:
        print('ERROR in calcInstanEnvelop: 3D seismic matrix expected')
        sys.exit()
    #
    attrib = np.angle(hilbert(seis3dmat, axis=0))
    attrib = attrib * 180.0 / np.pi
    #
    return attrib

def calcInstanFrequency(seis3dmat):
    """
    Calculate instantaneous frequency attribute
    Args:
        seis3dmat: seismic data in 3D matrix [Z/XL/IL]
    Return:
    """
    if np.ndim(seis3dmat) != 3:
        print('ERROR in calcInstanEnvelop: 3D seismic matrix expected')
        sys.exit()
    #
    instphase = np.unwrap(np.angle(hilbert(seis3dmat, axis=0)), axis=0) * 0.5 / np.pi
    #
    attrib = np.zeros(np.shape(seis3dmat))
    attrib[1:-1, :, :] = 0.5 * (instphase[2:, :, :] - instphase[0:-2, :, :])
    #
    return attrib

def calcInstanCosPhase(seis3dmat):
    """
    Calculate instantaneous cosine of phase attribute
    Args:
        seis3dmat: seismic data in 3D matrix [Z/XL/IL]
    Return:
    """
    if np.ndim(seis3dmat) != 3:
        print('ERROR in calcInstanEnvelop: 3D seismic matrix expected')
        sys.exit()
    #
    attrib = np.angle(hilbert(seis3dmat, axis=0))
    attrib = np.cos(attrib)
    #
    return attrib


class attribute:
    # pack all functions as a class
    #
    calcPowerSpectrum = calcPowerSpectrum
    #
    calcCumulativeSum = calcCumulativeSum
    calcFirstDerivative = calcFirstDerivative
    #
    calcInstanEnvelop = calcInstanEnvelop
    calcInstanQuadrature = calcInstanQuadrature
    calcInstanPhase = calcInstanPhase
    calcInstanFrequency = calcInstanFrequency
    calcInstanCosPhase = calcInstanCosPhase