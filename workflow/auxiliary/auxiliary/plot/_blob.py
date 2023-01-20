from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

def blob(imgs, blobs, figsize=None, show=True, multiplier=20, cmap='inferno'):
    """ Plot the detected Blobs on a image

    Args:
        imgs (dict): Either original images or after tophat filter
        blobs (dict): Result of process.blob
        figsize (tuple, optional): Figuresize. Defaults to None.
        show (bool, optional): Show the plot? Defaults to True.
        multiplier (int, optional): Intensify the colors of the image by multiplication. Defaults to 20.
        cmap (str, optional): Color map. Defaults to 'inferno'.
    """
    fig = plt.figure(figsize=figsize)
    total_layers = len(imgs)
    for (i, img), (_, blob) in zip(imgs.items(), blobs.items()):
        l = list(imgs).index(i)
        blob = np.copy(blob)

        blob[:, 2] = blob[:, 2] * sqrt(2)

        ax1 = plt.subplot(total_layers, 2, l*2 + 1)
        ax2 = plt.subplot(total_layers, 2, l*2 + 2)

        if l == 0:
            ax1.set_title('Image')
            ax2.set_title('Image with blobs')
        else:
            ax1.set_title('')
            ax2.set_title('')

        ax1.imshow(img*multiplier, cmap=cmap)
        ax2.imshow(img*multiplier, cmap=cmap)
        # for b in blob:
        #     y, x, r = b
        #     c = plt.Circle((x, y), r, color='green', linewidth=1, fill=False)
        #     ax2.add_patch(c)
        ax2.scatter(blob[:,1], blob[:,0], s=blob[:,2]/5, color='green', alpha=.7)
        ax1.set_axis_off()
        ax2.set_axis_off()
    if show:
        fig.show()
    return(fig)