"""
    Visualize map from known/ground truth trajectory and LIDAR.

    Author: Arturo Gil.
    Date: 03/2024

    TTD: Save map for future use in MCL localization.
         The map can be now saved in PCL format in order to use o3D directly.
         Also, the map can be saved in a series of pointclouds along with their positions, however path planning using,
         for example, PRM, may not be direct
"""
from eurocreader.eurocreader import EurocReader
from keyframemanager.keyframemanager import KeyFrameManager
from artelib.homogeneousmatrix import compute_homogeneous_transforms
import open3d as o3d


def visualize_map_online(global_transforms, keyframemanager, keyframe_sampling=10, radii=None, heights=None):
    """
    Builds map rendering updates at each frame.

    Caution: the map is not built, but the o3d window is in charge of storing the points
    and viewing them.
    """
    if radii is None:
        radii = [0.5, 35.0]
    if heights is None:
        heights = [-120.0, 120.0]
    print("COMPUTING MAP FROM KEYFRAMES")
    # First: add all keyframes with the known sampling
    keyframemanager.add_keyframes(keyframe_sampling=keyframe_sampling)
    keyframemanager.visualize_map_online(global_transforms=global_transforms, keyframe_sampling=keyframe_sampling,
                                         radii=radii, heights=heights)



def build_map(global_transforms, keyframemanager, keyframe_sampling=10):
    """
    Caution: in this case, the map is built using a pointcloud and adding the points to it. This may require a great
    amount of memory, however the result may be saved easily
    """
    print("COMPUTING MAP FROM KEYFRAMES")
    keyframemanager.add_keyframes(keyframe_sampling=keyframe_sampling)
    keyframemanager.build_map(global_transforms=global_transforms, keyframe_sampling=keyframe_sampling)



def main():
    # Read the final transform (i.e. via GraphSLAM)
    # You may be using different estimations to build the map: i.e. scanmatching or the results from graphSLAM
    # select as desired
    directory = '/media/arvc/INTENSO/DATASETS/INDOOR/2024-03-06-13-44-09'
    # filename = '/robot0/SLAM/solution_graphslam_sm.csv'
    filename = '/robot0/scanmatcher/scanmatcher_global.csv'
    # use, for example, 1 out of 5 LiDARS to build the map
    keyframe_sampling = 20
    # use, for example, voxel_size=0.2. Use voxel_size=None to use full resolution
    voxel_size = None

    # Remove by filtering max and min radius and heights
    # basic scan filtering to build the map (Radius_min, Radius_max, Height_min, Height_max)
    # CAUTION: add mor
    radii = [0, 35.0]
    heights = [-100, 3]


    # read data
    euroc_read = EurocReader(directory=directory)
    df_map_poses = euroc_read.read_csv(filename=filename)
    global_transforms = compute_homogeneous_transforms(df_data=df_map_poses)
    scan_times = df_map_poses['#timestamp [ns]'].to_numpy()
    keyframe_manager = KeyFrameManager(directory=directory, scan_times=scan_times, voxel_size=voxel_size)

    # Either view the map and visualize or visualize it as it goes
    # Option 1: build the map in a open3D cloud, then render it in a single shot
    # build_map(global_transforms, keyframe_manager, keyframe_sampling=keyframe_sampling)
    # Option 2: use the open3D renderer to add points and view them.
    visualize_map_online(global_transforms, keyframe_manager, keyframe_sampling=keyframe_sampling,
                         radii=radii, heights=heights)


if __name__ == '__main__':
    main()

