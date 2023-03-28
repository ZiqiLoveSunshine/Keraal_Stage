from torch.utils.data.dataloader import DataLoader
from data import create_dataset, get_character_names
from option_parser import get_args, try_mkdir
from models import create_model
from visualization.skeleton_plot import pyplot_skeleton
import torch
args = get_args()
# print(args)
characters = get_character_names(args)
dataset = create_dataset(args, characters)
print(len(dataset))
try_mkdir(args.save_dir)
data_loader = DataLoader(dataset, batch_size = args.batch_size, num_workers=0)
model = create_model(args, dataset)
args.specific = True
for step, motion in enumerate(data_loader):
    model.set_input(motion)
    # model.optimize_parameters()