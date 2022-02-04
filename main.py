from fastapi import FastAPI, File, UploadFile, Form
import shutil
from typing import List
from pydantic import BaseModel
import os
from random import choice
from fastapi.middleware.cors import CORSMiddleware

# import faceRecognition.validator
from faceRecognition import validator
from reconocimientoDeVoz import voz
from ocr import getOcrCurp

app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tmp = list(range(10000)) 
def asignaName(nameS, ext):
    name, _ = os.path.splitext(nameS.filename)
    newName = "{}_{}.{}".format(name, choice(tmp), ext)
    return newName

def saveFile(path, file):
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file, buffer)

@app.post("/faceRecognition")
async def create_file(
        INE: UploadFile = File(...), 
        selfie: UploadFile = File(...)):

    inePath = os.path.join(os.getcwd(), "faceRecognition", "INEs")
    selfPath = os.path.join(os.getcwd(), "faceRecognition", "selfie")

    ineName = asignaName(INE, "jpg")
    selName = asignaName(selfie, "jpg")

    saveFile(os.path.join(inePath, ineName), INE.file)
    saveFile(os.path.join(selfPath, selName), selfie.file)

    return validator.isTheSamePerson(ineName, selName)

@app.post("/voicePrint/save")
async def save_file(
        curp: str = Form(...),
        record1 : UploadFile = File(...),
        record2 : UploadFile = File(...),
        record3 : UploadFile = File(...)):
    
    reconocimientoPath = os.path.join(os.getcwd(), "reconocimientoDeVoz")
    audioPaths = os.path.join(reconocimientoPath, "audioDB")

    if os.path.exists(os.path.join(audioPaths, curp)):
        return {
            "r" : False,
            "message" : "La CURP ya existe."
        }
    else:
        pathCurp = os.path.join(audioPaths, curp)
        os.mkdir(pathCurp)
        try:
            tmp = asignaName(record1, "wav")
            saveFile(os.path.join(pathCurp, tmp), record1.file)

            tmp = asignaName(record2, "wav")
            saveFile(os.path.join(pathCurp, tmp), record2.file)

            tmp = asignaName(record3, "wav")
            saveFile(os.path.join(pathCurp, tmp), record3.file)
        except:
            shutil.rmtree(pathCurp)
            return {
                "r" : False,
                "message" : "No se pudieron guardar las notas de voz."
            }
        return {
            "r" : True,
            "messages" : "Notas de voz y CURP guardadas."
        }

@app.post("/voicePrint/validate")
async def compara_file(
        curp: str = Form(...),
        record : UploadFile = File(...)):
    
    reconocimientoPath = os.path.join(os.getcwd(), "reconocimientoDeVoz")
    audioPath    = os.path.join(reconocimientoPath, "audio")
    audio = asignaName(record, "wav")
    newAudio = os.path.join(audioPath, audio)
    saveFile(newAudio, record.file)
    r = voz.validate(reconocimientoPath,  curp, newAudio)
    os.remove(newAudio)
    return r


@app.post("/ocr/curp")
async def getOcr(
    curp : UploadFile = File(...)):

    curpPath = os.path.join(os.getcwd(), "ocr", "img")
    nameCurp = asignaName(curp, "jpg")

    saveFile(os.path.join(curpPath, nameCurp), curp.file)
    return getOcrCurp.getOcr(nameCurp)


@app.get("/")
def read_root():
    return {
            "Hola" : " ®Todos los derechos reservados. "
        }