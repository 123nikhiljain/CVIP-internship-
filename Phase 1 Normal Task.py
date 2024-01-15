#!/usr/bin/env python
# coding: utf-8

# # Phase 1 Normal Task
# 

# # Analyze customer behavior based on transaction data

# In[1]:


import pandas as pd # Importing Pandas library for data manipulation and analysis
import matplotlib.pyplot as plt # Importing Matplotlib library for data visualization
import seaborn as sns #Importing Seaborn library for statistical data visualization
import numpy as np # Importing NumPy library for numerical computations and arrays


# In[2]:


# Reading the data from a CSV file named 'Hackathon_Working_Data.csv' into a DataFrame called 'df'
df= pd.read_csv('Hackathon_Working_Data.csv')


# In[3]:


df


# In[4]:


# Display the first few rows of the DataFrame 'df'
df.head()


# In[5]:


# Displaying the column labels of the DataFrame 'df'
df.columns


# In[6]:


# Retrieving unique values in the 'STORECODE' column of the DataFrame 'df'
df['STORECODE'].unique()


# In[7]:


# Retrieve unique values in the 'MONTH' column of the DataFrame
df['MONTH'].unique()


# In[8]:


# Displaying concise summary information about the DataFrame 'df'
# This includes the index dtype, column data types, non-null values, and memory usage.
df.info()


# In[9]:


# Checking for missing values in each column of the DataFrame 'df'
df.isnull().sum()


# In[10]:


# This line generates descriptive statistics of the DataFrame 'df', including count, mean, std deviation, min, 25th percentile,
# median (50th percentile), 75th percentile, and max for numeric columns.
df.describe()


# # Sales by Store Analysis

# In[11]:


# Creating a new column 'Unique_ID' by combining 'Bill_ID' and 'Storecode'
df['UNIQUE_ID']= df['STORECODE']+'_'+df['BILL_ID']


# In[12]:


# Grouping the DataFrame 'df' by the unique identifier 'UNIQUE_ID'
# and calculating the mean values for specific columns ('DAY', 'BILL_AMT', 'QTY') within each group.

# Grouping by 'UNIQUE_ID' and computing the mean values for the columns
by_store = df.groupby("UNIQUE_ID").mean()[["DAY", "BILL_AMT", "QTY"]]


# In[13]:


by_store


# In[14]:


# Merging the original DataFrame 'df' with the aggregated DataFrame 'by_store' based on the shared column 'UNIQUE_ID'.

# Using the pd.merge() function to combine data from 'df' and 'by_store' on the column 'UNIQUE_ID'
merged_df = pd.merge(df,by_store,on="UNIQUE_ID")


# In[15]:


merged_df.head()


# In[16]:


# Removing columns 'DAY_x' and 'BILL_AMT_x' from the merged DataFrame 'merged_df'
merged_by= merged_df.drop(['DAY_x','BILL_AMT_x'],axis=1)


# In[17]:


merged_by


# In[18]:


# Grouping the 'merged_df' DataFrame by the unique identifier 'UNIQUE_ID' and calculating the mean values for specific columns ('DAY_y', 'BILL_AMT_y') within each group.

# Grouping by 'UNIQUE_ID' and computing the mean values for the columns 'DAY_y' and 'BILL_AMT_y'
unique_sales=merged_df.groupby('UNIQUE_ID', as_index=True).mean()[["DAY_y","BILL_AMT_y"]]


# In[19]:


unique_sales


# Let's start by finding out what are the total sales by store.

# In[20]:


# Extracting the 'STORE' information from the index of the 'unique_sales' DataFrame and creating a new column 'STORE' based on this extracted information.

# Using the index of the DataFrame to extract the portion before the '_' character
# This operation assumes that the index values follow a 'STORE_BILL_ID' format, extracting 'STORE' part.
unique_sales['STORE']=unique_sales.index.str.split('_').str[0]


# In[21]:


unique_sales


# In[22]:


# Grouping the 'unique_sales' DataFrame by 'STORE' and calculating the total sales for each store.
# Sorting stores by total sales in descending order.
sales_by_store = unique_sales.groupby("STORE").sum().sort_values('BILL_AMT_y', ascending=False)

# Creating a new figure for the plot with a specific size (20x10 inches)
plt.figure(figsize=(20, 10))

# Creating a bar plot using Seaborn to visualize total sales by store
sns.barplot(x=sales_by_store.index, y=sales_by_store['BILL_AMT_y'], data=sales_by_store)

# Adding a title, x-axis label, and y-axis label to the plot
plt.title("Total Sales by Store")
plt.xlabel("Store")
plt.ylabel("Sales")

