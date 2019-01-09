import sys
import os
from itertools import chain, combinations
from collections import defaultdict

class FPNode(object):
    
    def __init__(self, name, count, parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []

    def has_child(self, name):
        for node in self.children:
            if node.name == name:
                return True

        return False

    def get_child(self, name):
        for node in self.children:
            if node.name == name:
                return node

        return None

    def add_child(self, name):
        child = FPNode(name, 1, self)
        self.children.append(child)
        return child

class FPTree(object):

    def __init__(self, txList, threshold, root_name, root_count):
        self.frequent = self.find_frequent_items(txList, threshold)
        self.headers = self.build_header_table(self.frequent)
        self.root = self.build_fptree(txList, root_name, root_count,
                                        self.frequent, self.headers)

    def find_frequent_items(self, txList, threshold):
        freqItems = {}

        for tx in txList:
            for item in tx:
                if item in freqItems:
                    freqItems[item] += 1
                else:	
                    freqItems[item] = 1

        # iter dict without change size
        for key in list(freqItems.keys()):
            if freqItems[key] < threshold:
                del freqItems[key]

        return freqItems

    def build_header_table(self, frequent):
        headers = {}
        for key in frequent.keys():
            headers[key] = None

        return headers

    def build_fptree(self, txList, root_name,
                     root_count, frequent, headers):
        
        root = FPNode(root_name, root_count, None)

        for tx in txList:
            sorted_items = [x for x in tx if x in frequent]
            sorted_items.sort(key=lambda x: frequent[x], reverse=True)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, headers)

        return root

    def update_headers(self, node, targetNode):
        while node.link != None:
            node = node.link
        node.link = targetNode

    def insert_tree(self, items, node, headers):
        item = items[0]
        child = node.get_child(item)

        if child is not None:
            child.count += 1
        else:
            child = node.add_child(item)
            if headers[item] is None:
                headers[item] = child
            else:
                self.update_headers(headers[item], child)

        if len(items) > 1:
            self.insert_tree(items[1:], child, headers)

    def tree_has_single_path(self, node):
        num_children = len(node.children)
        
        if num_children != 1:
            return bool(num_children == 0)
        else:
            return self.tree_has_single_path(node.children[0])

    def mine_patterns(self, threshold):
        if self.tree_has_single_path(self.root):
            return self.generate_pattern_list()
        else:
            return self.zip_patterns(self.mine_subTrees(threshold))

    def zip_patterns(self, patterns):
        suffix = self.root.name

        if suffix is not None:
            # We are in a conditional tree.
            new_patterns = {}
            for key in patterns.keys():
                new_patterns[tuple(sorted(list(key) + [suffix]))] = patterns[key]

            return new_patterns

        return patterns

    def generate_pattern_list(self):
        patterns = {}
        items = self.frequent.keys()

        # If we are in a conditional tree,
        # the suffix is a pattern on its own.
        if self.root.name is None:
            suffix_name = []
        else:
            suffix_name = [self.root.name]
            patterns[tuple(suffix_name)] = self.root.count

        for i in range(1, len(items) + 1):
            for subset in combinations(items, i):
                pattern = tuple(sorted(list(subset) + suffix_name))
                patterns[pattern] = min([self.frequent[x] for x in subset])

        return patterns

    def mine_subTrees(self, threshold):
        """
        Generate subtrees and mine them for patterns.
        """
        patterns = defaultdict(int)
        mining_order = sorted(self.frequent.keys(),
                              key=lambda x: self.frequent[x])

        # Get items in tree in reverse order of occurrences.
        for item in mining_order:
            suffixes = []
            conditional_tree_input = []
            node = self.headers[item]

            # step 1. Get list of all occurrences of a item (like 'beer')
            while node is not None:
                suffixes.append(node)
                node = node.link

            # step 2. For each occurrence, trace back to root
            for suffix in suffixes:
                frequency = suffix.count
                pNode = suffix.parent
                path = []

                while pNode.parent is not None:
                    path.append(pNode.name)
                    pNode = pNode.parent

                for i in range(frequency):
                    conditional_tree_input.append(path)

            # step 3. Recursively mine all subtree
            subtree = FPTree(conditional_tree_input, threshold,
                             item, self.frequent[item])
            subtree_patterns = subtree.mine_patterns(threshold)

            # step 4. Insert subtree patterns into main patterns dictionary.
            for key in subtree_patterns.keys():
                patterns[key] += subtree_patterns[key]

        return patterns

def get_txList(fname):
    txList = []
    with open(fname, 'r') as fp:
        for line in fp:
            line = line.rstrip('\n')
            line = line.rstrip('\r')
            line = line.rstrip(',')
            lst = line.split(',')
            txList.append(lst)

    return txList

def get_frequent_patterns(transactions, support_threshold):
    tree = FPTree(transactions, support_threshold, None, None)
    return tree.mine_patterns(support_threshold)

def get_association_rules(patterns, confidence_threshold):
    rules = {}
    for itemset in patterns.keys():
        for i in range(1, len(itemset)):
            for premise in combinations(itemset, i):
                premise = tuple(sorted(premise))
                conclusion = tuple(sorted(set(itemset) - set(premise)))

                if premise not in patterns:
                    continue
                
                confidence = 1.0 * patterns[itemset] / patterns[premise]
                if confidence >= confidence_threshold:
                    rules[premise] = (conclusion, confidence)

    return rules

def print_rules(rules):
    for key, value in sorted(rules.items(), key=lambda x: x[1][1], reverse=True):
        left = key
        right, confidence = value
        print(left, '==>', right, '%.2f%%' % (confidence*100))

if __name__ == '__main__':
    if len(sys.argv) == 0:
        print('Please input dataset filename.')
        sys.exit()

    fname = sys.argv[1]
    if not os.path.exists(fname):
        print('%s does not exist.' % (fname) )
    
    minSup = 0.10
    minCon = 0.90
    try:
        minSup = float(sys.argv[2])
        minCon = float(sys.argv[3])
    except:
        pass

    txList = get_txList(fname)
    patterns = get_frequent_patterns(txList, 0.1*len(txList))
    rules = get_association_rules(patterns, 0.9)
    print_rules(rules)