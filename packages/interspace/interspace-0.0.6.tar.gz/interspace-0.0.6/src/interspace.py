import numpy as np
import math

def haversine(coord1, coord2, R = 6372800):
    '''
    Important to note is that we have to take the radians of the longitude and latitude values.
    R  corresponds to Earths mean radius in meters (6372800)
    '''
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

def manhattan(vector_1, vector_2):
    return minkowski(vector_1, vector_2, p=1)

def euclidean(vector_1, vector_2):
    return minkowski(vector_1, vector_2, p=2)


def minkowski(vector_1, vector_2, p=1):
    distance = 0.0
    for i in range(len(vector_1)):
            distance += (vector_1[i] - vector_2[i])**p
    return (distance)**(1.0/p)

def cosine_similarity(vector_1, vector_2):
    num = np.dot(vector_1, vector_2)
    den = (np.sqrt(np.dot(vector_1, vector_1)) * np.sqrt(np.dot(vector_2, vector_2)))
    return num / den
