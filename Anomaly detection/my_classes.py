import torch
from torch.utils import data
from PIL import Image
from torchvision import transforms
import pandas as pd
import os
import numpy as np

class Dataset(data.Dataset):
   #'Characterizes a dataset for PyTorch'
   #def __init__(self, list_IDs, labels):
    def __init__(self, csv_file, root_dir, transform):
       #'Initialization'
       #self.labels = labels
       #self.list_IDs = list_IDs
      list_IDs = pd.read_csv(csv_file)
      self.root_dir = root_dir
      #self.params = params

      self.img_list = list_IDs.filename
      #self.boxes = list_IDs[['xmin', 'ymin', 'xmax', 'ymax']]
      self.labels = list_IDs.label
      #self.oclusions = list_IDs.occluded



    def __len__(self): #OBLIGATORIA
       #'Denotes the total number of samples'
       return len(self.img_list.unique())

    def __getitem__(self, index): #OBLIGATORIA, per construir els batches
       #'Generates one sample of data'
       # Select sample
       if torch.is_tensor(index): #ho converteix a una llista perque pillow ho pugui entendre, perq no son compatibles pillow i pytotch
            index = index.tolist()

       ID = self.img_list[index]

       # Load data and get label
       #X = torch.load('Spectograms/' + ID + '.png')
       filename = os.path.join(root_dir, ID)
       image = Image.open(filename, mode='r') #filename = self.list[idx]

       #hem de convertir la imatge en un tensor amb les dimensions que volguem
      #img = Image.open(os.path.join(self.root_dir, self.img_list.unique()[index][1:]), mode = 'r')
      #rows = self.img_list == self.img_list.unique()[index]
      #boxes = torch.FloatTensor(self.boxes-loc[rows].to_numpy())
      labels = torch.LongTensor(self.labels[index].to_numpy())
      #oclusions = torch.ByteTensor(self.oclusions.loc[rows].to_numpy())

      image = transform(image)


       #y = self.labels[ID]

       #return X, y
       return image, labels



