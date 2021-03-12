from image_similarities import SimilarHistogram, EuclideanImageSimilarity, MeanSquaredErrorImageSimilarity, StructuralSimilarity, ORBsimilarity


##putting data into memory

##reference tiles
ref_good_busy = "./imgs/ref_tile13.tif"
ref_good_not_busy="./imgs/ref_tile24.tif"
ref_medium = "./imgs/ref_tile12.tif"
ref_bad = "./imgs/ref_tile15.tif"
ref_dir = {"good_busy": ref_good_busy, "good_not_busy": ref_good_not_busy, "medium": ref_medium,"bad": ref_bad}

##iss tiles of iss1 channel2
iss_good_busy= "./imgs/r1_c2_tile13.tif"
iss_good_not_busy="./imgs/r1_c2_tile24.tif"
iss_medium = "./imgs/r1_c2_tile12.tif"
iss_bad = "./imgs/r1_c2_tile15.tif"
iss_dir = {"good_busy": iss_good_busy, "good_not_busy":iss_good_not_busy, "medium":iss_medium, "bad":iss_bad}

##registered
registered_good_busy="./imgs/registered_with_simpleITK/registered_withSimpleITK_tile13.tif"
registered_good_not_busy="./imgs/registered_with_simpleITK/registered_withSimpleITK_tile24.tif"
registered_medium="./imgs/registered_with_simpleITK/registered_withSimpleITK_tile12.tif"
registered_bad="./imgs/registered_with_simpleITK/registered_withSimpleITK_tile15.tif"
registered_dir = {"good_busy": registered_good_busy, "good_not_busy":registered_good_not_busy, "medium":registered_medium, "bad": registered_bad}

##functionality

#euclidean:
# for key,value in ref_dir.items():
#     print(key, EuclideanImageSimilarity(value, iss_dir[key]))
##From this we can see that a super bad tile doesn't actually get flagged by this, because it contains no signal to "shake up" the distances
##also: medium and good_busy are extremely similar, meaning that the smear also does not influence the similarity enough.

#MSE
#lower = more similar
# for key,value in ref_dir.items():
#     print(key, MeanSquaredErrorImageSimilarity(value, iss_dir[key]))
##busy is again badly represented, mostly because large distances between pixel intensities do not necessarily mean the contents of the images are dramatically different.

#SSIM
#SSIM value can vary between -1 and 1, where 1 indicates perfect similarity.
# for key,value in ref_dir.items():
#     print(key, StructuralSimilarity(value, iss_dir[key]))
##weird scale, don't really understand this yet

##ORB
# for key, value in ref_dir.items():
#     print(key, ORBsimilarity(value, iss_dir[key], 50))
##does not work at all, didn't expect it to either, keypoints work weird.


for key,value in ref_dir.items():
    print(key +  "\t\t non-registered: " + "\t" +  str(StructuralSimilarity(value, iss_dir[key])) + "\t registered: " +  str(StructuralSimilarity(value, registered_dir[key])))