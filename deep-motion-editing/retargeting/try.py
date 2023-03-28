from datasets import create_dataset, get_character_names
from torch.utils.data.dataloader import DataLoader
from models import create_model
import option_parser


args = option_parser.get_args()
characters = get_character_names(args)

dataset = create_dataset(args, characters)
data_loader = DataLoader(dataset, batch_size = args.batch_size, shuffle=True, num_workers=0)
model = create_model(args, characters, dataset)


for step, motions in enumerate(data_loader):
    if step == 0:
        model.set_input(motions)
        model.optimize_parameters()