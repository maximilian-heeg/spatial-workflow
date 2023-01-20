from skimage import morphology
import matplotlib.pyplot as plt
import numpy as np

def tophat(imgs, tophats, figsize=None, show=True):
    """Plot the results before and after tophat

    Args:
        imgs (Dict): Dict of images
        tophats (Dict): Dict of images after tophat filter
        figsize (tuple, optional): Figure size. Defaults to None.
        show (bool, optional): Defaults to True.
    """
    fig = plt.figure(figsize=figsize)
    total_layers = len(imgs)
    for (i, img), (_, tophat) in zip(imgs.items(), tophats.items()):
        l = list(imgs).index(i)
        ax1 = plt.subplot(total_layers, 3, l*3 + 1)
        ax2 = plt.subplot(total_layers, 3, l*3 + 2)
        ax3 = plt.subplot(total_layers, 3, l*3 + 3)
        ax1.set_axis_off()
        ax2.set_axis_off()
        ax3.set_axis_off()
        if l == 0:
            ax1.set_title('Original')
            ax2.set_title('White tophat')
            ax3.set_title('Complementary')
        else:
            ax1.set_title('')
            ax2.set_title('')
            ax3.set_title('')
        ax1.imshow(img, cmap='gray')
        ax2.imshow(tophat*10, cmap='gray')
        ax3.imshow(img - tophat, cmap='gray')
    plt.tight_layout()
    if show:
        fig.show()
    return(fig)