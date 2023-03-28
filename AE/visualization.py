from models import create_model
import os
from data import create_dataset, get_character_names
import option_parser
from visualization.skeleton_plot import pyplot_skeleton
from visualization.draw_animation import draw_3Danimation, draw_3Danimation_2person

if __name__ == "__main__":
    save_dir = '../train_model/pretrained_AE/pretrained_AE0816'
    # save_dir = './pretrained_less_deep0811after'
    para_path = os.path.join(save_dir, 'para.txt')
    with open(para_path, 'r') as para_file:
        argv_ = para_file.readline().split()[1:]
        args = option_parser.get_parser().parse_args(argv_)
    args.cuda_device = 'cpu'
    args.is_train = False
    args.eval_seq = 0
    args.save_dir = save_dir
    character_names = get_character_names(args)
    print('character names: ', character_names)
    dataset = create_dataset(args, character_names)
    # print(args)
    model = create_model(args, dataset)
    model.load(epoch=args.epoch_num-1)

    motions = dataset[-3]
    model.set_input(motions)
    model.test()
    model.get_result()

    all_result = model.all_recons

    topo = list(dataset.joint_topology)
    topo[0] = 0

    for num in range(3):
        print(len(all_result[num]))
        # B
        retarget_gt = all_result[num][0].cpu().clone().numpy()
        retarget = all_result[num][1].cpu().clone().numpy()

        
        # A
        input = all_result[num][2].cpu().clone().numpy()

        i = 10

        # # retarget_gt_plot = pyplot_skeleton(topo, retarget_gt[i], show = False, color = "red", relative = False)
        # # input and output compare
        # pyplot_skeleton(topo, input[i], relative = False)

        # # retargeting compare
        # retarget_gt_plot = pyplot_skeleton(topo, retarget_gt[i], show = False, color = "red", relative = False)
        # pyplot_skeleton(topo, retarget[i], ax = retarget_gt_plot, color = "blue", relative = False)

        # draw_3Danimation(topo, retarget_gt, str(num)+"_retarget_gt.gif", world_position=True)
        if num == 0:
            draw_3Danimation(topo, input,"black", "results/unseen_input.gif", world_position=True)
        draw_3Danimation_2person(topo, retarget_gt, "red", retarget, "blue", "results/unseen_"+str(num)+"_retarget_comparaison.gif", world_position = True)

