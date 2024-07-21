from PIL import Image
import qrcode
import os
import os.path as osp
from tqdm import tqdm,trange

# 定义支持的图片文件扩展名集合
SUPPORTED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

def is_image_file(filename):
    # 使用os.path.basename获取文件名，并使用split分离扩展名
    _, file_extension = os.path.splitext(filename)
    # 检查文件扩展名是否在支持的集合中
    return file_extension.lower() in SUPPORTED_IMAGE_EXTENSIONS

def add_qr_code_to_image(image_path, qr_data, output_path, box_ratio=50):
    # 打开原始图片
    image = Image.open(image_path)
    
    # 获取图片的尺寸
    img_width, img_height = image.size

    # 根据图片宽度的50分之1确定二维码的尺寸
    qr_width = img_width // box_ratio
    qr_height = qr_width  # 保持二维码为正方形

    # 生成二维码
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # 将二维码转换为PIL图像，并调整大小
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((qr_width, qr_height), Image.Resampling.LANCZOS)
    
    # 计算二维码的位置，这里我们将其放在图片的右下角
    position = (img_width - qr_width-5, img_height - qr_height - 5)
    
    # 将二维码粘贴到图片上
    image.paste(qr_img, position, qr_img.convert('RGBA'))  # 使用RGBA以支持透明背景
    
    # 如果输出文件已存在，则删除它
    if os.path.exists(output_path):
        os.remove(output_path)
    image.save(output_path)
    print(f"Image with QR code saved to {output_path}")

import multiprocessing as mp

def add_qr_code_to_image_batch(image_dir, qr_data, output_dir, box_ratio=50, process_num=1):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 遍历目录中的所有文件
    image_files = [f for f in os.listdir(image_dir) if is_image_file(f)]
    image_files = sorted(image_files)
    task_list = []
    for idx, image_file in tqdm(enumerate(image_files), total=len(image_files)):
        # 拼接原始图片的完整路径
        image_path = os.path.join(image_dir, image_file)
        
        # 构建输出图片的路径
        output_file = os.path.splitext(image_file)[0] + '_qr.jpg'
        output_path = os.path.join(output_dir, output_file)
        
        # 添加二维码到图片
        qr_data = image_dir + str(idx)
        if process_num == 1:
            add_qr_code_to_image(image_path, qr_data, output_path, box_ratio)
        else:
            task_list.append((image_path, qr_data, output_path, box_ratio))
            
    if process_num != 1:
        with mp.Pool(processes=process_num) as pool: 
            # 使用 starmap 来并行执行函数  为了与 tqdm 配合，我们创建一个生成器来模拟迭代过程  
            def result_iterator():  
                # func; task_list
                for result in pool.starmap(add_qr_code_to_image, task_list): 
                    yield result  
            with tqdm(total=len(task_list), desc="Processing Add QR Code") as pbar:  
                proc_results = [res for res, _ in zip(result_iterator(), range(len(task_list)))]   
                for _ in range(len(task_list)):  
                    pbar.update()

# 使用示例
if __name__ == "__main__":
    image_path = '/Users/mac/code/vlm/xzg_958378extracted_frames/frame_0000.jpg' 
    output_path = 'path_to_save_new_image.jpg'  # 替换为你希望保存新图片的路径

    image_dir = '/Users/mac/code/vlm/xzg_958378_extracted_frames'  # 替换为你的图片路径
    output_dir = f'{image_dir}_add_qrcode'  # 替换为你希望保存新图片的路径

    qr_data = '111'  # 你希望添加到二维码中的数据 

    # add_qr_code_to_image(image_path, qr_data, output_path,20)
    print(os.cpu_count())
    qr_code_cover_ratio = 40
    add_qr_code_to_image_batch(image_dir, qr_data, output_dir, qr_code_cover_ratio, 20)
    from datetime import datetime
    import time
    # 获取当前时间戳
    current_timestamp = time.time()
    # 使用时间戳生成 datetime 对象
    dt_object = datetime.fromtimestamp(current_timestamp)

    print(f"Datetime object: {dt_object}")