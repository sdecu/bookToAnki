import json
import string
from monte import *

"""
for key in monte.keys():
   print(key)
   if key == string.punctuation:
      monte.pop(key, None) 
"""
    
json_data = json.dumps(monte)

f = open('./monte.json', 'w')
f.write(json_data.encode().decode('unicode-escape'))
f.close()
