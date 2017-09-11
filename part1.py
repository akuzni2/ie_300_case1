


# ##### 1) Importing packages + importing the csv into a dataframe.

# In[2]:

import csv
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
main_data = pd.read_csv("FlightTime.csv")
main_data.head(2)


# In[3]:

# just taking a look at how the csv imported into the dataframe
main_data.head(1)


# ### destination = source.ix[start:end,['Column1','Column2'']]
# #### [ ] around column names make sure to keep index on the destination dataframe
# ####  this returns the slice of the data frame of specific columns and length

# ###### 2) Removing flight times that are below 230 min.

# In[4]:

main_data = main_data[main_data['Flight Time.1'] > 230]
main_data.info() ## checking to see types/numbers of variables


# ##### 3) Below acts on dataFrame "main_data" - removes rows that have missing values for "Arrival Time" and "Departure Time" . Found from google search "How to drop rows of Pandas DataFrame whose value in certain columns is NaN"

# In[5]:

main_data = main_data[pd.notnull(main_data['Arrival Time'])]
main_data = main_data[pd.notnull(main_data['Departure Time'])]


# ###### This tells me the length of my data set. The same information is shown above using "main_data.info()"

# In[6]:

len(main_data)


# ###### TFT = 0.117 ∗ d + .517*(L_ori − L_des) + 20
# ###### L_ori = longitude of the origin
# ###### L_des = longitude of destination
# ###### d = spherical distance between L_ori and L_des
# ##### given in the problem --> | L_ori = -87.90 degrees |  L_des = -118.41 degree | d = 1741.16 |

# In[7]:

lori = -87.90
ldes = -118.41
d = 1741.16
tft = 0.117*d + .517*(lori-ldes) + 20
print ("The total flight time calculated is: ",tft, "Minutes")


# In[8]:

dep_delay_mean = main_data['Departure Delay'].mean()
arr_delay_mean = main_data['Arrival Delay'].mean()


# In[9]:

total_delay = dep_delay_mean + arr_delay_mean
tft_minutes = tft + total_delay
print ("The total delay calculated is: ",total_delay, "Minutes")


# In[10]:

### doing a rough view of what I should see. I would have done something like this if I didn't use "groupby()" below.
### this is also what I would have done if I just used the csv package.
carriers_test = main_data.groupby('Carrier')
for key,data in carriers_test:
    print (key)
    print (data['Departure Time'].mean())


# In[11]:

# this sets the index to be "Carrier". Then I group which takes the unique values in the Index.
# Then I take the mean of each column that corresponds to the unique values in the index.
carriers = main_data.set_index('Carrier').groupby(level = 0).mean()
carriers


# In[12]:

extra_time_per_carrier = carriers['Flight Time.1'] - tft


# In[13]:

plt.style.use('seaborn-pastel')
extra_time_per_carrier.plot(kind = 'bar')
plt.ylabel('Time Added (Minutes)')
label_size = 10
plt.rcParams['xtick.labelsize'] = label_size
plt.rcParams['ytick.labelsize'] = label_size


# In[14]:

extra_time_per_carrier.to_csv('Case1_solution.csv', header = True)
