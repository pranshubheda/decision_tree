import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def print_end_ponts(data, attribute):
    min_val = data[attribute].min()
    max_val = data[attribute].max()
    print("{} -> {}, {}".format(attribute, min_val, max_val))

def create_histogram(data, attribute, data_name, bin_size):
    # bin_size = 10
    counts, bins = np.histogram(data[attribute].to_numpy(dtype=float), bin_size)
    plt.hist(bins[:-1], bins, weights=counts)
    plt.title("{}->{}".format(data_name, attribute))
    plt.show()

def create_scatter_plot(g1, g2, attribute):
    n1 = g1[attribute].count()
    n2 = g2[attribute].count()

    # print(g1[attribute].array)
    # print(g1[attribute].values)
    # print("\n\n")
    
    data = ( (g1[attribute].to_numpy(dtype=float), np.random.rand(n1) ), (g2[attribute].to_numpy(dtype=float), np.random.rand(n2) ) )    

    # print(data)

    colors = ("red", "green")
    groups = ("muffin", "cupcake", "water")

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for data, color, group in zip(data, colors, groups):
        x, y = data
        # print(len(x))
        # print(len(y))
        # print(x)
        # print(data)
        ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)

    plt.title('Scatter plot for {}'.format(attribute))
    plt.legend(loc=2)
    plt.show()

def create_seaborn_scatterplot(g1, g2, attribute):
    n1 = g1[attribute].count()
    n2 = g2[attribute].count()

    y1 = np.random.rand(n1)
    y2 = np.random.rand(n2)

    x1 = g1[attribute].to_numpy(dtype=float)
    x2 = g2[attribute].to_numpy(dtype=float)

    sns.scatterplot(x1, y1, x_jitter=False, y_jitter=True)

    sns.scatterplot(x2, y2, x_jitter=3.5, y_jitter=True)
    plt.show()

def convert_to_interval_array(data):
    for d in data:
        print(d[1:-1].split(','))
    # print(type(data))

if __name__ == "__main__":
    colums_to_read = ['Flour_Binned', 'Sugar_Binned', 'Oils_Binned', 'Proteins_Binned', 'RecipeType']
    # colums_to_read = ['Flour_Binned', 'Sugar_Binned', 'Oils_Binned', 'Proteins_Binned']
    # colums_to_read = ['Flour_Binned']
    data = pd.read_csv("DT_Data_CakeVsMuffin_v012_TRAIN_CLEAN.csv", dtype='object', usecols=colums_to_read)
    attributes = data.columns
    # data['Flour_Binned']= data['Flour_Binned'].astype('interval')
    # print(data['Flour_Binned'].to_numpy())
    # convert_to_interval_array(data['Flour_Binned'].to_numpy('str'))

    # print(attributes)
    # data = data.round(3)

    muffins_data = data[data['RecipeType'] == 'Muffin']
    cupcakes_data = data[data['RecipeType'] == 'CupCake']

    bin_size_map = {'Flour_Binned':5, 'Sugar_Binned':5, 'Oils_Binned':5, 'Proteins_Binned':5}
    attributes = ['Flour_Binned', 'Sugar_Binned', 'Oils_Binned', 'Proteins_Binned']
    for attribute in colums_to_read[:-1]:
        # print(data[attribute].describe())
        # print_end_ponts(data, attribute)
        # create_histogram(data, attribute, "total data", bin_size_map[attribute])
        # create_scatter_plot(muffins_data, cupcakes_data, attribute)
        create_seaborn_scatterplot(muffins_data, cupcakes_data, attribute)
        # create_seaborn_scatterplot(data, attribute)
        # print("{}:\n\n{}".format(attribute, data[attribute].describe()))
        