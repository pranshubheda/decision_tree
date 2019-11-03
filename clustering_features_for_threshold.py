import pandas as pd
import numpy as np
from sys import maxsize

def calculate_mixed_variance(v1, v2, n1, n2):
    """
    Calculate the mixed variance for the given
    arguments for a particular threshold
    
    Arguments:
        v1 -- variance of cluster records <= threshold
        v2 -- variance of cluster records > threshold
        n1 -- number of cluster records <= threshold
        n2 -- number of cluster records > threshold
    """
    n = n1+n2
    mixed_variance = (n1/n)*v1 + (n2/n)*v2
    return mixed_variance

def regularization(slow_group, fast_group, objective_function):
    """
    Function used to calculate the cost_function value
    which is minimized in situation where we are adding
    a regularization term to the mixed variance
    
    Arguments:
        slow_group -- dataframe object holding cluster records <= threshold
        fast_group -- dataframe object holding cluster records > threshold
        objective_function -- [description]
    """
    norm_factor = 50
    alpha = 1
    regularization_val = (abs(slow_group - fast_group)/norm_factor) * alpha
    cost_function = objective_function + regularization_val
    return cost_function

def find_threshold(df, regularize, bin_intervals, attribute):
    """
    Find the threshold with minimum mixed variance
    for the given dataframe
    
    Arguments:
        df -- dataframe containing all records
        regularize -- boolean flag to use regularization or not
        bin_intervals -- the bin values that need to be tested
    """
    min_mv = maxsize
    min_bin = -1
    min_slow_group = 0
    min_fast_group = 0

    mixed_variance = []
    for bin in bin_intervals:
        #divide the dataframe into 2 based on 
        #threshold
        d1 = df[df['bin']<=bin][attribute]
        d2 = df[df['bin']>bin][attribute]

        #size of clusters
        n1, n2 = len(d1), len(d2)

        #variance of cluster
        v1 = np.var(d1)
        v1 = np.nan_to_num(v1)

        v2 = np.var(d2)
        v2 = np.nan_to_num(v2)

        #mean of cluster
        m1 = d1.mean()
        m1 = np.nan_to_num(m1)

        m2 = d2.mean()
        m2 = np.nan_to_num(m2)

        #calculate mixed variance
        mv = calculate_mixed_variance(v1, v2, n1, n2)

        #add regularization term
        if regularize:
            mv = regularization(n1, n2, mv)

        #record min mixed value and the corresponding bin
        if mv <= min_mv:
            min_mv = mv
            min_bin = bin
            min_slow_group = n1
            min_fast_group = n2

        mixed_variance.append(mv)
        # print("Bin->{}, M1-{}, M2->{}, V1->{}, V2->{}".format(bin, m1, m2, v1, v2))
        # print("N1->{}, N2->{}".format(n1, n2))
        # print("bin->{}, MV->{}".format(bin, mv))

    return ((min_bin, min_mv), (min_slow_group, min_fast_group))

if __name__ == "__main__":
    #load the data into pandas dataframe
    data = pd.read_csv('DT_Data_CakeVsMuffin_v012_TRAIN_CLEAN.csv')
    attributes = data.columns
    for attribute in attributes[:-1]:
        # attribute = 'Flour'
        # data = data['Flour'].to_frame()
        bin_floor = round(data[attribute].min())
        bin_ceil = round(data[attribute].max())
        # print(data)
        #creating a ndarray [bin_floor .. bin_ceil]
        bins = np.linspace(bin_floor, bin_ceil, bin_ceil-bin_floor+1)
        # print(bins)

        #quantizing the given data in bins created
        #in the above step
        res = pd.cut(data[attribute], bins)
        #create a new column called bin with
        #the assigned bin value
        #example
        # id | car speed | bin
        # 0     24.234     (24, 25]
        attribute_data = data[attribute].to_frame()
        attribute_data['bin'] = res
        #sorting the data based on the bin value
        attribute_data = attribute_data.sort_values(by=[attribute, 'bin'], ascending=False)
        # print(attribute_data)
        #creating interval range of the created bin categories
        #we use these bins for filtering car speeds > bin and 
        #car speeds <= bin
        #[ (40, 41], ... (79, 80] ]
        bin_interval_ranges = pd.interval_range(start=bin_floor, end=bin_ceil)
        # print(bin_interval_ranges)
        (min_bin, min_mv), (n1, n2) = find_threshold(attribute_data, False, bin_interval_ranges, attribute)
        print("Threshold for {} : Bin->{} Minimum Mixed Variance->{} G1->{} G2->{}\n\n".format(attribute, min_bin, min_mv, n1, n2))