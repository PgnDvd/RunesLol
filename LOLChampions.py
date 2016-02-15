__author__ = 'davide'
import requests,re

start = 'http://leagueoflegends.wikia.com/wiki/List_of_Champions'
f = requests.get(start)
# print(f.text)

result = re.findall('<span><a href="/wiki/(.*)">((?:.|\\n)*?)</a></span></span>\n', f.text)

championNames = []
for name in result:
    index = name[0].rfind('"') + 1
    # print(name[0][index:])
    championNames.append(name[0][index:])

print (championNames)


from collections import defaultdict
# d = defaultdict(int)
d = defaultdict(list)
runes = []
# list=["Riven"]
championsAnalyzed = 0

lanes = ["Top", "Jungle", "ADC", "Middle", "Support"]
# lane = "Top"
for lane in lanes:
    for championName in championNames:
        print(championName)
        championName = championName.replace("'", "")
        championName = championName.replace(" ", "")
        championName = championName.replace(".", "")
        championName = championName.replace("Wukong", "MonkeyKing")
        start = 'https://champion.gg/champion/'+championName+'/' + lane
        f = requests.get(start)
        # print(f.text)
        if not f.history:
            championsAnalyzed +=1
            # > <span class="rune-title">Greater Mark of Attack Damage </span>
            startHighestWinRunes = '<h2 class="champion-stats" style="margin-top:45px">Highest Win % Runes</h2>'
            endHighestWinRunes = '<h2 class="champion-stats">Most Frequent Core Build</h2>'
            highestRunes = f.text[f.text.index(startHighestWinRunes):f.text.index(endHighestWinRunes)]
            # print(highestRunes)
            result = re.findall('<span class="rune-title">((?:.|\\n)*?)</span>', highestRunes)
            for rune in result:
                print(rune)
                d[rune].append(lane+"-"+championName)
                runes.append(rune)

# print(d)
from collections import Counter
print("Analyzed "+str(championsAnalyzed)+ " "+lane+" champions")
print(Counter(runes).most_common())

import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(d)

import collections
od = collections.OrderedDict(sorted(d.items()))
for key in od:
    print(key, d[key].__len__())