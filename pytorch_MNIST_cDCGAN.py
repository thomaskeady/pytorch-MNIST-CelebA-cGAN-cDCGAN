import os, time
import matplotlib.pyplot as plt
import itertools
import pickle
import imageio
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

from CustomDataset import CustomDataset

from torchviz import make_dot

# G(z)
class generator(nn.Module):
    # initializers
    def __init__(self, d=128):
        super(generator, self).__init__()
        # self.deconv1_1 = nn.ConvTranspose2d(100, d*4, 8, 1, 0)
        # self.deconv1_1_bn = nn.BatchNorm2d(d*4)
        # self.deconv1_2 = nn.ConvTranspose2d(10, d*4, 4, 1, 0)
        # self.deconv1_2_bn = nn.BatchNorm2d(d*2)
        # self.deconv2 = nn.ConvTranspose2d(d*8, d*4, 4, 2, 1)
        # self.deconv2_bn = nn.BatchNorm2d(d*4)
        # self.deconv3 = nn.ConvTranspose2d(d*4, d*2, 4, 2, 1)
        # self.deconv3_bn = nn.BatchNorm2d(d*2)
        # #self.deconv4 = nn.ConvTranspose2d(d, 1, 4, 2, 1)
        # self.deconv4 = nn.ConvTranspose2d(d*2, d, 4, 2, 1)
        # self.deconv4_bn = nn.BatchNorm2d(d)
        # self.deconv5 = nn.ConvTranspose2d(d, 1, 4, 2, 1)

        # #self.fc1 = nn.Linear(300, 8192)    # 512*4*4
        # self.fc1 = nn.Linear(300, 32768)    # 512*8*8
        # #self.fc1 = nn.Linear(300, 32768*2)    # 512*8*8

        self.deconv1_1 = nn.ConvTranspose2d(100, d*2, 8, 1, 0)
        self.deconv1_1_bn = nn.BatchNorm2d(d*2)
        self.deconv1_2 = nn.ConvTranspose2d(10, d*4, 4, 1, 0)
        self.deconv1_2_bn = nn.BatchNorm2d(d*2)
        self.deconv2 = nn.ConvTranspose2d(d*4, d*2, 4, 2, 1)
        self.deconv2_bn = nn.BatchNorm2d(d*2)
        self.deconv3 = nn.ConvTranspose2d(d*2, d, 4, 2, 1)
        self.deconv3_bn = nn.BatchNorm2d(d)
        #self.deconv4 = nn.ConvTranspose2d(d, 1, 4, 2, 1)
        #self.deconv4 = nn.ConvTranspose2d(d*2, d, 4, 2, 1)
        #self.deconv4_bn = nn.BatchNorm2d(d)
        self.deconv5 = nn.ConvTranspose2d(d, 1, 4, 2, 1)

        #self.fc1 = nn.Linear(300, 8192)    # 512*4*4
        #self.fc1 = nn.Linear(300, 32768)    # 512*8*8
        self.fc1 = nn.Linear(300, 16384)    # 512*8*8
        #self.fc1 = nn.Linear(300, 32768*2)    # 512*8*8



    # weight_init
    def weight_init(self, mean, std):
        for m in self._modules:
            normal_init(self._modules[m], mean, std)

    # forward method
    def forward(self, input, label):

        #print(input.shape)
        #print(label.shape)

        x = F.leaky_relu(self.deconv1_1_bn(self.deconv1_1(input)))

        #print(input.shape)
        #print(x.shape)
        #print(label.shape)

        y = F.leaky_relu(self.fc1(label))

        #y = F.relu(self.deconv1_2_bn(self.deconv1_2(label)))

        #y = y.view(-1, 512, 8, 8)
        y = y.view(-1, 256, 8, 8)

        #print(x.shape)
        #print(y.shape)

        x = torch.cat([x, y], 1)
        x = F.leaky_relu(self.deconv2_bn(self.deconv2(x)))
        x = F.leaky_relu(self.deconv3_bn(self.deconv3(x)))
        #x = F.tanh(self.deconv4(x))
        #x = F.relu(self.deconv4_bn(self.deconv4(x)))
        x = F.tanh(self.deconv5(x))

        return x

