import numpy as np
import math
from multiprocessing import Pool
from tqdm import tqdm


# generate candidate values
def convert_num2list(num):
    return [int(x) for x in str(num)]

def check_duplication(number):
    if len(number) < 3:
        return False
    elif len(number) == 3:
        number.insert(0,0)
    if (len(number) != len(set(number))):
        return False
    return True

all_numbers = [convert_num2list(x) for x in range(123,10000)]
all_numbers = [x for x in all_numbers if check_duplication(x)]

all_HB = [
    (0,0), (0,1), (0,2), (0,3), (0,4),
    (1,0), (1,1), (1,2), (1,3),
    (2,0), (2,1), (2,2), (3, 0), (4,0)
]

# calculate hit and blow
def calcH(x, y):
    return sum([x[i]==y[i] for i in range(4)])

def calcB(x, y):
    return sum([(x_i in y) for x_i in x]) - calcH(x, y)

def calcHB(x, y):
    return (calcH(x, y), calcB(x, y))

# calculate candidate values
def calcHBX(x, h, b):
    return [y for y in all_numbers if calcHB(x, y) == (h, b)]

# calculate distribution
def calc_distribution(x):
    return [calcHBX(x, h, b) for (h, b) in all_HB]

# set binary operation
def intersect_list(l1, l2):
    return [x for x in l1 if x in l2]

def intersect_all(ll):
    res = all_numbers
    for l in ll:
        res = intersect_list(res, l)
    return res

def prod_distribution(dist1, dist2):
    ret = []
    for l1 in dist1:
        ret += [intersect_list(l1, l2) for l2 in dist2]
    return ret

# calculate entropy
def selected_entropy(p):
    return -p * math.log(p, 2) if p != 0 else 0

def total_entropy(dist):
    return sum([selected_entropy(len(d)/5040) for d in dist])

def entropy(dist):
    if len(dist) == 0:
        return 0
    size = sum([len(d) for d in dist])
    return sum([selected_entropy(len(d)/size) for d in dist])
