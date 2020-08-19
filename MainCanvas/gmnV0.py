import numpy as np
from PIL import Image, ImageOps
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img


def reformatJSON(drawingJSON):

    position = drawingJSON[14:-2].replace('{', '').replace('}', '').replace('"', '') \
        .replace(':', '').replace(',', '').replace('x', ' ').replace('y', ' ').split(' ')
    position = [int(i) for i in position]
    position = np.array(position).reshape((int(len(position) / 2), 2))

    w, h = 280, 280
    output = np.zeros((h, w, 3), dtype=np.uint8)

    for element in position:
        for i in range(25):
            output[element[0]:element[0] + i, element[1]:element[1] + i] = [255, 255, 255]

    img = Image.fromarray(output, 'RGB').convert('1')
    img_mirror = ImageOps.mirror(img)
    transposed = img_mirror.transpose(Image.ROTATE_90)
    return transposed


def predictwithkeras(image):
    img_width, img_height = 28, 28
    test_model = load_model("MainCanvas/static/results/conv2D_classifier.h5")
    if type(image) == str:
        image = load_img(image, False, target_size=(img_width, img_height), color_mode="grayscale")
    else:
        image = image.resize((28, int(28 * (img_height / img_width))) if img_width < img_height else (
            int(28 * (img_width / img_height)), 28))

    x = img_to_array(image)
    x = np.expand_dims(x, axis=0)

    #preds = test_model.predict_classes(x)
    #prob = test_model.predict_proba(x)
    prob = test_model.predict(x)
    return int(np.where(prob[0] == np.amax(prob[0]))[0]), max(prob[0])
