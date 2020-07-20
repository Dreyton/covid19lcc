import requests
import pandas as pd
import json

url = 'https://brasil.io/api/dataset/covid19/caso/data/?city=' + 'Marabá' + '&format=json'
url_data = requests.get(url).content
json_data = json.loads(url_data)
df = pd.read_json(json.dumps(json_data['results']))
df_new = df.sort_values(by='date')
print(df_new.columns)

date=df_new['date'][0]
confirmed=df_new['confirmed'][0]
confirmed_per_100k=df_new['confirmed_per_100k_inhabitants'][0]
death_rate=df_new['death_rate'][0]
deaths=df_new['deaths'][0]

print(date)
print(confirmed)
print(confirmed_per_100k)
print(deaths)
print(death_rate)
