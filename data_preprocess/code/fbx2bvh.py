import bpy
import numpy as np
from os import listdir, path

def fbx2bvh(data_path, file):
    sourcepath = data_path+"/"+file
    bvh_path = data_path+"/"+file.split(".fbx")[0]+".bvh"

    bpy.ops.import_scene.fbx(filepath=sourcepath)

    frame_start = 9999
    frame_end = -9999
    action = bpy.data.actions[-1]
    # print("action:", action)
    if  action.frame_range[1] > frame_end:
      frame_end = int(action.frame_range[1])
    if action.frame_range[0] < frame_start:
      frame_start = int(action.frame_range[0])
    print(frame_start)
    frame_end = np.max([60, frame_end])
    print(bvh_path)
    bpy.ops.export_anim.bvh(filepath=bvh_path,
                            frame_start=frame_start,
                            frame_end=frame_end, root_transform_only=True)
    bpy.data.actions.remove(bpy.data.actions[-1])
    print(data_path+"/"+file+" processed.")

if __name__ == '__main__':
    print("aaa")
    data_path = "../Mixamo_fbx/"
    directories = sorted([f for f in listdir(data_path) if not f.startswith(".")])
    for d in directories:
      files = sorted([f for f in listdir(data_path+d) if f.endswith(".fbx")])
      for file in files:
          fbx2bvh(path.join(data_path,d), file)


    # data_path = "fbx"
    # document = sorted([f for f in listdir(data_path) if not f.startswith(".")])
    # print(document)
    # for d in document:
    #     # path = path.join(data_path, d)
    #     fbx2bvh(data_path, d)