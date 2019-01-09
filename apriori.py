import os
import sys
from itertools import chain, combinations
from collections import defaultdict

def get_dataIter(fname):
    with open(fname, 'r') as fp:
        for line in fp:
            line = line.rstrip('\n')
            line = line.rstrip('\r')
            transaction = frozenset(line.split(','))
            yield transaction

def get_itemSet_and_transactionList(dataIter):
    transactionList = list()
    itemSet = set()

    for transaction in dataIter:
        transactionList.append(transaction)
        for item in transaction:
            # Create set of set, later will iter itemSet to get single set
            itemSet.add(frozenset([item]))

    # print(itemSet)
    # print(transactionList)
    return itemSet, transactionList

def get_items_with_minSupport(itemSet, transactionList, minSup, freqSet):

    returnSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, times in localSet.items():
        sup = float(times) / len(transactionList)
        if sup >= minSup:
            returnSet.add(item)

    # print(returnSet)
    return returnSet

def get_jointSet(itemSet, length):
    jointSet = set()

    for i in itemSet:
        for j in itemSet:
            tmp = i.union(j)
            if len(tmp) == length:
                jointSet.add(tmp)

    # print(jointSet)
    return jointSet


def do_aprior(dataIter, minSup, minCon):

    itemSet, transactionList = get_itemSet_and_transactionList(dataIter)

    freqSet = defaultdict(int)
    largeSet = dict()
    initCSet = get_items_with_minSupport(itemSet,
                                         transactionList,
                                         minSup,
                                         freqSet)

    nowLSet = initCSet
    k = 2
    while not not nowLSet:
        largeSet[k-1] = nowLSet
        nowLSet = get_jointSet(nowLSet, k)
        nowCSet = get_items_with_minSupport(nowLSet,
                                            transactionList,
                                            minSup,
                                            freqSet)

        nowLSet = nowCSet
        # print('now k = %d' % (k) )
        k += 1
    # end of while

    get_support = lambda item: float(freqSet[item]) / len(transactionList)
    get_subset  = lambda arr: chain(*[combinations(arr, i + 1) for i, _ in enumerate(arr)])

    associateRules = []
    finalItemSet = []
    for k, currentSet in list(largeSet.items())[1:]:
        for item in currentSet:

            # append item
            tmp = (tuple(item), get_support(item))
            finalItemSet.extend( [(tuple(item), get_support(item))] )

            # append rule
            subsets = map(frozenset, [x for x in get_subset(item)])
            for element in subsets:
                remain = item.difference(element)
                if len(remain) == 0:
                    continue
                confidence = freqSet[item] * 1.0 / freqSet[element]
                if confidence >= minCon:
                    tmp = (tuple(element), tuple(remain))
                    tmp = (tmp, confidence)
                    associateRules.append(tmp)

    return finalItemSet, associateRules

def print_result(items, rules):
    n = 0
    for rule, confidence in sorted(rules, key=lambda x: x[1], reverse=True):
        pre, post = rule
        n += 1
        print("Rule %d: %s ==> %s %.2f%%" % 
                (n, str(pre), str(post), confidence * 100))

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print('Please input dataset filename.')
        sys.exit()

    fname = sys.argv[1]
    if not os.path.exists(fname):
        print('%s does not exist.' % (fname) )
    dataIter = get_dataIter(fname)
    
    minSup = 0.10
    minCon = 0.90
    try:
        minSup = float(sys.argv[2])
        minCon = float(sys.argv[3])
    except:
        pass

    items, rules = do_aprior(dataIter, minSup, minCon)
    print_result(items, rules)
