# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import keypointstoangles


keypointsToAngles = keypointstoangles.KeypointsToAngles()

LShoulderPitch_list = []
LShoulderRoll_list = []
RShoulderPitch_list = []
RShoulderRoll_list = []
LElbowYaw_list = []
LElbowRoll_list = []
RElbowYaw_list = []
RElbowRoll_list = []
LWristYaw_list = []
RWristYaw_list = []
HipPitch_list = []
LHand_list = []
RHand_list = []
HeadPitch_list = []
HeadYaw_list = []


df = pd.read_csv('gesture.csv')
# #----------   Command angles  -------------------
Hips_X = df['Hips.X'].values.tolist()
Hips_Y = df['Hips.Y'].values.tolist()
Hips_Z = df['Hips.Z'].values.tolist()
Neck_X = df['Neck.X'].values.tolist()
Neck_Y = df['Neck.Y'].values.tolist()
Neck_Z = df['Neck.Z'].values.tolist()
LeftArm_X = df['LeftArm.X'].values.tolist()
LeftArm_Y = df['LeftArm.Y'].values.tolist()
LeftArm_Z = df['LeftArm.Z'].values.tolist()
LeftForeArm_X = df['LeftForeArm.X'].values.tolist()
LeftForeArm_Y = df['LeftForeArm.Y'].values.tolist()
LeftForeArm_Z = df['LeftForeArm.Z'].values.tolist()
LeftHand_X = df['LeftHand.X'].values.tolist()
LeftHand_Y = df['LeftHand.Y'].values.tolist()
LeftHand_Z = df['LeftHand.Z'].values.tolist()
RightArm_X = df['RightArm.X'].values.tolist()
RightArm_Y = df['RightArm.Y'].values.tolist()
RightArm_Z = df['RightArm.Z'].values.tolist()
RightForeArm_X = df['RightForeArm.X'].values.tolist()
RightForeArm_Y = df['RightForeArm.Y'].values.tolist()
RightForeArm_Z = df['RightForeArm.Z'].values.tolist()
RightHand_X = df['RightHand.X'].values.tolist()
RightHand_Y = df['RightHand.Y'].values.tolist()
RightHand_Z = df['RightHand.Z'].values.tolist()

for i in range(len(Hips_X)):

    pNeck =   [Neck_X[i], Neck_Y[i],Neck_Z[i]]
    pMidHip = [Hips_X[i], Hips_Y[i],Hips_Z[i]]
    p2 = [LeftArm_X[i], LeftArm_Y[i],LeftArm_Z[i]]
    p3 = [LeftForeArm_X[i], LeftForeArm_Y[i],LeftForeArm_Z[i]]
    p4 = [LeftHand_X[i], LeftHand_Y[i],LeftHand_Z[i]]
    p5 = [RightArm_X[i], RightArm_Y[i],RightArm_Z[i]]
    p6 = [RightForeArm_X[i], RightForeArm_Y[i],RightForeArm_Z[i]]
    p7 = [RightHand_X[i], RightHand_Y[i],RightHand_Z[i]]  

    LShoulderPitch, LShoulderRoll = keypointsToAngles.obtain_LShoulderPitchRoll_angles(pNeck, p2, p3, pMidHip)
    RShoulderPitch, RShoulderRoll = keypointsToAngles.obtain_RShoulderPitchRoll_angles(pNeck, p5, p6, pMidHip)

    LElbowYaw, LElbowRoll, LHand = keypointsToAngles.obtain_LElbowYawRoll_angle(pNeck, p2, p3, p4)
    RElbowYaw, RElbowRoll, RHand = keypointsToAngles.obtain_RElbowYawRoll_angle(pNeck, p5, p6, p7)

    LShoulderPitch_list.append(LShoulderPitch*(-1))
    LShoulderRoll_list.append(LShoulderRoll)
    RShoulderPitch_list.append(RShoulderPitch*(-1))
    RShoulderRoll_list.append(RShoulderRoll)
    if LElbowRoll > -0.1:
        LElbowRoll = -0.1
    if LElbowRoll < -1.5:
        LElbowRoll = -1.5
    LElbowYaw_list.append(LElbowYaw)
    LElbowRoll_list.append(LElbowRoll)
    if LElbowRoll > 1.5:
        LElbowRoll = 1.5
    if LElbowRoll < 0.1:
        LElbowRoll = 0.1
    RElbowYaw_list.append(RElbowYaw)
    RElbowRoll_list.append(RElbowRoll)


angles = {'LShoulderPitch': LShoulderPitch_list, 'LShoulderRoll': LShoulderRoll_list, 
            'LElbowYaw': LElbowYaw_list, 'LElbowRoll': LElbowRoll_list,
            'RShoulderPitch': RShoulderPitch_list, 'RShoulderRoll': RShoulderRoll_list,
            'RElbowYaw': RElbowYaw_list, 'RElbowRoll': RElbowRoll_list}

ThetaR = pd.DataFrame.from_dict(angles)
ThetaR.to_csv('./csv/angles_bvh.csv', index=False)

