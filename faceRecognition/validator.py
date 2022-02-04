import matplotlib.pyplot as plt
from mtcnn.mtcnn import MTCNN
import os
import tensorflow as tf
import base64

from deepface import DeepFace


def cutFaces(filename, result_list, salida):
    # load the image
    data = plt.imread(filename)
    # plot each face as a subplot
    for i in range(len(result_list)):
        # get coordinates
        x1, y1, width, height = result_list[0]['box']
        x2, y2 = x1 + width, y1 + height
        # define subplot
        plt.subplot(1, len(result_list), 0+1)
        plt.axis('off')
        # plot face
        # plt.imshow(data[y1:y2, x1:x2])
        plt.imsave(salida, data[y1:y2, x1:x2])

def cargarImage(path):
    img_raw = tf.io.read_file(path)
    img = tf.io.decode_image(
        img_raw, channels=3, dtype=tf.dtypes.uint8, name=None,
        expand_animations=True
    )
    return img.numpy()

def verify(img1Path, img2Path):    
    result = DeepFace.verify(img1Path, img2Path, model_name = 'ArcFace', detector_backend = 'retinaface', enforce_detection=False)
    if (result['verified']):
        return True
    else:
        return False
    
def imageLoad(path):
    data = {}
    with open(path, mode='rb') as file:
        img = file.read()

    # data['img'] = base64.encodebytes(img).decode('utf-8')
    return base64.encodebytes(img).decode('utf-8')



def isTheSamePerson(photo1, photo2):
    pathImg  = "INEs"
    pathCrop = "caraCrop"
    pathSelf = "selfie"

    nameImg = photo1
    selfie = photo2

    fullName  = os.path.join("faceRecognition", pathImg, nameImg)
    fullName2 = os.path.join("faceRecognition", pathSelf, selfie)


    face1 = cargarImage(fullName)
    face2 = cargarImage(fullName2)

    detector1 = MTCNN()
    detector2 = MTCNN()

    try: 
        faces1 = detector1.detect_faces(face1)
        # print(faces1)
    except:
        return {
            "r" : False,
            "message" : "No se detectó rostro en la imagen."
        }
    
    try: 
        faces2 = detector2.detect_faces(face2)
        # print(faces2)
    except:
        return {
            "r" : False,
            "message" : "No se detectó rostro en la imagen."
        }
    

    if len(faces1) == 0 or len(faces2) == 0:
        os.remove(fullName)
        os.remove(fullName2)
        return {
            "r" : False,
            "message" : "No se detectó rostro en la imagen."
        }
    
    cropFace = "cropIne" + nameImg
    fullName3 = os.path.join("faceRecognition", pathCrop, cropFace)
    cutFaces(fullName, faces1, fullName3)

    cropFace = "cropSelfie" + selfie
    fullName4 = os.path.join("faceRecognition", pathCrop, cropFace)
    cutFaces(fullName2, faces2, fullName4)

    os.remove(fullName)
    os.remove(fullName2)


    r = verify(fullName3, fullName4)
    img1 = imageLoad(fullName3)
    img2 = imageLoad(fullName4)
    os.remove(fullName3)
    os.remove(fullName4)
    if r:
        return {
            "r" : True,
            "message" : "Son la misma persona.",
            "ine" : img1,
            "selfie" : img2
        }
    else:
        return {
            "r" : False,
            "message" : "No son la misma persona.",
            "ine" : img1,
            "selfie" : img2
        }