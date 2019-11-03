import pandas as pd
import numpy as np
import math
import pprint
import json

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

def check_if_stopping_criteria_met(data, target_attribute, depth):
    if(depth > 10):
        return True
    
    n = data.shape[0]
    if(n < 23):
        return True
    
    entropy = calculate_entropy(data, target_attribute)
    if(entropy <= 0.467):
        return True
    
    return False

def find_majority_class(data, target_attribute):
    target_classes = data[target_attribute].unique()
    majority_target_class_size = -999999
    majority_target_class = None
    for target_class in target_classes:
        target_class_data = data[data[target_attribute] == target_class]
        target_class_size = target_class_data.shape[0]
        if(target_class_size > majority_target_class_size):
            majority_target_class_size = target_class_size
            majority_target_class = target_class
    return majority_target_class

def train(data, target_attribute, depth, res, outfile):
    indent = "   " * (depth+1)
    #if stopping criteria met 0.467 entr, depth 10, or n<23
    stopping_criteria_met = check_if_stopping_criteria_met(data, target_attribute, depth)
    if(stopping_criteria_met):
        majority_target_class = find_majority_class(data, target_attribute)
        # print(majority_target_class)
        # print ("{}return {}".format(indent, majority_target_class))
        outfile.write("{}return {}\n".format(indent, majority_target_class))
        return majority_target_class
    #   find majority class in the data and report it
    else:
        #find best one rule
        one_rule = find_best_one_rule(data, target_attribute)
        left_split, right_split = split_data(data, one_rule[0], one_rule[1])
        #report best one rule
        # print(one_rule)
        # res_key = "{}-{}".format(one_rule[0], one_rule[1])
        res[one_rule] = {}
        #recurse
        # print ("{}if data[{}] < {}:".format(indent, one_rule[0], one_rule[1]))
        outfile.write("{}if row[{}] < {}:\n".format(indent, one_rule[0], one_rule[1]))
        res[one_rule]['<'] = train(left_split, target_attribute, depth+1, res, outfile)
        # print ("{}else:  # if data[{}] >= {}".format(indent, one_rule[0], one_rule))
        outfile.write("{}else:  # if row['{}'] >= {}\n".format(indent, one_rule[0], one_rule))
        res[one_rule]['>='] = train(right_split, target_attribute, depth+1, res, outfile)
        return res

def pretty(d, indent=0):
    for key, value in res.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))

if __name__ == "__main__":
    training_data_file = "DT_Data_CakeVsMuffin_v012_TRAIN_CLEAN.csv"
    # colums_to_read = ['Flour_Binned', 'Sugar_Binned', 'Oils_Binned', 'Proteins_Binned', 'RecipeType']
    # names = ['Flour', 'Sugar', 'Oils', 'Proteins', 'RecipeType']
    data = pd.read_csv(training_data_file)
    target_attribute = 'RecipeType'
    pp = pprint.PrettyPrinter(indent=4)
    # pretty(res)
    # print(json.dumps(res, indent=4))
    # print(pp.pprint(res))
    with open('dtree_porgram.py', 'a') as outfile:
        res = train(data, target_attribute, 0, {}, outfile)
        