import os
import sys
import codecs

os.environ['TRIDENT_BACKEND'] = 'pytorch'
import  trident  as T
import math
import numpy as np
import linecache
import PIL
import PIL.Image as Image
import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo
from torch.utils.data import *
from torch.autograd import Variable
import torch.nn.functional as F
import torch.optim as optim
import torchvision

from trident.backend.pytorch_backend import *
from trident.layers.pytorch_blocks import  *

# 是否使用GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# C.debugging.set_computation_network_trace_level(1000)
# C.debugging.set_checked_mode(True)
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))



def _get_shape(x):
    "single object"
    if isinstance(x, np.ndarray):
        return tuple(x.shape)
    else:
        return tuple(x.size())


# data = T.load_cifar('cifar100', 'train', is_flatten=False)
# dataset = T.Dataset('cifar100')
# dataset.mapping(data=data[0], labels=data[1], scenario='train')

num_epochs=1000
minibatch_size=8

# train_loader = T.load_cifar('cifar100', 'train', is_flatten=False)
# train_loader.minibatch_size=minibatch_size



import torchvision.transforms as transforms
transform = transforms.Compose(
 [transforms.Resize(240, Image.BICUBIC),
    transforms.RandomCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.RandomErasing(0.2,(0.02,0.2)),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])


cifar=torchvision.datasets.cifar.CIFAR100(root='C:/Users/Allan/.trident/datasets/cifar100/', train=True, transform=transform, target_transform=None, download=True)


train_loader = DataLoader(
        cifar,
        batch_size=minibatch_size,
        num_workers=0,
        shuffle=True
    )





#raw_imgs, raw_labels = dataset.next_bach(minibatch_size)




class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()

        self.feats = nn.Sequential(
            nn.Conv2d(3, 32, 5, 1, 1),
            nn.MaxPool2d(2, 2),
            nn.ReLU(True),
            nn.BatchNorm2d(32),
            nn.Conv2d(32, 64, 3,  1, 1),
            nn.ReLU(True),
            nn.BatchNorm2d(64),
            nn.Conv2d(64, 64, 3,  1, 1),
            nn.MaxPool2d(2, 2),
            nn.ReLU(True),
            nn.BatchNorm2d(64),
            nn.Conv2d(64, 128, 3, 1, 1),
            nn.ReLU(True),
            nn.BatchNorm2d(128)
        )
        self.classifier = nn.Conv2d(128, 100, 1)
        self.avgpool = nn.AvgPool2d(6, 6)
        self.dropout = nn.Dropout(0.5)
    def forward(self, inputs):
        out = self.feats(inputs)
        out = self.dropout(out)
        out = self.classifier(out)
        out = self.avgpool(out)
        out = out.view(-1, 100)
        return out


#= torch.load('resnet50_model_pytorch_cifar100_224.pth')

resnet50=torchvision.models.resnet50(pretrained=True)
resnet50.avgpool = Classifier1d(100,classifier_type='global_avgpool')
resnet50.fc =Linear(100,100)
ps=list(resnet50.parameters())
for k in list(resnet50.state_dict().keys()):
    if re.search(r'in\d+\.running_(mean|var)$', k):
        del resnet50.state_dict()[k]
for para in list(resnet50.parameters())[:-2]:
    para.requires_grad=False
for para in list(resnet50.parameters())[-5:]:
        para.requires_grad = True

resnet50.to(device)

optimizer = optim.Adam(resnet50.parameters(), lr=2e-3)
criterion=nn.CrossEntropyLoss(reduction='mean')


