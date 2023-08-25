import requests
import json

url = 'http://movie.douban.com/j/search_subjects?'
payload = {
  'search_text': '无心法师',
  'cat': 'movie',
  'start': 0,
  'count': 100,
}
response = requests.get(url, params=payload)
print(response.text)
data = json.loads(response.text)

url2 = 'http://movie.douban.com/j/search_subjects?'
payload2 = {
  'search_text': '致青春',
  'cat': 'movie',
  'start': 0,
  'count': 100,
}
response2 = requests.get(url2, params=payload2)
data2 = json.loads(response2.text)

actors1 = []
actors2 = []
for item in data['subjects']:
  if item['title'] == '无心法师':
    actors1.append(item['casts'])
for item in data2['subjects']:
  if item['title'] == '致青春':
    actors2.append(item['casts'])
common_actors = list(set(actors1) & set(actors2))
if len(common_actors) > 0:
  print('无心法师和致青春共有的演员有：', common_actors)
else:
  print('无心法师和致青春没有共同演员')  