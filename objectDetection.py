import cv2
import time
import numpy as np


class ObjectDetection():
    """ Detecting people and vehicles using openCV """

    # Constant values
    CONFIDENCE = 0.5
    SCORE_THRESHOLD = 0.5
    IOU_THRESHOLD = 0.5
    FONTSCALE = 0.6
    THICKNESS = 1

    # Load Yolo network
    network = cv2.dnn.readNetFromDarknet('yolov3.cfg','yolov3.weights')

    def __init__(self):
        self.loadLabels()


    def loadLabels(self):
        # Load labels from coco.names
        self.labels = []

        try:
            with open("coco.names","r") as coco:
                for line in coco.readlines():
                    self.labels.append(line.strip())

            # Set colors for plotting
            self.colors = np.random.uniform(0, 255, size=(len(self.labels), 3))
        except(Exception) as error:
            print(error)



    def loadImage(self,imageName):
        # Load image

        try:
            self.imageName = imageName
            image = cv2.imread(f"images/{self.imageName}.jpg")
            self.image = cv2.resize(image, None, fx=0.6, fy=0.6)

            # Run function
            self.setBlob()

        except:
            print("Could not find image!")
        

    def setBlob(self):
        # Edit image to be suitable as an input to the Neural Network
        blob = cv2.dnn.blobFromImage(self.image, 1/255.0, (416, 416), swapRB=True, crop=False)

        # Set blob as a input to network
        self.network.setInput(blob)

        # Get all layer names
        layerNames = self.network.getLayerNames()
        layerNames = [layerNames[i[0] - 1] for i in self.network.getUnconnectedOutLayers()]

        # Feed forward and get the network output
        self.layerOutputs = self.network.forward(layerNames)

        # Run function
        self.setValues()


    def setValues(self):
        # Create lists for store values
        self.boxes  = []
        self.confidences = []
        self.classIDs = []

        height, width, channels = self.image.shape
        
        for out in self.layerOutputs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                # If probability is greater than the minimum probability
                if (confidence > self.CONFIDENCE):
                    # Object detected
                    box = detection[:4] * np.array([width,height,width,height])
                    
                    centerX, centerY, w, h = box.astype("int")
                    
                    # Top and left corner of bounding box
                    x = int(centerX - (w/2))
                    y = int(centerY - (h/2))

                    # Update values
                    self.boxes.append([x, y, int(w), int(h)])
                    self.confidences.append(float(confidence))
                    self.classIDs.append(class_id)
        # Run function
        self.drawingObjects()


    def drawingObjects(self):
        # Perform non maximum suppression
        indexes = cv2.dnn.NMSBoxes(self.boxes, self.confidences, 
                        self.SCORE_THRESHOLD, self.IOU_THRESHOLD)

        if (len(indexes) > 0):
            for i in indexes.flatten():        
                # Coordinates of bounding box
                x, y = self.boxes[i][0], self.boxes[i][1]
                w, h = self.boxes[i][2], self.boxes[i][3]

                # Draw and label on the image
                color = [int(j) for j in self.colors[self.classIDs[i]]]
                cv2.rectangle(self.image, (x,y), (x+w, y+h), color=color, thickness=self.THICKNESS)

                # Text for image
                text = f"{self.labels[self.classIDs[i]]}: %{(self.confidences[i]*100):.1f}"
                
                # Set width and height of image
                textWidth, textHeight = cv2.getTextSize(
                                            text, 
                                            cv2.FONT_HERSHEY_SIMPLEX,
                                            fontScale=self.FONTSCALE, 
                                            thickness=self.THICKNESS)[0]

                # Set coordinates for box
                textOffsetX = x
                textOffsetY = y - 5
                coordinatesOfBox = ((textOffsetX, textOffsetY),
                                    (textOffsetX+textWidth+2, textOffsetY-textHeight))
                
                # Set rectangle
                cv2.rectangle(
                    self.image, 
                    coordinatesOfBox[0], 
                    coordinatesOfBox[1], 
                    color=color, 
                    thickness=cv2.FILLED
                    )
                
                cv2.putText(
                    self.image, 
                    text, 
                    (x, y - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=self.FONTSCALE, 
                    color=(0, 0, 0), 
                    thickness=self.THICKNESS
                    )


    def displayImage(self):
        # Display image
        cv2.imshow("image", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def writeImage(self, path_to_directory):
        # Write image to a file

        try:
            cv2.imwrite(path_to_directory + self.imageName + "_yolo3." + ".jpg", self.image)

        except(Exception) as error:
            print(error)



if __name__ == "__main__":
    ob = ObjectDetection()
    ob.loadImage('motorbike')
    #ob.displayImage()
    #ob.writeImage(path_to_directory)