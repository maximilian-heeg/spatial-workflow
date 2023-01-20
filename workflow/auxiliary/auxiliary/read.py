import glob
import tifffile
import numpy as np
from skimage.transform import resize

def _tiff(name, layer=3, verbose=False):
    """ Imports a TIFF file
    
    Parameters
    --------------
    name: String to the tiffile. %i is the layer. E.g. "images/pyrmosaic_Fabp1_z%i._subset.tif"
    layer: layer of the stack
    
    Returns
    --------------
    A np array of shape (Y x X)
    
    """
    file = name % layer

    if verbose: print(f"Import file \"{file}\"")
    img = tifffile.imread(file)
    return img

def stack(name, layers, verbose=False):
    """Reads a stack of TIFF files

    Args:
        name (String): String to the tiffile. %i is the layer. E.g. "images/pyrmosaic_Fabp1_z%i._subset.tif"
        layers (array of int): Layers to import
        verbose (bool, optional): Defaults to False.

    Returns:
        Dict: (Z => np.array(Y x X))
    """
    imgs = dict()
    for l in layers:
        img = _tiff(name, layer=l, verbose=verbose)
        imgs[l] = img
    return imgs
        