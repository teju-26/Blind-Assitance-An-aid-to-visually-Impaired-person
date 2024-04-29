import cv2
import imutils
import RPi.GPIO as GPIO
import time
from gtts import gTTS
import os
from picamera import PiCamera

# Initialize the ultrasonic sensor pins
TRIG_PIN = 27
ECHO_PIN = 17

# Initialize the GPIO settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialize the camera
camera = PiCamera()

# Initialize the object detection model (adjust paths as needed)
classNames = []
classFile = "/home/vcet/Desktop/Object_Detection_Files/coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/vcet/Desktop/Object_Detection_Files/frozen_inference_graph.pb"
weightsPath = "/home/vcet/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Function to measure distance using the ultrasonic sensor
def measure_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    
    return distance

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text)
    tts.save("voice.mp3")
    os.system("mpg321 voice.mp3")

while True:
    # Capture a frame from the camera
    camera.capture('image.jpg')

    # Read the captured image
    frame = cv2.imread('image.jpg')

    # Resize the frame for faster processing
    frame = imutils.resize(frame, width=400)

    # Perform object detection
    classIds, confs, bbox = net.detect(frame, confThreshold=0.45, nmsThreshold=0.2)
    
    # Measure distance using the ultrasonic sensor
    distance = measure_distance()

    # Process only the object with the highest confidence score
    if len(classIds) > 0:
        max_conf_index = confs.argmax()  # Get the index of the object with the highest confidence
        classId = classIds[max_conf_index]
        confidence = confs[max_conf_index]
        box = bbox[max_conf_index]
        className = classNames[classId - 1]
        
        cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
        cv2.putText(frame, f"{className}: {confidence:.2f}", (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Combine detected object and distance information into a single message
        message = f"{className} detected. Distance: {distance} centimeters."
        
        # Use text-to-speech to output the message
        text_to_speech(message)

    # Display distance on the frame
    cv2.putText(frame, f"Distance: {distance} cm", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Object Detection", frame)

    # Exit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up GPIO and release the camera
GPIO.cleanup()
camera.close()
cv2.destroyAllWindows()
  

