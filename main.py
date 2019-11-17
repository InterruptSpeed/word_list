import requests
import re
import os


def download_book(book_id: int, force: bool = False) -> str:
    out_fname = f"books/{book_id}-0.txt"

    if force or not os.path.exists(out_fname):
        book_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        resp = requests.get(book_url)
        if resp.status_code == 200:
            with open(out_fname, "wb") as f:
                f.write(resp.content)
        else:
            book_url = f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"
            resp = requests.get(book_url)
            if resp.status_code == 200:
                with open(out_fname, "wb") as f:
                    f.write(resp.content)

    return out_fname


def get_words(fname: str) -> list:
    with open(fname, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_words = list(set("\n".join(lines).split(" ")))
    # TODO: be more pythonic with the replaces
    new_words = [x.replace("\n", "").replace("“", "").replace("”", "").lower() for x in new_words]
    pattern = r'^[a-zA-Z]*$'
    new_words = [x.strip() for x in new_words if re.search(pattern, x)]
    new_words.sort()

    return new_words


def save_words(words: list) -> str:
    out_fname = f"words.txt"

    with open(out_fname, "w", encoding="utf-8") as f:
        f.write("\n".join(words))

    return out_fname


# TODO: get the list from gutenberg directly
ids = [
    36,     # The War of the Worlds
    43,     # The Strange Case of Dr. Jekyll and Mr. Hyde
    41,     # The Legend of Sleepy Hollow 
    46,     # A Christmas Carol
    84,     # Frankenstein
    345,    # Dracula
    1342,   # Pride and Prejudice
    1661,   # The Adventures of Sherlock Holmes
    2591,   # Grimms' Fairy Tales
    2701,   # Moby Dick
    50133,  # The Dunwich Horror
    60716   # A Song of the Open Road and Other Verses
]
words = []
# TODO: be more pythonic
for id in ids:
    fname = download_book(id)
    words = words + get_words(fname)

words = list(set(words))
words.sort()

save_words(words)

print(f"{len(ids)} books contain {len(words)} distinct words.")
