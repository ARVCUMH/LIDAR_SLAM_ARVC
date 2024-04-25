"""
Visualize the all data easily
"""
from eurocreader.eurocreader import EurocReader
from tools.gpsconversions import gps2utm
from tools.plottools import plot_gps_OSM, plot_gps_points, plot_3D_data
from tools.plottools import plot_xy_data, plot_xyz_data, plot_quaternion_data
import numpy as np
from artelib.vector import Vector
from artelib.euler import Euler
from artelib.homogeneousmatrix import HomogeneousMatrix
import matplotlib.pyplot as plt

def plot_result(df_data, text):
    plt.plot(df_data['x'], df_data['y'])
    plt.legend()


def compute_basic_end_error(df_sm):
    x = df_sm['x'].tolist()
    y = df_sm['y'].tolist()
    z = df_sm['z'].tolist()
    e = np.array([x[-1], y[-1], z[-1]])
    return np.linalg.norm(e)

def transform_gps_data(df_gps):
    df_gps = gps2utm(df_gps)
    x = df_gps['x'].tolist()
    y = df_gps['y'].tolist()
    angle = np.arctan2(y[1]-y[0], x[1]-x[0])
    T = HomogeneousMatrix(Vector([0, 0, 0]), Euler([0, 0, angle]))
    t = []
    for i in range(len(x)):
        v = Vector([x[i], y[i], [0], 1.0])
        vp = T*v
        t.append(vp)
    return np.array(t)

def view_gps_data(directory):
    """
    View lat/lng data on 2D. Also, plot on OSM
    """
    try:
        euroc_read = EurocReader(directory=directory)
        df_gps = euroc_read.read_csv(filename='/robot0/gps0/data.csv')
        plot_gps_points(df_gps=df_gps, annotate_index=True)
        plot_gps_points(df_gps=df_gps, annotate_error=True)
        # plot_gps_OSM(df_gps=df_gps, save_fig=True, expand=0.001)
    except FileNotFoundError:
        print('NO GPS DATA FOUND')


def view_gps_utm_data(directory):
    """
    View lat/lng data on 2D. Also, plot on OSM
    """
    try:
        euroc_read = EurocReader(directory=directory)
        df_gps = euroc_read.read_csv(filename='/robot0/gps0/data.csv')
        df_gps = gps2utm(df_gps)
        plot_xy_data(df_data=df_gps)
        # plot_gps_OSM(df_gps=df_gps, save_fig=True, expand=0.001)
    except FileNotFoundError:
        print('NO GPS DATA FOUND')


if __name__ == "__main__":
    directory = '/media/arvc/INTENSO/DATASETS/OUTDOOR/O2-2024-03-07-13-33-34'

    euroc_read = EurocReader(directory=directory)
    # df_sm = euroc_read.read_csv(filename='/robot0/scanmatcher/O2/scanmatcher_global_0.3_icppointpoint.csv')
    # # plot_xyz_data(df_data=df_sm, title='SM ICP POINT POINT')
    # plot_3D_data(df_data=df_sm)
    # plot_xy_data(df_data=df_sm, title='SM ICP POINT POINT')
    # error = compute_basic_end_error(df_sm)
    # print('SM ICP point point error: ', error)
    #
    # df_sm = euroc_read.read_csv(filename='/robot0/scanmatcher/O2/scanmatcher_global_0.3_icppointplane.csv')
    # # plot_xyz_data(df_data=df_sm, title='SM ICP POINT POINT')
    # plot_3D_data(df_data=df_sm)
    # plot_xy_data(df_data=df_sm, title='SM ICP POINT PLANE')
    # error = compute_basic_end_error(df_sm)
    # print('SM ICP point plane error: ', error)
    #
    # df_sm = euroc_read.read_csv(filename='/robot0/scanmatcher/scanmatcher_global_icp2planes.csv')
    # # plot_xyz_data(df_data=df_sm, title='SM ICP POINT POINT')
    # plot_3D_data(df_data=df_sm)
    # plot_xy_data(df_data=df_sm, title='SM ICP 2PLANES')
    # error = compute_basic_end_error(df_sm)
    # print('SM ICP 2 planeS error: ', error)

    df_gps = euroc_read.read_csv(filename='/robot0/gps0/data.csv')
    df_gps = gps2utm(df_gps=df_gps)
    df_sm = euroc_read.read_csv(filename='/robot0/SLAM/solution_graphslam_sm.csv')
    df_sm_gps = euroc_read.read_csv(filename='/robot0/SLAM/solution_graphslam_sm_gps.csv')
    df_sm_gps_lc = euroc_read.read_csv(filename='/robot0/SLAM/solution_graphslam_sm_gps_LC.csv')
    df_sm_odo = euroc_read.read_csv(filename='/robot0/SLAM/solution_graphslam_sm_odo.csv')
    df_sm_odo_gps = euroc_read.read_csv(filename='/robot0/SLAM/solution_graphslam_sm_odo_gps.csv')
    df_sm_odo_gps_lc = euroc_read.read_csv(filename='/robot0/SLAM/solution_graphslam_sm_odo_gps_LC.csv')
    df_0prior = euroc_read.read_csv(filename='/robot0/SLAM/solution_graphslam_0prior.csv')

    plot_result(df_gps, 'GPS_ONLY')
    plot_result(df_sm, 'SM')
    plot_result(df_sm_gps, 'SM_GPS')
    plot_result(df_sm_gps_lc, 'SM_GPS_LC')
    plot_result(df_sm_odo, 'SM_ODO')
    plot_result(df_sm_odo_gps, 'SM_ODO_GPS')
    plot_result(df_sm_odo_gps_lc, 'SM_ODO_GPS_LC')
    plot_result(df_0prior, '0prior')
    plt.legend(['GPS_ONLY', 'SM', 'SM_GPS', 'SM_GPS_LC', 'SM_ODO', 'SM_ODO_GPS', 'SM_ODO_GPS_LC', '0prior'])
    plt.show()
    # plot_3D_data(df_data=df_sm)
    # plot_xy_data(df_data=df_sm, title='SM ICP 2PLANES')
    # error = compute_basic_end_error(df_sm)
    # print('SM ICP 2 planeS error: ', error)
    # view_gps_utm_data(directory=directory)
    # view_gps_data(directory=directory)
