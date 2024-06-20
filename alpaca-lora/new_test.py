import os

import chardet

search_path = './data'

for root, dirs, files in os.walk(search_path):
    for file in files:
        print(file)
        file_name = os.path.join(root, file)
        f3 = open(file=file_name, mode='rb')
        data = f3.read()
        f3.close()
        result = chardet.detect(data)
        print(result)
