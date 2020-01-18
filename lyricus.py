import requests
import bs4

search = input("Enter song name: ")

srch = requests.get("https://api.genius.com/search?q=" + search, headers = {'Authorization': "Bearer xusaWFOMFCJROk_SfLi-8vZAXmCQfuLa5YjTSXuxItxyUj28ie1YscW26jwQz7o3"})

results = []

print("\nSelect a song:")

for index, i in enumerate(srch.json()["response"]["hits"]):
    if index + 1 > 10:
        break
    results.append(i)
    print("  " + str((index + 1)) + ". " + i["result"]["title"] + " - " + i["result"]["primary_artist"]["name"])

selection = ""
while(True):
    try:
        selection = int(input("Enter a number: "))
        break
    except ValueError as err:
        print("\nThat is not a number!!\n")
        continue

selectedJson = results[selection - 1]
page = requests.get("https://genius.com" + selectedJson["result"]["path"])

print(bs4.BeautifulSoup(page.content, 'html.parser').find('div', class_ = 'lyrics').text)
print("\nLyrics provided by https://genius.com")

input("\nPress any key to exit")
