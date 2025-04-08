import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Loading the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the color image
# image_path = 'captured_image.jpg'  # Replace with the path to your image

def process_image(image):
    print("Processing Started")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # Detect faces
    print("Detecting faces")
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

    # Display the detected faces (optional)
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # # Save/Show the image with highlighted faces
    # cv2.imshow('Detected Faces', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Process only the first detected face (or iterate for multiple faces)
    if len(faces) > 0:
        # Find the face closest to the camera (largest area)
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])  # rect[2] * rect[3] is the area (w * h)
        x, y, w, h = largest_face  # Coordinates of the largest face
        face = gray_image[y:y+h, x:x+w]  # Crop the face
        face = cv2.resize(face, (48, 48))  # Resize to 48x48 pixels
        face = face / 255.0  # Normalize the values
        face = np.stack((face,)*3, axis=-1)  # Convert grayscale to 3-channel format
        face = face.reshape(1, 48, 48, 3)  # Adjust dimensions for the model

    # Load the trained model
    model = load_model('model.h5')

    # Make the prediction
    predictions = model.predict(face)[0]  # Get the prediction probabilities for each emotion

    # Map the predictions to the corresponding emotions
    emotions = {
        'angry': predictions[0],
        'disgust': predictions[1],
        'fear': predictions[2],
        'happy': predictions[3],
        'sad': predictions[4],
        'surprise': predictions[5],
        'neutral': predictions[6]
    }

    print("Emotion probabilities:", emotions)

    # Calculate a "satisfaction" score based on weighted emotion probabilities
    satisfaction = (
        emotions['happy'] * 1.5 +
        emotions['neutral'] * 0.8 +
        emotions['surprise'] * 0.6 -
        emotions['angry'] * 1.0 -
        emotions['sad'] * 0.9 -
        emotions['disgust'] * 1.0 -
        emotions['fear'] * 0.7
    )

    # Normalize the satisfaction score to a 0-100 scale
    normalized = max(0, min(100, (satisfaction + 1) * 50))
    satisfaction_score = round(normalized, 1)

    return satisfaction_score

def train_model():
    # Diretórios para o dataset
    train_dir = 'FER/train'
    val_dir = 'FER/test'

    # Pré-processamento das imagens
    datagen = ImageDataGenerator(rescale=1./255)

    train_data = datagen.flow_from_directory(
        train_dir,
        target_size=(48, 48),
        color_mode='grayscale',
        batch_size=64,
        class_mode='categorical'
    )

    val_data = datagen.flow_from_directory(
        val_dir,
        target_size=(48, 48),
        color_mode='grayscale',
        batch_size=64,
        class_mode='categorical'
    )

    # Construindo o modelo CNN
    model = Sequential([
        Conv2D(64, (3, 3), activation='relu', input_shape=(48, 48, 1)),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(train_data.num_classes, activation='softmax')
    ])

    # Compilando o modelo
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Treinando o modelo
    model.fit(train_data, validation_data=val_data, epochs=10, use_multiprocessing=True, workers=4)

    # Salvando o modelo treinado
    model.save('emotion_recognition_model.h5')
