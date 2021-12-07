import numpy as np
import cv2 as cv
import base64

def nilaiPOC(value):
    arrValue = value.split(",")

    tempFrame = []
    temp = []
    x = 6
    y = 3
    box = 1


    decoded_data1 = base64.b64decode(arrValue[0])
    decoded_data2 = base64.b64decode(arrValue[1])

    np_data1 = np.fromstring(decoded_data1, np.uint8)
    np_data2 = np.fromstring(decoded_data2, np.uint8)

    img1 = cv.imdecode(np_data1,cv.IMREAD_UNCHANGED)
    img1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    img1_result = cv.resize(img1, (600, 300))
    img1_new = np.uint8([[[0, 0, 0]]])

    img2 = cv.imdecode(np_data2,cv.IMREAD_UNCHANGED)
    img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    img2_result = cv.resize(img2, (600, 300))
    img2_new = np.uint8([[[0, 0, 0]]])

    for k in range(0, 2):
        for i in range(0, y):
            for j in range(0, x):
                if k == 0:
                    img1_new = cv.rectangle(img1_result, (0, i * 100),
                                        ((j + 1) * 100, (i + 1) * 100), (0, 0, 0), 1)
                    cropped_box = img1_new[i * 100:(i + 1) * 100, j * 100: (j + 1) * 100]

                if k == 1:
                     img2_new = cv.rectangle(img2_result, (0, i * 100),
                                         ((j + 1) * 100, (i + 1) * 100), (0, 0, 0), 1)
                     cropped_box = img2_new[i * 100:(i + 1) * 100, j * 100: (j + 1) * 100]

                tempFrame.append(cropped_box)
                temp.append(cropped_box)

    # end of preprocessing
    # calculation
    tempArray = np.array(temp)
    tempFrameArray = np.array(tempFrame)
    boxFrame = x * y
    idx = boxFrame
    nilai = 0
    totalBox = 0
    idxLast = boxFrame
    totalnilainol = 0
    tempCor = []
    box = 1

    # POC method
    for i in range(0, tempFrameArray.shape[0]):
        if i == idxLast:
            idxLast += boxFrame

        if idx < tempFrameArray.shape[0]:
            frameA = tempFrameArray[i]
            frameB = tempFrameArray[idx]

            G_a = np.fft.fft2(frameA)
            G_b = np.fft.fft2(frameB)
            conj_b = np.ma.conjugate(G_b)
            R = G_a * conj_b
            R /= np.absolute(R)
            arr = R[R >= 0]
            r = np.array(arr.min())
            o = r.real
            p = float(o)
            q = round(p, 4)

            corImage = q

            print("box :{} : {}".format(box, corImage))

            tempCor.append(corImage)

            if corImage != 1:
                nilai += corImage
                totalBox += 1

            if corImage == 0:
                totalnilainol += 1

        idx += 1
        box += 1

    # end of POC method


    tempCor = np.array(tempCor)
    tempCor = tempCor.reshape((-1, boxFrame))
    data = []

    for i in range(0, tempCor.shape[0]):
        idx = []
        for j in range(0, tempCor.shape[1]):
            if tempCor[i, j] != 1:
                idx.append(j)
        if len(idx) > 0:
            for k in range(len(idx)):
                if idx[k] not in data:
                    data.append(idx[k])

    banyak = len(data)

    if totalBox == 0:
        rerata = 0
        rerata = round(rerata, 5)
        totalnilainol = 0
    else :
        rerata = nilai / totalBox
        rerata = round(rerata, 5)
        totalnilainol = round((totalnilainol / totalBox) * 100, 3)

    result = "rata-rata : {}, banyak box: {}, persentase 0 : {}". format(rerata, banyak, totalnilainol)
    # end of calculation

    return result