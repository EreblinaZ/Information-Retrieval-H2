import tkinter as tk
from tkinter import messagebox
import math
import os
import re

# Funksioni qe numeron te gjitha fjalet ne nje dokument
def count_all_words(document):
    words = re.findall(r'\b\w+\b', document.lower())  # Regex pattern per te gjetur fjalet
    return len(words)

# Funksioni qe llogarit TF
def calculate_tf(document, term):
    words = re.findall(r'\b\w+\b', document.lower())
    term_count = sum(1 for word in words if word.lower() == term.lower())
    total_words = len(words)
    if total_words == 0:
        return 0.0
    tf = term_count / total_words
    return tf

# Funksioni qe llogarit IDF
def calculate_idf(documents, term):
    num_documents = len(documents)
    num_documents_containing_term = sum(1 for document in documents if term.lower() in re.findall(r'\b\w+\b', document.lower()))
    if num_documents_containing_term == 0:
        return 0.0
    idf = math.log10(num_documents / num_documents_containing_term)
    return idf

# Funksioni qe llogarit TF-IDF
def calculate_tf_idf(tf, idf):
    return tf * idf

# Funksioni per te shkruar llogaritjet
def write_calculations_to_file(term, tf_values, idf):
    with open("calculations.txt", 'a') as output_file:
        output_file.write(f"\nCalculations for term '{term}':\n")
        for filename, tf in tf_values.items():
            output_file.write(f"\tTF in {filename}: {tf}\n")
        output_file.write(f"\tIDF: {idf}\n")
        for filename, tf in tf_values.items():
            tf_idf = calculate_tf_idf(tf, idf)
            output_file.write(f"\tTF-IDF in {filename}: {tf_idf}\n")

# Funksioni per te numeruar te gjitha fjalet ne index.txt dhe index2.txt
def count_total_words_in_index():
    word_counts = {}
    for filename in ["index.txt", "index2.txt"]:
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"The file {filename} does not exist in the current directory.")
        with open(filename, 'r') as file:
            content = file.read()
            words = re.findall(r'\b\w+\b', content.lower())  # Regex pattern per te gjetur fjalet
            word_counts[filename] = len(words)
    return word_counts

# Funksion per te ndertuar inverted index
def build_inverted_index():
    inverted_index = {}
    word_counts = {}
    for filename in ["index.txt", "index2.txt"]:
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"The file {filename} does not exist in the current directory.")
        with open(filename, 'r') as file:
            word_counts[filename] = {}
            for line_num, line in enumerate(file, start=1):
                words = re.findall(r'\b\w+\b', line.strip().lower())
                for word in words:
                    if word not in inverted_index:
                        inverted_index[word] = [(filename, line_num)]
                    else:
                        inverted_index[word].append((filename, line_num))
                    
                    # Shto fjalen ne numerimin e fjaleve ne dokumentin aktual
                    if word not in word_counts[filename]:
                        word_counts[filename][word] = 1
                    else:
                        word_counts[filename][word] += 1

    total_words = count_total_words_in_index()
    write_total_words_to_file(total_words)
    return inverted_index

# Funksioni per te shkruar numrin total te fjaleve ne fajll
def write_total_words_to_file(total_words):
    with open("calculations.txt", 'w') as output_file:
        for filename, count in total_words.items():
            output_file.write(f"Total number of words in {filename}: {count}\n")

# Funksioni per te kerkuar nje fjale dhe per te llogaritur TF-IDF
def search_word_and_calculate_tf_idf(inverted_index, documents, word):
    word = word.lower()
    if word in inverted_index:
        search_result = inverted_index[word]
        # Llogaritja e TF per secilin dokument
        tf_values = {filename: calculate_tf(documents[filename], word) for filename in documents}
        # Llogaritja e IDF per fjalen
        idf = calculate_idf([doc for doc in documents.values()], word)
        # Shkruaj llogaritjet e TF dhe IDF në fajll
        write_calculations_to_file(word, tf_values, idf)
        return search_result, False
    else:
        documents['index.txt'] += f'\n{word}'  # Shto fjalen e re ne permbajtjen e index.txt
        with open("index.txt", 'a') as file:
            file.write('\n' + word)  # Shto fjalen e re ne index.txt
        inverted_index[word] = [("index.txt", len(documents['index.txt'].splitlines()))]  # Perditeso inverted index
        return [("index.txt", len(documents['index.txt'].splitlines()))], True

# Funksioni per te kryer kerkimin
def search():
    search_word_result = entry.get()
    documents = read_documents_from_files(["index.txt", "index2.txt"])
    search_result, word_added = search_word_and_calculate_tf_idf(inverted_index, documents, search_word_result)

    if search_result:
        if not word_added:
            with open("search_result.txt", 'w') as output_file:
                output_file.write(f"Search results for '{search_word_result}':\n")
                positions = {}
                for filename, line_num in search_result:
                    with open(filename, 'r') as index_file:
                        lines = index_file.readlines()
                        if line_num <= len(lines):
                            line = lines[line_num - 1].strip()
                            output_file.write(f"Line {line_num} in {filename}: {line}\n")
                            line_positions = [i+1 for i in range(len(line.split())) if line.split()[i].lower() == search_word_result.lower()]
                            positions[(filename, line_num)] = line_positions
                for (filename, line_num), pos_list in positions.items():
                    output_file.write(f"Positions of '{search_word_result}' in Line {line_num} of {filename}: {pos_list}\n")
            
            # Numero paraqitjet e fjales se kerkuar ne index.txt dhe index2.txt
            count_index = len(re.findall(r'\b{}\b'.format(re.escape(search_word_result.lower())), documents["index.txt"].lower()))
            count_index2 = len(re.findall(r'\b{}\b'.format(re.escape(search_word_result.lower())), documents["index2.txt"].lower()))

            # Shkruaj numerimet e fjales ne calculations.txt si output
            with open("calculations.txt", 'a') as output_file:
                output_file.write(f"In document index.txt, the term '{search_word_result}' appears: {count_index} times\n")
                output_file.write(f"In document index2.txt, the term '{search_word_result}' appears: {count_index2} times\n")
        else:
            messagebox.showinfo("Search Result", f"The word '{search_word_result}' has been added to the document index.txt.")

# Funksioni per mbylljen e aplikacionit
def on_closing():
    if messagebox.askokcancel("Close", "Do you want to close the app?"):
        root.destroy()

# Funksioni qe lexon dokumentet nga fajllat
def read_documents_from_files(filenames):
    documents = {}
    for filename in filenames:
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"The file {filename} does not exist in the current directory.")
        with open(filename, 'r') as file:
            documents[filename] = file.read()
    return documents

# Nderfaqja grafike e perdoruesit (GUI)
root = tk.Tk()
root.title("Search Box")

window_width = 400
window_height = 100
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

frame = tk.Frame(root, width=300, height=200)
frame.pack_propagate(False)
frame.pack()

label = tk.Label(frame, text="Enter the word to search:")
label.pack()

entry = tk.Entry(frame)
entry.pack()

search_button = tk.Button(frame, text="Search", command=search)
search_button.pack()

try:
    inverted_index = build_inverted_index()
except FileNotFoundError as e:
    messagebox.showerror("Error", str(e))

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()