import os
import pydicom as pm
import numpy as np
from keras.models import load_model
from keras.utils import get_file
from keras.preprocessing.image import load_img,img_to_array
from segmentation_models.losses import *
from matplotlib import pyplot as plt


class pneumothorax():

    #### class to access methods for segmentation ####

    def __init__(self):
        pass

    def preprocess_input(self,x):
        return x/255.0
    
    def get_model(self):
        
        #### loads model with custom objects ####
        
        self.model_path=get_file('efb0_pnmtrx_e200_dice_0.019_val_dice_0.182.h5','https://github.com/SamSepi0l59/medikalnet/releases/download/v0.0.1a13/efb_e200_dice_0.019_val_dice_0.182.h5',cache_subdir='models')

        return load_model(self.model_path,custom_objects={'binary_crossentropy_plus_dice_loss':bce_dice_loss,'dice_loss':dice_loss})

    def infer(self,path,model,viz=False,thresh=0.5):

        #### predicts input img after converting to array #####

        self.path=path
        self.model=model
        self.viz=viz
        self.thresh=thresh
        
        if not(os.path.exists(self.path)):
            raise ValueError('file path found {} is not valid '.format(self.path))

        if not(os.path.exists(self.path)):
            raise ValueError('No model found to predicted')

        
        if self.path.endswith('.jpg'):
            input_=img_to_array(load_img(self.path,target_size=(512,512)))
            
        elif self.path.endswith('.dcm'):
            #os.mkdir('cache')
            #assert(os.path.exists('cache'))
            #print('curr dir:',os.getcwd())
            plt.imsave(str(self.path[:-4])+'.jpg',pm.dcmread(self.path).pixel_array,cmap='gray')
            input_=img_to_array(load_img(str(self.path[:-4])+'.jpg',target_size=(512,512)))
            os.remove(str(self.path[:-4])+'.jpg')
        else:
            raise ValueError('file path must end with {} but found {}'.format(formats,path))

        out=self.model.predict(np.expand_dims(self.preprocess_input(input_),axis=0))

        if not self.viz:
            return out

        else:
            #### creating thresholded hard predictions ####
            out[out<=thresh]=0
            out[out>thresh]=1
            out=out.reshape(input_.shape[-3],input_.shape[-2])

            #### plotting visualizations ####
            fig,ax=plt.subplots(nrows=1,ncols=1,sharex=True,sharey=True,figsize=(10,10))
            ax.imshow(input_.astype(np.int32))
            ax.imshow(out.astype(np.int32),cmap='Reds',alpha=0.3)
            plt.show()

            #### return hard outputs ####
            return out
        
