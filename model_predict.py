import numpy as np
import tensorflow as tf


from keras.preprocessing.image import ImageDataGenerator

model_1 = tf.keras.models.load_model("./final_model_new.h5")



batch_size = 128


def GetClassNames():
    test_preprocess = ImageDataGenerator(rescale=1 / 255.0)
    img_size = 224
    test_data = test_preprocess.flow_from_directory(
        directory=r"./class_names",
        target_size=(img_size, img_size),
        color_mode="rgb",
        batch_size=batch_size,
        class_mode="categorical",
        shuffle=False,  # Set this to False for test data
        seed=42
    )

    class_labels = list(test_data.class_indices.keys())
    return class_labels


from PIL import Image


def vegetable_predict(class_labels, img_path):
    img_size = 224
    img = Image.open(img_path)
    img = img.resize((img_size, img_size))
    img = np.array(img) / 255.0  # Rescale the image
    img = np.expand_dims(img, axis=0)
    prediction = model_1.predict(img)
    predicted_label = class_labels[np.argmax(prediction)]
    
    return class_labels.index(predicted_label) + 1
