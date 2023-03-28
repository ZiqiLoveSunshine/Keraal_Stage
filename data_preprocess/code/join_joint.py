import sys
import os
from option_parser import try_mkdir
import numpy as np
from tqdm import tqdm
from bvh_parser import BVH_file

sys.path.append("../utils")
import BVH_mod as BVH

def join_joint(file_name, save_file=None):
    if save_file is None:
        save_file = file_name
    target_joints = ['Spine1_split', 'LeftShoulder_split', 'RightShoulder_split']
    target_idx = [-1] * len(target_joints)
    anim, names, ftime = BVH.load(file_name)

    # print(target_idx)
    n_joint = len(anim.parents)
    # print("n_joint: ", n_joint)
    for i, name in enumerate(names):
        if ':' in name:
            name = name[name.find(':') + 1:]
            names[i] = name

        for j, joint in enumerate(target_joints):
            if joint == names[i]:
                target_idx[j] = i
    # print("target index: ", target_idx)
    new_anim = anim.copy()
    new_anim.offsets = []
    new_anim.parents = []
    new_anim.rotations = []
    new_names = []

    target_idx.sort()

    bias = 0
    new_parent = {}
    target_idx.append(-1)
    for i, parent in enumerate(anim.parents):
        # print(target_idx)
        if parent == target_idx[bias]:
            new_parent[i] = parent -1
            bias +=1
            # print(bias)
        else:
            new_parent[i] = parent

    new_idx = {}
    for i, parent in new_parent.items():
        if i in target_idx:
            continue
        else:
            if target_idx[0] < i < target_idx[1]:
                new_i = i - 1
            elif target_idx[1] < i < target_idx[2]:
                new_i = i - 2
            elif target_idx[2] < i:
                new_i = i - 3
            else:
                new_i = i

            if target_idx[0] < parent < target_idx[1]:
                ne_parent = parent - 1
            elif target_idx[1] < parent < target_idx[2]:
                ne_parent = parent - 2
            elif target_idx[2] < parent:
                ne_parent = parent - 3
            else:
                ne_parent = parent
            new_idx[new_i] = ne_parent

    # print("new index: ",new_idx)

    identity = np.zeros_like(anim.rotations)
    identity = identity[:, :1, :]

    bias = 0
    for i in range(n_joint):
        if i == target_idx[bias]:
            parent = new_parent[i]
            new_anim.offsets[parent-bias] += anim.offsets[i]
            bias +=1
            continue
        new_anim.parents.append(new_idx[i-bias])
        new_names.append(names[i])
        new_anim.rotations.append(anim.rotations[:, [i], :])
        new_anim.offsets.append(anim.offsets[i])
    # print("new_anim parent : ",len(new_anim.parents))
    # print(new_anim.offsets)

    offset_spine = new_anim.offsets[2] + new_anim.offsets[3]
    new_anim.offsets[2] = offset_spine / 2
    new_anim.offsets[3] = offset_spine / 2
    new_anim.offsets = np.array(new_anim.offsets)
    # print(new_anim.offsets)
    new_anim.rotations = np.concatenate(new_anim.rotations, axis=1)
    try_mkdir(os.path.split(save_file)[0])
    BVH.save(save_file, new_anim, names=new_names, frametime=ftime, order='xyz')

def batch_join(source, dest):
    files = [f for f in os.listdir(source) if f.endswith('.bvh')]
    try:
        bvh_file = BVH_file(os.path.join(source, files[0]))
        if bvh_file.skeleton_type != 1: return
    except:
        return

    print("Working on {}".format(os.path.split(source)[-1]))
    try_mkdir(dest)
    files = [f for f in os.listdir(source) if f.endswith('.bvh')]
    print(source)
    print(dest)
    for i, file in tqdm(enumerate(files), total=len(files)):
        in_file = os.path.join(source, file)
        out_file = os.path.join(dest, file)
        join_joint(in_file, out_file)

if __name__ == "__main__":
    prefix = '../test_set/'
    names = [f for f in os.listdir(prefix) if os.path.isdir(os.path.join(prefix, f)) and '_m' in f]
    dest = "../datasets/test_set/"
    for name in names:
        batch_join(os.path.join(prefix, name), os.path.join(dest, name.split("_")[0]))