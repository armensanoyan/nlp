import os
import tika
import json
from tika import parser

def pdf_to_json(file_name):
    parsed = parser.from_file(os.path.join(os.getcwd(), 'artcles', file_name))
    whole_data = parsed["metadata"]
    whole_data['text'] = parsed["content"].replace('\n','')
    with open(f'jsons/{file_name}.json', 'w', encoding='utf-8') as file:
        #  file.write(parsed["content"])
        json.dump(whole_data, file, indent=4, sort_keys=False)

file_list = os.listdir('./artcles')
file_list.remove('.DS_Store')
[pdf_to_json(i) for i in file_list]

print('done')