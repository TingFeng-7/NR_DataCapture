import cv2
import pyzbar.pyzbar as pyzbar
import os
import os.path as osp
import shutil
from tqdm import tqdm, trange
# mac pip install git+https://github.com/npinchot/zbar
def decode_qr_code_from_image(image_path, region_size=0.1, is_mp=False, scale=15.0):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to read image: {image_path}")
        return None
    
    height, width, _ = image.shape
    
    # 计算右下角区域的坐标
    region_width = int(width * region_size)
    region_height = int(height * region_size)
    x = width - region_width
    y = height - region_height
    
    # 提取右下角区域
    region = image[y:y + region_height, x:x + region_width]
    # 缩放图像以提高二维码的尺寸
    new_size = (int(region_width * scale), int(region_height * scale))
    region = cv2.resize(region, new_size, interpolation=cv2.INTER_AREA)
    # 转换为灰度图像
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

    
    # 二维码检测和解码
    decoded_objects = pyzbar.decode(gray)
    decoded_data = []
    if len(decoded_objects) == 0 :
        print(f"{image_path} 未检测到")
    for obj in decoded_objects:
        # 打印解码后的数据
        decoded_data.append(obj.data.decode("utf-8"))
        print("Decoded data:", obj.data.decode("utf-8"))
    if is_mp:
        return decoded_data[0] 

# 定义支持的图片文件扩展名集合
SUPPORTED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

def is_image_file(filename):
    # 使用os.path.basename获取文件名，并使用split分离扩展名
    _, file_extension = os.path.splitext(filename)
    # 检查文件扩展名是否在支持的集合中
    return file_extension.lower() in SUPPORTED_IMAGE_EXTENSIONS

import multiprocessing as mp

def result_iterator(pool, func, task_list):  
    for result in pool.starmap(func, task_list): 
        yield result

def decode_qr_code_from_image_batch(image_dir, process_num=10):
    is_mp = True
    params = [[(osp.join(image_dir, f)), is_mp] for f in os.listdir(image_dir)]
    if process_num <= 1:
        for img_path, _ in params:
            decode_qr_code_from_image(img_path)
    else:  
        with mp.Pool(processes=process_num) as pool: 
            result_iter = result_iterator(pool, decode_qr_code_from_image, params)
            with tqdm(total=len(params), desc="Processing Add QR Code") as pbar:  
                decode_results = [res for res, _ in result_iter]   
                for _ in range(len(params)):  
                    pbar.update()
    # with mp.Pool(processes=process_num) as pool:
    #     results = pool.starmap(decode_qr_code_from_image, image_files)
    # # 处理解码结果
    # for image_path, decoded_data in zip(image_files, results):
    #     if decoded_data:
    #         print(f"Decoded data from {image_path}: {decoded_data}")
if __name__ == "__main__":
    # 使用示例
    image_path = '/Users/mac/code/vlm/path_to_save_new_image.jpg'  # 替换为你的图片路径包含二维码

    image_path = '/Users/mac/code/vlm/xzg_958378_extracted_frames_add_qrcode/frame_0000_qr.jpg'
    decode_qr_code_from_image(image_path)
    
    image_dir = '/Users/mac/code/vlm/xzg_958378_extracted_frames_add_qrcode'  # 替换为你的图片路径包含二维码
    decode_qr_code_from_image_batch(image_dir,1)