"""
Team: Cluster and Cloud Computing Team 3
Contents: Assigment 2
Authors: Kimple Ke, Roger Li, Fei Tang, Bofan Jin, David Ye
"""

import csv
import math

postcodes = list(csv.reader(open("postcodes.csv")))
sla = list(csv.reader(open("sla.csv"), delimiter='\t'))

"""
Given a longitude and latitude, returns the postcode as a string.
"""
def find_postcode(longitude, latitude):
    
    distance = -1
    postcode = -1
    
    for p in postcodes:
        temp = math.sqrt(((float(p[4]) - longitude) ** 2) + \
        ((float(p[3]) - latitude) ** 2)) 
        if distance == -1:
            postcode = p[0]
            distance = temp
        else:
            if temp < distance:
                postcode = p[0]
                distance = temp
    return postcode[1:-1]
    
"""
Given a longitude and latitude, returns the statisical local area (SLA) 
as a string.
"""
def find_sla(longitude, latitude):
    
    postcode = find_postcode(longitude, latitude)
    result = -1
    
    for s in sla:
        if s[0] == postcode:
            result = s[1]
            
    return result