class GcdNet_1(nn.Module):
    def __init__(self):
        super(GcdNet_1, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)#4*(2*2)
        self.b1 = T.GcdConv2d_Block_1((3, 3), 24, 1, auto_pad=True, activation='leaky_relu', divisor_rank=0)  # 4*(2*3)
        self.b1_1 = T.GcdConv2d_Block_1((3, 3), 4*7, 1, auto_pad=True, activation='leaky_relu', divisor_rank=0)  #4*7
        self.b1_2 = T.GcdConv2d_Block_1((3, 3), 6*5, 1, auto_pad=True, activation='leaky_relu',divisor_rank=0)  # (2*3)*5
        #self.b1_3 = T.GcdConv2d_Block_1((3, 3), 24, 1, auto_pad=True, activation='leaky_relu',divisor_rank=0)
        self.b2 = T.GcdConv2d_Block_1((3, 3), 48, 2, auto_pad=True, activation='leaky_relu', divisor_rank=0)  # (2*3)*8
        self.b3 = T.GcdConv2d_Block_1((3, 3), 80, 1, auto_pad=True, activation='leaky_relu', divisor_rank=0)  # 8*(2*5)
        self.b3_1 = T.GcdConv2d_Block_1((3, 3), 88, 1, auto_pad=True, activation='leaky_relu', divisor_rank=0)  # 8*11
        self.b3_2 = T.GcdConv2d_Block_1((3, 3), 70, 1, auto_pad=True, activation='leaky_relu', divisor_rank=0)  # (2*5)*7

        self.b4 = T.GcdConv2d_Block_1((3, 3), 120, 2, auto_pad=True, activation='leaky_relu',divisor_rank=0)  # (2*5)*12
        self.b5 = T.GcdConv2d_Block_1((3, 3),168 , 1, auto_pad=True, activation='leaky_relu',divisor_rank=0)  # 12*(2*7)
        self.b6 = T.GcdConv2d_Block_1((3, 3), 224, 2, auto_pad=True, activation='leaky_relu',divisor_rank=0)  # (2*7)*16
        self.b7 = T.GcdConv2d_Block_1((3, 3), 352, 1, auto_pad=True, activation='leaky_relu',divisor_rank=0)  # 16*(2*11)
        self.b8 = T.GcdConv2d_Block_1((3, 3), 440, 2, auto_pad=True, activation='leaky_relu', divisor_rank=0)  # (2*11)*20
        self.b9 = T.GcdConv2d_Block_1((3, 3), 520, 1, auto_pad=True, activation='leaky_relu',divisor_rank=0)  # 20*(2*13)
        self.b10 = T.GcdConv2d_1((1, 1), 100, 1, auto_pad=True, activation=None, divisor_rank=0)
        self.pool=nn.AdaptiveAvgPool2d(output_size=1)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        out = F.relu(self.conv1(x), inplace=True)
        out = self.b1(out)
        branch1=self.b1_1(out)
        branch2= self.b1_2(out)


        out=torch.cat([branch1,branch2],1)
        out = self.b2(out)
        out = self.b3(out)
        branch3 = self.b3_1(out)
        branch4 = self.b3_2(out)

        out = torch.cat([branch3, branch4], 1)
        out = self.b4(out)
        out = self.b5(out)
        out = self.b6(out)
        out = self.b7(out)
        out = self.b8(out)
        out = self.b9(out)
        out = self.b10(out)
        out = self.pool(out)
        out=out.view(out.size(0),out.size(1))
        out=out.sigmoid()
        return out


class GcdNet_2(nn.Module):
    def __init__(self):
        super(GcdNet_2, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)#4*4
        self.b1 = T.GcdConv2d_Block_1((3, 3), 24, 1, auto_pad=True, activation='leaky_relu', divisor_rank=0)  # 4*(2*3)
        self.b2 = T.GcdConv2d_Block_1((3, 3), 40, 2, auto_pad=True, activation='leaky_relu', divisor_rank=0)  # (2*3)*9
        self.b3 = T.GcdConv2d_Block_1((3, 3), 112, 1, auto_pad=True, activation='leaky_relu', divisor_rank=0)  # 9*(2*5)
        self.b4 = T.GcdConv2d_Block_1((3, 3), 176, 2, auto_pad=True, activation='leaky_relu',divisor_rank=0)  # (2*5)*16
        self.b5 = T.GcdConv2d_Block_1((3, 3),208 , 1, auto_pad=True, activation='leaky_relu',divisor_rank=0)  # 16*(2*7)
        self.b6 = T.GcdConv2d_1((1, 1), 100, 1, auto_pad=True, activation=None, divisor_rank=0)
        self.pool=nn.AdaptiveAvgPool2d(output_size=1)

    def forward(self, x):
        out = F.relu(self.conv1(x), inplace=True)
        out = self.b1(out)
        out = self.b2(out)
        out = self.b3(out)
        out = self.b4(out)
        out = self.b5(out)
        out = self.b6(out)
        out = self.pool(out)
        out=out.view(out.size(0),out.size(1))
        out=out.sigmoid()
        return out


gcd_model = torch.load('gcd_model_pytorch_cifar100_224.pth')
#gcd_model=GcdNet_1()

gcd_model.to(device)
flops_gcd_model = calculate_flops(gcd_model)

gcd_model2 = torch.load('gcd_model2_pytorch_cifar100_224.pth')
#gcd_model2=GcdNet_2()

gcd_model2.to(device)
flops_gcd_model2 = calculate_flops(gcd_model2)



