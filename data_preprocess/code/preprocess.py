from calendar import c
import os
import numpy as np
from bvh_parser import BVH_file
import shutil
from option_parser import try_mkdir

def collect_bvh(data_path, character, files, save_path):
    print('begin {}'.format(character))
    motions = []
    for i, motion in enumerate(files):
        if not os.path.exists(data_path + character + '/' + motion):
            continue
        file = BVH_file(data_path + character + '/' + motion)
        a_data = file.to_dataset()
        motions.append(a_data)

    save_file = save_path + character + '.npy'

    np.save(save_file, motions)
    print('Npy file saved at {}'.format(save_file))
    

def copy_offset_bvh(source_path, character, files, dest_path):
    """
    copy an arbitrary bvh file as a static information (skeleton's offset) reference
    """
    # cmd = 'cp \"{}\" ../datasets/offsets/{}.bvh'.format(data_path + character + '/' + files[0], character)
    shutil.copy(source_path + character + '/' + files[0], dest_path+'/{}.bvh'.format(character) )


if __name__ == '__main__':
    prefix = '../train_set/'
    characters = [f for f in os.listdir(prefix) if os.path.isdir(os.path.join(prefix, f))]
    try_mkdir('../datasets')
    try_mkdir('../datasets/train_set')
    try_mkdir('../datasets/train_set/offsets')
    try_mkdir('../datasets/train_set/npy')
    for character in characters:
        data_path = os.path.join(prefix, character)
        files = sorted([f for f in os.listdir(data_path) if f.endswith(".bvh")])

        collect_bvh(prefix, character, files, '../datasets/train_set/npy/')
        copy_offset_bvh(prefix, character,files, '../datasets/train_set/offsets/')

    # prefix = '../datasets/test_set/'
    # characters = [f for f in os.listdir(prefix) if os.path.isdir(os.path.join(prefix, f))]
    # try_mkdir('../datasets/test_set/offsets')
    # # try_mkdir('../datasets/test_set/npy')
    # for character in characters:
    #     data_path = os.path.join(prefix, character)
    #     files = sorted([f for f in os.listdir(data_path) if f.endswith(".bvh")])
        
    #     # collect_bvh(prefix, character, files, '../datasets/test_set/npy/')
    #     copy_offset_bvh(prefix, character, files, '../datasets/test_set/offsets/')


    # prefix = '../train_AE/'
    # characters = [f for f in os.listdir(prefix) if os.path.isdir(os.path.join(prefix, f))]
    # try_mkdir('../datasets')
    # try_mkdir('../datasets/train_AE')
    # try_mkdir('../datasets/train_AE/offsets')
    # try_mkdir('../datasets/train_AE/npy')
    # for character in characters:
    #     data_path = os.path.join(prefix, character)
    #     files = sorted([f for f in os.listdir(data_path) if f.endswith(".bvh")])
    #     print(character, files)
    #     collect_bvh(prefix, character, files, '../datasets/train_AE/npy/')
    #     copy_offset_bvh(prefix, character, files, '../datasets/train_AE/offsets/')

    # prefix = '../Mixamo/test_AE/'
    # characters = [f for f in os.listdir(prefix) if os.path.isdir(os.path.join(prefix, f))]
    # try_mkdir('../datasets')
    # try_mkdir('../datasets/test_AE')
    # try_mkdir('../datasets/test_AE/offsets')
    # for character in characters:
    #     data_path = os.path.join(prefix, character)
    #     files = sorted([f for f in os.listdir(data_path) if f.endswith(".bvh")])
    #     print(character, files)
    #     copy_offset_bvh(prefix, character, files, '../datasets/test_AE/offsets/')