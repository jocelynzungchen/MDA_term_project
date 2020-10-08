
# data object
class Row:
    def __init__(self, product, user):
        self.product = product
        self.user    = user

###### Convert Row list to baskets ##########

# key : user
# value : [product]
def user_basket_mapper(row):
    return (row.user, [row.product])

# key : product
# value : [user]
def product_basket_mapper(row):
    return (row.product, [row.user])

# append the value to a list for given key
def basket_reducer(acum, v):
    if acum != None:
        # basket represents non-duplicate set (same item appears multiple times in same basket only count once)
        if v[0] not in acum:
            acum.append(v[0])
        return acum
    else:
        return [v[0]]


############ count the basket ############

def counter_mapper(item):
    return (item, 1)

def counter_reducer(acum, v):
    return acum+v

############# generate frequent items ###############

from collections import Counter

# pass in basket (key - basket, value - list of items) and get the frequent items
def freq_items(basket, min_support):
    flatten = [item for items in basket.values() for item in items]
    item_counts = Counter(flatten)
    item_counts = {k: v for k, v in item_counts.items() if v >= min_support}
    return item_counts, item_counts.keys()

############## frequent pairs ##################

def pairs(lst):
    ind = 1
    pair_set = set()
    for left in lst:
        # non-duplicate -> start from after the left elem
        for right in lst[ind:]:
            pair_set.add((left, right))
        ind += 1

    return pair_set

def freq_pairs(possible_pairs, basket, min_support):
    
    pair_counts = dict()
    
    for items in basket.values():
#         print('items', items)
#         print('pairs', pairs(items))
        for pair in pairs(items):
            if pair in possible_pairs:
                if pair not in pair_counts:
                    pair_counts.update({pair:1})
                else:
                    pair_counts[pair] += 1
            elif (pair[1], pair[0]) in possible_pairs:
                pair2 = (pair[1], pair[0])
#                 print('hello', pair2)
                if pair2 not in pair_counts:
                    pair_counts.update({pair2:1})
                else:
                    pair_counts[pair2] += 1
    
    pair_counts = {k: v for k, v in pair_counts.items() if v >= min_support}
    return pair_counts
