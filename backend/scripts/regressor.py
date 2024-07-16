import pandas as pd
from sklearn.model_selection import  train_test_split
from sklearn.preprocessing import LabelEncoder as le
from sklearn.tree import DecisionTreeRegressor as dtr
from sklearn.feature_selection import RFE
from datetime import datetime
import json 
import sys
import argparse

'''
    THIS IS THE MAIN CODE FRAME WHICH PREDICTS THE MAINTENANCE COST AND NUMBER OF DAYS LEFT FOR NEXT MAINTENANCE
    SAMPLE DICT ARG:
        dict={
            'asset_id':[1],
            'asset_name':[4],
            'asset_type':[1],
            'manufacturer':[3],
            'cost':[8716],'location':[2],
            'department':[1],
            'asset_status':[0],
            'assigned_to':[2], 
            'days_from_purchase':[3415.24495],
            'days_to_warranty_expiry':[661.2807] 
        }

    FOR THE VALUES, REFER value_counts.txt
'''


class ITgpt:
    def __init__(self):
        self.data = pd.read_csv('scripts/ITAM dataset.csv')
        self.model = dtr()
        self.enc = le()
        self.rfe = RFE(self.model, n_features_to_select=5)
        self.dict = None
        self.fit = None
        self.__start__()
    
    #PREPROCESSOR
    def __start__(self):
        cols = ['asset_type','asset_name','assigned_to',  'manufacturer', 'location', 'department', 'asset_status']
        for i in cols:
            self.data[i] = self.enc.fit_transform(self.data[i])
        
        self.data['purchase_date'] = pd.to_datetime(self.data['purchase_date'])
        self.data['warranty_expiry_date'] = pd.to_datetime(self.data['warranty_expiry_date'])
        self.data['days_from_purchase'] = (datetime.now() - self.data['purchase_date']).dt.days
        self.data['days_to_warranty_expiry'] = (self.data['warranty_expiry_date'] - datetime.now()).dt.days
        self.data['next_maintenance_date'] = pd.to_datetime(self.data['next_maintenance_date'])
        self.data['days_to_next_maintenance'] = (self.data['next_maintenance_date'] - datetime.now()).dt.days

        cols = ['purchase_date','warranty_expiry_date', 'next_maintenance_date','serial_number','model_number']
        for i in cols:
            del self.data[i]

    #MODEL TRAINER
    def  __next_maintenance__(self):
        y = self.data[['days_to_next_maintenance']]
        x = self.data.drop(['days_to_next_maintenance', 'maintenance_cost'], axis=1)
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8)
        self.fit = self.rfe.fit(x_train, y_train)
    
    def  next_maintenance(self, dict):
        self.dict = pd.DataFrame(dict)
        self.__next_maintenance__()
        arr = self.fit.predict(self.dict)
        return arr[0]
    
    #MODEL TRAINER
    def  __maintenance_cost__(self):
        y = self.data[['maintenance_cost']]
        x = self.data.drop(['days_to_next_maintenance', 'maintenance_cost'], axis=1)
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8)
        self.fit = self.rfe.fit(x_train, y_train)
    
    def  maintenance_cost(self, dict):
        self.dict = pd.DataFrame(dict)
        self.__maintenance_cost__()
        arr = self.fit.predict(self.dict)
        return arr[0]

ai = ITgpt()
def main(target, dict):
    dict = json.loads(dict)
    if target == 'cost':
        result = ai.maintenance_cost(dict)
    else:
        result = ai.next_maintenance(dict)
    print(result)

target = sys.argv[1]
dict = sys.argv[2]
main(target, dict)
# print(dict)