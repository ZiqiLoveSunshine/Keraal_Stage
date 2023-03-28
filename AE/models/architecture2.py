import torch
import numpy as np
import random
import os
from torch import optim
from models.enc_and_dec import Encoder, Decoder
from models.base_model import BaseModel
from option_parser import try_mkdir

class DEEP_model(BaseModel):
    def __init__(self, args, dataset):
        super(DEEP_model, self).__init__(args)
        self.dataset = dataset
        self.n_topologies = self.dataset.character_num
        self.args = args
        self.enc = Encoder(args, self.dataset.joint_topology).to(self.device)
        self.dec = Decoder(args, self.enc).to(self.device)

        self.AE_para = list(self.enc.parameters()) +list(self.dec.parameters())
        #train
        if self.args.is_train:
            self.optimizerAE = optim.Adam(self.AE_para, args.learning_rate, betas=(0.9, 0.999))
            self.criterion_rec = torch.nn.MSELoss()
        else:
            from option_parser import try_mkdir
            self.results_path = os.path.join(args.save_dir, 'results')
            try_mkdir(self.results_path)


    def set_input(self, motions):
        self.motions = motions

        if self.is_train:
            
            if not self.args.specific:
                index_list = list(range(self.dataset.character_num))
                tmp = random.sample(index_list, 2)
            else:
                index_list = list(range(self.dataset.character_num-1))
                tmp = random.sample(index_list,1)
                tmp.append(self.dataset.character_num-1)
            self.motions_input, self.targets_input = motions[tmp[0]], motions[tmp[1]]
            print(self.targets_input[1])

        if not self.is_train:
            self.target_gt = []
            self.fake_list = []
            self.item_len = self.motions[-1]
            for i in range(1,self.n_topologies):
                self.target_gt.append(self.motions[0][i])
                self.fake_list.append(self.motions[1][i])
            self.motions_input = self.motions[0][0], [self.motions[1][0]]

    def forward(self):
        self.offset_repr = self.dataset.offsets
        self.offset_repr = self.offset_repr.to(self.device)
        self.motion, self.offset_idx = self.motions_input # batch_size * frame * joint * features_in
        self.target, self.target_idx = self.targets_input # batch_size * frame * joint * features_in
        self.motion = self.motion.to(self.device)
        self.target = self.target.to(self.device)


        self.offset_idx = self.offset_idx[0]
        self.true_offset = self.offset_repr[self.offset_idx]
        self.true_offset_enc = torch.concat(self.motion.shape[1]*[self.true_offset.unsqueeze(-1).unsqueeze(0)], dim=0) 
        self.true_offset_enc = torch.concat(self.motion.shape[0]*[self.true_offset_enc.unsqueeze(0)], dim = 0) 
        # latent space
        self.latent = self.enc(self.motion, self.true_offset_enc) # batch_size * frame/nnn * joint *features_in 
        
        # retargeting
        self.fake_idx = self.target_idx[0]
        self.fake_offset = self.offset_repr[self.fake_idx]
        self.fake_offset_latent = torch.concat(self.latent.shape[1]*[self.fake_offset.unsqueeze(-1).unsqueeze(0)], dim = 0)
        self.fake_offset_latent = torch.concat(self.latent.shape[0]*[self.fake_offset_latent.unsqueeze(0)], dim = 0)
        # print("retargeting: ")
        self.fake_res = self.dec(self.latent, self.fake_offset_latent)
        # print(self.fake_res.shape)
        # print(self.target.shape)

    def optimize_parameters(self):
        self.forward()
        # update G
        print("update")
        self.optimizerAE.zero_grad()
        # rec_loss
        self.rec_loss = self.criterion_rec(self.target, self.fake_res)
        self.loss_recoder.add_scalar('rec_loss', self.rec_loss)
        self.rec_loss.backward()
        self.optimizerAE.step()


    def verbose(self):
        res = {'rec_loss': self.rec_loss.item()}
        return sorted(res.items(), key=lambda x: x[0])

    def save(self):

        path = os.path.join(self.model_save_dir, "epoch_"+str(self.epoch_cnt))
        try_mkdir(path)
        torch.save(self.enc.state_dict(), os.path.join(path, 'encoder.pt'))
        torch.save(self.dec.state_dict(), os.path.join(path, 'decoder.pt'))
        print('Save at {} succeed!'.format(path))

        try_mkdir(os.path.join(self.model_save_dir,"optimizers"))
        file_name = os.path.join(self.model_save_dir, 'optimizers/{}/{}.pt'.format(self.epoch_cnt, 0))
        try_mkdir(os.path.split(file_name)[0])
        torch.save(self.optimizerAE.state_dict(), file_name)

        loss_path = os.path.join(self.model_save_dir,"loss")
        try_mkdir(loss_path)
        loss_path = os.path.join(self.model_save_dir,"loss/")
        self.loss_recoder.save(loss_path)

    def load(self, epoch=None):
        path = os.path.join(self.model_save_dir, 'epoch_{}'.format(epoch))
        print('loading from', path)
        if not os.path.exists(path):
            raise Exception('Unknown loading path')
        print('loading from epoch {}......'.format(epoch))
        self.enc.load_state_dict(torch.load(os.path.join(path, 'encoder.pt'),
                                                     map_location=self.args.cuda_device))
        self.dec.load_state_dict(torch.load(os.path.join(path, 'decoder.pt'),
                                                map_location=self.args.cuda_device))
        if self.is_train:
            file_name = os.path.join(self.model_save_dir, 'optimizers/{}/{}.pt'.format(epoch, 0))
            self.optimizerAE.load_state_dict(torch.load(file_name))
        self.epoch_cnt = epoch

    def compute_test_result(self):
        all_err = []
        # self.all_recons = []
        for i in range(len(self.fake_list)):
            self.target_idx = [i]
            self.targets_input = self.target_gt[i], [self.fake_list[i]]
            # print(self.targets_input)
            self.forward()
            # print(self.fake_res.shape)
            # print(1/0)
            _,__,joint_num, fea = self.fake_res.shape
            gt = self.target_gt[i].reshape((-1, joint_num, fea))[:self.item_len,...]
            fake = self.fake_res.reshape((-1, joint_num, fea))[:self.item_len,...]
            err = torch.sqrt((gt-fake)**2)
            err = torch.mean(err)
            all_err.append(err)
        all_err = torch.tensor(all_err)
        print("all_err: ", all_err.mean(), all_err)
        return all_err.mean()

    def get_result(self):
        with torch.no_grad():
            self.all_recons = []
            for i in range(len(self.fake_list)):
                self.target_idx = [i]
                self.targets_input = self.target_gt[i], [self.fake_list[i]]
                self.forward()
                print(self.fake_res.shape)
                # print(1/0)
                _,__,joint_num, fea = self.fake_res.shape
                input = self.motion.reshape((-1, joint_num, fea))[:self.item_len,...]
                gt = self.target_gt[i].reshape((-1, joint_num, fea))[:self.item_len,...]
                fake = self.fake_res.reshape((-1, joint_num, fea))[:self.item_len,...]
                self.all_recons.append([gt, fake, input])