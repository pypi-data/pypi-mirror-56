__version__ = '0.1'
import numpy as np

def LIA(data,sampling_freq,load_freq):
    """
    Function to obtain magnitude and phase of a thermal signal usign a lock-in analyzer
    
    Arguments:
        data {np.array} -- sequence of thermal images
        sampling_freq {float} -- sampling frequency if thermal video [Hz]
        load_freq {float} -- frequency of excitaiton load [Hz]
    
    Returns:
        mag -- magnitude of locked-in signal [DL -- digital level]
        ph -- phase of locked-in signal [deg -- degrees]
    """
    t = np.linspace(0, data.shape[0]/sampling_freq, data.shape[0]) # Time vector
    sine = np.sin(load_freq*t*2*np.pi) # Sine wave at the expected thermal frequency (i.e. the load frequency)
    cosine = np.cos(load_freq*t*2*np.pi) # Cosine wave at the expected thermal frequency (i.e. the load frequency)

    S = (np.ones((data.shape[0], data.shape[1], data.shape[2])).T*sine).T 
    C = (np.ones((data.shape[0], data.shape[1], data.shape[2])).T*cosine).T 

    L1 = S*data # sine matrix * data matrix
    L2 = C*data # cosine matrix * data matrix
    Re = np.sum(L1 ,0)/data.shape[0] # real part
    Img = np.sum(L2, 0)/data.shape[0] #imaginary part
    
    mag = np.sqrt(Re**2 + Img**2) # magnitude
    ph = np.arctan(Img/Re) * 180/np.pi #phase in degrees

    return mag, ph
