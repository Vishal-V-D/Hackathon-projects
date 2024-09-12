from itertools import product
import requests

inp = input("enter what u want to search for: ")

lis = inp.split(" ")
adds = ["s", "es"]

word_dict = dict().fromkeys(lis)

for i in lis:
    l = []
    for t in adds:
        l += [i+t]
    word_dict[i] = [i]+l


combinations = product(*word_dict.values())
li = []
# Print each combination
for combination in combinations:
    li += [('+'.join(combination))]

save_path = r"D:\My Drive\mine\codes\python\learning\AI\dataset\image"

c = 0
for g in li:
    response = requests.get(f"https://th.bing.com/th?q={g}")
    response.raise_for_status()  # Check for HTTP errors
    pt = save_path+f"{c}"+".jpg"
    with open(pt, 'wb') as file:
        file.write(response.content)
    c += 1
    print(f"Image downloaded and saved as {pt}")