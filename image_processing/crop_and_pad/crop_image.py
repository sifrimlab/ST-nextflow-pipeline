
##concept here is to crop 200 pixels in both axes, but the needs to become 50 on each side obviously
##WATCH OUT this is written for windows filenames, so you have to change the backslashed to forward slashes in unix based systems
import cv2.cv2
import os

os.chdir("T:\\spatial1\\starfish_format\\1")
def crop(filename, resolution_x, resolution_y, output_dir):
    if not output_dir.endswith("\\"):
        output_dir = output_dir + r"\\"
    if not os.path.exists(output_dir):
        raise Exception("Output directory does not exist!")
    img = cv2.cv2.imread(filename, cv2.cv2.IMREAD_GRAYSCALE)
    wid = img.shape[1] 
    hgt = img.shape[0] 
    print(str(wid) + "x" + str(hgt))
    if resolution_x > wid:
        raise Exception("x is larger or equal than the width of the image")
    if resolution_y > hgt:
        raise Exception("y is larger or equalthan the width of the image")
    ##calcs
    difference_x = wid - resolution_x
    difference_y= hgt - resolution_y
    if difference_x % 2 !=0:
        print("""Warning: your resolution was not divisible by 2, so your requested resolution was subtracked by 1.
    This May cause unforseen weird crop behaviour""")
        difference_x = difference_x-1
    if difference_y % 2 !=0:
        print("""Warning: your resolution was not divisible by 2, so your requested resolution was subtracked by 1.
    This May cause unforseen weird crop behaviour""")
        difference_y = difference_y-1
    target_x = int(difference_x/2)
    target_y = int(difference_y/2)
    crop_img = img[target_y:hgt-target_y,target_x:wid-target_x].copy()
    wid2 = crop_img.shape[1] 
    hgt2 = crop_img.shape[0] 
    print(str(wid2) + "x" + str(hgt2))
    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)
    basename = os.path.basename(filename)
    cv2.cv2.imwrite(f"{output_dir}{basename}_cropped.tif", crop_img)


crop("T:\\spatial1\\starfish_format\\1\\c3.tif", 6758,22397, r"T:\spatial1\starfish_format\resolution_fixing")