from flask import Flask, request, render_template, redirect, url_for
import cv2
import numpy as np
import tensorflow as tf

app = Flask(__name__)
model = tf.keras.models.load_model('license_plate_model.h5')

def preprocess_image(image):
    image = cv2.resize(image, (150, 150))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            image = np.frombuffer(file.read(), np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            processed_image = preprocess_image(image)
            prediction = model.predict(processed_image)
            label = 'License Plate Detected' if prediction[0] > 0.5 else 'No License Plate'
            
            if prediction[0] > 0.5:
                # Draw a green border around the image for positive cases
                h, w, _ = image.shape
                cv2.rectangle(image, (10, 10), (w-10, h-10), (0, 255, 0), 2)
            
            cv2.imwrite('static/result.jpg', image)
            return render_template('result.html', label=label)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
