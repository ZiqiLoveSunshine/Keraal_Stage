Readme: Organization of Vicon and Kinect and Poppy control files

Authors: Maxime Devanne (maxime.devanne@uha.fr)
         Sao Mai Nguyen (nguyensmai@gmail.com)

*************************************************
The recordings are organized into 4 folders for each participant subgroup, the subfolders correspond to each recording modality, and sub-subfolders correspond to each of the 3 exercise types.
Groups : 1A= labelled patient coached by Poppy, 1B= unlabelled patient coached by Poppy, 2A= labelled healthy adults coached by Poppy, 2B= unlabelled healthy adults coached by Poppy, 3= labelled healthy participants simulating errors.
 In the case of groups 1a, 1b, 2a and 2b, each recording is given a unique number, which is the same for all recording modalities (The nomenclature of the files in the data set includes the following information: groupA/Modality/GA_SubjectId_ExerciseName_Site_RecordingId.extension). In the case of group 3, the name of the file indicates the label of the error and the recording id. The nomenclature of the files in this case is : group3/Modality/G3_ExerciseName_ParticipantId_TrialId_label_RecordingId.extension 
************************************************
The directories are:
group1A --- annotations
        |-- kinect
        |-- openpose
        |-- blazepose
        |-- videos

group1B --- kinect
        |-- openpose
        |-- blazepose
        |-- videos


group2A --- annotations
        |-- kinect
        |-- openpose
        |-- blazepose
        |-- videos


group2B --- kinect
        |-- openpose
        |-- blazepose
        |-- videos

