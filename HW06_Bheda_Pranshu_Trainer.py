#Pranshu Bheda ..... HW06
import pandas as pd
import numpy as np

def find_best_one_rule(data):
    #get all the attributes of the data
    attributes = data.columns()
    #for each attribute except target atttribute calculate
    #the badness of the split
    for attribute in attributes:
        

def train(data, target_attribute):
    print("Train dtree for {}".format(target_attribute))
    #if stopping criteria met??
        #return majority value of target_attribute
    #else
        #find one best one rule
        #record best one rule
        #split into left and right
        #recurse for left and right

    # attributes = data.columns()

if __name__ == "__main__":
    training_data_file = "DT_Data_CakeVsMuffin_v012_TRAIN_CLEAN.csv"
    data = pd.read_csv(training_data_file)
    print(data)

    train(data)