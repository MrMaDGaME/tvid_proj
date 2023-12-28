import numpy as np
from PIL import Image


def YUV_to_RGB(y, u, v) :
    r = y + 1.13983 * v
    g = y - 0.39465 * u - 0.58060 * v
    b = y + 2.03211 * u
    
    return r, g, b


def PGM_to_PPM(yuv_array, TFF=True) :
    # loading pgm info

    height, width = yuv_array.shape
    
    uv_width = width // 2
    y_height = int(height * 2 / 3)
    
    # extraction
    
    y_array = yuv_array[0:y_height, 0:width]
    u_array = yuv_array[y_height:height, 0:uv_width]
    v_array = yuv_array[y_height:height, uv_width:width]
    
    # duplication (to match the size of y)
    
    u_array = np.repeat(np.repeat(u_array, 2, axis=1), 2, axis=0)
    v_array = np.repeat(np.repeat(v_array, 2, axis=1), 2, axis=0)
    
    if TFF :
        y_array = np.repeat(y_array, 2, axis=0)
        u_array = np.repeat(u_array, 2, axis=0)
        v_array = np.repeat(v_array, 2, axis=0)
        
        y_height *= 2
    
    # normalization

    y_array = y_array / 255
    
    u_max = 0.436
    u_min = -u_max
    u_array = u_min + (u_array / 255) * 2 * u_max
    
    v_max = 0.615
    v_min = -v_max
    v_array = v_min + (v_array / 255) * 2 * v_max
    
    # stacking and conversion to rgb data between [0, 1]
    
    r_array, g_array, b_array = YUV_to_RGB(y_array, u_array, v_array)
    
    rgb_data = np.stack([r_array, g_array, b_array], axis=-1)
    
    rgb_data = np.clip(rgb_data, 0, 1)
            
    # conversion to uint-8 values between [0, 255]
    
    rgb_data = (rgb_data * 255).astype('uint8')
    
    return rgb_data


def generic_PGM_to_PPM(pgm_path, TFF=True) :
    # loading pgm
    
    img = Image.open(pgm_path)
    
    yuv_array = np.array(img)
    
    # top first field order
    
    if TFF :
        rgb_data_top = PGM_to_PPM(yuv_array[::2], TFF=True)
        rgb_data_bottom = PGM_to_PPM(yuv_array[1::2], TFF=True)
            
        return [rgb_data_top, rgb_data_bottom]
    
    # progressive order
    
    rgb_data = PGM_to_PPM(yuv_array, TFF=False)
    
    return [rgb_data]