# Adding grid lines along the y-axis in black color for better readability
plt.grid(axis='y', color='black')


# In[23]:


# Creating a new figure for the plot with a specific size (20x10 inches)
plt.figure(figsize=(20, 10))

# Creating a box plot using Seaborn to visualize the variability of sales by store
sns.boxplot(x=df["STORECODE"], y=df["BILL_AMT"], data=df)

# Adding a title, y-axis label, and x-axis label to the plot
plt.title("Variability of Sales by Store")
plt.ylabel("Sales")
plt.xlabel("Store")

# Displaying the box plot
plt.show()


# # What are the daily sales by Store?

# In[24]:


# Iterating through each unique store in the 'unique_sales' DataFrame
for i in unique_sales.STORE.unique():
    # Filtering the 'unique_sales' DataFrame for the current store ('i') and aggregating total sales per day
    store = unique_sales.loc[unique_sales.STORE == i].groupby("DAY_y").sum()
    
    # Creating a new figure for each store's bar plot with a specific size (20x5 inches)
    plt.figure(figsize=(20, 5))
    
    # Generating a bar plot for total sales per day for the current store
    # Adding a horizontal line representing the mean total sales across days for the store
    sns.barplot(x=store.index, y=store["BILL_AMT_y"], data=store).axhline(store["BILL_AMT_y"].mean(), color='purple')
    
    # Setting the title, x-axis label, and y-axis label for the plot
    plt.title("Total Sales from Store: " + i)
    plt.xlabel("Day")
    plt.ylabel("Total Sales")
    
    # Adding horizontal grid lines for better readability along the y-axis
    plt.grid(axis='y', color='black')


# In[25]:


# Iterate over unique store IDs
for store_id in unique_sales['STORE'].unique():
    
    # Filter data for the current store and group by day
    store_data = unique_sales.loc[unique_sales['STORE'] == store_id].groupby("DAY_y").sum()
    
    # Create a new figure for each store
    plt.figure(figsize=(20, 5))
    
    # Create a bar plot for total sales per day
    sns.barplot(x=store_data.index, y=store_data["BILL_AMT_y"], data=store_data)
    
    # Add a horizontal line for the mean total sales
    plt.axhline(store_data["BILL_AMT_y"].mean(), color='purple', linestyle='dashed', linewidth=2)
    
    # Add title and labels
    plt.title('Total Sales from Store: ' + store_id)
    plt.xlabel('Day')
    plt.ylabel('Total Sales')
    
    # Add grid lines for better readability
    plt.grid(axis='y', color='black')
    
    # Display the plot
    plt.show()


# # Which category sells the most items in general and by store?

# In[26]:


# Group by 'GRP' and sum values, then sort in descending order by 'VALUE'
top_items_sales = merged_df.groupby('GRP').sum().sort_values('VALUE', ascending=False)[['QTY_x', 'PRICE', 'VALUE']][:25]

# Create a bar plot for the top 25 categories based on 'VALUE'
plt.figure(figsize=(12, 8))
sns.barplot(x='VALUE', y=top_items_sales.index, data=top_items_sales)

# Add title and labels
plt.title('Sales from Top 25 Categories')
plt.xlabel('Sales')
plt.ylabel('Categories')

# Add grid lines for better readability
plt.grid(axis='y', color='black')

# Display the plot
plt.show()


# In[27]:


# Group by 'GRP', sum values, and sort in descending order by 'QTY_x'
top_items = merged_df.groupby('GRP').sum().sort_values('QTY_x', ascending=False)[['QTY_x', 'PRICE']][:25]

# Create a bar plot for the top 25 categories based on 'QTY_x'
plt.figure(figsize=(12, 8))
sns.barplot(x='QTY_x', y=top_items.index, data=top_items)

# Add title and labels
plt.title('Number of Units Sold by Top 25 Categories')
plt.xlabel('Number of Units')
plt.ylabel('Categories')

# Add grid lines for better readability
plt.grid(axis='x', color='black')

# Display the plot
plt.show()


# In[28]:


# Group by 'GRP', sum values, and sort in descending order by 'QTY_x'
top_items = merged_df.groupby('GRP').sum().sort_values('QTY_x', ascending=False)[['QTY_x', 'PRICE']][:25]

# Create a bar plot for the top 25 categories based on 'QTY_x'
plt.figure(figsize=(12, 8))
sns.barplot(x='QTY_x', y=top_items.index, data=top_items)

# Add title and labels
plt.title('Number of Units Sold by Top 25 Categories')
plt.xlabel('Number of Units')
plt.ylabel('Categories')

# Add grid lines for better readability
plt.grid(axis='x', color='black')

# Display the plot
plt.show()


