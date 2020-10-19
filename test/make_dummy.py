# テストデータ作成
# 放物線のような何か
import pandas as pd

t = range(30)
h = [-x**2 + 30 * x for x in t]
lat = []
lon = []
for i in t:
    lat.append(40.242865 - i * 0.0005)
    lon.append(140.010450 - i * 0.0005)

df = pd.DataFrame()
df["latitude"] = lat
df["longitude"] = lon
df["height"] = h

df.to_csv("test/data.csv", index=None, float_format='%5f')
