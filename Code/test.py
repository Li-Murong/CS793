import os
import json

# 指定包含 .jsonl 文件的目录
data_dir = '../Resources/data'

# 指定输出 .txt 文件的目录
output_dir = '../Resources/GPT2-output'

# 如果输出目录不存在，则创建
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取 data_dir 目录下的所有 .jsonl 文件
jsonl_files = [f for f in os.listdir(data_dir) if f.endswith('.jsonl')]

for jsonl_file in jsonl_files:
    jsonl_path = os.path.join(data_dir, jsonl_file)
    base_name = os.path.splitext(jsonl_file)[0]  # 去掉扩展名

    # 确定拆分数量 N
    # 对于 'large-762M.' 和 'xl-1542M.'，生成 3 个文件
    if 'large-762M.' in base_name or 'xl-1542M.' in base_name:
        N = 3
    else:
        N = 2

    # 目标每个文件大小（5 MB）
    target_size = 5 * 1024 * 1024  # 50 MB

    # 初始化变量
    current_size = 0
    file_index = 1
    part_texts = []

    # 读取 JSONL 文件并提取文本
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            text_content = data.get('text', '')
            text_size = len(text_content.encode('utf-8'))

            # 添加文本到当前部分
            part_texts.append(text_content)
            current_size += text_size

            # 检查当前部分是否达到目标大小
            if current_size >= target_size:
                # 保存当前部分到文件
                combined_text = '\n'.join(part_texts)
                output_filename = f"{base_name}_part{file_index}.txt"
                output_path = os.path.join(output_dir, output_filename)
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(combined_text)
                print(f"已创建 {output_filename}，大小约为 {current_size / (1024 * 1024):.2f} MB。")

                # 重置变量，准备下一部分
                part_texts = []
                current_size = 0
                file_index += 1

                # 检查是否已生成指定数量的文件
                if file_index > N:
                    break  # 退出循环，不再读取更多数据

        # 如果在读取完文件后还有剩余文本，并且尚未达到指定的文件数量
        else:
            if part_texts and file_index <= N:
                combined_text = '\n'.join(part_texts)
                output_filename = f"{base_name}_part{file_index}.txt"
                output_path = os.path.join(output_dir, output_filename)
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(combined_text)
                print(f"已创建 {output_filename}，大小约为 {current_size / (1024 * 1024):.2f} MB。")
                file_index += 1

    print(f"已处理 {jsonl_file}，共生成了 {min(file_index - 1, N)} 个文件。")

print("所有文件已处理完成。")