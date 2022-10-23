# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 10:40:30 2022

@author: User
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''import datasets'''
parsedate=['date']
ORDERS=pd.read_csv('C:\\Users\\User\\Documents\\Datascience\\rawdata\\Maven Analytics\\Pizza+Place+Sales\\pizza_sales\\orders.csv',parse_dates=parsedate)

ORDER_DETAILS=pd.read_csv('C:\\Users\\User\\Documents\\Datascience\\rawdata\\Maven Analytics\\Pizza+Place+Sales\\pizza_sales\\order_details.csv')

PIZZA=pd.read_csv('C:\\Users\\User\\Documents\\Datascience\\rawdata\\Maven Analytics\\Pizza+Place+Sales\\pizza_sales\\pizzas.csv')

PIZZA_TYPES=pd.read_csv('C:\\Users\\User\\Documents\\Datascience\\rawdata\\Maven Analytics\\Pizza+Place+Sales\\pizza_sales\\pizza_types.csv',encoding_errors='ignore')

'''duplicate tables and work with duplicates'''

orders=ORDERS
order_details=ORDER_DETAILS
pizza=PIZZA
pizza_types=PIZZA_TYPES

'''print and show heads of tables'''
print(orders.info())
print(order_details.info())
print(pizza.info())
print(pizza_types.info())

'''check for duplicate values'''

duplicate_orders= orders.duplicated()
print(orders[duplicate_orders])

duplicate_order_details=order_details.duplicated()
print(order_details[duplicate_order_details])

duplicate_pizza=pizza.duplicated()
print(pizza[duplicate_pizza])

duplicate_pizza_types=pizza_types.duplicated()
print(pizza_types[duplicate_pizza_types])  

#no duplicate entries

'''let's merge the tables on the required id'''

platos_pizza=orders.merge(order_details,how='inner',on='order_id').merge(pizza,how='inner',on='pizza_id').merge(pizza_types,how='inner',on='pizza_type_id')

print(platos_pizza.info())

'''checking for unique values'''

print(platos_pizza['category'].unique())

print(platos_pizza['size'].unique())

print(platos_pizza['name'].nunique())

print(platos_pizza['order_id'].nunique())

print(platos_pizza['order_details_id'].nunique())


print(platos_pizza['pizza_type_id'].nunique())


'''change the datatypes to the respective datatypes'''

platos_pizza[['order_id','order_details_id','pizza_id','pizza_type_id','category']]=platos_pizza[['order_id','order_details_id','pizza_id','pizza_type_id','category']].astype('category')

cat1=pd.CategoricalDtype(['S','M','L','XL','XXL'],ordered=True)
platos_pizza['size']=platos_pizza['size'].astype(cat1)

'''Adding the total sales and day of week column'''

platos_pizza['sales']=platos_pizza['quantity']*platos_pizza['price']

platos_pizza['day_of_week']=platos_pizza['date'].dt.day_name()


def pizza(size):
    if size=='S' or size=='M':
        return 1
    elif size=='L':
        return 2
    else:
        return 3

platos_pizza['guest_number']=platos_pizza['size'].apply(pizza)

print(platos_pizza['guest_number'].head())      
'''Adding a predicted number of guests'''

print(platos_pizza.info())

platos_pizza.to_csv('C:\\Users\\User\\Documents\\Datascience\\Cleaned data\\platos_pizza.csv')
#%%

'''getting a new table for ingredients used'''
platos_ingredients=platos_pizza[['order_id','order_details_id','date','time','sales','ingredients']]

print(platos_ingredients.info())

'''expand the ingredients columns to get each ingredent spread out in each order'''
print(platos_ingredients['ingredients'].head())


new_platos_ingredients=pd.DataFrame(platos_ingredients['ingredients'].str.split(',').to_list(),index=platos_ingredients['order_details_id']).stack()

new_platos_ingredients=new_platos_ingredients.reset_index(['order_details_id'])

new_platos_ingredients.columns=['order_details_id','each_ingredient']
print(new_platos_ingredients.head())
print(new_platos_ingredients.info())

# duplicate_ingredients=new_platos_ingredients.duplicated()
# print(new_platos_ingredients[duplicate_ingredients])

'''merging the two datafames'''
new_pizza_ingredients=platos_ingredients.merge(new_platos_ingredients,how='inner',on='order_details_id')
                                           
print(new_pizza_ingredients.info())


new_pizza_ingredients.to_csv('C:\\Users\\User\\Documents\\Datascience\\Cleaned data\\pizza_ingredients.csv')