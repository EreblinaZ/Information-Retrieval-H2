# Homework 2 - Information Retrieval
This Python code creates a GUI application using Tkinter to search for words in text files (index.txt and index2.txt). It calculates TF-IDF values for the searched term and writes the results to a file. Here's a brief overview:

## 1. Word Counting and TF-IDF Calculation:
- count_all_words(document): Counts all words in a document.
- calculate_tf(document, term): Calculates the Term Frequency (TF) of a term in a document.
- calculate_idf(documents, term): Calculates the Inverse Document Frequency (IDF) of a term across multiple documents.
- calculate_tf_idf(tf, idf): Computes the TF-IDF value.
- write_calculations_to_file(term, tf_values, idf): Writes TF and IDF calculations to calculations.txt.

## 2. Inverted Index Construction:
- build_inverted_index(): Creates an inverted index from index.txt and index2.txt, mapping words to their positions in the files, and counts total words in each file.
- count_total_words_in_index(): Counts total words in index.txt and index2.txt and writes the counts to calculations.txt.

## 3. Search and Update:
- search_word_and_calculate_tf_idf(inverted_index, documents, word): Searches for a word, calculates TF-IDF, and updates the inverted index if the word is not found.
- search(): Handles the search action triggered by the user, writing results to search_result.txt and updating calculations.txt.

## 4. GUI Setup:
- Creates a Tkinter window with an entry box for user input and a search button.
- The search button triggers the search() function.

## 5. Error Handling:
- If files index.txt or index2.txt are missing, a message box shows an error.

## 6. File Reading:
- read_documents_from_files(filenames): Reads content from specified files into a dictionary.

## 7. Application Initialization:
- Builds the inverted index and starts the Tkinter main loop to run the application.

The application allows users to search for words, view search results, and see TF-IDF calculations, while updating the index if new words are added.
