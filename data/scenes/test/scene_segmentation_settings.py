import numpy as np


masks_points = []

#positive point mask0 (skin)
mask0_pos_x=750
mask0_pos_y=375

mask0_pos2_x=620
mask0_pos2_y=800

#mask0_pos3_x=780 #(glasses)
#mask0_pos3_y=300

mask0_pos3_x=620
mask0_pos3_y=800

#negative point mask0 
mask0_neg_x=750
mask0_neg_y=450

masks_points.append([np.array([[mask0_pos_x, mask0_pos_y],[mask0_pos2_x, mask0_pos2_y],[mask0_pos3_x, mask0_pos3_y],[mask0_neg_x, mask0_neg_y]], dtype=np.float32), np.array([1,1,1,0], np.int32)])

#positive point mask1 # (glasses)
mask1_pos_x=780
mask1_pos_y=300

masks_points.append([np.array([[mask1_pos_x, mask1_pos_y]], dtype=np.float32), np.array([1], np.int32)])

#positive point mask2 (shirt)
mask2_pos_x=720
mask2_pos_y=820

mask2_pos2_x=700
mask2_pos2_y=410

#negative point mask2 
mask2_neg_x=750
mask2_neg_y=450

masks_points.append([np.array([[mask2_pos_x, mask2_pos_y],[mask2_pos2_x, mask2_pos2_y],[mask2_neg_x, mask2_neg_y]], dtype=np.float32), np.array([1,1,0], np.int32)])

#positive point mask21 (shirt)
#mask21_pos_x=700
#mask21_pos_y=410

#mask21_pos2_x=700
#mask21_pos2_y=410

#masks_points.append([np.array([[mask21_pos_x, mask21_pos_y],[mask2_pos2_x, mask2_pos2_y]], dtype=np.float32), np.array([1,1], np.int32)])


#positive point mask3 (trousers)
mask3_pos_x=750
mask3_pos_y=900

masks_points.append([np.array([[mask3_pos_x, mask3_pos_y]], dtype=np.float32), np.array([1], np.int32)])

#positive point mask4 (jersey)
mask4_pos_x=750
mask4_pos_y=600

#negative point mask4 
mask4_neg_x=700
mask4_neg_y=410

masks_points.append([np.array([[mask4_pos_x, mask4_pos_y],[mask4_neg_x, mask4_neg_y]], dtype=np.float32), np.array([1,0], np.int32)])

#positive point mask5 (hair)
mask5_pos_x=700
mask5_pos_y=370

#negative point mask5 
mask5_neg_x=750
mask5_neg_y=375

masks_points.append([np.array([[mask5_pos_x, mask5_pos_y],[mask5_neg_x, mask5_neg_y]], dtype=np.float32), np.array([1,0], np.int32)])
