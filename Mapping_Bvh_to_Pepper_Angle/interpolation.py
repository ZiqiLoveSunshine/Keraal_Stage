import pandas as pd
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

df_1 = pd.read_csv('complete.csv')
df_2 = pd.read_csv('semantic.csv')

# #----------   Command angles  -------------------
LShoulder_Pitch = df_1['LShoulderPitch'].values.tolist()
RShoulder_Pitch = df_1['RShoulderPitch'].values.tolist()
LElbow_Yaw      = df_1['LElbowYaw'].values.tolist()
RElbow_Yaw      = df_1['RElbowYaw'].values.tolist()
LShoulder_Roll  = df_1['LShoulderRoll'].values.tolist()
RShoulder_Roll  = df_1['RShoulderRoll'].values.tolist()
LElbow_Roll     = df_1['LElbowRoll'].values.tolist()
RElbow_Roll     = df_1['RElbowRoll'].values.tolist()
LWrist_Yaw      = df_1['LWristYaw'].values.tolist()
RWrist_Yaw      = df_1['RWristYaw'].values.tolist()
LHand           = df_1['LHand'].values.tolist()
RHand           = df_1['RHand'].values.tolist()
Hip_Pitch       = df_1['HipPitch'].values.tolist()
Head_Yaw        = df_1['HeadYaw'].values.tolist()
Head_Pitch      = df_1['HeadPitch'].values.tolist()
# TimeStamp       = df_1['TimeStamp'].values.tolist()

LShoulder_Pitch_inter = df_2['LShoulderPitch'].values.tolist()
RShoulder_Pitch_inter = df_2['RShoulderPitch'].values.tolist()
LElbow_Yaw_inter      = df_2['LElbowYaw'].values.tolist()
RElbow_Yaw_inter      = df_2['RElbowYaw'].values.tolist()
LShoulder_Roll_inter  = df_2['LShoulderRoll'].values.tolist()
RShoulder_Roll_inter  = df_2['RShoulderRoll'].values.tolist()
LElbow_Roll_inter     = df_2['LElbowRoll'].values.tolist()
RElbow_Roll_inter     = df_2['RElbowRoll'].values.tolist()
LWrist_Yaw_inter      = df_2['LWristYaw'].values.tolist()
RWrist_Yaw_inter      = df_2['RWristYaw'].values.tolist()
LHand_inter           = df_2['LHand'].values.tolist()
RHand_inter           = df_2['RHand'].values.tolist()
Hip_Pitch_inter       = df_2['HipPitch'].values.tolist()
Head_Yaw_inter        = df_2['HeadYaw'].values.tolist()
Head_Pitch_inter      = df_2['HeadPitch'].values.tolist()

T_1 = 8

angles_comp = [LShoulder_Roll, LShoulder_Pitch, RShoulder_Roll, RShoulder_Pitch, 
               LElbow_Roll, LElbow_Yaw, RElbow_Roll, RElbow_Yaw, Hip_Pitch,
               LWrist_Yaw, RWrist_Yaw, LHand, RHand, Head_Pitch, Head_Yaw]

angles_sem = [LShoulder_Roll_inter, LShoulder_Pitch_inter, RShoulder_Roll_inter, RShoulder_Pitch_inter, 
               LElbow_Roll_inter, LElbow_Yaw_inter, RElbow_Roll_inter, RElbow_Yaw_inter, Hip_Pitch_inter,
               LWrist_Yaw_inter, RWrist_Yaw_inter, LHand_inter, RHand_inter, Head_Pitch_inter, Head_Yaw_inter]

names = ['LShoulderRoll', 'LShoulderPitch', 'RShoulderRoll', 'RShoulderPitch', 
         'LElbowRoll', 'LElbowYaw','RElbowRoll', 'RElbowYaw','HipPitch',
         'LWristYaw', 'RWristYaw', 'LHand', 'RHand', 'HeadPitch', 'HeadYaw']


length = len(names)

mediate_angles_front = [[] for i in range(length)]

for i in range(length):
    mediate_angles_front[i] = np.linspace(angles_comp[i][10*T_1 - 10], angles_sem[i][0], 10)
    # print(mediate_angles_front[0])

# print('mediate_angles_front:', mediate_angles_front)

frame_2 = 10 * T_1 + len(angles_sem[0])

mediate_angles_after = [[] for i in range(length)]

for i in range(length):
    mediate_angles_after[i] = np.linspace(angles_sem[i][-1], angles_comp[i][frame_2 + 10],  10)

angle_final = [[] for i in range(length)]


print(type(angles_comp[0][0:(10*T_1 - 10)]))
print(type(mediate_angles_front[0]))
print(type(angles_sem[0]))

for i in range(length):
    angles_comp[i] = angles_comp[i][0:(10*T_1 - 10)] + mediate_angles_front[i].tolist() + angles_sem[i] + mediate_angles_after[i].tolist() + angles_comp[i][(frame_2 + 10):(-1)]
print('angle_final:', angles_comp[0])

# angles = {'LShoulderPitch': LShoulder_Pitch, 'LShoulderRoll': LShoulder_Roll, 
#             'LElbowYaw': LElbow_Yaw, 'LElbowRoll': LElbow_Roll, 
#             'RShoulderPitch': RShoulder_Pitch, 'RShoulderRoll': RShoulder_Roll, 
#             'RElbowYaw': RElbow_Yaw, 'RElbowRoll': RElbow_Roll, 'HipPitch': Hip_Pitch,
#             'LWristYaw': LWrist_Yaw, 'RWristYaw': RWrist_Yaw, 'LHand': LHand, 
#             'RHand': RHand, 'HeadPitch': Head_Pitch, 'HeadYaw': Head_Yaw}

angles = {'LShoulderRoll':angles_comp[0], 'LShoulderPitch':angles_comp[1], 'RShoulderRoll':angles_comp[2], 'RShoulderPitch':angles_comp[3], 
         'LElbowRoll':angles_comp[4], 'LElbowYaw':angles_comp[5],'RElbowRoll':angles_comp[6], 'RElbowYaw':angles_comp[7],'HipPitch':angles_comp[8],
         'LWristYaw':angles_comp[9], 'RWristYaw':angles_comp[10], 'LHand':angles_comp[11], 'RHand':angles_comp[12], 'HeadPitch':angles_comp[13], 'HeadYaw':angles_comp[14]}
# def main():
#     print("result")
ThetaSensor = pd.DataFrame.from_dict(angles)
ThetaSensor.to_csv('test.csv', index=False)

# if __name__ == "__main__":
    
#     main()


