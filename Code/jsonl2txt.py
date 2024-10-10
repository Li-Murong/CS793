import os
import json

# Specify the directory containing .jsonl files
data_dir = '../Resources/data'

# Specify the output directory for .txt files
output_dir = '../Resources/GPT2-output'

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get all .jsonl files in the data_dir directory
jsonl_files = [f for f in os.listdir(data_dir) if f.endswith('.jsonl')]

for jsonl_file in jsonl_files:
    jsonl_path = os.path.join(data_dir, jsonl_file)
    base_name = os.path.splitext(jsonl_file)[0]  # Remove the extension

    # Determine the number of files to generate (N)
    # For 'large-762M.' and 'xl-1542M.', generate 3 files
    if 'large-762M.' in base_name or 'xl-1542M.' in base_name:
        N = 3
    else:
        N = 2

    # Target size for each file (5 MB)
    target_size = 5 * 1024 * 1024  # 5 MB

    # Initialize variables
    current_size = 0
    file_index = 1
    part_texts = []

    # Read the JSONL file and extract text
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            text_content = data.get('text', '')
            text_size = len(text_content.encode('utf-8'))

            # Add text to the current part
            part_texts.append(text_content)
            current_size += text_size

            # Check if the current part has reached the target size
            if current_size >= target_size:
                # Save the current part to a file
                combined_text = '\n'.join(part_texts)
                output_filename = f"{base_name}_part{file_index}.txt"
                output_path = os.path.join(output_dir, output_filename)
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(combined_text)
                print(f"Created {output_filename}, size approximately {current_size / (1024 * 1024):.2f} MB.")

                # Reset variables for the next part
                part_texts = []
                current_size = 0
                file_index += 1

                # Check if the specified number of files have been generated
                if file_index > N:
                    break  # Exit the loop and stop reading more data

        # If there is remaining text after reading the file and the specified number of files has not been reached
        else:
            if part_texts and file_index <= N:
                combined_text = '\n'.join(part_texts)
                output_filename = f"{base_name}_part{file_index}.txt"
                output_path = os.path.join(output_dir, output_filename)
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(combined_text)
                print(f"Created {output_filename}, size approximately {current_size / (1024 * 1024):.2f} MB.")
                file_index += 1

    print(f"Processed {jsonl_file}, generated {min(file_index - 1, N)} files.")

print("All files have been processed.")
