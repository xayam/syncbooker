import numpy as np
from sklearn.preprocessing import MinMaxScaler
from PIL import Image


def count_of_eps(inp, a, b):
    delta_range = range(-6, 7)
    delta = [(a + delta_a, b + delta_b) for delta_a in delta_range for delta_b in delta_range]
    result = 0
    for d in delta:
        try:
            if inp[d[0]][d[1]] == 255:
                result += 1
        except IndexError:
            pass
    return result


def filtered_main_diag(filename):
    min_max_scaler = MinMaxScaler(feature_range=(0, 1))
    img = np.asarray(Image.open(filename))
    res = np.zeros_like(img)
    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i, j] == 255:
                res[i, j] = count_of_eps(img, i, j)
    res_min_max = min_max_scaler.fit_transform(res)
    for i in range(len(res_min_max)):
        for j in range(len(res_min_max[i])):
            if res_min_max[i, j] < 0.7:
                res_min_max[i, j] = 0
    return res_min_max
