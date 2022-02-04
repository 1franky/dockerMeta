import tensorflow as tf
import os
import librosa
import numpy as np


def load_data(data_path):
    wav, sr = librosa.load(data_path, sr=16000)
    intervals = librosa.effects.split(wav, top_db=20)
    wav_output = []
    for sliced in intervals:
        wav_output.extend(wav[sliced[0]:sliced[1]])
    assert len(wav_output) >= 8000, "La frecuencia de audio efectiva es inferior a 0,5 s"
    wav_output = np.array(wav_output)
    ps = librosa.feature.melspectrogram(y=wav_output, sr=sr, hop_length=256).astype(np.float32)
    ps = ps[np.newaxis, ..., np.newaxis]
    return ps

def validate(reconocimientoPath, curp, newAudio):
    pathModels  = os.path.join(reconocimientoPath, "models")
    pathAudioDB = os.path.join(reconocimientoPath, "audioDB", curp) 
    nameModel = "model_Best.h5"
    listPre = []
    if not os.path.exists(pathAudioDB):
        return {
            "r" : False,
            "message" : "No se encontró la curp.",
            "similitud" : ""
        }

    layer_name = 'dropout'
    model = tf.keras.models.load_model(os.path.join(pathModels, nameModel))
    intermediate_layer_model = tf.keras.Model(inputs=model.input, outputs=model.get_layer(layer_name).output) 

    def infer(audio_path):
        data = load_data(audio_path)
        feature = np.array(intermediate_layer_model.predict(data),dtype=np.float64)

        print("feature ",feature[0].dtype," end feature")
        return feature 

    feature1 = infer(newAudio)[0]


    for file in os.listdir(pathAudioDB):
        if not file.endswith(".wav"):
            continue
        feature2 = None
        feature2 = infer(os.path.join(pathAudioDB, file))[0]
        dist = np.dot(feature1, feature2) / (np.linalg.norm(feature1) * np.linalg.norm(feature2))
        listPre.append(dist)
        print("\n\n\n", listPre)
        if dist > 0.80:
            print(dist)
            return {
                "r" : True,
                "message" : "La persona es la misma.",
                "similitud" : str(dist),
                "lista" : listPre
            }
    return {
        "r" : False,
        "message" : "No se encontró similitud alguna.",
        "similitud" : "",
        "lista" : listPre
    }

