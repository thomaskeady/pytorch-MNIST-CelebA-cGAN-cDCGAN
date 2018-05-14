import pandas as pd
#from torch import np # Torch wrapper for Numpy
import numpy as np

import os
from PIL import Image

import torch
from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader
from torchvision import transforms
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

from sklearn.preprocessing import MultiLabelBinarizer



# Taken from https://github.com/pytorch/tutorials/issues/78
class CustomDataset(Dataset):
    """Dataset wrapping images and target labels for Kaggle - Planet Amazon from Space competition.

    Arguments:
        A CSV file path
        Path to image folder
        Extension of images
        PIL transforms
    """

    def __init__(self, csv_path, img_path, img_ext, transform=None):
    
        tmp_df = pd.read_csv(csv_path, header=None)
        targetFile = img_path + tmp_df[0][0] + img_ext;
        #print(targetFile)
        #print(type(tmp_df))
        #assert tmp_df[0].apply(lambda x: os.path.isfile(targetFile)).all(), \
#"Some images referenced in the CSV file were not found"
        
        self.mlb = MultiLabelBinarizer()
        self.img_path = img_path
        self.img_ext = img_ext
        
        if transform is None:
            self.transform = transforms.Compose([
                transforms.Grayscale(), # Default output channels is 1
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
            ])
        else:
            self.transform = transform


        #self.X_train = tmp_df['image_name']
        self.X_train = tmp_df[0]
        #self.y_train = self.mlb.fit_transform(tmp_df['tags'].str.split()).astype(np.float32)
        vectors = tmp_df.loc[:,1:300]

        #print(type(vectors))
        #print(type(vectors[1][1]))
        #print(type(vectors.as_matrix()))
        #print(type(vectors[1][1].as_matrix()))


        #self.y_train = self.mlb.fit_transform(str(tmp_df.loc[:,1:301]).split()).astype(np.float32)
        #self.y_train = tmp_df.loc[:,1:301].values.astype(np.float32)
        self.y_train = vectors.as_matrix()
        #print(self.y_train.shape)
        #print(type(self.y_train[0][0]))





    def __getitem__(self, index):
        img = Image.open(self.img_path + self.X_train[index] + self.img_ext)
        img = img.convert('RGB')
        if self.transform is not None:
            img = self.transform(img)

        #print(self.y_train[index])
        #print(type(self.y_train[index]))
        #print(type(self.y_train[index][1]))
        label = torch.from_numpy(self.y_train[index])
        return img, label

    def __len__(self):
        return len(self.X_train.index)

