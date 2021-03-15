from image_processing.merging.merge_images import createComposite
from skimage import io
img_list= ["/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks/MERFISH_primary-0001.tif","/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks/MERFISH_primary-0005.tif", "/media/david/Puzzles/starfish_test_data/MERFISH/seperate_stacks/MERFISH_primary-0007.tif"]

io.imsave("test.tiff", createComposite(img_list[0], img_list[1]))