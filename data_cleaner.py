import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def remove_rows_with_negative_values(data, attributes):
    for attribute in attributes[:-1]:
        data = data[data[attribute] > 0]
        # data = pd.DataFrame(data, index=negative_rows)
    return data

if __name__ == "__main__":
    data = pd.read_csv("DT_Data_CakeVsMuffin_v012_TRAIN.csv")
    attributes = data.columns

    data = remove_rows_with_negative_values(data, attributes)

    data = data.round(3)

    # clean_data = pd.DataFrame(data)
    bin_size_map = {'Flour_Binned':10, 'Sugar_Binned':10, 'Oils_Binned':10, 'Proteins_Binned':10}

    for attribute in attributes[:-1]:
        # attribute = attributes[i]
        # quantile_list = [0, .1, 0.2, .3, .4, .5, .6, .7, .8, .9, 1.]
        quantile_list = np.linspace(0, 1, endpoint=True, num=bin_size_map[attribute+"_Binned"])
        print(quantile_list)
        attribute_quantile_values = data[attribute].quantile(quantile_list)
        print(attribute+":\n")
        # print(attribute_quantile_values.round(3).to_numpy())
        attribute_quantile_values_array = attribute_quantile_values.round(3).to_numpy()
        attribute_quantile_labels = attribute_quantile_values.round(3).to_numpy(dtype=str)
        # print(attribute_quantile_values_array)
        # print(attribute_quantile_labels)
        attribute_binned_values, bins = pd.cut(data[attribute], attribute_quantile_values_array, labels=attribute_quantile_labels[1:], retbins=True, include_lowest=True)
        # print(bins)
        # print(attribute_binned_values)
        data[attribute] = attribute_binned_values
        # attribute_binned_values = pd.cut(data[attribute], attribute_quantile_values.round(3), labels=bins[1:])
        # print(bins)
        # print(attribute_binned_values.to_numpy())
        # idx = pd.IntervalIndex(attribute_binned_values)
        # print(bins)
        # print(idx)
        # print([v for v in idx])
        # data["{}_Binned".format(attribute)] = attribute_binned_values
        # interval_dataframe = pd.DataFrame({'intervals': idx, 'left': idx.left, 'right': idx.right})
        # print(interval_dataframe['right'])
        # clean_data["{}_Binned".format(attribute)] = attribute_binned_values
        # print(interval_dataframe['right'])
        # print(interval_dataframe.shape)
        # print(data.shape)
        # data["{}_Binned".format(attribute)] = interval_dataframe['right']
        # interval_dataframe.to_csv("{}.csv".format(attribute), index=False)
        # print(data["{}_Binned".format(attribute)])
        # data.insert(i+1, "{}_Binned".format(attribute), attribute_binned_values)

    print(data)

    data.to_csv("DT_Data_CakeVsMuffin_v012_TRAIN_CLEAN.csv", index=False)