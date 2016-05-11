"""
Team: Cluster and Cloud Computing Team 3
Contents: Assigment 2
Authors: Kimple Ke, Roger Li, Fei Tang, Bofan Jin, David Ye
"""
# SLA Module
import csv
import math

postcodes = list(csv.reader(open("./data/postcodes.csv")))
sla = list(csv.reader(open("./data/sla.csv"), delimiter='\t'))


def find_postcode(longitude, latitude):
    """
    Given a longitude and latitude, returns the postcode as a string.
    """
    
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
    

def find_postcodes(longitude, latitude):
    """
    Given a longitude and latitude, returns a list of postcodes as a string.
    """
    
    distance = 10000
    postcode_results = []
    
    for p in postcodes:
        temp = math.sqrt(((float(p[4]) - longitude) ** 2) + \
        ((float(p[3]) - latitude) ** 2)) 
        
        if round(temp, 3) < (round(distance, 3) - 1.0):
            postcode_results = [p[0]]
            distance = temp
        elif not (round(temp, 3) > round(distance, 3)):
            postcode_results.append(p[0])
            distance = temp
            
    return postcode_results
    

def find_sla(longitude, latitude):
    """
    Given a longitude and latitude, returns the statisical local area (SLA) 
    as a string.
    """
    
    postcode_results = find_postcodes(longitude, latitude)
    result = -1
    
    # print postcode_results
    
    for p in postcode_results:
        for s in sla:
            if s[0] == p[1:-1]:
                result = s[1]
                
    return result