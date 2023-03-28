import pandas as pd
import sys
from naoqi import ALProxy
import time
import numpy as np

df = pd.read_csv('./csv/angles_bvh22.csv')
# #----------   Command angles  -------------------
LShoulder_Pitch = df['LShoulderPitch'].values.tolist()
RShoulder_Pitch = df['RShoulderPitch'].values.tolist()
LElbow_Yaw          = df['LElbowYaw'].values.tolist()
RElbow_Yaw          = df['RElbowYaw'].values.tolist()
LShoulder_Roll    = df['LShoulderRoll'].values.tolist()
RShoulder_Roll    = df['RShoulderRoll'].values.tolist()
LElbow_Roll          = df['LElbowRoll'].values.tolist()
RElbow_Roll          = df['RElbowRoll'].values.tolist()
# LWrist_Yaw             = df['LWristYaw'].values.tolist()
# RWrist_Yaw            = df['RWristYaw'].values.tolist()
# LHand                      = df['LHand'].values.tolist()
# RHand                      = df['RHand'].values.tolist()
# Hip_Pitch                = df['HipPitch'].values.tolist()
# Head_Yaw               = df['HeadYaw'].values.tolist()
# Head_Pitch            = df['HeadPitch'].values.tolist()
# TimeStamp       = df['TimeStamp'].values.tolist()

angles = [LShoulder_Roll, LShoulder_Pitch, RShoulder_Roll, RShoulder_Pitch, 
          LElbow_Roll, LElbow_Yaw, RElbow_Roll, RElbow_Yaw]
names = ['LShoulderRoll', 'LShoulderPitch', 'RShoulderRoll', 'RShoulderPitch', 
         'LElbowRoll', 'LElbowYaw','RElbowRoll', 'RElbowYaw']
# angles = [LShoulder_Roll, LShoulder_Pitch, LElbow_Roll, LElbow_Yaw]
# names = ['LShoulderRoll', 'LShoulderPitch', 'LElbowRoll', 'LElbowYaw']
def main():
    PORT = 46623
    robotIP = "127.0.0.1"
    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception as e:
        print ("Could not create proxy to ALMotion")
        print ("Error was: ",e)
        sys.exit(1)

    data_num = len(LShoulder_Roll)
    data_used = np.arange(data_num)
    for i in data_used:
        # motionProxy.setAngles(names, [LShoulder_Roll[i], LShoulder_Pitch[i], LElbow_Roll[i], LElbow_Yaw[i]], 1)
                                            # , Head_Yaw[i], Head_Pitch[i], LHand[i], RHand[i]], 1)
        motionProxy.setAngles(names, [LShoulder_Roll[i], LShoulder_Pitch[i], RShoulder_Roll[i], RShoulder_Pitch[i], 
                                            LElbow_Roll[i], LElbow_Yaw[i], RElbow_Roll[i], RElbow_Yaw[i]], 1)
                                            # ,  LWrist_Yaw[i], RWrist_Yaw[i]], 1)
        #                                     # , Head_Yaw[i], Head_Pitch[i], LHand[i], RHand[i]], 1)
        time.sleep(0.03)
    # ThetaSensor = pd.DataFrame.from_dict(angles)
    # ThetaSensor.to_csv('body_language_sensor.csv', index=False)

if __name__ == "__main__":
    
    main()


