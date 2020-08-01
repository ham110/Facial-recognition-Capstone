# Two-factor-Authentication-Door-Lock-System
This work represents all the necessary code to build a reliable two factor door lock authentication system with facial recognition and fingerprint recognition.

What you need to setup the project:
- Microcontroller (tested  on a Raspberry Pi 3B+) + USB module (if needed)
- Webcam
- Electric lock
- R305 Fingerprint sensor
- Transistors/Resistors/Capacitors and a proximity sensor
- RFID interface (Optional)
- Buttons to trigger the fingerprint recognition

The main code is located in src/main.py, setting SETUP_TRAINING=True will use your camera to take pictures of whoever is in front of the camera, will extrapolate images (duplicate the training dataset to obtain a larger set if needed to prototype), and will store the training dataset under data/person1 folder. A Facenet (ref: https://github.com/davidsandberg/facenet) model is then trained using this dataset and imported onto the project.  
The remaining code will then use OpenCV2 for facial detection. Once a face is detected, it will be classified by our trained Facenet model, if the owner of the lock is recognized, the door lock will open.  
  
The fingerprint sensor is able to store up to 1024 fingerprints, whom are stored and classified in an internal database.  
  
Below is an architecture diagram of the whole system:  
![Alt text](architecture_diagram.png?raw=true "Circuit")
  
The picture below shows a minimum viable product (MVP) of a working door lock system.  
![Alt text](door_lock_circuit.png?raw=true "Circuit")