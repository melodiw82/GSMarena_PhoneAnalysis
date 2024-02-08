import pickle
import pandas as pd

with open('infinix.pkl','rb') as f:
    infinix_list = pickle.load(f)
infinix_df = pd.DataFrame(infinix_list)


def make_it_one_dictionary(one_device):
    sub_dict = {}

    for sub_dict_key, sub_dict_value in one_device.items():
        if isinstance(sub_dict_value, dict):
            if sub_dict_key in ['Tests','Display' , 'Battery','Main Camera', 'Selfie camera']:
                for key, value in sub_dict_value.items():
                    new_key = f"{sub_dict_key} {key}"
                    sub_dict[new_key] = value
            else:
                for key, value in sub_dict_value.items():
                    sub_dict[key] = value
        else:
            sub_dict[sub_dict_key] = sub_dict_value
    if '\xa0' in sub_dict:
        del sub_dict['\xa0']

    return sub_dict

#example
print(make_it_one_dictionary(infinix_list[55]))

one_dic_list = []

for device in infinix_list:
    one_dic_list.append(make_it_one_dictionary(device))
'''
infinix_one_dic_df = pd.DataFrame(one_dic_list)
for column_name in infinix_one_dic_df.columns:
    num_none_values = infinix_one_dic_df[column_name].isna().sum()
    print(f"Column '{column_name}' has {num_none_values} None values")
'''
