import os
import requests
import json
from bs4 import BeautifulSoup
import subprocess

def main():
    print_text = ""
    with open(file="./print.txt", mode="r", encoding="utf-8") as file:
        print_text = file.read()
    print(print_text)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    }
    book_base_url = 'https://ncode.syosetu.com/'
    api_base_url = 'https://api.syosetu.com/novelapi/api/'
    while True:
        book_id = input("Book id $ ")
        book_url = book_base_url + book_id
        book_info = json.loads(requests.get(f"{api_base_url}?out=json&ncode={book_id}").content.decode("utf-8"))
        book_title = book_info[1]["title"]
        book_no = book_info[1]["general_all_no"]
        book_text = ""
        print(f"Title: {book_title}\nNo.: {book_no}")
        for i in range(book_no):
            url = f"{book_url}/{str(i+1)}/"
            print(f"Load novel. {i+1}/{book_no}")
            response = requests.get(url, headers=headers).content.decode("utf-8")
            HTML = BeautifulSoup(response, "html.parser")
            text = HTML.select("#novel_honbun")[0].get_text()
            book_text += text + "\n"

        with open(file=f"{book_title}.txt", mode="w", encoding="utf-8") as file:
            file.write(book_text)
        os.system(f"start {book_title}.txt")

if __name__ == '__main__':
    main()