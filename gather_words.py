import requests


def get_five_letter_words():
    words = []
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    for letter in alphabet:
        url = f"https://api.datamuse.com/words?sp={letter}????"
        response = requests.get(url)
        words_data = response.json()
        words.extend([word_data["word"] for word_data in words_data if len(word_data["word"]) == 5])

    return words


def write_words_to_file(filename, words):
    with open(filename, "w") as file:
        for word in words:
            file.write(word + "\n")


filename = "five_letter_words.txt"
five_letter_words = get_five_letter_words()
write_words_to_file(filename, five_letter_words)

print("5-letter words written to", filename)
