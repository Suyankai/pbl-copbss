import torch 
import torchvision as tv
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torchvision.utils import save_image
from torch.utils import data
from my_classes import Dataset
from Autoencoder import Autoencoder
from pytorchDevTool.framework.function import Autoencoder
from pytorchDevTool.framework.function import trainClassifier
import os
import cv2
from training import train

# Parameters
hparams = {'batch_size': 8, #Quantes imatges a la vegada passem a la xarxa
		  'num_epochs': 3,
		  'test_batch_size': 16,
		  #'num_classes': 2,
		  'learning_rate': 1e-3, #depèn de l'optimitzador, hauré d'anar canviant-lo perq és el q modifica més els resultats
		  'log_interval': 10, #cada quant imprimir el loss
		  'ckpt_interval': 500, #cada quants batches guardar el model
          'shuffle': True,
          'num_workers': 6} #npi
#max_epochs = 100

hparams['device'] = 'cuda' if torch.cuda.is_available() else 'cpu' #en lloc de .cpu fer lo de cuda; imgs = imgs.to(device)

dataset = Dataset(csv_file = 'Spectograms/train.csv',
				  root_dir = 'Spectograms/',
				  transform = transforms.Compose(
				  	[
				  	transforms.Grayscale(),
				  	transforms.Resize(300), #cal interpolar?
				  	transforms.ToTensor(),
				  	#transforms.Normalize(macros))
				  ])

validation_split = 0.2
test_split = 0.2
random_seed = 30

dataset_size = len(dataset)
indices = list(range(dataset_size))
split = int(np.floor(validation_split * len(indices)))
split2 = int(np.floor(test_split * (len(indices)) - split) #REVISAR, per agafar part de la dataset com a test

#Shuffle dataset --> per mantenir q la dataset passi amb el mateix ordre
torch.manual_seed(random_seed)
np.random.seed(random_seed)
np.random.shuffle(indices)

#Get samples indices
train_indices, val_indices, test_indeces = indices[split:], indices[:split]

train_sampler = SubsetRandomSampler(train_indices)
valid_sampler = SubsetRandomSampler(val_indices)

train_loader = torch.utils.data.DataLoader(dataset,
										   batch_size = hparams['batch_size'],
										   sampler = train_sampler)
validation_loader = torch.utils.data.DataLoader(dataset,
												batch_size = hparams['test_batch_size'],
												sampler = valid_sampler)

#crear test_loader

###########################PRETRAINING#####################

model = Autoencoder()
model = model.to(hparams['device'])
optimizer = optim.Adam(model.parameters(), #L'optimitzador aquí és el Adam, però he de mirar quin és millor i per a quins paràmetres és millor --> all the autoencoders I've seen use the Adam optimizer
					   lr = 1e-3)
#class_weights = dataset.class_weights #per reconstrucció d'imatges en ppi no cal, però tampoc molesta
#criterion = nn.CrossEntropyLoss(weight = class_weights.to(hparams['device'])) #LI HE DE PASSAR PER PARAMETRES EL OUTPUT I INPUT DEL MODEL, PERQ E CALCULI EL COST Q ES LA DIERENCIA ENTRE LES DUES #crossentropyloss és per un loss de classificació, he de mirar a la docuementació del roger de losses quina és adequada per reconstrucció, segurament el de MSE és el més simple però pot anar bé. He de mirar quina funció de cost és més adequasa per reconstrucció
distance = nn.MSELoss()
train_losses, val_losses, test_losses = train(train_loader, validation_loader, model, optimizer, distance, hparams) #test loader no cal passar-li al train



###########################VALIDATION#####################

#model.eval()

#original = image.open(os.path.join('view_frontal.jpg'), mode = 'r')
#trans = transforms.Compose(
#						   [
#						   transforms.Grayscale(),
#						   transforms.Resize(300),
#						   transforms.ToTensor(),
#						   ])
#input = trans(original)
#input = input.reshape(-1, 1, 300, 300).to(hparams['device'])

#heatmap = gradcam(model, input, size = original.size)

#original = np.stack((original,)*3, axis =-1)













