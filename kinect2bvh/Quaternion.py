import numpy as np
# def quat_conjugate(q):
#     return np.array([-q[0], -q[1], -q[2], q[3]])
# def quat_inverse(q):
#     q_norm = q/np.linalg.norm(q)
#     return quat_conjugate(q_norm)
# def quat_left_multiply(l,r):
#     q = np.zeros(4)
#     q[0] = r[3]*l[0] + r[0]*l[3] + r[1]*l[2] - r[2]*l[1]
#     q[1] = r[3]*l[1] + r[1]*l[3] + r[2]*l[0] - r[0]*l[2]
#     q[2] = r[3]*l[2] + r[2]*l[3] + r[0]*l[1] - r[1]*l[0]
#     q[3] = r[3]*l[3] - r[0]*l[0] - r[1]*l[1] - r[2]*l[2]
#     return q

def quat_conjugate(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

    
def quat_inverse(q):
    q_norm = q/np.linalg.norm(q)
    return quat_conjugate(q_norm)


def quat_left_multiply(l,r):
    q = np.zeros(4)
    q[0] = l[0]*r[0] - l[1]*r[1] - l[2]*r[2] - l[3]*r[3]
    q[1] = l[0]*r[1] + l[1]*r[0] + l[2]*r[3] - l[3]*r[2]
    q[2] = l[0]*r[2] + l[2]*r[0] + l[3]*r[1] - l[1]*r[3]
    q[3] = l[0]*r[3] + l[3]*r[0] + l[1]*r[2] - l[2]*r[1]
    return q

#roll->yaw->pitch
def euler_from_quat(q):
    res = np.zeros(3)
    x = q[0]
    y = q[1]
    z = q[2]
    w = q[3]
    res[0] = np.rad2deg(np.arctan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y)))
    res[1] = np.rad2deg(np.arcsin(2 * (w * y - z * x)))
    res[2] = np.rad2deg(np.arctan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z)))
    # fix nan value
    for i in range(3):
        if np.isnan(res[i]):
            res[i] = 0
    return res

# #roll->yaw->pitch
# def euler_from_quat(q):
#     res = np.zeros(3)
#     x = q[0]
#     y = q[1]
#     z = q[2]
#     w = q[3]
#     res[0] = np.arctan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
#     res[1] = np.arcsin(2 * (w * y - z * x))
#     res[2] = np.arctan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
#     # fix nan value
#     for i in range(3):
#         if np.isnan(res[i]):
#             res[i] = 0
#     return res