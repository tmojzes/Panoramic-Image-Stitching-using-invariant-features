from panorama import Panaroma
import imutils
from imutils import paths
import cv2
import argparse
import re

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True,
	help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True,
	help="path to the output image")
args = vars(ap.parse_args())

# #Take picture from folder like: Hill1 & Hill2, scene1 & scene2, my1 & my2, taj1 & taj2, lotus1 & lotus2, beach1 & beach2, room1 & room2

# print("Enter the number of images you want to concantenate:")
# no_of_images = int(input())
# print("Enter the image name in order of left to right in way of concantenation:")
# #like taj1.jpg, taj2.jpg, taj3.jpg .... tajn.jpg
# filename = []

# for i in range(no_of_images):
#     print("Enter the %d image:" %(i+1))
#     filename.append(input())

# grab the paths to the input images and initialize our images list
print("[INFO] loading images...")
imagePaths = list(paths.list_images(args["images"]))
images = []

 
def sorted_nicely(image_list):
    """ Sorts the given iterable in the way that is expected. 
    Required arguments: 
    l -- The iterable to be sorted. 
    """  
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]  
    return sorted(image_list, key = alphanum_key)

imagePaths = sorted_nicely(imagePaths)
# print(imagePaths)

# loop over the image paths, load each one, and add them to our
# images to stitch list
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)

no_of_images = len(imagePaths)
print(no_of_images)
# print(images)


# for i in range(no_of_images):
#     images.append(cv2.imread(filename[i]))

# #We need to modify the image resolution and keep our aspect ratio use the function imutils

# for i in range(no_of_images):
#     images[i] = imutils.resize(images[i], width=400)

# for i in range(no_of_images):
#     images[i] = imutils.resize(images[i], height=400)


panaroma = Panaroma()
if no_of_images==2:
    (result, matched_points) = panaroma.image_stitch([images[0], images[1]], match_status=True)
else:
    (result, matched_points) = panaroma.image_stitch([images[no_of_images-2], images[no_of_images-1]], match_status=True)
    for i in range(no_of_images - 2):
        (result, matched_points) = panaroma.image_stitch([images[no_of_images-i-3], result], match_status=True)

#to show the got panaroma image and valid matched points
# for i in range(no_of_images):
#     cv2.imshow("Image {k}".format(k=i+1), images[i])

# cv2.imshow("Keypoint Matches", matched_points)
# cv2.imshow("Panorama", result)

#to write the images
cv2.imwrite("Matched_points.jpg", matched_points)
cv2.imwrite(args["output"], result)

# cv2.waitKey(0)
cv2.destroyAllWindows()
