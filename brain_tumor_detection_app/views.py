from django.shortcuts import render
from django.http import HttpResponse
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from io import BytesIO

def predict_image(request):
    if request.method == 'POST':
        model_path = 'D:/vaigaivalley/Projectcentre/roshan FP/brain_tumor_detection_project/brain_tumor_detection_app/braintumor_11508211086.h5'
        class_path = 'D:/vaigaivalley/Projectcentre/roshan FP/brain_tumor_detection_project/brain_tumor_detection_app/classes.names'
        
        # Load model
        model = tf.keras.models.load_model(model_path, custom_objects={'KerasLayer': hub.KerasLayer})
        input_shape = model.input_shape[1:]

        # Image preprocessing
        uploaded_image = request.FILES['image_path']  # Getting the uploaded image
        img_content = uploaded_image.read()  # Reading the image content
        img = tf.keras.preprocessing.image.load_img(BytesIO(img_content), target_size=input_shape)  # Loading the image from content
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = img / 255

        # Prediction
        result = model.predict(img)
        lines = [line.replace("\n", "") for line in open(class_path, "r").readlines()]
        classes = {i: lines[i] for i in range(len(lines))}
        prediction_probability = {i: j for i, j in zip(classes.values(), result.tolist()[0])}

        # Check if 'yes' probability is higher than a threshold
        threshold = 0.5  # Adjust threshold as needed
        if prediction_probability.get("yes", 0) > threshold:
            show = "Brain tumor detected with probability: {:.2f}%".format(prediction_probability.get("yes", 0) * 100)
        else:
            show = "No brain tumor detected"

        return render(request, 'index.html', {'prediction': show})
    else:
        return render(request, 'index.html')  