#gcd_model.load_state_dict(torch.load('gcd_model_pytorch_mnist.pth'))
for i, (input, target) in enumerate(train_loader):
    #input, target = torch.from_numpy((input)), torch.from_numpy(target)
    input, target = Variable(input).to(device), Variable(target).to(device)
    gcd_model(input)
    gcd_model2(input)
    break
print(gcd_model)
for i,para in enumerate(gcd_model.parameters()):
    print('{0} {1} {2}'.format(i,para.name,_get_shape(para)))

gcd_optimizer = optim.Adam(gcd_model.parameters(),lr=2e-4, betas=(0.9, 0.999), eps=1e-08, weight_decay=4e-5)
gcd_mse_criterion=nn.MSELoss(reduction='mean')
gcd_ce_criterion=nn.CrossEntropyLoss(reduction='mean')
#flops_model = calculate_flops(model)
#print('flops_model:{0}'.format(flops_model))
gcd2_optimizer = optim.Adam(gcd_model2.parameters(),lr=2e-4, betas=(0.9, 0.999), eps=1e-08, weight_decay=4e-5)
gcd2_mse_criterion=nn.MSELoss(reduction='mean')
gcd2_ce_criterion=nn.CrossEntropyLoss(reduction='mean')



import collections
weight_dict=collections.OrderedDict()
weight_dict_current=collections.OrderedDict()
for i,para in enumerate(gcd_model.named_parameters()):
    weight_dict_current[para[0]] = para[1].data.cpu().detach().numpy()
    print('{0} {1} {2} {3}'.format(i,para[0],_get_shape(para[1]),para[1].requires_grad))


flops_resnet50 = calculate_flops(resnet50)
print('flops_{0}:{1}'.format('resnet50', flops_resnet50))

flops_gcd_model = calculate_flops(gcd_model)
print('flops_{0}:{1}'.format('gcd_model', flops_gcd_model))

print('{0:.3%}'.format(flops_gcd_model/flops_resnet50))

flops_gcd2_model = calculate_flops(gcd_model2)
print('flops_{0}:{1}'.format('gcd_model2', flops_gcd2_model))
print('{0:.3%}'.format(flops_gcd2_model/flops_resnet50))
weight_dict2=collections.OrderedDict()
weight_dict_current2=collections.OrderedDict()
for i,para in enumerate(gcd_model2.named_parameters()):
    weight_dict_current2[para[0]] = para[1].data.cpu().detach().numpy()
    print('{0} {1} {2} {3}'.format(i,para[0],_get_shape(para[1]),para[1].requires_grad))


#f = codecs.open('model_log_cifar100.txt', 'a', encoding='utf-8-sig')
#model = Function.load('Models/model5_cifar100.model')
os.remove('model_log_cifar100_test3d.txt')
f = codecs.open('model_log_cifar100_test3d.txt', 'a', encoding='utf-8-sig')
losses=[]
metrics=[]


