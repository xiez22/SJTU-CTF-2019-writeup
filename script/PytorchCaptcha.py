import cv2
import torch
import torchvision
import torch.nn as nn
import torch.utils.data as Data
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import time
import os
import splitImg

# Hyper Parameters
MIN_BIT_SIZE = 10
BATCH_SIZE = 32
EPOCH = 100
LR = 0.002

sys.setrecursionlimit(4000)

captcha_data = None
captcha_label = None


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 16, 5, 1, 2),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 64, 5, 1, 2),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.out = nn.Linear(5*3*64, 26)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(-1, 5*3*64)
        out = self.out(x)
        return out


cnn = CNN().cuda()


try:
    cnn.load_state_dict(torch.load('E:/Test/Captcha/net_param.pkl'))
    print('已加载网络')
except Exception as err:
    print(err)
    print('加载网络失败')


def train(show_result=False):
    print(cnn)

    loss_func = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(cnn.parameters(), LR)

    print('开始训练')
    for epoch in range(EPOCH):
        for step, (batchx, batchy) in enumerate(dataloader):
            batchx.requires_grad = True
            prediction = cnn(batchx)
            loss = loss_func(prediction, batchy)

            optimizer.zero_grad()
            loss.backward(retain_graph=True)
            optimizer.step()

            if step % 10 == 0:
                print('EPOCH:', epoch, 'Step:', step, 'Loss:', loss.item())
                if(show_result):
                    prediction = torch.max(prediction, 1)[1]
                    for i in range(16):
                        plt.subplot(4, 4, i+1)
                        plt.imshow(batchx[i].squeeze().detach().cpu().numpy())
                        plt.title('{} {}'.format(chr(batchy[i].cpu().numpy()+ord('a')),
                                                 chr(prediction[i].detach().cpu().numpy()+ord('a'))))
                    plt.show()

        torch.save(cnn.state_dict(), 'E:/Test/Captcha/net_param.pkl')
        print('神经网络保存成功')


'''
try:
    print('尝试从上一次的训练中恢复..')
    captcha_data = np.load('./Data/np_data.npy')
    captcha_label = np.load('./Data/np_label.npy')
    print('已加载数据')
except:
    print('数据加载失败。不过我们可以重新开始。')
    captcha_data = np.zeros((0, 40, 40))
    captcha_label = np.zeros((0))

print('正在构建神经网络......')
dataset = Data.TensorDataset(
    torch.from_numpy(captcha_data).type(torch.FloatTensor).unsqueeze(1).cuda(),
    torch.from_numpy(captcha_label).type(torch.LongTensor).cuda()
)

dataloader = Data.DataLoader(dataset, BATCH_SIZE, True)
train(show_result=True)
'''


def captchaDecode(URL_PATH: str):
    cap = cv2.VideoCapture(URL_PATH)
    ret, img = cap.read()
    img0 = img

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, img = cv2.threshold(img, 215, 255, cv2.THRESH_BINARY)

    new_data = np.array(splitImg.Split(img))

    img_input = torch.from_numpy(
        new_data).type(torch.FloatTensor).unsqueeze(1).cuda()
    prediction = torch.softmax(cnn(img_input), 1)
    chance = torch.max(prediction, 1)[0].cpu().detach().numpy()
    result = torch.max(prediction, 1)[1].cpu().detach().numpy()
    result_str = ''
    for i in result:
        result_str += chr(ord('a')+i)
    return result_str
