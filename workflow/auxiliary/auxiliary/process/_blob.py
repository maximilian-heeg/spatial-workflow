from skimage.feature import blob_log
from math import sqrt
from skimage.util import apply_parallel
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import dask.array as da
import dask
from dask.diagnostics import ProgressBar

def blob(tophats, max_sigma=5, num_sigma=10, threshold=.01, verbose=False, chunks=2000):
    """Detect spots using LOG

    Args:
        tophats (dict): Images after tophat
        max_sigma (int, optional): Passed to `blob_log`. Defaults to 5.
        num_sigma (int, optional): Passed to `blob_log`. Defaults to 10.
        threshold (float, optional): Passed to `blob_log`. Defaults to .01.
        plot (bool, optional): Make plots. Defaults to True.
    """
    if verbose: print(f"Starting Blob detection")
    if type(tophats) is not dict:
        raise ValueError('tophats should be a Dict of np arrays')

    res = dict()   
    for i, img in tophats.items():
        if verbose: print(f"Working on layer \"{i}\"")
        # x = da.from_array(img, chunks=chunks)
        # blocks = x.to_delayed().ravel()
        # results = [da.from_delayed(_detect_blobs(b, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold), shape=(np.nan, 3), dtype=np.int64) for b in blocks]
        # arr = da.concatenate(results, axis=0, allow_unknown_chunksizes=True)
        # res[i] = arr.compute()
        current_blobs = []
        if verbose: print(f"... Creating dask delayed array")
        for y in range(0, img.shape[0], chunks):
            for x in range(0, img.shape[1], chunks):
                # Get the current window
                window = img[y:y+chunks, x:x+chunks]


                # Use the Laplacian of Gaussian method to detect blobs in the window
                blobs = _detect_blobs(window, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold, xoffset=x, yoffset=y)

                # Extract the x, y coordinates of the blobs, and adjust them based on the window position
                
                current_blobs.append(blobs)
        # res[i] = blob_log(img, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold) 

        if verbose: print(f"... Computing dask delayed array")
        with ProgressBar():
            current_blobs = dask.compute(*current_blobs)
        current_blobs = np.vstack(current_blobs)
        res[i] = current_blobs
    return(res)

@dask.delayed
def _detect_blobs(block, max_sigma, num_sigma, threshold, xoffset, yoffset):
  blobs = blob_log(block, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold)
  blobs[:, 0] = blobs[:, 0] + yoffset
  blobs[:, 1] = blobs[:, 1] + xoffset
  return(blobs)


def blobsToPandas(blobs, gene, micron_to_mosaic_pixel_transform):
    """Generate a pandas data.frame from the results

    Args:
        blobs (dict): results from blob function
        gene (string): name of the gene
        micron_to_mosaic_pixel_transform (string): Path to the micron_to_mosaic_pixel_transform file
    """
    df = pd.DataFrame(columns=['global_x', 'global_y', 'global_z', 'gene'])

    rescale_fun = _create_rescaling_function(micron_to_mosaic_pixel_transform)

    for i, b in blobs.items():
        # get the rescaled points
        points = rescale_fun(
            b[:, 1],
            b[:, 0],
            i
        )

        df = pd.concat([df, pd.DataFrame({
            'global_x': points[0],
            'global_y': points[1],
            'global_z': points[2],
            'gene': gene
        })], ignore_index=True)
    return(df)

def _create_rescaling_function(micron_to_mosaic_pixel_transform):
    """
    Here we create a rescaling function that takes three argument: x, y, z.
    These are the coordinates of out point. We will apply the transformation
    defined in 'micron_to_mosaic_pixel_transform' to convert the pixel to micron
    """
    mmpt = pd.read_csv(
        micron_to_mosaic_pixel_transform,
        header=None, 
        sep=' '
    )
    mmpt = np.array(mmpt)

    def rescale_fun(x,y,z):
        z = np.resize(z, len(x)) 
        points = np.array([x,y,z])
        # coordinates to pixel
        points = (points.T - np.append(mmpt[0:2,2], 0)) / np.diag(mmpt)
        return(points.T)
    
    return(rescale_fun)