# In[29]:


# Iterate over unique store codes
for store_code in merged_df['STORECODE'].unique():
    # Filter data for the current store code and group by 'GRP', sum values, and sort by 'VALUE'
    top_categories = merged_df.loc[merged_df['STORECODE'] == store_code].groupby('GRP').sum().sort_values('VALUE', ascending=False)[['VALUE', 'QTY_x']][:25]

    # Create a bar plot for the top 25 categories based on 'VALUE'
    plt.figure(figsize=(20, 5))
    sns.barplot(x='VALUE', y=top_categories.index, data=top_categories)

    # Add title and labels
    plt.title(f'Top 25 Categories by Sales from store: {store_code}')
    plt.xlabel('Sales')
    plt.ylabel('Categories')

    # Show the plot
    plt.show()


# In[30]:


# Group by 'GRP', calculate mean, and sort in descending order by 'PRICE'
grp_per_price = merged_df.groupby('GRP').mean().sort_values('PRICE', ascending=False)[['PRICE', 'QTY_x']][:25]

# Create a bar plot for the 25 most expensive categories based on 'PRICE'
plt.figure(figsize=(12, 8))
sns.barplot(x='PRICE', y=grp_per_price.index, data=grp_per_price)

# Add title and labels
plt.title('25 Most Expensive Categories')
plt.ylabel('Category')
plt.xlabel('Average Price')

# Add grid lines for better readability
plt.grid(axis='x', color='black')

# Show the plot
plt.show()


# In[31]:


# grp_per_price =merged_df.groupby('GRP').mean().sort_values('PRICE',ascending=False)[['PRICE','QTY_x']][0:25]
# plt.figure(figsize=(12,8))
# sns.barplot(x='PRICE',y=grp_per_price.index,data=grp_per_price)
# plt.title('25 Most Expensive Categories')
# plt.ylabel('Category')
# plt.xlabel('Average Price')
# plt.grid(axis='x',color='black')


# In[32]:


# Group by 'GRP', calculate mean, and sort in ascending order by 'PRICE'
grp_per_price2 = merged_df.groupby('GRP').mean().sort_values('PRICE', ascending=True)[['PRICE', 'QTY_x']][:25]

# Create a bar plot for the 25 least expensive categories based on 'PRICE'
plt.figure(figsize=(12, 8))
sns.barplot(x='PRICE', y=grp_per_price2.index, data=grp_per_price2)

# Add title and labels
plt.title('25 Least Expensive Categories')
plt.ylabel('Category')
plt.xlabel('Average Price')

# Add grid lines for better readability
plt.grid(axis='x', color='black')

# Show the plot
plt.show()


# # Which Brands sell more by dollars and by units

# In[33]:


# Group by 'BRD', sum values, and sort in descending order by 'VALUE'
brands_v = merged_df.groupby('BRD').sum().sort_values('VALUE', ascending=False)[['VALUE', 'QTY_x']][:25]

# Create a bar plot for the top 25 brands based on 'VALUE'
plt.figure(figsize=(12, 8))
sns.barplot(x='VALUE', y=brands_v.index, data=brands_v)

# Add title and labels
plt.title('Top 25 Brands by Sales')
plt.xlabel('Sales')
plt.ylabel('Brands')

# Add grid lines for better readability
plt.grid(axis='x', color='black')

# Show the plot
plt.show()


# In[34]:


# Group by 'BRD', sum values, and sort in descending order by 'QTY_x'
brands_q = merged_df.groupby('BRD').sum().sort_values('QTY_x', ascending=False)[['VALUE', 'QTY_x']][:25]

# Create a bar plot for the top 25 brands based on 'QTY_x'
plt.figure(figsize=(12, 8))
sns.barplot(x='QTY_x', y=brands_q.index, data=brands_q)

# Add title and labels
plt.title('Top 25 Brands by Units Sold')
plt.xlabel('Number of Units')
plt.ylabel('Brands')

# Add grid lines for better readability
plt.grid(axis='x', color='black')

# Show the plot
plt.show()


# # Brand analysis by store
# 

# In[35]:


# Create a figure outside the loop to avoid creating a new figure for each store
plt.figure(figsize=(12, 8))

# Iterate over unique store codes
for store_code in merged_df['STORECODE'].unique():
    # Filter data for the current store code and group by 'BRD', sum values, and sort by 'VALUE'
    brd_st = merged_df.loc[merged_df['STORECODE'] == store_code]
    brd = brd_st.groupby('BRD').sum().sort_values('VALUE', ascending=False)[['VALUE', 'QTY_x']][:25]

    # Create a bar plot for the top 25 brands by sales for the current store
    sns.barplot(x='VALUE', y=brd.index, data=brd)

    # Add title and labels
    plt.title(f'Top 25 Brands by Sales from store: {store_code}')
    plt.xlabel('Sales')
    plt.ylabel('Brands')

    # Add grid lines for better readability
    plt.grid(axis='x', color='black')

    # Show the plot
    plt.show


