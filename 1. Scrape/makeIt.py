import pickle
import pandas as pd
brands = ["alcatel", "apple", "asus", "blu", "htc", "huawei", "infinix", "lenovo", "lg", "nokia", "samsung", "sony",
              "xiaomi", "zte"]
data = []
for brand in brands:
    with open(f'{brand}.pkl','rb') as f:
        one_list = pickle.load(f)
    data.extend(one_list)

with open('data_list.pkl', 'wb') as file:
    pickle.dump(data, file)

df = pd.DataFrame(data)
df.to_csv("data_list.csv")