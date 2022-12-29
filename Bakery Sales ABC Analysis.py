#!/usr/bin/env python
# coding: utf-8

# #### Importing Libraries and reading file

# In[1]:


##Credits to the url below for base code on ABC function
"https://practicaldatascience.co.uk/data-science/how-to-create-an-abc-customer-segmentation-in-pandas"

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import calendar

# In[3]:


df = pd.read_csv("Bakery sales.csv")

# In[4]:


df = df.drop('Unnamed: 0',axis = 1)

# #### Renaming columns

# In[5]:


df.columns=['Date','Time','Ticket Number','Article','Quantity','Unit Price']

# #### Cleaning Price data

# In[6]:


df['Unit Price'] = df['Unit Price'].str.replace(' €','')
df['Unit Price'] = df['Unit Price'].str.replace(',','').astype('float')

# In[7]:


df['Line Price'] = df['Quantity']*df['Unit Price']

# #### Converting Date column to datetime type

# In[8]:


df['Month'] = pd.DatetimeIndex(df['Date']).month

df['Month Name'] = df['Month'].apply(lambda x: calendar.month_abbr[x])

# ### ABC ANALYSIS

# In[9]:


df_products = df.groupby('Article').agg(
    Quantity=('Quantity', 'sum'),
    Price=('Unit Price', 'mean'),
    Revenue=('Line Price', 'sum'),
    Ticket=('Ticket Number','count')
)

# In[10]:


df_products = df_products[df_products['Price'] > 0].round(2)

# In[11]:


df_products

# In[12]:


def abc (dataframe, ColumnForSegmentation, abc_class_name = 'class'):
    
    #Dataframe containing de data, ColumnForSegmentation are the values to use for ABC analysis, 
    #abc_class_name is to assign a name to the Segmentation column.
    
    def abc_segmentation(percentage):
        if 0 < percentage <= 80:
            return 'A' 
        #Segment A is between 0% to 80% including [0,80]
        elif 80 < percentage <= 95:
            return 'B' 
        #Segment B is between 80% not including and 95% including (80,95]
        else:
            return 'C'
        #Segment c is between 95% not including and 100% (95,100]
    
    data = dataframe.sort_values(by=ColumnForSegmentation, ascending=False) 
    #Sorts descending by column segmentation.
    
    data[ColumnForSegmentation+'_sum'] = data[ColumnForSegmentation].sum() 
    #Creates a new column with sum of column for segmentation
    
    data[ColumnForSegmentation+'_cumsum'] = data[ColumnForSegmentation].cumsum() 
    #Creates a new column with cumulative sum for segmentation column
    
    data[ColumnForSegmentation+'_running_pc'] = (data[ColumnForSegmentation+'_cumsum'] / data[ColumnForSegmentation+'_sum']) * 100
    #Creates a column with percentage of cumulative sum
    
    data[abc_class_name] = data[ColumnForSegmentation+'_running_pc'].apply(abc_segmentation)
    #Creates a column with name assigned at the beginning. Class name. 
    
    data[abc_class_name+'_rank'] = data[ColumnForSegmentation+'_running_pc'].rank().astype(int)
    #Creates a column with rank of the product in ABC. From 1 to n product.
    
    data.drop([ColumnForSegmentation+'_sum', ColumnForSegmentation+'_cumsum', ColumnForSegmentation+'_running_pc'], axis=1, inplace=True)
    #Deletes the Columns created for segmentation. Sum, cumulative sum and percentage calculator.
    
    return data

# In[13]:


df_segments = abc(df_products, 'Revenue','Segmentation')

# In[14]:


df_summary = df_segments.groupby('Segmentation').agg(
    Orders=('Ticket','mean'),
    Quantity=('Quantity', 'sum'),
    Price=('Price', 'mean'),
    Revenue=('Revenue', 'sum')
).reset_index()

#Summary for Segmentation

#Adding Metrics
df_summary['Average Quantity'] = df_summary['Quantity'] / df_summary['Orders']
df_summary['Average Revenue'] = df_summary['Revenue'] / df_summary['Orders']
df_summary['Percentage'] = df_summary['Revenue'] / df_summary['Revenue'].sum() *100
df_summary['Cumulative Percentage'] = df_summary['Revenue'].cumsum()/ df_summary['Revenue'].sum() *100

# In[15]:


df_summary=df_summary.round(2)

# #### Adding ABC analysis dataframe into first one

# In[16]:


df_merged = df.merge(df_segments, on=['Article'], how = 'inner')

# In[17]:


df_merged = df_merged.drop('Price',axis=1).drop('Revenue',axis=1).drop('Quantity_y',axis=1).drop('Ticket',axis=1)

# In[18]:


df_merged = df_merged.rename(columns = {'Line Price':'Revenue'})

# In[19]:


df_merged['Date'] = pd.to_datetime(df_merged['Date']) #Converting into Datetime type

# In[20]:


df_merged.head()

# # Visualizations

# ### Bar Chart for Pareto Analysis Analysis

# In[21]:


df_bars = pd.concat([df_summary['Segmentation'],df_summary['Revenue']],axis = 1)
df_bars['Revenue in Thousands of Euros'] = df_bars['Revenue']/1000
df_bars

# In[51]:


ay = sns.barplot(data=df_bars, x = 'Segmentation', y= 'Revenue in Thousands of Euros',palette = 'Greens_d')
for i in ay.containers:
    ay.bar_label(i,)

# In[39]:


pd.DataFrame(df_segments.Segmentation).count(axis=0)

# In[48]:


df_count = df_segments.groupby('Segmentation').agg(
    Frecuency=('Quantity', 'count')
).reset_index()
ax = sns.barplot(data=df_count,x = 'Segmentation', y='Frecuency',palette = 'Greens_d')
for i in ax.containers:
    ax.bar_label(i,)

# #### Revenue in time viz

# In[69]:


df_lines = pd.concat([df_merged['Date'],df_merged['Revenue'], df_merged['Segmentation']],axis= 1)

# In[70]:


sns.lineplot(data = df_lines, x='Date',y='Revenue',hue='Segmentation',estimator='sum')

# In[54]:


Table_A = df_segments[df_segments['Segmentation']=='A'].nlargest(5,'Revenue')
Table_B = df_segments[df_segments['Segmentation']=='B'].nlargest(5,'Revenue')
Table_C = df_segments[df_segments['Segmentation']=='C'].nlargest(5,'Revenue')

Table_ABC = pd.concat([Table_A,Table_B,Table_C])


# In[55]:


Table_ABC = Table_ABC.drop("Quantity",axis=1).drop("Price",axis=1).drop("Ticket",axis=1).drop("Segmentation_rank",axis=1)

# In[56]:


cm = sns.light_palette("green", as_cmap=True)

s = Table_ABC.style.background_gradient(cmap=cm)
s
