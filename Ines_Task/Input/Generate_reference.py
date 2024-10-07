import json

img = [f"{i}.png" for i in range(1, 17)]
player = [f"{i}" for i in range(0, 16)]


ref = dict(zip(player, img))


# Save the dictionary to a JSON file
with open('reference.json', 'w') as json_file:
    json.dump(ref, json_file)



#with open('Input/reference.json', 'r') as json_file:
#    loaded_dict = json.load(json_file)