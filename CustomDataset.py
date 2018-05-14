import pandas as pd
from torch import np # Torch wrapper for Numpy
#import numpy as np

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
        
        #self.mlb = MultiLabelBinarizer()
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


        self.words = tmp_df[0]
        #self.X_train = np.empty([64, 64, 4, len(tmp_df[0])]) # This feels so janky # hardcoding ok because it is custom after all
        self.X_train = np.empty([64, 64, len(tmp_df[0])]) # This feels so janky # hardcoding ok because it is custom after all
        #self.X_train = tmp_df[0]   # X should not be words, shoudl be images
        print(self.X_train.shape)
        #for word in tmp_df[0]:
        for wi in range(len(tmp_df[0])):
        #for wi in range(len(tmp_df[0])-1, -1, -1):
            #image = imageio.imread(img_path + tmp_df[0][wi] + img_ext)
            image = Image.open(img_path + tmp_df[0][wi] + img_ext).convert('L')
            #try:
            #self.X_train = np.append(self.X_train, np.expand_dims(np.array(image), 3))
            #self.X_train[wi] = np.expand_dims(np.array(image), 3)
            self.X_train[:,:,wi] = np.array(image)
            #print('added ' + str(wi) + ' ' + tmp_df[0][wi])
            #except Exception as e:
            #    print (e)

        #self.X_train = self.X_train[:,:,:,1:]   # Take everything except the first which was just for starting

        vectors = tmp_df.loc[:,1:300]

        self.y_train = vectors.as_matrix()

        # To make it more like MNIST
        self.imgs = self.X_train





    def __getitem__(self, index):
        img = Image.open(self.img_path + self.words[index] + self.img_ext)
        img = img.convert('RGB')
        if self.transform is not None:
            img = self.transform(img)

        #print(self.y_train[index])
        #print(type(self.y_train[index]))
        #print(type(self.y_train[index][1]))
        label = torch.from_numpy(self.y_train[index])
        return img, label

    def __len__(self):
        #return len(self.X_train.index)
        return len(self.X_train)

