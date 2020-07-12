# Making prediction about user data
from tensorflow import keras
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np

def prediction(userUploaded):

    # print('----------------------------------')
    # print(os.getcwd())
    # workingdir = os.getcwd()
    # print(os.listdir(os.getcwd()))
    # # img=io.imread(os.getcwd()+'/media/'+testdata)
    # # io.imshow(img)
    # # print(img)
    # # print(img.shape)
    # print('----------------------------------')

    # load json and create modeli
    json_file = open(os.getcwd()+'/imageClassification/regression.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights(os.getcwd()+"/imageClassification/regression.h5")

    if userUploaded.find('.') > -1 :
        test_image = keras.preprocessing.image.load_img(os.getcwd()+''+userUploaded, target_size = (64, 64))
        test_image = keras.preprocessing.image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        #prediction
        result = loaded_model.predict(test_image)
        print(result)
        if result[0][0] == 1:
            prediction = 'Malignant'
        else:
            prediction = 'Benign'

        print(f"\n\nFile: {userUploaded}, prediction : {prediction}\n\n")
        return {'file':userUploaded,'prediction':prediction}

    else:

        #prediction code
        test_datagen = ImageDataGenerator(rescale = 1./255)
        user_data = test_datagen.flow_from_directory(os.path.join(os.getcwd(),userUploaded), target_size = (64, 64), batch_size = 1, shuffle=False, class_mode = 'binary')
        
        # evaluate loaded model on user data
        loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        result = loaded_model.predict(user_data)
        print(f'result shape before : {result.shape}')


        for res in result:

            print(f'pridiction of each image {res}')

            if res <= 0.5:
                print('The convolutional neural network predicts that this tumor is malignant!')
            else:
                print('The convolutional neural network predicts that this tumor is benign.')
