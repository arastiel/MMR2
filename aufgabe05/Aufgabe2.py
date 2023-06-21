import numpy as np
import cv2 as cv
import random


#img = cv.imread("./CleanWindows.png")
img = cv.imread("./CurvyWindows.png")
#img = cv.imread("./real.jpg")

height = np.shape(img)[0]
width = np.shape(img)[1]


def get_patches(img, w):
    patches = []
    for i in range(np.shape(img)[0] - w):
        for j in range(np.shape(img)[1] - w):
            patches.append(img[i:i+w, j:j+w])

    return patches, w

test, w = get_patches(img, 32)
print(np.shape(img))
print(len(test))
# test[y][x]

'''
for i in test:
    cv.imshow(str(i), i)

cv.imshow("teslt", test[1])
'''

def test_random_patches(img, w, num_tests, percent):

    patches, w = get_patches(img, w)
    og_img = img.copy()

    #dict_equal = dict()
    
    for r_patch in range(num_tests):
        r_patch_index = random.randint(0, len(patches)-1)

        test = patches[r_patch_index]
        #cv.imshow("og_img" + str(r_patch), og_img)
        cv.imshow("testpatch" + str(r_patch), test)
        #print(r_patch_index)
        min_vals = []
        #min_val = (np.infty, 0, 0)
        #min_vals.append(min_val)
        for i in range(np.shape(img)[0] - w):
            sum_value = 0
            for j in range(np.shape(img)[1] - w):
                value = np.sum(np.subtract(test, img[i:i+w, j:j+w]) ** 2)
                min_vals.append((value, i, j))


        print(np.amax(min_vals))
        threshold = np.amax(min_vals)
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

        for x in min_vals:
            if x[0] < percent*threshold:
                og_img[x[1]:x[1]+w, x[2]:x[2]+w] = color

   #            #print(value)
   #            if value < min_val[0]:
   #                min_vals = []
   #                min_val = (value, i, j)
   #                min_vals.append(min_val)
   #            if value == min_val[0]:
   #                min_vals.append((value, i, j))
   #            sum_value += value
   #        dict_equal[r_patch_index] = sum_value
   #
   #    color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
   #    for x in min_vals:
   #        og_img[x[1]:x[1]+w, x[2]:x[2]+w] = color
   #
    
    cv.imshow("test", og_img)


test_random_patches(img, 80, 2, 0.6)
#print(test[0])

#cv.imshow("test", img)

cv.waitKey(0)