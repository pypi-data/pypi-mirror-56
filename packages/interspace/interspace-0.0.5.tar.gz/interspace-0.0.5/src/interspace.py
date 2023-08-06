import numpy as np

# calculate the Euclidean distance between two vectors
def euclidean(vector_1, vector_2):
    distance = 0.0
    for i in range(len(vector_1)):
            distance += (vector_1[i] - vector_2[i])**2 
    return (distance)**0.5

def minkowski(vector_1, vector_2, p=1):
    distance = 0.0
    for i in range(len(vector_1)):
            distance += (vector_1[i] - vector_2[i])**p
    return (distance)**(1.0/p)

def cosine_similarity(vector_1, vector_2):
    return np.dot(vector_1, vector_2) / ((np.sqrt(np.dot(vector_1, vector_1)) * np.sqrt(np.dot(vector_2, vector_2))))

def distance(vector_1, vector_2, p=1):
    if len(vector_1) != len(vector_2):
        return "Vector lengths mismatch"
    
    distances = {}
    
    distances['Euclidean'] = euclidean(vector_1, vector_2)
    distances[str('Minkowski-')+str(p)] = minkowski(vector_1, vector_2, p=p)
    distances['Cosine Similarity'] = cosine_similarity(vector_1, vector_2)

        
    return distances