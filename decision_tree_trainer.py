import pandas as pd
import numpy as np
import math

def split_data(data, attribute, value):
    left_split = data[data[attribute] < value]
    right_split = data[data[attribute] >= value]

    return left_split, right_split

def calculate_entropy(data, target_attribute):
    target_classes = data[target_attribute].unique()
    n = data.shape[0]
    entropy = 0
    for target_class in target_classes:
        target_class_data = data[data[target_attribute] == target_class]
        target_class_probability = target_class_data.shape[0]/n
        entropy = entropy - (target_class_probability*math.log(target_class_probability, 2)) 
    return entropy

def calculate_mixed_weighted_entropy(left_split, right_split, target_attribute):
    left_split_entropy = calculate_entropy(left_split, target_attribute)
    right_split_entropy = calculate_entropy(right_split, target_attribute)
    n1 = left_split.shape[0]
    n2 = right_split.shape[0]
    n = n1 + n2
    mixed_weighted_entropy = ((n1/n)*left_split_entropy) + ((n2/n)*right_split_entropy) 
    return mixed_weighted_entropy

def find_best_one_rule(data, target_attribute):
    entropy = calculate_entropy(data, target_attribute)
    attributes = data.columns
    attributes = attributes[attributes!=target_attribute]
    information_gain = 0
    one_rule = ()
    for attribute in attributes:
        values = data[attribute].unique()
        for value in values:
            #split - left_split and right_split
            left_split, right_split = split_data(data, attribute, value)
            # print("{}->{} left_split_size:{} right_split_size:{}".format(attribute, value, left_split.shape[0], right_split.shape[0]))
            
            # calculate weighted entropy of split
            mixed_weighted_entropy = calculate_mixed_weighted_entropy(left_split, right_split, target_attribute)
            
            # calculate the information gain
            current_rule_information_gain = entropy-mixed_weighted_entropy
            if(current_rule_information_gain > information_gain):
                information_gain = current_rule_information_gain
                one_rule = (attribute, value)

    return one_rule

def check_if_stopping_criteria_met(data, target_attribute):
    n = data.shape[0]
    if(n<23):
        return True
    entropy = calculate_entropy(data, target_attribute):
    if(entropy <= 0.467)
    return False

def train(data, target_attribute):
    #if stopping criteria met 0.467 entr, depth 10, or n<23
    #   find majority class in the data and report it
    #else
    #find best one rule
    one_rule = find_best_one_rule(data, target_attribute)
    
    #report best one rule
    #recurse
            # remember attribute-value pair with max information gain
            # 
            # recurse            

if __name__ == "__main__":
    training_data_file = "DT_Data_CakeVsMuffin_v012_TRAIN_CLEAN.csv"
    colums_to_read = ['Flour_Binned', 'Sugar_Binned', 'Oils_Binned', 'Proteins_Binned', 'RecipeType']
    data = pd.read_csv(training_data_file, usecols=colums_to_read)
    target_attribute = 'RecipeType'
    train(data, target_attribute)