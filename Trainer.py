import cv2
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import os

filename = input("Input image name: ")
if os.path.exists(filename) == False:  # check whether the file exists
    print("No this image named by " + filename)
    exit(0)

img = cv2.imread(filename)
noiseMask = img != 0
img = img / 255 # normalization
radius = 8
dupImg = np.copy(img) # get a duplicate file of an image
rows, cols, channel = img.shape # get the info of file
Count = 0
Last = 0
for row in range(rows):
    for col in range(cols):
        rowl = row - radius # get the neighborhood pixel
        rowr = row + radius
        coll = col - radius
        colr = col + radius

        if rowl < 0:
            rowl = 0
            rowr = rowl + 2 * radius
        if rowr >= rows:
            rowr = rows - 1
            rowl = rowr - 2 * radius

        if coll < 0:
            coll = 0
            colr = coll + 2 * radius
        if colr >= cols:
            colr = cols - 1
            coll = colr - 2 * radius


        for chan in range(channel):
            if noiseMask[row, col, chan] != 0.:
                continue
            x_train = []
            y_train = []
            for i in range(rowl, rowr):
                for j in range(coll, colr):
                    if noiseMask[i, j, chan] == 0. or (i == row and j == col):
                        continue
                    x_train.append([i, j])
                    y_train.append([img[i, j, chan]])
            if len(x_train) == 0:
                continue
            # quadratic linear regression
            quadratic = PolynomialFeatures(degree=3)
            x_train_quadratic = quadratic.fit_transform(x_train)
            regressor_quadratic = linear_model.LinearRegression()
            regressor_quadratic.fit(x_train_quadratic, y_train)
            # predict
            test = quadratic.transform([[row, col]])
            dupImg[row, col, chan] = regressor_quadratic.predict(test)

        Count += 1
        rate = int(float(Count) / rows / cols * 100)
        if rate != Last :
            print(filename + " fix:" + str(rate) + "%")
            Last = rate

dupImg *= 255 # restore the image
cv2.imwrite("3150102193_"+filename, dupImg)
