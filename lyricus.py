#!/usr/bin/python

import sys
import os
import platform
import json
from requests import get
import bs4

def clear():
    if(platform.system() == "Windows"):
        os.system("cls")
    else:
        os.system("clear")


def main():
    key = ""

    print("Loading....")

    with open("data.json") as dataJson:
        try:
            key = json.load(dataJson)["apiKey"]
        except KeyError:
            print("\nThere was an error loading, please check if you have the file \"data.json\" in your working directory.")
            input("\nPress Enter to exit")
            clear()
            sys.exit()

    clear()

    search = input("Enter the name of a song: ")

    print("\nPlease wait....")

    srch = get("https://api.genius.com/search?q=" + search, headers = {'Authorization': "Bearer " + key})

    clear()

    results = []

    print("Choose a song:")
    
    for index, i in enumerate(srch.json()["response"]["hits"]):
        if index + 1 > 10:
            break
        results.append(i)
        print("  " + str((index + 1)) + ". " + i["result"]["title"] + " - " + i["result"]["primary_artist"]["name"])

    selection = ""
    while(True):
        try:
            selection = input("Enter a number or 'exit': ")
            if(selection == "exit"):
                clear()
                sys.exit()

            selection = int(selection)
            break
        except ValueError:
            print("\nThat isn't a number\n")
            continue

    clear()
    print("Please wait....")

    selectedJson = results[selection - 1]
    page = get("https://genius.com" + selectedJson["result"]["path"])

    clear()

    # A hacky way of getting the lyrics, sometimes the scrapper gives weird resutlts :/
    try:
        print(bs4.BeautifulSoup(page.content, 'html.parser').find('div', class_ = 'lyrics').text[:-2])
    except AttributeError:
        soup = bs4.BeautifulSoup(page.content, 'html.parser')

        for br in soup.find_all("br"):
            br.replace_with("\n")

        divs = soup.select("div[class^=SongPageGrid]")

        for div in divs[1:-3]:
            print(div.text)
    
    print("\nLyricy provided by https://genius.com")

    input("\nPress Enter to exit")
    
    clear()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
