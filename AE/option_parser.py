import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch_size", type = int, default = 32)
    parser.add_argument("--position_feature", type = int, default = 3)
    parser.add_argument("--offset_feature", type = int, default = 1)
    parser.add_argument('--save_dir', type=str, default='./pretrained', help='directory for all savings')
    parser.add_argument('--cuda_device', type=str, default='cuda:0', help='cuda device number, eg:[cuda:0]')
    parser.add_argument('--learning_rate', type=float, default=2e-3, help='learning rate')
    parser.add_argument('--window_size', type=int, default=64, help='length of time axis per window')
    parser.add_argument('--verbose', type=int, default=1)
    parser.add_argument('--debug', type=int, default=0)
    parser.add_argument('--is_train', type=int, default=1)
    parser.add_argument('--epoch_num', type=int, default=40001, help='epoch_num')
    parser.add_argument('--epoch_begin', type=int, default=0)
    parser.add_argument('--scheduler', type=str, default='none')
    parser.add_argument('--eval_seq', type=int, default=0)
    # parser.add_argument('--specific', type=bool, default=False)
    return parser


def get_args():
    parser = get_parser()
    # args = parser.parse_args()
    args,unknown = parser.parse_known_args()
    return args

def get_std_bvh(args=None, dataset=None):
    if args is None and dataset is None: raise Exception('Unexpected parameter')
    if dataset is None: dataset = args.dataset
    std_bvh = './datasets/train_set/offsets/{}.bvh'.format(dataset)
    return std_bvh

def get_std_bvh_test(args=None, dataset=None):
    if args is None and dataset is None: raise Exception('Unexpected parameter')
    if dataset is None: dataset = args.dataset
    std_bvh = './datasets/test_set/offsets/{}.bvh'.format(dataset)
    return std_bvh

def try_mkdir(path):
    import os
    if not os.path.exists(path):
        os.mkdir(path)
