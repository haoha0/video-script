import json

with open('video_zone_tags_list_filtered.json', 'r') as file:
    tags_list = json.load(file)

tags = []

for item in tags_list:
    for zone in item:
        tags.append(zone['tag_name'])

print(tags)