class discriminator(nn.Module):
    # initializers
    def __init__(self, d=128):
        super(discriminator, self).__init__()
        self.conv1_1 = nn.Conv2d(1, int(d/4), 4, 2, 1)
        self.conv1_2 = nn.Conv2d(10, int(d/4), 4, 2, 1)
        self.conv2 = nn.Conv2d(int(d/2), d, 4, 2, 1)
        self.conv2_bn = nn.BatchNorm2d(d)
        self.conv3 = nn.Conv2d(d, d*2, 4, 2, 1)
        self.conv3_bn = nn.BatchNorm2d(d*2)
        #self.conv4 = nn.Conv2d(d * 2, 1, 4, 1, 0)
        self.conv4 = nn.Conv2d(d * 2, d*4, 4, 1, 0)
        self.conv4_bn = nn.BatchNorm2d(d*4)
        self.conv5 = nn.Conv2d(d * 4, 1, 5, 1, 0)

        #self.fc1 = nn.Linear(300, 16384)    # 16*16*64
        #self.fc1 = nn.Linear(300, 10240)    # 4*4*10*64
        #self.fc1 = nn.Linear(300, 4194304)    # 64*64*32*32
        self.fc1 = nn.Linear(300, 32768)    # 

    # weight_init
    def weight_init(self, mean, std):
        for m in self._modules:
            normal_init(self._modules[m], mean, std)

    # forward method
    def forward(self, input, label):
        x = F.leaky_relu(self.conv1_1(input), 0.2)

        #print(input.shape)
        #print(x.shape)

        y_ = F.leaky_relu(self.fc1(label), 0.2)
        #y = F.leaky_relu(self.conv1_2(label), 0.2)
        #print(y_.shape)

        y_ = y_.view(64, 32, 32, 32)
        #y = F.leaky_relu(self.conv1_2(y_), 0.2)
        y=y_

        #print(x.shape)
        #print(y.shape[0])

        x = torch.cat([x, y], 1)
        x = F.leaky_relu(self.conv2_bn(self.conv2(x)), 0.2)
        x = F.leaky_relu(self.conv3_bn(self.conv3(x)), 0.2)
        x = F.leaky_relu(self.conv4_bn(self.conv4(x)), 0.2)
        #x = F.sigmoid(self.conv4(x))
        x = F.sigmoid(self.conv5(x))

        return x

def normal_init(m, mean, std):
    if isinstance(m, nn.ConvTranspose2d) or isinstance(m, nn.Conv2d):
        m.weight.data.normal_(mean, std)
        m.bias.data.zero_()

# fixed noise & label
temp_z_ = torch.randn(8, 100)
fixed_z_ = temp_z_
fixed_y_ = torch.zeros(8, 1)
for i in range(7):
    fixed_z_ = torch.cat([fixed_z_, temp_z_], 0)
    temp = torch.ones(8, 1) + i
    fixed_y_ = torch.cat([fixed_y_, temp], 0)

#fixed_z_ = fixed_z_.view(-1, 100, 1, 1)
fixed_z_ = torch.rand(64, 100).view(64, 100, 1, 1)
fixed_y_label_ = torch.zeros(64, 300)
#fixed_y_label_.scatter_(1, fixed_y_.type(torch.LongTensor), 1)
fixed_y_label_ = (torch.rand(64, 300) * 1).type(torch.FloatTensor).squeeze()
#fixed_y_label_ = fixed_y_label_.view(-1, 300, 1, 1)
fixed_z_, fixed_y_label_ = Variable(fixed_z_.cuda(), volatile=True), Variable(fixed_y_label_.cuda(), volatile=True)
def show_result(num_epoch, show = False, save = False, path = 'result.png'):
    
    G.eval()
    # print('fixed')
    # print(fixed_z_.shape)
    # print(fixed_y_label_.shape)


    test_images = G(fixed_z_, fixed_y_label_)
    G.train()

    size_figure_grid = 8
    fig, ax = plt.subplots(size_figure_grid, size_figure_grid, figsize=(5, 5))
    for i, j in itertools.product(range(size_figure_grid), range(size_figure_grid)):
        ax[i, j].get_xaxis().set_visible(False)
        ax[i, j].get_yaxis().set_visible(False)

    for k in range(8*8):
        i = k // 8
        j = k % 8
        ax[i, j].cla()
        ax[i, j].imshow(test_images[k, 0].cpu().data.numpy(), cmap='gray')

    label = 'Epoch {0}'.format(num_epoch)
    fig.text(0.5, 0.04, label, ha='center')
    plt.savefig(path)

    if show:
        plt.show()
    else:
        plt.close()

