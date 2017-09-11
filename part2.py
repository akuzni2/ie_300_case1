# In this file, data from FlightDelay.csv is used in a Naive Bayes classifier model to determine whether or not a flight will be delayed depending on its origin and destination.

import csv
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
flight_delay = pd.read_csv("FlightDelay.csv")
flight_delay.head(2)


delay = flight_delay['Departure Delay'].values
arrival = flight_delay['Arrival Delay'].values
total_delay = delay + arrival
flight_delay['Total Delay'] = total_delay
flight_delay.tail(2)
flight_delay['Classify Delay'] = np.where(flight_delay['Total Delay']>=15, 'Y', 'N')

#Just cleaning up the data
df = flight_delay.drop('Arrival Delay', 1)
df = df.drop('Departure Delay', 1)
df = df.drop('Total Delay', 1)
data_set = df

count_delay = data_set.groupby('Classify Delay').count()
count_delay

## getting p for number of carriers
carriers_array = data_set.set_index('Carrier').index.unique()
p_carrier = 1/len(carriers_array)

## getting p for number of origins
origin_array = data_set.set_index('Origin').index.unique()
p_origin = 1/len(origin_array)

## getting p for number of destinations
dest_array = data_set.set_index('Destination').index.unique()
p_dest = 1/len(dest_array)


num_yes = count_delay.iloc[1]['Carrier']
num_no = count_delay.iloc[0]['Carrier']
num_total = num_yes + num_no

P_y = num_yes/num_total
P_n = num_no/num_total

def flight_delay_prediction(origin_input,destination_input,carrier_input):

    specific_origin = data_set['Origin'] == origin_input
    no_delay = data_set['Classify Delay'] =='N'
    yes_delay = data_set['Classify Delay'] =='Y'

    # counting the number of non delayed flights, and number of delayed flights with specific origin
    number_of_N_origin = len(data_set[specific_origin & no_delay])
    number_of_Y_origin = len(data_set[specific_origin & yes_delay])

    #counting total number of flights from that origin
    number_of_flights_from_origin = number_of_N_origin + number_of_Y_origin

    specific_dest = data_set['Destination'] == destination_input
    no_delay_dest = data_set['Classify Delay'] =='N'
    yes_delay_dest = data_set['Classify Delay'] =='Y'

    # counting the number of non delayed flights, and number of delayed flights with specific destination
    number_of_N_dest = len(data_set[specific_dest & no_delay_dest])
    number_of_Y_dest = len(data_set[specific_dest & yes_delay_dest])

    #counting total number of flights from that origin
    number_of_flights_from_dest = number_of_N_dest + number_of_Y_dest

    specific_carrier = data_set['Carrier'] == carrier_input
    no_delay_carrier = data_set['Classify Delay'] =='N'
    yes_delay_carrier = data_set['Classify Delay'] =='Y'

    # counting the number of non delayed flights, and number of delayed flights with specific destination
    number_of_N_carrier = len(data_set[specific_carrier & no_delay_carrier])
    number_of_Y_carrier = len(data_set[specific_carrier & yes_delay_carrier])

    #counting total number of flights from that origin
    number_of_flights_from_carrier = number_of_N_carrier + number_of_Y_carrier


    # This calculates the probability of a delay
    P_YES_DELAY = (P_y*
                            (number_of_Y_origin + 3*p_origin)/(number_of_flights_from_origin + 3)*
                            (number_of_Y_dest + 3*p_dest)/(number_of_flights_from_dest + 3)*
                            (number_of_Y_carrier + 3*p_carrier)/(number_of_flights_from_carrier + 3))
    # This calculates the probability that there won't be a delay.
    P_NOT_DELAY = (P_n*
                            (number_of_N_origin + 3*p_origin)/(number_of_flights_from_origin + 3)*
                            (number_of_N_dest + 3*p_dest)/(number_of_flights_from_dest + 3)*
                            (number_of_N_carrier + 3*p_carrier)/(number_of_flights_from_carrier + 3))

    print("For flight: ", origin_input, "to ", destination_input, "on " , carrier_input)
    print("Probability of delay: ", P_YES_DELAY)
    print("Probability of no delay: ", P_NOT_DELAY)

    if P_NOT_DELAY > P_YES_DELAY:
        print("The Flight is Not Delayed")
    else:
        print("The Flight is Delayed")

    print("-------------------------------")


flight_delay_prediction("Test","LAS","AA")
