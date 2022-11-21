def get_text(file_name):
    """
    reads the original text file, decodes, and returns the entire file as a string
    :return: str
    """
    with open(file_name, "rb") as f:
        return f.read().decode('utf-8')


def get_word_list(file_name):
    """
    Reads and returns the file contents as a list of cleaned words
    :param filename:
    :return: list of str
    """
    return [x.strip() for x in get_text(file_name).split()]


input_file_name = "petofi.txt"
output_file_name = "results.csv"
with open(output_file_name, "wb") as outfile:  # open result file in binary, so utf-8 encoding is possible
    for number, word in enumerate(
            get_word_list(input_file_name)):  # iterates through the word list with the matching numbers
        human_readable_number = number + 1  # python starts from 0, humans count from 1
        if human_readable_number % 2 == 0:  # print only even words
            outfile.write(f'{human_readable_number}, {word}\n'.encode("utf-8"))  # write result as bytes type