def show_train_hist(hist, show = False, save = False, path = 'Train_hist.png'):
    x = range(len(hist['D_losses']))

    y1 = hist['D_losses']
    y2 = hist['G_losses']

    plt.plot(x, y1, label='D_loss')
    plt.plot(x, y2, label='G_loss')

    plt.xlabel('Epoch')
    plt.ylabel('Loss')

    plt.legend(loc=4)
    plt.grid(True)
    plt.tight_layout()

    if save:
        plt.savefig(path)

    if show:
        plt.show()
    else:
        plt.close()

# training parameters
batch_size = 128
G_lr = 0.002
D_lr = 0.0002
train_epoch = 100

# data_loader
#img_size = 32
img_size = 64
transform = transforms.Compose([
        #transforms.Scale(img_size),
        transforms.Grayscale(), # Default output channels is 1
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
])
# train_loader = torch.utils.data.DataLoader(
#     datasets.MNIST('data', train=True, download=True, transform=transform),
#     batch_size=batch_size, shuffle=True)

img_dir = 'data/processed/cedict_dir_v2/'
csv_dir = 'data/processed/cedict_vectors_v2.csv'

dset = CustomDataset(csv_dir, img_dir, '.png', transform)

train_loader = torch.utils.data.DataLoader(dset, batch_size=128, shuffle=True)

# temp = plt.imread(train_loader.dataset.imgs[0])
# print(temp.shape)
# if (temp.shape[0] != img_size) or (temp.shape[0] != img_size):
#     sys.stderr.write('Error! image size is not 64 x 64! run \"celebA_data_preprocess.py\" !!!')
#     sys.exit(1)


# network
G = generator(128)
D = discriminator(128)
G.weight_init(mean=0.0, std=0.02)
D.weight_init(mean=0.0, std=0.02)
G.cuda()
D.cuda()

# Binary Cross Entropy loss
BCE_loss = nn.BCELoss()

# Adam optimizer
G_optimizer = optim.Adam(G.parameters(), lr=G_lr, betas=(0.5, 0.999))
D_optimizer = optim.Adam(D.parameters(), lr=D_lr, betas=(0.5, 0.999))

# results save folder
root = 'MNIST_cDCGAN_results/'
model = 'MNIST_cDCGAN_'
if not os.path.isdir(root):
    os.mkdir(root)
if not os.path.isdir(root + 'Fixed_results'):
    os.mkdir(root + 'Fixed_results')

train_hist = {}
train_hist['D_losses'] = []
train_hist['G_losses'] = []
train_hist['per_epoch_ptimes'] = []
train_hist['total_ptime'] = []

# label preprocess
# onehot = torch.zeros(10, 10)
# onehot = onehot.scatter_(1, torch.LongTensor([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).view(10,1), 1).view(10, 10, 1, 1)
# fill = torch.zeros([10, 10, img_size, img_size])
# for i in range(10):
#     fill[i, i, :, :] = 1

# Train D if its loss is greater than this
D_loss_thresh = 10
train_D = False


# Train G if its loss is greater than this
G_loss_thresh = 4
train_G = True


# print('Trying to make_dot')

# noisex = torch.randn(100, 100, 64, 64)
# noisey = torch.randn(100, 300)
# y = G(Variable(noisex.cuda()), Variable(noisey.cuda()))
# img = make_dot(y)
# g.view()




