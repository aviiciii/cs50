from cs50 import get_string


def main():

    text = get_string("Text: ")

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # avg no of letters per 100 words
    avg_let = letters / words * 100
    # avg no of sentences per 100 words
    avg_words = sentences / words * 100

    # formula
    grade = round(0.0588 * avg_let - 0.296 * avg_words - 15.8)

    # print
    if grade < 1:
        print("Before Grade 1")
    elif grade > 16:
        print("Grade 16+")
    else:
        print("Grade " + str(grade))


def count_letters(text):
    l = 0
    for i in range(len(text)):
        if str.isalpha(text[i]):
            l += 1
    return l


def count_words(text):
    w = 1
    for i in range(len(text)):
        if str.isspace(text[i]):
            w += 1
    return w


def count_sentences(text):
    s = 0
    for i in range(len(text)):
        if text[i] == '.' or text[i] == '!' or text[i] == '?':
            s += 1
    return s


if __name__ == "__main__":
    main()