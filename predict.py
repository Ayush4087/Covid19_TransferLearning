from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
from keras.models import Model,load_model
import os
import numpy as np
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 
import pandas as pd
import tensorflow as tf

model = load_model('covid19_vgg16.h5')
result_df = pd.DataFrame(columns=['Image_Name','Prediction'])

def classification(res):
    ma = max(res)
    ind = res.index(ma)
    if(ind==0):
        prediction = "NORMAL"
    else:
        prediction = "PNEUMONIA"
    return prediction

path = "TEST/"
images = os.listdir(path)

for img in images:
    img_path = os.path.join(path,img)
    image = load_img(img_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    ans = model.predict(image)
    ans = ans[0].tolist()
    res_array = [int(i) for i in ans]
    result = classification(res_array)
    result_df = result_df.append(
                                   {
                        'Image_Name':img,
                        'Prediction':result,
                        
                    },
                    ignore_index=True  
                        )



if(os.path.isfile('FINAL_RESULT.csv')):
    os.remove("FINAL_RESULT.csv")
    result_df.to_csv("FINAL_RESULT.csv")
else:
    result_df.to_csv("FINAL_RESULT.csv")
    
    