gcd_losses=[]
gcd_metrics=[]
gcd2_losses=[]
gcd2_metrics=[]
print('epoch start')
for epoch in range(num_epochs):
    mbs = 0

    for  mbs ,(input, target) in enumerate(train_loader):
        #input, target = torch.from_numpy(input),torch.from_numpy(target)
        input, target = Variable(input).to(device), Variable(target).to(device)

        resnet50_output = resnet50(input)

        resnet50_loss=criterion(resnet50_output,target)

        accu =accuracy(resnet50_output,target)
        losses.append(resnet50_loss.item())
        metrics.append(to_numpy(accu))


        #optimizer.zero_grad()
        #lenet_loss.backward( retain_graph=True)
        #optimizer.step()


        gcd_optimizer.zero_grad()
        gcd_output = gcd_model(input)
        #print(gcd_output.cpu().detach().numpy()[:2])
        gcd_loss =gcd_ce_criterion(gcd_output,target)#+ gcd_mse_criterion(gcd_output, lenet_output)
        if (mbs + 1) % 200 == 0:
            weight_dict = weight_dict_current.copy()
            for i, para in enumerate(gcd_model.named_parameters()):
                weight_dict_current[para[0]] = para[1].data.cpu().detach().numpy()
            #     print('{0} {1} {2}'.format(i, para[0], _get_shape(para[1])))
            for k, v in weight_dict_current.items():
                print('{0}   mean: {1:.5f} max: {2:.5f} min: {3:.5f}  diff:{4:.3%}  '.format(k, v.mean(), v.max(),   v.min(), np.abs( v - weight_dict[k]).mean() / np.abs(weight_dict[k]).mean()))
            result = gcd_output.cpu().detach().numpy()
            print('mean: {0:} max: {1} min: {2}'.format(result.mean(), result.max(), result.min()))

        gcd_accu = accuracy(gcd_output,target)
        gcd_losses.append(gcd_loss.item())
        gcd_metrics.append(to_numpy(gcd_accu))
        gcd_loss.backward( )
        gcd_optimizer.step()

        gcd2_optimizer.zero_grad()
        gcd2_output = gcd_model2(input)
        # print(gcd_output.cpu().detach().numpy()[:2])
        gcd2_loss = gcd2_ce_criterion(gcd2_output, target)  #+ 2*gcd2_mse_criterion(gcd2_output, lenet_output)
        if (mbs + 1) % 200 == 0:
            weight_dict2 = weight_dict_current2.copy()
            for i, para in enumerate(gcd_model2.named_parameters()):
                weight_dict_current2[para[0]] = para[1].data.cpu().detach().numpy()
            #     print('{0} {1} {2}'.format(i, para[0], _get_shape(para[1])))
            for k, v in weight_dict_current2.items():
                print('{0}   mean: {1:.5f} max: {2:.5f} min: {3:.5f}  diff:{4:.3%}  '.format(k, v.mean(), v.max(), v.min(), np.abs(v - weight_dict2[k]).mean() / np.abs(weight_dict2[k]).mean()))
            result = gcd_output.cpu().detach().numpy()
            print('mean: {0:} max: {1} min: {2}'.format(result.mean(), result.max(), result.min()))

        gcd2_accu =accuracy(gcd2_output,target)
        gcd2_losses.append(gcd2_loss.item())
        gcd2_metrics.append(to_numpy(gcd2_accu))
        gcd2_loss.backward()
        gcd2_optimizer.step()


        if mbs % 20 == 0:
            print("Baseline:     Epoch: {}/{} ".format(epoch + 1, num_epochs),
                  "Step: {} ".format(mbs),
                  "Loss: {:.4f}...".format(np.array(losses).mean()),
                  "Accuracy:{:.3%}...".format(np.array(metrics).mean()))
            f.writelines(['model: {0}  learningrate {1}  epoch {2}  {3}/ 1000 loss: {4} metrics: {5} \n'.format('AlexNet', 0.01, epoch, mbs + 1, np.array(losses).mean(), np.array(metrics).mean())])


            losses=[]
            metrics=[]

            print("Gcd_Conv    Epoch: {}/{} ".format(epoch + 1, num_epochs), "Step: {} ".format(mbs),
                  "Loss: {:.4f}...".format(np.array(gcd_losses).mean()),
                  "Accuracy:{:.3%}...".format(np.array(gcd_metrics).mean()))
            f.writelines([
                'model: {0}  learningrate {1}  epoch {2}  {3}/ 1000 loss: {4} metrics: {5} \n'.format('gcd_model', 0.01, epoch, mbs + 1, np.array(gcd_losses).mean(), np.array(gcd_metrics).mean())])

            gcd_losses = []
            gcd_metrics = []

            print("Gcd_Conv2    Epoch: {}/{} ".format(epoch + 1, num_epochs), "Step: {} ".format(mbs),
                  "Loss: {:.4f}...".format(np.array(gcd2_losses).mean()),
                  "Accuracy:{:.3%}...".format(np.array(gcd2_metrics).mean()))
            f.writelines([
                'model: {0}  learningrate {1}  epoch {2}  {3}/ 1000 loss: {4} metrics: {5} \n'.format('gcd2_model',0.01, epoch,mbs + 1,np.array(gcd2_losses).mean(),np.array(gcd2_metrics).mean())])

            gcd2_losses = []
            gcd2_metrics = []
        if (mbs+1)%100==0:
            # torch.save(lenet_model.state_dict(),'lenet_model_pytorch_mnist_1.pth' )
            # torch.save(gcd_model.state_dict(), 'gcd_model_pytorch_mnist_1.pth')
            torch.save(resnet50, 'resnet50_model_pytorch_cifar100_224.pth')
            torch.save(resnet50, 'resnet50_model_pytorch_cifar100_224_0.pth')
            torch.save(gcd_model, 'gcd_model_pytorch_cifar100_224.pth')
            torch.save(gcd_model2, 'gcd_model2_pytorch_cifar100_224.pth')
            torch.save(gcd_model, 'gcd_model_pytorch_cifar100_224_0.pth')
            torch.save(gcd_model2, 'gcd_model2_pytorch_cifar100_224_0.pth')

        mbs += 1
