from skimage import morphology
from skimage.util import apply_parallel
import matplotlib.pyplot as plt
import numpy as np
from dask.diagnostics import ProgressBar

def tophat(imgs, size=5, chunks=2000, verbose=False):
    """Remove background with tophat

    Args:
        imgs (dict): Dict of np arrays
        size (int, optional): Radius for `morphology.disk`. Passed on to `white_tophat`. Defaults to 5.
    """
    if verbose: print(f"Running Tophat")
    footprint = morphology.disk(size)

    if type(imgs) is not dict:
        raise ValueError('Images should be a Dict of np arrays')

    res = dict()   
    for i, img in imgs.items():
        if verbose: print(f"Working on layer \"{i}\"")
        with ProgressBar():
            res[i] = apply_parallel(
                function=morphology.white_tophat,
                array=img,
                chunks=chunks,
                extra_keywords={
                    'footprint': footprint
                }
                )
    return(res)

