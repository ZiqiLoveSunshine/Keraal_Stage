import numpy as np
import math


class ForwardKinematics:
    def rotation_to_position3d(rotation, position, offset, topology, order='xyz', ignore_root_offset = True):
        result = np.empty(rotation.shape[:-1] + (3, ))
        # print("result: ", result.shape)

        transform = ForwardKinematics.transform_from_euler(rotation, order)
        offset_matrix = ForwardKinematics.transform_offset_matrix(position.shape[0],offset, ignore_root_offset)
        position_matrix = ForwardKinematics.transform_position_matrix(position)
        parent = np.zeros_like(transform)
    #     print("transform:", transform.shape)
    #     print("offset_matrix: ", offset_matrix.shape)

    #     print("position:", position_matrix.shape)
        for i, pi in enumerate(topology):
            if pi == -1:
            # we ignore the root offset or there will be problems
                localtoworld_root = np.matmul(offset_matrix[:,0,...],position_matrix)
                parent[:, 0,...] = np.matmul(localtoworld_root, transform[:, 0, ...])
    #             print(temp)
                result[:, 0, 0] = localtoworld_root[...,0,3]
                result[:, 0, 1] = localtoworld_root[...,1,3]
                result[:, 0, 2] = localtoworld_root[...,2,3]
    #             print(result)
                continue
    #         print("parent: {}, now: {}".format(pi, i))
            localtoworld = np.matmul(parent[:,pi,...],offset_matrix[:, i, ...])
            parent[:, i,...] = np.matmul(localtoworld, transform[:, i, ...])
            result[:, i, 0] = localtoworld[...,0,3]
            result[:, i, 1] = localtoworld[...,1,3]
            result[:, i, 2] = localtoworld[...,2,3]
        return result

    def transform_from_euler(rotation, order):
        rotation = rotation / 180 * np.pi
        transform = np.matmul(ForwardKinematics.transform_from_axis(rotation[..., 1], order[1]),
                                ForwardKinematics.transform_from_axis(rotation[..., 2], order[2]))
        transform = np.matmul(ForwardKinematics.transform_from_axis(rotation[..., 0], order[0]), transform)
        return transform
    
    def transform_from_axis(euler, axis):
        transform = np.zeros(euler.shape[0:3] + (4, 4))
        cos = np.cos(euler)
        sin = np.sin(euler)
    #     transform[..., :, :] = transform[..., :, :] = 0.0
        for i in range(4):
            transform[..., i, i] = 1.0
        
    #     print(transform)
        if axis == 'x':
            transform[..., 1, 1] = transform[..., 2, 2] = cos
            transform[..., 1, 2] = -sin
            transform[..., 2, 1] = sin
        if axis == 'y':
            transform[..., 0, 0] = transform[..., 2, 2] = cos
            transform[..., 0, 2] = sin
            transform[..., 2, 0] = -sin
        if axis == 'z':
            transform[..., 0, 0] = transform[..., 1, 1] = cos
            transform[..., 0, 1] = -sin
            transform[..., 1, 0] = sin

        return transform
    def transform_offset_matrix(frame, offset, ignore_root_offset):
        offset_matrix = np.zeros([frame, offset.shape[0], 4, 4])
        for i in range(4):
            offset_matrix[..., i, i] = 1.0
    #     print(offset_matrix)
        offset_matrix[..., :3, 3] = offset
        if ignore_root_offset:
            offset_matrix[:,0,...] = np.eye(4)
    #     print(offset_matrix)
        return offset_matrix

    def transform_position_matrix(position):
        position_matrix = np.zeros([position.shape[0], 4, 4])
        for i in range(4):
            position_matrix[..., i, i] = 1.0
    #     print(offset_matrix)
        position_matrix[:, :3, 3] = position
        return position_matrix