`
group3 --- kinect
        |-- openpose
        |-- blazepose
        |-- vicon
        |-- videos

************************************************

1. Vicon System

1.1 Vicon skeleton
The Vicon files are acquired using Vicon Motion Capture System. 17 targets from ART were placed on the human body. The full list of target names and associated ids is:
0. Right Forearm
1. Left Forearm
2. Right Arm
3. Left Arm
4. Chest
5. Right Tigh
6. Left Tigh
7. Right Shoulder
8. Left Shoulder
9. Right Hand
10. Left Hand
11. Right Foot
12. Left Foot
13. Hips
14. Head
15. Right Tibia
16. Left Tibia

1.2 Vicon files
Each Vicon file corresponds to a motion sequence. Within the file, each row represents a frame and includes 119 floating values corresponding to the 3D global position and the global orientation (Quaternion) of each target:
x_pos y_pos z_pos x_quat y_quat z_quat w_quat
Each target's position and quaternion is concatenated according to the order described in 1.1


2. Kinect System

2.1 Kinect skeleton
The Kinect skeleton includes 25 joints:
0. SpineBase
1. SpineMid
2. Neck
3. Head
4. ShoulderLeft
5. ElbowLeft
6. WristLeft
7. HandLeft
8. ShoulderRight
9. ElbowRight
10. WristRight
11. HandRight
12. HipLeft
13. KneeLeft
14. AnkleLeft
15. FootLeft
16. HipRight
17. KneeRight
18. AnkleRight
19. FootRight
20. SpineShoulder
21. HandTipLeft
22. ThumbLeft
23. HandTipRight
24. ThumbRight

2.2 Kinect files
Each Kinect file corresponds to a motion sequence. Within the file, each row represents a frame and includes 175 floating values corresponding to the 3D position and the orientation (Quaternion) of each joint:
x_pos y_pos z_pos x_quat y_quat z_quat w_quat
Each joint's position and quaternion is concatenated according to the order described in 2.2

Something about the data:
https://lisajamhoury.medium.com/understanding-kinect-v2-joints-and-coordinate-system-4f4b90b9df16

what is x_quat, y_quat, z_quat, w_quat:
https://pterneas.com/2017/05/28/kinect-joint-rotation/

3. OpenPose 

3.1. OpenPose skeleton
The OpenPose skeleton used is the COCO model, from which we have recorded the following joints:
0. Head
1. mShoulder
2. rShoulder
3. rElbow
4. rWrist
5. lShoulder
6. lElbow
7. lWrist
8. rHip
9. rKnee
10. rAnkle
11. lHip
12. lKnee
13. lAnkle

3.2. OpenPose files
Each Kinect file corresponds to a motion sequence. within the file, is a dictionary of positions. The second level of dictionary is the video frame number. The third level of the dictionary is the joint name. For each joint is a 2D position :
x_pos, y_pos

4 Blazepose

4.1 Blazepose skeleton

0. Nose
1. Left_eye_inner
2. Left_eye
3. Left_eye_outer
4. Right_eye_inner
5. Right_eye
6. Right_eye_outer
7. Left_ear
8. Right_ear
9. Mouth_left
10. Mouth_right
11. Left_shoulder
12. Right_shoulder
13. Left_elbow
14. Right_elbow
15. Left_wrist
16. Right_wrist
17. Left_pinky #1 knuckle 
18. Right_pinky #1 knuckle 
19. Left_index #1 knuckle 
20. Right_index #1 knuckle 
21. Left_thumb #2 knuckle 
22. Right_thumb #2 knuckle 
23. Left_hip
24. Right_hip
25. Left_knee
26. Right_knee
27. Left_ankle
28. Right_ankle
29. Left_heel
30. Right_heel
31. Left_foot_index
32. Right_foot_index

4.2 Blazepose file

x_pos, y_pos, z_pos

POSE_LANDMARKS

A list of pose landmarks. Each landmark consists of the following:

- `x` and `y`: Landmark coordinates normalized to `[0.0, 1.0]` by the image width and height respectively.
- `z`: Represents the landmark depth with the depth at the midpoint of hips being the origin, and the smaller the value the closer the landmark is to the camera. The magnitude of `z` uses roughly the same scale as `x`.

#### POSE_WORLD_LANDMARKS

Another list of pose landmarks in world coordinates. Each landmark consists of the following:

- `x`, `y` and `z`: Real-world 3D coordinates in meters with the origin at the center between hips.
- `visibility`: Identical to that defined in the corresponding pose_landmarks.


5.Control command files of the robot Poppy to demonstrate the three exercises.
They are json files that use the syntax commonly used by the library pypot as described in its documentation (https://docs.poppy-project.org/en/programming/python.html) and can be used with the web-interface developed by the project Keraal (https://github.com/GRLab/Poppy_GRR) to execute on Poppy. They can be used with the physical robotPoppy or its simulation. 

6 Kinect - OpenPose
(Convert Kinect coordinate system to openpose, for example point 3 in Kinect correspond to point 0(Head) in Openpose)

- 3 - 0 (Head)
- 20 - 1 (mShoulder)
- 8 - 2 (rShoulder)
- 9 - 3 (rElbow)
- 10 - 4 (rWrist)
- 4 - 5 (lShoulder)
- 5 - 6 (lElbow)
- 6 - 7 (lWrist)
- 16 - 8 (rHip)
- 17 - 9 (rKnee)
- 18 - 10 (rAnkle)
- 12 - 11 (lHip)
- 13 - 12 (lKnee)
- 14 - 13 (lAnkle)

7 Blazepose- Openpose

- 0 - 0 (Head)
- Moy(11,12) - 1 (mShoulder)
- 12 - 2 (rShoulder)
- 14 - 3 (rElbow)
- 16 - 4 (rWrist)
- 11 - 5 (lShoulder)
- 13 - 6 (lElbow)
- 15 - 7 (lWrist)
- 24 - 8 (rHip)
- 26 - 9 (rKnee)
- 28 - 10 (rAnkle)
- 23 - 11 (lHip)
- 25 - 12 (lKnee)
- 27 - 13 (lAnkle)

8 Blazepose - Vicon

- 0 - 14 (Head)
- Moy(11,12,23,24) - 4 (Chest)
- Moy(23,24) - 13 (Hips)
- 11 - 8 (Left Shoulder)
- Moy(11,13) - 3 (Left Arm)
- Moy(13,15) - 1 (Left Forearm)
- Moy(17,19) - 10 (Left Hand)
- 12 - 7 (Right Shoulder)
- Moy(12,14) - 2 (Right Arm)
- Moy(14,16) - 0 (Right Forearm)
- Moy(18, 20) - 9 (Right Hand)
- Moy(23,25) - 6 (Left Tigh)
- Moy(25,27) - 16 (Left Tibia)
- Moy(29,31) - 12 (Left Foot)
- Moy(24,26) - 5 (Right Tigh)
- Moy(26,28) - 15 (Right Tibia)
- Moy(30,32) - 11 (Right Foot)

9 Openpose- Vicon

- 0 - 14 (Head)
- Moy(1，Moy(8,11)) - 4 (Chest)
- Moy(8,11) - 13 (Hips)
- 5 - 8 (Left Shoulder)
- Moy(5,6) - 3 (Left Arm)
- Moy(6,7) - 1 (Left Forearm)
- nan - 10 (Left Hand)
- 2 - 7 (Right Shoulder)
- Moy(2,3) - 2 (Right Arm)
- Moy(3,4) - 0 (Right Forearm)
- nan - 9 (Right Hand)
- Moy(11,12) - 6 (Left Tigh)
- Moy(12,13) - 16 (Left Tibia)
- nan - 12 (Left Foot)
- Moy(8,9) - 5 (Right Tigh)
- Moy(9,10) - 15 (Right Tibia)
- nan - 11 (Right Foot)

10 Kinect- Vicon

- 3 - 14 (Head)
- Moy(1，20) - 4 (Chest)
- 0 - 13 (Hips)
- 4 - 8 (Left Shoulder)
- Moy(4,5) - 3 (Left Arm)
- Moy(5,6) - 1 (Left Forearm)
- 7 - 10 (Left Hand)
- 8 - 7 (Right Shoulder)
- Moy(8,9) - 2 (Right Arm)
- Moy(9,10) - 0 (Right Forearm)
- 11 - 9 (Right Hand)
- Moy(12,13) - 6 (Left Tigh)
- Moy(13,14) - 16 (Left Tibia)
- 15 - 12 (Left Foot)
- Moy(16,17) - 5 (Right Tigh)
- Moy(17,18) - 15 (Right Tibia)
- 19 - 11 (Right Foot)
