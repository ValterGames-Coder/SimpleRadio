import json

stream_name = input('Add stream name: ')
stream_url = input('Add stream url: ')

with open('stream_list.json', 'r') as openfile:
    streams = json.load(openfile)

with open('stream_list.json', 'w') as openfile:
    streams.append({'name': stream_name.strip(), 'url': stream_url.strip()})
    json_obj = json.dump(streams, openfile)