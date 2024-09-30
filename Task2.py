import nltk
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import os


# Preprocess text
def preprocess_text(text):
    words = nltk.word_tokenize(text.lower())  # Tokenize and convert to lowercase
    words = [word for word in words if word.isalpha()]  # Remove punctuation/numbers
    return words


# Compute word frequencies
def get_word_frequencies(words):
    return Counter(words)


# Create theoretical Zipf distribution
def get_theoretical_zipf_distribution(num_words, s):
    ranks = np.arange(1, num_words + 1)
    theoretical_zipf = 1 / (ranks ** s)  # Theoretical Zipf distribution
    theoretical_zipf /= np.sum(theoretical_zipf)  # Normalize to make it a probability distribution
    return theoretical_zipf


# Read and collect word frequencies from directory
def read_and_collect_frequencies_from_directory(directory_path):
    all_frequencies = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Only read .txt files
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()  # Read the text file
                words = preprocess_text(text)  # Preprocess the text (tokenize, lowercase, remove punctuation)
                frequencies = get_word_frequencies(words)  # Get word frequencies
                all_frequencies.append((filename, frequencies))  # Store file name and its frequencies
    return all_frequencies


def texts_selection(dict):
    print('Choose texts to compare:')
    for i, k in enumerate(dict.keys(), 1):
        print(i, '.', k)
    print('Select types:')
    input_dir = input()


# Get Q-Q Plot for each txt file, and set paremeter as 1.15
def plot_qq_for_zipf_law(all_frequencies, s=1.15):
    for filename, frequencies in all_frequencies:
        # Step 1: Get the word frequencies sorted in descending order
        word_counts = np.array([count for word, count in frequencies.most_common()])
        num_words = len(word_counts)

        # Step 2: Create the theoretical Zipf distribution
        theoretical_zipf = get_theoretical_zipf_distribution(num_words, s)

        # Step 3: Normalize word counts to make them a probability distribution
        word_probabilities = word_counts / np.sum(word_counts)

        # Step 4: Get Quantiles
        zipf_quantile = np.cumsum(theoretical_zipf)
        word_quantile = np.cumsum(word_probabilities)

        # Step 4: Generate the QQ plot
        plt.figure(figsize=(4, 4))
        plt.scatter(zipf_quantile, word_quantile, alpha=0.6, label='Actual vs Theoretical')

        # Plot a reference line (y=x) to visualize deviation from Zipf law
        max_val = max(max(zipf_quantile), max(word_quantile))
        plt.plot([0, max_val], [0, max_val], color='red', linestyle='--')

        plt.title(f'QQ Plot for Zipf Law - {filename}')
        plt.xlabel('Theoretical Quantiles (Zipf)')
        plt.ylabel('Actual Quantiles (Word Frequencies)')
        plt.grid(True)
        plt.legend()
        plt.show()


def plot_pp_for_comparison(all_frequencies):
    titles = []
    probs = []
    for filename, frequencies in all_frequencies:
        # Step 1: Get the word frequencies sorted in descending order
        word_counts = np.array([count for word, count in frequencies.most_common()])

        titles.append(filename)
        probs.append(word_counts)

    plt.figure(figsize=(4, 4))
    plt.loglog(np.arange(1, len(probs[0]) + 1), probs[0], marker='o', alpha=0.6, label=f'{titles[0]}')

    plt.loglog(np.arange(1, len(probs[1]) + 1), probs[1], marker='x', alpha=0.6, label=f'{titles[1]}')

    plt.title(f'Distribution Plot for comparison: - {titles[0]} vs {titles[1]}')
    plt.xlabel('Log Rank')
    plt.ylabel('Log Frequency')
    plt.grid(False)
    plt.legend()
    plt.show()


def display_menu():
    print("Types:")
    for index, (key, value) in enumerate(categories.items(), 1):
        print(f"{index}. {key}")


# Get selected directory
def get_directory_choice():
    choice = int(input("Select type: "))
    descriptions = list(categories.keys())
    if 1 <= choice <= len(descriptions):
        selected_description = descriptions[choice - 1]
        selected_directory = categories[selected_description]
        return selected_directory
    else:
        print("Invalid choice")
        return None


# List all files under selected directory
def list_files_in_directory(directory):
    try:
        files = os.listdir(directory)
        files=[file for file in files if file.endswith(".txt")]

        print(f"Texts in '{directory}' :")
        for index, file in enumerate(files, start=1):
            print(f"{index}. {file}")
        return files
    except FileNotFoundError:
        print("No Such File")
        return []


# Select file
def get_file_choice(files):
    choice = int(input("Select file: "))
    if 1 <= choice <= len(files):
        return files[choice - 1]
    else:
        print("Invalid choice")
        return None


categories = {
    "Finance": 'finance',
    "Neural Network": 'NN',
    "Aero Physics": 'Physics',
    "President Inaugural Address": 'speech',
    "Wikipedia": 'Wiki',
    "Adventure Novels": 'novel',
    "NeurIPS 2022": 'NeurIPS2022',
    "NeurIPS 2023": 'NeurIPS2023'
}

all_frequencies = []
for i in range(2):
    display_menu()
    directory = get_directory_choice()
    if directory:
        files = list_files_in_directory(directory)
        if files:
            selected_file = get_file_choice(files)
            if selected_file:
                print(f"Selected file: {selected_file}")
                with open(os.path.join(directory, selected_file), 'r', encoding='utf-8') as file:
                    text = file.read()  # Read the text file
                    words = preprocess_text(text)  # Preprocess the text (tokenize, lowercase, remove punctuation)
                    frequencies1 = get_word_frequencies(words)  # Get word frequencies
                    all_frequencies.append((selected_file, frequencies1))
            else:
                print("No file")
        else:
            print("Empty")
    else:
        print("Invalid choice")

plot_pp_for_comparison(all_frequencies)
