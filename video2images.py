import cv2
import os
import os.path as osp

def extract_frames(video_path, output_folder, end_id=200):
    """
    提取视频的所有帧并保存到指定文件夹。
    
    参数:
    - video_path: 视频文件的路径。
    - output_folder: 保存帧的文件夹路径。
    """
    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # 获取视频信息
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video has {total_frames} frames with a frame rate of {fps} FPS")

    # 逐帧读取并保存
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 如果没有帧了，退出循环
        if frame_idx >= end_id:
            break
        # 保存帧
        frame_filename = os.path.join(output_folder, f"frame_{frame_idx:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        print(f"Saved {frame_filename}")

        frame_idx += 1

    # 释放资源
    cap.release()
    print("All frames have been saved.")

def basename_wo_suffix(path):
    return osp.basename(video_path).split('.')[0]
if __name__ == "__main__":
    # 使用示例
    video_path = './xzg_958378.mp4'  # 替换为你的视频文件路径
    output_folder = basename_wo_suffix(video_path) + 'extracted_frames'  # 替换为你希望保存帧的文件夹路径
    extract_frames(video_path, output_folder)