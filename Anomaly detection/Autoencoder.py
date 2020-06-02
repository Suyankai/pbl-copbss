import torch 
import torchvision as tv
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torchvision.utils import save_image
from torch.utils import data
from my_classes import Dataset




#Datasets 
#partition = {'train': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'], 'validation': ['14','15', '16', '17', '18', '19', '20', '21']} # IDs
#labels = {'id-1': 0, 'id-2': 1, 'id-3': 2, 'id-4': 1}

# Generators
#training_set = Dataset(partition['train'], labels)
#training_set = Dataset(partition['train'])
#training_generator = data.DataLoader(training_set, **params)

#validation_set = Dataset(partition['validation'], labels)
#validation_set = Dataset(partition['validation'])
#validation_generator = data.DataLoader(validation_set, **params)

# Loading and Transforming data
#transform = transforms.Compose([transforms.ToTensor(),  transforms.Normalize((0.4914, 0.4822, 0.4466), (0.247, 0.243, 0.261))]) #A Tensor is a multidimensional array
#trainTransform  = tv.transforms.Compose([tv.transforms.ToTensor(), tv.transforms.Normalize((0.4914, 0.4822, 0.4466), (0.247, 0.243, 0.261))])
#trainset = tv.datasets.CIFAR10(root='./data',  train=True,download=True, transform=transform)
#dataloader = torch.utils.data.DataLoader(trainset, batch_size=32, shuffle=False, num_workers=4) #8 to 64 el valor de batch_size
#testset = tv.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
#classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
#testloader = torch.utils.data.DataLoader(testset, batch_size=4, shuffle=False, num_workers=2)

# Writing our model
class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder,self).__init__()
        
        self.encoder = nn.Sequential(			#defines a layer
            nn.Conv2d(3, 6, kernel_size=5),
            nn.ReLU(True),						#activation function
            nn.Conv2d(6,16,kernel_size=5),
            nn.ReLU(True))
        self.decoder = nn.Sequential(             
            nn.ConvTranspose2d(16,6,kernel_size=5),
            nn.ReLU(True),
            nn.ConvTranspose2d(6,3,kernel_size=5),
            nn.ReLU(True))
    def forward(self,x):		#defines which way will go our data
        x = self.encoder(x)
        x = self.decoder(x)
        return x

#defining some params
#num_epochs = 5 #you can go for more epochs, I am using a mac, they are the number of iterations to minimize the cost function
#batch_size = 128







    #per guardar el tensor q tinc ara a imatge he de transformar-lo primer (ToNumpy) i guardar la imatge

#guardar el model cada cert temps, guardes els pesos q és el q necessites
#model_save_name = "checkpoint_{}_{}_{}.pt".format(hparams['model_name'],epoch,num)
 #               path = os.path.join(hparams['checkpoint_dir'],model_save_name)
  #              torch.save({
   #                 'model_state_dict': model.state_dict(), 
    #                'train_losses':train_losses,
     #               'val_losses':val_losses},
      #              path)