# In[36]:


# Create a figure outside the loop to avoid creating a new figure for each store
plt.figure(figsize=(12, 8))

# Iterate over unique store codes
for store_code in merged_df['STORECODE'].unique():
    # Filter data for the current store code and group by 'BRD', sum values, and sort by 'QTY_x'
    brd_st = merged_df.loc[merged_df['STORECODE'] == store_code]
    brd = brd_st.groupby('BRD').sum().sort_values('QTY_x', ascending=False)[['VALUE', 'QTY_x']][:25]

    # Create a bar plot for the top 25 brands by units sold for the current store
    sns.barplot(x='QTY_x', y=brd.index, data=brd)

    # Add title and labels
    plt.title(f'Top 25 Brands by Units Sold from store: {store_code}')
    plt.xlabel('Number of Units')
    plt.ylabel('Brands')

    # Add grid lines for better readability
    plt.grid(axis='x', color='black')

    # Show the plot
    plt.show()


# # Which Store Sells More Units

# In[37]:


# Group by 'UNIQUE_ID', sum the quantities and prices
store_qty = merged_df.groupby("UNIQUE_ID").sum()[['QTY_x', 'PRICE']]

# Extract 'STORE' information from 'UNIQUE_ID' and set it as a new column
store_qty['STORE'] = store_qty.index.str.split('_').str[0]

# Display the resulting DataFrame
store_qty


# In[38]:


# Group by 'STORE', sum the quantities, and sort in descending order by 'QTY_x'
units_by_store = store_qty.groupby('STORE').sum().sort_values('QTY_x', ascending=False)

# Create a bar plot for the quantity of items sold by store
plt.figure(figsize=(12, 8))
sns.barplot(x=units_by_store.index, y=units_by_store['QTY_x'], data=units_by_store)

# Add title and labels
plt.title('Quantity of Items Sold by Store')
plt.xlabel('Stores')
plt.ylabel('Units')

# Add grid lines for better readability
plt.grid(axis='x', color='black')

# Show the plot
plt.show()


# In[39]:


# Group by 'STORECODE' and count the number of unique brands ('BRD') for each store
str_brd = df.groupby('STORECODE')['BRD'].nunique().sort_values(ascending=False)

# The resulting 'str_brd' is a Pandas Series where the index is 'STORECODE'
# and the values are the count of unique brands for each store code.



# In[40]:


str_brd


# # Sales by Month

# In[41]:


month_info = merged_df[['MONTH',"UNIQUE_ID"]]


# In[42]:


month_info 


# In[43]:


# Merge the 'month_info' and 'unique_sales' DataFrames on the common column 'UNIQUE_ID'
monthly_sales = pd.merge(month_info, unique_sales, on="UNIQUE_ID")

# The resulting DataFrame 'monthly_sales' contains the information from both DataFrames
# with matching 'UNIQUE_ID' values.




# In[44]:


# Add a new column 'N_MONTH' to the 'monthly_sales' DataFrame
# Extract the second character from the 'MONTH' column using a lambda function
monthly_sales['N_MONTH'] = monthly_sales['MONTH'].apply(lambda x: x[1])

# The resulting DataFrame now contains the new column 'N_MONTH',
# representing the second character of each value in the 'MONTH' column.


# In[45]:


monthly_sales


# In[46]:


monthly_sales=monthly_sales.drop('MONTH',axis=1)
monthly_sales


# In[47]:


# Convert the values in the 'N_MONTH' column to numeric type
monthly_sales['N_MONTH'] = pd.to_numeric(monthly_sales['N_MONTH'])

# The 'N_MONTH' column now contains numeric values, making it suitable for numerical operations.


# In[48]:


month_uq=monthly_sales.groupby("UNIQUE_ID").mean()


# In[49]:


month_uq


# In[50]:


# Group by 'N_MONTH' and calculate the sum of total sales ('BILL_AMT_y') for each month
m_sales = month_uq.groupby('N_MONTH').sum()

# Create a bar plot for total sales by month
plt.figure(figsize=(20, 10))
sns.barplot(x=m_sales.index, y='BILL_AMT_y', data=m_sales)

# Add title and labels
plt.title('Total Sales by Month')
plt.xlabel('Month')
plt.ylabel('Sales')

# Add grid lines for better readability
plt.grid(axis='y', color='black')

# Show the plot
plt.show()

