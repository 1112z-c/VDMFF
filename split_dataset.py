# import os
# import glob
# import random
# import json
# import pandas as pd
#
# def split_data(file_list, output_path):
#     # 根据文件名的最后一位分离出target为0和1的数据
#     target_0_files = [file for file in file_list if os.path.basename(file).endswith('0.json')]
#     target_1_files = [file for file in file_list if os.path.basename(file).endswith('1.json')]
#
#     # 合并target 0和1的数据集
#     all_files = target_0_files + target_1_files
#
#     # 计算训练集和测试集的大小
#     total_count = len(all_files)
#     train_count = int(total_count * 0.8)
#     test_count = total_count - train_count
#
#     # 分配数据到训练集和测试集
#     random.shuffle(all_files)
#     train_files = all_files[:train_count]
#     test_files = all_files[train_count:]
#
#     # 保存为新的 JSON 文件
#     save_to_json(train_files, os.path.join(output_path, 'train.json'))
#     save_to_json(test_files, os.path.join(output_path, 'test.json'))
#
# def save_to_json(file_list, output_file):
#     json_data = pd.DataFrame(
#         columns=["file_name", "target", "text_embedding", "node_features", "graph", "image_features"])
#
#     for file_path in file_list:
#         try:
#             with open(file_path, 'r') as f:
#                 json_text = json.load(f)
#                 # 提取所需字段
#                 file_name = json_text['file_name']
#                 target = int(file_name.split('.')[0].split('_')[-1])
#                 text_embedding = json_text['text_embedding']
#                 node_features = json_text['node_features']
#                 graph = json_text['graph']
#                 image_features = json_text['image_features']
#
#                 # 将数据添加到 DataFrame
#                 json_data.loc[file_name] = [file_name, target, text_embedding, node_features, graph, image_features]
#         except Exception as e:
#             print(f"Error processing {file_path}: {str(e)}")
#
#     # 保存为 JSON 文件
#     json_data.to_json(output_file, orient='index', force_ascii=False)
#     print(f"Saved data to {output_file}")
#
# def main():
#     input_data = '/opt/data/VulCNN-main/dataset/Dataset-sard/vecjson/'
#     output_path = '/opt/data/VulCNN-main/dataset/Dataset-sard/tvtjson/'
#
#     if not os.path.exists(output_path):
#         os.makedirs(output_path)
#
#     # 获取所有 JSON 文件
#     file_list = glob.glob(os.path.join(input_data, '*.json'))
#
#     # 分割数据
#     split_data(file_list, output_path)
#
# if __name__ == '__main__':
#     main()

import os
import glob
import random

def split_data(file_list, output_path):
    # 根据文件名的最后一位分离出target为0和1的数据
    target_0_files = [file for file in file_list if os.path.basename(file).endswith('0.json')]
    target_1_files = [file for file in file_list if os.path.basename(file).endswith('1.json')]

    # 合并target 0和1的数据集
    all_files = target_0_files + target_1_files

    # 计算训练集和测试集的大小
    total_count = len(all_files)
    train_count = int(total_count * 0.8)
    test_count = total_count - train_count

    # 分配数据到训练集和测试集
    random.shuffle(all_files)
    train_files = all_files[:train_count]
    test_files = all_files[train_count:]

    # 保存为文本文件
    save_to_txt(train_files, os.path.join(output_path, 'train.txt'))
    save_to_txt(test_files, os.path.join(output_path, 'test.txt'))

def save_to_txt(file_list, output_file):
    with open(output_file, 'w') as f:
        for file_path in file_list:
            f.write(file_path + '\n')
    print(f"Saved data to {output_file}")

def main():
    input_data = '/opt/data/VulCNN-main/dataset/Dataset-sard/vecjson/'
    output_path = '/opt/data/VulCNN-main/dataset/Dataset-sard/tvtjson/'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 获取所有 JSON 文件
    file_list = glob.glob(os.path.join(input_data, '*.json'))

    # 分割数据
    split_data(file_list, output_path)

if __name__ == '__main__':
    main()