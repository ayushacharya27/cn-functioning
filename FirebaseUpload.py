import firebase_admin
import cv2
import time
from firebase_admin import credentials , storage
from datetime import datetime
import os

Time_Interval = 10 #Change the Interval as per your need

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\DELL\Desktop\CN_PROJECT\computernetowrk-d0548-firebase-adminsdk-gedtp-dd07cd9ec2.json")

firebase_admin.initialize_app(cred, {
    'storageBucket': 'computernetowrk-d0548.appspot.com'
})

def upload_snapshot():
    cap = cv2.VideoCapture(0)
    ret , frame = cap.read()
    filename = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(filename , frame)

    bucket = storage.bucket()
    blob = bucket.blob(f"snapshots/{filename}")
    blob.upload_from_filename(filename)

    print("File Uploaded Succesfully")
    os.remove(filename)
    print("File removed Locally")

while True:
    upload_snapshot()
    time.sleep(Time_Interval)
