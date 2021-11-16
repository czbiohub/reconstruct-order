import os
import glob
import numpy as np
import zarr
from dynamorph_seg_map import get_sms_im_name
from waveorder2reconorder import parse_sms_name, read_img, write_img
from ReconstructOrder.utils.imgIO import get_sub_dirs

if __name__ == '__main__':
    # input_path = '/CompMicro/projects/HEK/2021_05_12_HEK_RSV_20x_055na_TimeLapse/TimeLapse_HEK_RSV_2.zarr'
    input_path = '/CompMicro/projects/HEK/2021_07_29_LiveHEK_NoPerf_63x_09NA'
    # output_path = '/CompMicro/projects/HEK/2021_05_12_HEK_RSV_20x_055na_TimeLapse_tif'
    output_path = '/CompMicro/projects/HEK/2021_07_29_LiveHEK_NoPerf_63x_09NA_tif_test'
    # conditions = ['TimeLapse_HEK_RSV_2']
    # conditions = ['']
    conditions = ['Full_Timelapse']
    channels = ['Retardance', 'Phase3D']
    chan_ids = [0, 3]
    # z_ids = [9, 10, 11, 12, 13]
    # z_ids = [35, 36, 37, 38, 39]
    z_ids = [31, 33, 41, 43]
    t_ids = [0, 25, 51, 76, 114]

    # input_path = '/CompMicro/projects/HEK/2021_06_04_HEK_Nuclei_DAPI'
    # output_path = '/CompMicro/projects/HEK/2021_06_04_HEK_Nuclei_DAPI_tif'
    # conditions = ['HEK_Phase3D_Padded']
    # channels = ['Phase3D']
    # chan_ids = [0]
    # exp_paths = glob.glob(os.path.join(input_path, '*/'))
    for condition in conditions:
        print('processing condition {}...'.format(condition))
        # pos_zarrs = get_sub_dirs(os.path.join(input_path, condition + '.zarr'))
        pos_zarrs = get_sub_dirs(os.path.join(input_path, condition))
        # dst_dir = os.path.join(output_path, condition)
        # os.makedirs(dst_dir, exist_ok=True)
        dst_dir = output_path
        os.makedirs(dst_dir, exist_ok=True)
        t_idx = 0
        for pos_zarr in pos_zarrs:
            # dst_dir = os.path.join(output_path, pos_zarr.strip('.zarr'))
            # os.makedirs(dst_dir, exist_ok=True)
            # zarr_store = zarr.open(os.path.join(input_path, condition + '.zarr', pos_zarr), mode='r')
            zarr_store = zarr.open(os.path.join(input_path, condition, pos_zarr), mode='r')
            img_tcz = zarr_store['physical_data']['array']
            pos_idx = int(pos_zarr[:-5].split("_")[1])
            # pos_idx = 0
            for t_idx in t_ids:
                img_cz = img_tcz[t_idx]
                for c_idx, chan in zip(chan_ids, channels):
                    img_z = img_cz[c_idx]
                    for z_idx in z_ids:
                        img = img_z[z_idx]
                        print(
                            'Processing position {}, time {}, channel {}, z {}...'.format(pos_idx, t_idx, chan, z_idx))
                        im_name_dst = get_sms_im_name(
                            time_idx=t_idx,
                            channel_name=chan,
                            slice_idx=z_idx,
                            pos_idx=pos_idx,
                            ext='.tif',
                        )
                        write_img(img, dst_dir, im_name_dst)