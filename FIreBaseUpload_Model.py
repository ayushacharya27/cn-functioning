import cv2
import firebase_admin

from inference_sdk import InferenceHTTPClient
import sys
import base64
import time
from datetime import datetime
import os
from firebase_admin import credentials , storage

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\DELL\Desktop\CN_PROJECT\computernetowrk-d0548-firebase-adminsdk-gedtp-dd07cd9ec2.json")

firebase_admin.initialize_app(cred, {
    'storageBucket': 'computernetowrk-d0548.appspot.com'
})

def initialize_client():
    print("\nInitializing Roboflow client...")
    return InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="g0jdpuOtT3tvqoBi70aV"
    )

def initialize_camera():
    cap = cv2.VideoCapture(0)
    
    
    
    if not cap.isOpened():
        raise RuntimeError("Failed to open camera")
    
    ret, test_frame = cap.read()
    if not ret or test_frame is None:
        cap.release()
        raise RuntimeError("Camera opened but failed to read frame")
        
    print("Camera successfully initialized!")
    print(f"Resolution: {test_frame.shape[1]}x{test_frame.shape[0]}")
    return cap

def encode_image(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    img_str = base64.b64encode(buffer).decode('utf-8')
    return img_str

def draw_detections(frame, detections):
    # Draw detection boxes and labels on the frame
    annotated_frame = frame.copy()
    for detection in detections:
        # The center coordinates
        center_x = int(detection['x'])
        center_y = int(detection['y'])
        width = int(detection['width'])
        height = int(detection['height'])
        class_name = detection['class']
        confidence = detection['confidence']
        
        # Calculate the top-left corner coordinates from the center
        x1 = center_x - width // 2
        y1 = center_y - height // 2
        x2 = center_x + width // 2
        y2 = center_y + height // 2

        # Draw the bounding box
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Prepare and draw label
        label = f"{class_name}: {confidence:.2f}"
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), (x1 + label_size[0], y1), (0, 255, 0), -1)
        cv2.putText(annotated_frame, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    return annotated_frame
'''def verify_detection(){
    cap=initialize_camera()
        
    CLIENT = initialize_client()
    MODEL_ID = "guns-knive-detection/1"
    ret , frame = cap.read()


}'''

def run_detection():
    print("\n=== Weapon Detection System (GUI Mode) ===")
    print("System initialization starting...")
    
    try:
        cap = initialize_camera()
        
        CLIENT = initialize_client()
        MODEL_ID = "guns-knive-detection/1"
        
        cv2.namedWindow('Weapon Detection', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Weapon Detection', 1280, 720)
        
        print("\nSystem ready! Starting detection...")
        print("Press 'q' to quit the program\n")
        
        frame_count = 0
        start_time = time.time()
        last_fps_print = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame")
                break
            
            frame_count += 1
            current_time = time.time()
            fps = frame_count / (current_time - start_time)

            if frame_count % 3 == 0:
                img_str = encode_image(frame)
                result = CLIENT.infer(img_str, model_id=MODEL_ID)
                
                print("API response:", result)  # Print the response for debugging

                if 'predictions' in result and isinstance(result['predictions'], list):
                    if result['predictions']:
                        frame = draw_detections(frame, result['predictions'])
                        filename = f"danger_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        cv2.imwrite(filename, frame)
                        bucket = storage.bucket()
                        blob = bucket.blob(f"danger/{filename}")
                        blob.upload_from_filename(filename)

                        print("File Uploaded Succesfully")
                        os.remove(filename)
                        print("File removed Locally")

                         
                    else:
                        filename = filename = f"snapshots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        cv2.imwrite(filename, frame)
                        bucket = storage.bucket()
                        blob = bucket.blob(f"snapshots/{filename}")
                        blob.upload_from_filename(filename)

                        print("File Uploaded Succesfully")
                        os.remove(filename)
                        print("File removed Locally")

                else:
                    print("Unexpected response format:", result)  # Handle unexpected format

            if current_time - last_fps_print >= 1.0:
                last_fps_print = current_time
                print(f"FPS: {fps:.1f}")
            
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Weapon Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nDetection system stopped by user")
                break
    
    except KeyboardInterrupt:
        print("\nDetection system stopped by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()
        print(f"\nSession Summary:")
        print(f"Total frames processed: {frame_count}")
        if frame_count > 0:
            print(f"Average FPS: {frame_count / (time.time() - start_time):.1f}")

if __name__ == "__main__":
    try:
        run_detection()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