print('training start!')
start_time = time.time()
for epoch in range(train_epoch):
    D_losses = []
    G_losses = []

    # learning rate decay
    if (epoch+1) == 11:
        G_optimizer.param_groups[0]['lr'] /= 10
        D_optimizer.param_groups[0]['lr'] /= 10
        print("learning rate change!")

    if (epoch+1) == 16:
        G_optimizer.param_groups[0]['lr'] /= 10
        D_optimizer.param_groups[0]['lr'] /= 10
        print("learning rate change!")

    epoch_start_time = time.time()
    y_real_ = torch.ones(batch_size)
    y_fake_ = torch.zeros(batch_size)
    y_real_, y_fake_ = Variable(y_real_.cuda()), Variable(y_fake_.cuda())

    #print(fill)
    count = 0

    for x_, y_ in train_loader:
        # train discriminator D

        #print(x_.shape)
        #print(y_.shape)
        #y_ = torch.ones(y_.shape)    # Consistent conditions for tseting

        D.zero_grad()

        mini_batch = x_.size()[0]

        if mini_batch != batch_size:
            y_real_ = torch.ones(mini_batch)
            y_fake_ = torch.zeros(mini_batch)
            y_real_, y_fake_ = Variable(y_real_.cuda()), Variable(y_fake_.cuda())

        #print('\t' + str(count))
        count = count + 1
        #print(y_[0])
        #print(y_[1])
        #y_fill_ = fill[y_]
        y_fill_ = y_
        x_, y_fill_ = Variable(x_.cuda()), Variable(y_fill_.cuda())

        #print(y_fill_.shape)
        #print(x_.shape)

        D_result = D(x_, y_fill_.float()).squeeze()

        make_dot(D_result)
        #print(D_result.shape)
        #print(y_real_.shape)

        D_real_loss = BCE_loss(D_result, y_real_)

        z_ = torch.randn((mini_batch, 100)).view(-1, 100, 1, 1)
        y_ = (torch.rand(mini_batch, 300) * 1).type(torch.FloatTensor).squeeze()
        #y_label_ = onehot[y_]
        #print(y_.shape)
        y_label_ = y_
        y_fill_ = y_
        z_, y_label_, y_fill_ = Variable(z_.cuda()), Variable(y_label_.cuda()), Variable(y_fill_.cuda())

        #print(y_label_.shape)


        G_result = G(z_, y_label_)
        #print(G_result.shape)

        lg = make_dot(G_result)
        lg.view()


        D_result = D(G_result, y_fill_.float()).squeeze()

        D_fake_loss = BCE_loss(D_result, y_fake_)
        D_fake_score = D_result.data.mean()

        D_train_loss = D_real_loss + D_fake_loss

        D_train_loss.backward()

        if train_D:
            D_optimizer.step()

        D_losses.append(D_train_loss.data[0])


        # for f in D.parameters():
        #     print(f.grad)            



        # train generator G
        G.zero_grad()

        z_ = torch.randn((mini_batch, 100)).view(-1, 100, 1, 1)
        #y_ = (torch.rand(mini_batch, 1) * 10).type(torch.LongTensor).squeeze()
        y_ = (torch.rand(mini_batch, 300) * 1).type(torch.FloatTensor).squeeze()
        y_label_ = y_
        y_fill_ = y_
        z_, y_label_, y_fill_ = Variable(z_.cuda()), Variable(y_label_.cuda()), Variable(y_fill_.cuda())

        G_result = G(z_, y_label_)
        D_result = D(G_result, y_fill_).squeeze()

        G_train_loss = BCE_loss(D_result, y_real_)

        
        G_train_loss.backward()
        if train_G:
            G_optimizer.step()

        G_losses.append(G_train_loss.data[0])



    epoch_end_time = time.time()
    per_epoch_ptime = epoch_end_time - epoch_start_time

    print('[%d/%d] - ptime: %.2f, loss_d: %.3f, loss_g: %.3f' % ((epoch + 1), train_epoch, per_epoch_ptime, torch.mean(torch.FloatTensor(D_losses)),
                                                              torch.mean(torch.FloatTensor(G_losses))))

    if torch.mean(torch.FloatTensor(D_losses)) > D_loss_thresh:
        train_D = True
    else:
        train_D = False

    if torch.mean(torch.FloatTensor(G_losses)) > G_loss_thresh:
        train_G = True
    else:
        train_G = False
    
    print('Training D: ' + str(train_D) + '\tTraining G: ' + str(train_G))


    fixed_p = root + 'Fixed_results/' + model + str(epoch + 1) + '.png'
    show_result((epoch+1), save=True, path=fixed_p)
    train_hist['D_losses'].append(torch.mean(torch.FloatTensor(D_losses)))
    train_hist['G_losses'].append(torch.mean(torch.FloatTensor(G_losses)))
    train_hist['per_epoch_ptimes'].append(per_epoch_ptime)

end_time = time.time()
total_ptime = end_time - start_time
train_hist['total_ptime'].append(total_ptime)

print("Avg one epoch ptime: %.2f, total %d epochs ptime: %.2f" % (torch.mean(torch.FloatTensor(train_hist['per_epoch_ptimes'])), train_epoch, total_ptime))
print("Training finish!... save training results")
torch.save(G.state_dict(), root + model + 'generator_param.pkl')
torch.save(D.state_dict(), root + model + 'discriminator_param.pkl')
with open(root + model + 'train_hist.pkl', 'wb') as f:
    pickle.dump(train_hist, f)

show_train_hist(train_hist, save=True, path=root + model + 'train_hist.png')

images = []
for e in range(train_epoch):
    img_name = root + 'Fixed_results/' + model + str(e + 1) + '.png'
    images.append(imageio.imread(img_name))
imageio.mimsave(root + model + 'generation_animation.gif', images, fps=5)
