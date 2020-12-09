import cv2
import numpy as np

_faceCascadeHAAR = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
_faceCascadeLBP = cv2.CascadeClassifier('/home/pi/opencv/data/lbpcascades/lbpcascade_frontalface.xml') #
_faceProfileCascadeHAAR = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_profileface.xml')
_faceProfileCascadeLBP = cv2.CascadeClassifier('/home/pi/opencv/data/lbpcascades/lbpcascade_profileface.xml')
_smile_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_smile.xml')

class Face():
    """ Face and smile detection class"""

    @staticmethod
    def _prepare_image(img, doSecondRescale):
        """ scaling the image and using histogram equilisation"""
        img = Face.resizeImage(img, 640)
        clahe = cv2.createCLAHE(clipLimit = 4.5, tileGridSize=(15, 15)) #contrast limited adaptive histogram equilisation. This is very important!
        img = clahe.apply(img)
        img = cv2.medianBlur(img, 5)
        img = cv2.resize(img, (0,0), fx = 0.6, fy = 0.6)
        if doSecondRescale:
            img = Face.resizeImage(img, 320)
        return img

    @staticmethod
    def smile(img, scale = 1.3, minNeighbors = 1, doSecondRescale = True):
        """ Detect smiles, returns list of confidences for detected smiles"""
        img = Face._prepare_image(img, doSecondRescale)
        # oversensitve face detection
        faces = Face.faces_lbpCascade(img, scale, 1)
        img_list = Face.getFaces(img, faces)
        smiles = []
        # search only where a face was detected
        for face_img in img_list:
            temp_smiles = Face.smile_haarcascade(face_img, 1.1, 1)
            for s in temp_smiles[1]:
                smiles.append(s)
        return smiles


    @staticmethod
    def faceInPicture(img, scale = 1.3, minNeighbors  = 5, doSecondRescale = True):

        img = Face._prepare_image(img, doSecondRescale)

        # first detection with lbp
        faces = Face.faces_lbpCascade(img, scale, int(max(1, minNeighbors / 2)) )


        if(len(faces) != 0):
            # face found? use slower haar detection to verify
            faces = Face.facesHaarCascade(img, scale, minNeighbors)
            if len(faces) != 0:
                # found face with booth methods
                return 2
            else:
                # found face with lbp
                return 1

        # no face found
        return 0

    # Cascades
    @staticmethod
    def facesHaarCascade(img, scale, minNeighbors):

        return _faceCascadeHAAR.detectMultiScale(img, scale, minNeighbors, minSize=(20, 20))

    @staticmethod
    def faces_lbpCascade(img, scale, minNeighbors):

        return _faceCascadeLBP.detectMultiScale(img, scale, minNeighbors, minSize=(20, 20))

    @staticmethod
    def faces_Profile_lbpCascade(img, scale, minNeighbors):

        return _faceProfileCascadeLBP.detectMultiScale(img, scale, minNeighbors, minSize=(20, 20))

    @staticmethod
    def faces_Profile_HaarCascade(img, scale, minNeighbors):

        return _faceProfileCascadeHAAR.detectMultiScale(img, scale, minNeighbors, minSize=(20, 20))

    @staticmethod
    def smile_haarcascade(img, scale, minNeighbors):
        return _smile_cascade.detectMultiScale2(img, scale, minNeighbors, minSize=(5,5)) # , outputRejectLevels=True (for detectMultiScale3)


    @staticmethod
    def getFaces(image, faces):
        """ returns list of images - faces croped from original image"""
        list = []
        for (x, y, w, h) in faces:
            list.append(image[y:y+h, x:x+w])
        return list

    # https://stackoverflow.com/questions/4195453/how-to-resize-an-image-with-opencv2-0-and-python2-6
    @staticmethod
    def resizeImage(img, maxi):
        height, width = img.shape[:2]
        max_height = maxi
        max_width = maxi

        # only shrink if img is bigger than required
        if max_height < height or max_width < width:
            # get scaling factor
            scaling_factor = max_height / float(height)
            if max_width/float(width) < scaling_factor:
                scaling_factor = max_width / float(width)
                # resize image
            img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor)
        return img
