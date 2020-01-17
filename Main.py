# Below is where all libraries used within the code are imported
import re   # imports regular expression library

# Below is the initialization of variables used in the project that need to be available throughout the entire code
input_data = ""     # Initialize the input data variable as a string
words = []      # Initialize the list that will contain the words found in the input data
words_dict = {}  # Initialize word dictionary, each word a key with the number of occurrences as the corresponding value
words_dict_desc = {}  # Initialize word dictionary for descending order
output_text = ""   # Initialize the string that will be writing to the output file
longest_word_len = 0  # Initialize the variable for longest word
pattern = re.compile(r"\b\w*'?\w*[^\W]\b")  # Initialize the the regular expression pattern used to find words

# This following comments are a more in-depth explanation of the regular expression pattern initialized above:

# The pattern begins and ends with "\b", "\b" represents a word boundary thus it is ideal for the starting and ending
# point of each match because it will insure that we are not collecting substrings or full lines of text.

# Within the word boundaries the pattern first looks for "\w*". "\w" means any word character, it is equal to the
# regex pattern "[a-zA-Z0-9_]" but more concise. The "*" following it tells the pattern that the amount of word
# characters adjacent to each other could range from 0 to infinity and to match for all possibilities of word length.

# Next is "'?", the "'" is a literal apostrophe, the "?" following it tells the pattern that the preceding character
# may or may not occur once within the pattern. Since more valid characters may occur after an apostrophe to
# complete the word, another "\w*" follows it, otherwise it would cause the pattern to begin a new match after any
# apostrophe.

# While there are no words with apostrophes in the input provided I found it necessary to add this level of flexibility
# so that the process will work with a wider range of inputs.

# The last segment of this pattern before the closing word boundary is "[^\W]". This segment tells the pattern what
# not to include in our matches if they are to appear. First the "^" signifies that all characters listed within the
# square brackets are not to be matched upon. The '\W' is the inverse of the previously used '\w' meaning that it
# signifies all non-word characters. The reason for this addition is to prevent the pattern from matching on
# vertical tabs (https://en.wikipedia.org/wiki/Tab_key#Tab_characters) which would technically match the rest of the
# pattern if it was not explicitly stated that they should not be included. While the signifier for vertical tabs ('\v')
# could be used to alleviate this problem as well, the pattern would interpret this as any character besides vertical
# tabs is allowed to follow the last character in the word as long as it has a word boundary following it. '\W' covers
# the pattern on all bases and prevents words from having a tailing whitespace character or any other potential issue
# that could arise. The only potential downfall to it is that this separates a hyphenated word/phrase into the words
# it's composed of, my interpretation is that a hyphenated phrase should be separated into it's composing words. If
# you want to count each hyphenated word/phrase as it's own entity the pattern used would be "\b\w*'?[-?\w*]*[^\W]\b"

# -------------------------------------------------------------------------------------------------------------------

# Below is the process that reads the data from input.txt and assigns it's value to the string variable input_data

# A 'with' statement is used to automatically close the file after the process has finished reading and assigning its
# value to input_data, 'r' means that the process will only read the file
with open('input.txt', 'r') as input_file:
    input_data = input_file.read()   # read file and place the value into variable input_data

# -------------------------------------------------------------------------------------------------------------------

# Below is the line of code that finds all the occurrences that match the previously defined regular expression pattern
# using the function findall (imported from re library) and assigns the returned list to the words list
words = pattern.findall(input_data)

# -------------------------------------------------------------------------------------------------------------------

# Below is the loop that creates a key for each unique word in the words list and calculates it's number of occurrences
for word in words:
    word_low = word.lower()    # assigns the word to a new variable, using the function lower to insure uniformity
    if word_low in words_dict.keys():   # If the word already appears in the dictionary, add 1 to it's existing value
        words_dict[word_low] = words_dict[word_low] + 1
    else:        # If the word is appearing for the first time, create a key for it and assign it a value of 1
        words_dict[word_low] = 1

# -------------------------------------------------------------------------------------------------------------------

# Below is the code that finds the length of the longest word, the longest_word_len value is used calculate how many
# spaces are required so that the pipes in the output form a vertical line.
# The longest word is calculated by using the sorted function with the len function as it's sorting key since the
# list needs to be sorted by the length of each word. By default it is sorted by the lengths in ascending order so the
# sorted function's reverse value is set to true to make it descending. The first value in the returned list is
# taken and and the len function is run on it so the value assigned is the amount characters within the word.
longest_word_len = len(sorted(words, key=len, reverse=True)[0])

# -------------------------------------------------------------------------------------------------------------------

# Below is the code that orders the words_dict into descending order
# The new dictionary is created by using the sorted function with the lambda function as its sorting key since the
# dictionary needs to be sorted on it's mathematical value. By default it is sorted by the value in ascending order so
# the sorted function's reverse value is set to true to make it descending
words_dict_desc = {word: value for word, value in sorted(words_dict.items(), key=lambda item: item[1], reverse=True)}

# -------------------------------------------------------------------------------------------------------------------

# Below is the code that creates the string that will be written to the output file
for word, value in words_dict_desc.items():  # Iterates through words_dict_desc in sequential order
    word_len = len(word)  # Get the amount of characters in the word
    spaces = " " * (longest_word_len - word_len)  # Calculate and create a string for the amount of spaces needed
    equal_signs = "=" * value  # Create a string for the amount of equal signs needed
    line_value = f"{spaces}{word} | {equal_signs} ({value})\n"  # The variables are placed in their appropriate place
    output_text = output_text + line_value  # adds the line to the output text string

output_text = output_text[:-1]   # Removes the new line character at the end of the file so there isn't an empty line

# -------------------------------------------------------------------------------------------------------------------

# Below is the code that writes the value of output_text to the output.txt file
# A similar process is used that was used for reading the input file, the main difference being that when opening
# the file, "w" is used to tell python that the program is writing to the file and the write function is used to
# write the value of output_text to it
with open("Output.txt", "w") as output_file:
    output_file.write(output_text)
