from flask import Flask, request, jsonify
from pymongo import MongoClient
from model import process_image
import base64
from cryptography.fernet import Fernet
import threading
import time
from bson import ObjectId
from datetime import datetime
from flask_cors import CORS # type: ignore
import numpy as np
import cv2
import asyncio

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB configuration
client = MongoClient("mongodb://172.20.240.39:27017/")
db = client["Store"]
order_collection = db["orders"]
image_collection = db["image_data"]

# Initialize a variable to keep track of the current order number and date
current_date = datetime.now().date()
order_num = 0

@app.route('/order', methods=['POST'])
def create_order():
    global order_num, current_date
    try:
        # Parse JSON input
        order_data = request.get_json()
        if not order_data:
            return jsonify({"error": "Invalid JSON input"}), 400

        # Check if the date has changed and reset the order number if necessary
        today = datetime.now().date()
        if today != current_date:
            current_date = today
            order_num = 0

        # Increment the order number
        order_num += 1

        # Add the order number, hasConsented, and isActive fields to the order data
        order_data['orderNum'] = order_num
        order_data['hasConsented'] = order_data.get('hasConsented', False)
        order_data['isActive'] = True
        order_data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert into MongoDB
        result = order_collection.insert_one(order_data)

        return jsonify({
            "message": "Order saved",
            "order_id": str(result.inserted_id),
            "orderNum": order_num
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-orders', methods=['GET'])
def get_inactive_orders():
    try:
        # Query MongoDB for documents where isActive is False
        inactive_orders = list(order_collection.find({"isActive": True}))
        
        # Convert ObjectId to string for JSON serialization
        for order in inactive_orders:
            order["_id"] = str(order["_id"])
        
        return jsonify(inactive_orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/complete-order', methods=['POST'])
def complete_order():
    try:
        # Parse JSON input
        data = request.get_json()
        if not data or 'orderId' not in data:
            return jsonify({"error": "Invalid JSON input or missing orderId"}), 400

        # Update the isActive field to False for the given order_id
        result = order_collection.update_one(
            {"_id": ObjectId(data['orderId'])},
            {"$set": {"isActive": False}}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Order not found"}), 404

        return jsonify({"message": "Order completed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Generate a key for encryption (in a real-world scenario, store this securely)
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

@app.route('/process-facial-data', methods=['POST'])
def process_facial_data():
    print("Entered the flow")
    try:
        # Check if both image and string data are provided
        if 'image' not in request.files or 'orderId' not in request.form:
            return jsonify({"error": "Image file and data string are required"}), 400

        # Retrieve the image and string data
        image = request.files['image']
        orderId = request.form['orderId']

        # Read and encrypt the image
        print("Reading the image")
        image_bytes = image.read()

        print("Converting the image to numpy array")
        np_arr = np.frombuffer(image_bytes, np.uint8)
        print("Decoding the image")
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


        print("Ecrypting the image")
        encrypted_image = cipher.encrypt(image_bytes)

        # Save the encrypted image to a different MongoDB collection
        image_collection = db["image_data"]
        image_record = {
            "encrypted_image": base64.b64encode(encrypted_image).decode('utf-8'),
            "orderId": orderId
        }
        print("Saving the image to MongoDB")
        image_collection.insert_one(image_record)

        # Call the process_image function from model.py with the original image
        async def process_and_update_image():
            print("Processing the image")
            result = await asyncio.to_thread(process_image, img)
            # Update the confidenceScore field in the database for the corresponding order_number
            order_collection.update_one(
                {"_id": ObjectId(orderId)},
                {"$set": {"satisfactionScore": float(result)}}
            )

        asyncio.run(process_and_update_image())

        return jsonify({"message": "Processing successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/satisfaction-data', methods=['GET'])
def get_satisfaction_data():
    try:
        # Query the image_data collection for date and confidenceScore fields
        satisfaction_data = list(order_collection.find(
            {"isActive": False, "hasConsented": True},
            {"_id": 0, "date": 1, "satisfactionScore": 1}
        ))

        return jsonify(satisfaction_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_old_images():
    while True:
        try:
            # Get the current time
            current_time = time.time()

            # Query for images older than 24 hours (86400 seconds)
            old_images = image_collection.find({"timestamp": {"$lt": current_time - 86400}})

            # Delete the old images
            for image in old_images:
                image_collection.delete_one({"_id": ObjectId(image["_id"])})

        except Exception as e:
            print(f"Error deleting old images: {e}")

        # Sleep for an hour before checking again
        time.sleep(3600)

# Add a timestamp field when saving images
@app.before_request
def add_timestamp_to_images():
    if request.endpoint == 'process_facial_data' and request.method == 'POST':
        db["image_data"].update_many({}, {"$set": {"timestamp": time.time()}})

# Start the background thread for deleting old images
threading.Thread(target=delete_old_images, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)