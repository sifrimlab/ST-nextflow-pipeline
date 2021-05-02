from skimage import io
import matplotlib.pyplot as plt
from modules.convolving import gaussianPass
from modules.deconvolving import createGaussianKernel, deconvolvePSF, calculateKernelSize


if __name__=="__main__":
    image_path = "/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks_cropped/convolving_test.tif"
    img = io.imread(image_path)

    fig,axs = plt.subplots(1,3)
    axs[0].imshow(img, cmap="gray")
    axs[0].set_title("original")

    convolved = gaussianPass(image_path, 3)
    io.imsave("convolved.tif", convolved)
    axs[1].imshow(convolved, cmap="gray")
    axs[1].set_title("convolved")

    kernel_size = calculateKernelSize(2)
    kernel = createGaussianKernel((kernel_size,kernel_size), 2)
    deconvolved = deconvolvePSF("convolved.tif", kernel, 15)
    axs[2].imshow(deconvolved, cmap="gray")
    axs[2].set_title("deconvolved")
    plt.show()
