def plot_spectrum(MZ, I, show=True):
    """A simple stem-plot stick spectrum.
    
    You need to have matplotlib installed for this method to work.
    
    Args:
        MZ (iterable): mass over charge values.
        I (iterable): intensities corresponding to mass over charge ratios.
        show (bool): show the plot
    """
    import matplotlib.pyplot as plt
    plt.stem(MZ, I)
    if show:
        plt.show()
