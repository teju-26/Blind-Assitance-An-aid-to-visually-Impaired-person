#steps to create THIS PROJ USING 
1. Raspberry Pi
2. pi camera
3. Ultrasonic sensor
4. SD card (16 gb)

According to the interface diagrm do the connections 

#Setup of raspberry pi:

1. Add raspberry pi os into the SD card using card reader get it from the offical website of pi
 https://www.raspberrypi.com/software/operating-systems/ (64 bit os)

 2. Compelte the isntalltion part of os and then login as new user into the pi system with your usernmae and password.
 3. Download this project from chrome of Pi
 4. Unzip the file

#Steps to run the file 

A. Camera Setup:
  - check the camera using the following command:
    1. aattch pi camera into the camera module of the pi nitley.
    2. Check the camera permission using 
      - sudo raspi -config 
      -> Go to Interfacing Options and enable
    3. Enable the camera in python by typing :  
       raspistill -o image.jpg
    4. check the output of the camera .


    