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

#Training

def train(train_loader, validation_loader, model, optimizer, distance, hparams)
	for epoch in range(params['num_epochs']):
 	 	model.train()
     	val_regressionLoss = 0.0
     	val_classificationLoss = 0.0

##########################TRAINING###################################

    #for data in training_generator: #for i, data in enumerate(train_generator): el enumerate et torna el mateix q abans i el index de l'element, q és el número de batch de tots els q tinc en la meva dataset
    	for i, data in enumerate(train_loader):    #i = numero d'iteració i data = numero de batch
        #Move to default device
        	images = images.to(device)
        	#boxes = [b.to(device) for b in boxes]
        	labels = [l.to(device) for l in labels]


        #img, _ = data
        #img = Variable(img).cpu() #'cuda' if torch.cuda.is_available() else 'cpu' en lloc de .cpu fer lo de cuda; imgs = imgs.to(device)
        # ===================forward=====================
        	output = model(images)
        	loss = distance(output, img)
        #criterion = nn.CrossEntropyLoss(weight = class_weights.to(hparams['device'])) #LI HE DE PASSAR PER PARAMETRES EL OUTPUT I INPUT DEL MODEL, PERQ E CALCULI EL COST Q ES LA DIERENCIA ENTRE LES DUES #crossentropyloss és per un loss de classificació, he de mirar a la docuementació del roger de losses quina és adequada per reconstrucció, segurament el de MSE és el més simple però pot anar bé. He de mirar quina funció de cost és més adequasa per reconstrucció
        # ===================backward====================
        	optimizer.zero_grad()
        	loss.backward()
        	optimizer.step() #recalcula els pesos per a la següent iteració
    # ===================log========================
    	 if i%hparams['log_interval'] == 0 #ho printarà quan i sigui múltiple de log interval
    	 print('epoch [{}/{}], loss:{:.4f}'.format(epoch+1, num_epochs, loss.data))

    	 if i%hparams['ckpt_interval'] == 0 #guardar el model



##########################VALIDATION###################################

     	model.eval()
     	with torch.no_grad():  #per no calcular gradients pel validation
        	for i, (images, labels) in enumerate(val_loader):

            	#Move to default device
            	images = images.to(device)

            	#forward propagation
            	predicted_locs, predicted_scores = model(images)

            	#Loss
            	val_loss, val_conf_loss, val_loc_loss = distance(predicted_locs, #NO SÉ SI LA DISTÀNCIA AQUI ESTÀ BEN IMPLEMENTADA#perq et surti la info per pantalla
                                                              predicted_scores,
                                                              boxes,
                                                              labels,
                                                              hparams)

           	 	val_regressionLoss = val_regressionLoss + val_loc_loss.cpu()
            	val_classificationLoss = val_classificationLoss + val_conf_loss.cpu()

