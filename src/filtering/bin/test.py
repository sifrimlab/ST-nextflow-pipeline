from skimage import io
import matplotlib.pyplot as plt
from modules.convolving import gaussianPass
from modules.deconvolving import createGaussianKernel, deconvolvePSF, calculateKernelSize
import numpy as np
from skimage.restoration import richardson_lucy


if __name__=="__main__":
    image_path = "/media/nacho/Puzzles/starfish_test_data/MERFISH/seperate_stacks/results_nacho_deconvolving/filtered/merfish_10_padded_tiled_3_filtered.tif"
    img = io.imread(image_path)

    fig,axs = plt.subplots(1,3)
    axs[0].imshow(img, cmap="gray")
    axs[0].set_title("original")

    convolved = gaussianPass(image_path, 3)
    # io.imsave("convolved.tif", convolved)
    axs[1].imshow(convolved, cmap="gray")
    axs[1].set_title("convolved")

    kernel_size = calculateKernelSize(2)
    kernel = createGaussianKernel((kernel_size,kernel_size), 2)
    #deconvolved = restoration.richardson_lucy(camera, psf, 5, clip=False)
    # psf = np.ones((5, 5)) / 25
    convolved += np.amax(convolved) * 1E-5
    deconvolved = richardson_lucy(convolved, kernel, 15)
    axs[2].imshow(deconvolved, cmap="gray")
    axs[2].set_title("deconvolved")
    plt.show()
