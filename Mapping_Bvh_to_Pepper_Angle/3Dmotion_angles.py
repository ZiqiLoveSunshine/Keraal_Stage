# -*- coding: utf-8 -*-

import argparse
import cv2 as cv
import numpy as np
import mediapipe as mp
import pandas as pd
import keypointstoangles

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
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

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=1280)
    parser.add_argument("--height", help='cap height', type=int, default=720)
    parser.add_argument("--video", type=str, default="../videos/complete.mp4")
    parser.add_argument("--model_complexity",
                        help='model_complexity(0,1(default),2)',
                        type=int,
                        default=1)
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.5)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=float,
                        default=0.5)
    args = parser.parse_args()
    return args

def angle_calculation(p):
    p = np.array(p)

    pNeck =   (0.5 * (np.array(p[11]) + np.array(p[12]))).tolist()
    pMidHip = (0.5 * (np.array(p[23]) + np.array(p[24]))).tolist()
    pMidMouth = (0.5 * (np.array(p[9]) + np.array(p[10]))).tolist()

    LShoulderPitch, LShoulderRoll = keypointsToAngles.obtain_LShoulderPitchRoll_angles(pNeck, p[11], p[13], pMidHip)
    RShoulderPitch, RShoulderRoll = keypointsToAngles.obtain_RShoulderPitchRoll_angles(pNeck, p[12], p[14], pMidHip)
    
    LElbowYaw, LElbowRoll, LHand = keypointsToAngles.obtain_LElbowYawRoll_angle(pNeck, p[11], p[13], p[15])
    RElbowYaw, RElbowRoll, RHand = keypointsToAngles.obtain_RElbowYawRoll_angle(pNeck, p[12], p[14], p[16])

    LWristYaw = keypointsToAngles.obatin_LwristYaw_angle(p[11], p[13], p[15], p[21], p[17])
    RWristYaw = keypointsToAngles.obatin_RwristYaw_angle(p[12], p[14], p[16], p[22], p[18])

    HeadPitch = keypointsToAngles.obatin_HeadPitch_angle(p[0], pNeck)
    HeadYaw  = keypointsToAngles.obatin_HeadYaw_angle(p[0], p[12], p[11])

    HipPitch = keypointsToAngles.obtain_HipPitch_angles(pMidHip, pNeck)

    LShoulderPitch_list.append(LShoulderPitch)
    LShoulderRoll_list.append(LShoulderRoll)
    RShoulderPitch_list.append(RShoulderPitch)
    RShoulderRoll_list.append(RShoulderRoll)
    LElbowYaw_list.append(LElbowYaw)
    LElbowRoll_list.append(LElbowRoll)
    RElbowYaw_list.append(RElbowYaw)
    RElbowRoll_list.append(RElbowRoll)
    HipPitch_list.append(HipPitch)
    LWristYaw_list.append(LWristYaw)
    RWristYaw_list.append(RWristYaw)
    LHand_list.append(LHand)
    RHand_list.append(RHand)
    HeadPitch_list.append(HeadPitch)
    HeadYaw_list.append(HeadYaw)

def main():
    ## set Parameters
    args = get_args()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height
    model_complexity = args.model_complexity
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence
    video = args.video

    #Choose the video source
    if len(video) == 0:
        cap = cv.VideoCapture(cap_device)
    else:
        cap = cv.VideoCapture(video)
        print("the video is detected")

    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        model_complexity=model_complexity,
        enable_segmentation=False,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    while cap.isOpened():
        
        pos = []

        ret, image = cap.read()
        if not ret:
            break

        # Convert the BGR image to RGB.
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        #draw the landmarrks in the image
        mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv.imshow('MediaPipe Pose', image)

        for index, landmark in enumerate(results.pose_world_landmarks.landmark):
            pos.append([landmark.x, landmark.y, landmark.z])

        angle_calculation(pos)

        if cv.waitKey(5) & 0xFF == 27:
            break

    angles = {'LShoulderPitch': LShoulderPitch_list, 'LShoulderRoll': LShoulderRoll_list, 
                'LElbowYaw': LElbowYaw_list, 'LElbowRoll': LElbowRoll_list, 
                'RShoulderPitch': RShoulderPitch_list, 'RShoulderRoll': RShoulderRoll_list, 
                'RElbowYaw': RElbowYaw_list, 'RElbowRoll': RElbowRoll_list, 
                'LWristYaw': LWristYaw_list, 'RWristYaw': RWristYaw_list, 'LHand': LHand_list, 
                'RHand': RHand_list, 'HeadPitch': HeadPitch_list, 'HeadYaw': HeadYaw_list, 
                'HipPitch': HipPitch_list}

    ThetaR = pd.DataFrame.from_dict(angles)
    ThetaR.to_csv('complete.csv', index=False)

    pose.close()
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    
    main()
