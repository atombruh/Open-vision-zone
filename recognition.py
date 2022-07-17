import cv2
import random
from face_recognition import *
import json







cascade = cv2.CascadeClassifier('cascades\haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)


class Face():
    def write(self,name,encode):
        self.face_encoding = encode
        self.name = name
        file = open('students_list.json','w')
        data= {self.face_encoding:self.name}
        json.dump(data,file)
        file.close()

        
    def get_name_by_encoding(self,encode):
        self.encode = encode
        file = open('students_list.json','r')
        data = json.load(file)
        file.close()
        data = data[self.encode]
        return data
        




        
        

    
