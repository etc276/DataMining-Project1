# DataMining-Project1

* F74044020 洪得揚
* 前次成績: 49
    * 主要扣分為 description, discussion 等部分

## Project Introduction

* What is this project for ?
    * Implement apriori and fp-growth algorithm by python3
* How to run this project ?
    * `git clone https://github.com/etc276/DataMining-Project1.git`
    * `python apriori.py ./dataset/IBM.csv [min_sup] [min_conf]`
    * `python fp-growth.py ./dataset/IBM.csv [min_sup] [min_conf]`
    * default (min_support, min_confidence) = (0.1, 0.9)

## Dataset

### Kaggle Dataset

* [source](https://www.kaggle.com/acostasg/random-shopping-cart)
* description
    * Random Shopping cart
    * Date to add register
    * Id transaction
    * Product for id transaction

| Date | Id | Product |
| -------- | -------- | -------- |
| 2000-01-01 | 1 | yogurt |


### IBM Dataset

* use `IBM Quest Data Generator.exe` to generate data

```
D:\Data Mining\HW1>"IBM Quest Data Generator.exe" lit -help
Command Line Options:
  -ntrans number_of_transactions_in_000s (default: 1000)
  -tlen avg_items_per_transaction (default: 10)
  -nitems number_of_different_items_in_000s) (default: 100)

  -npats number_of_patterns (default: 10000)
  -patlen avg_length_of_maximal_pattern (default: 4)
  -corr correlation_between_patterns (default: 0.25)
  -conf avg_confidence_in_a_rule (default: 0.75)

  -fname <filename> (write to filename.data and filename.pat)
  -ascii (default: True)
  -randseed # (reset seed used generate to x-acts; must be negative)
  -version (to print out version info)
```

* parameters
    * `ntrans`: number of transactions (1 for 1000)
    * `tlen`: average commodity per transaction
    * `nitems`: kind of commodity (1 for 1000)
    * `npats`: number of patterns

```
IBM Quest Data Generator.exe" lit -ntrans 1 -tlen 10 -nitems 1 -npats 100 -fname test
```

## Implementation

### FP-growth

* code
    * see `fp-growth.py`
* description
    * step 1. find frequent 1-item set, sorted and delete items
    * step 2. scan datebase, construct the FP-tree and  maintain a header table
    * step 3. min_subtrees, and get association rules
        * step 3.1 get list of all occurrences of a item (like 'beer')
        * step 3.2 trace back to root for each item
        * step 3.3 mine recursively all subtrees
        * step 3.4 insert subtree patterns into main patterns dictionary.

### Apriori

* code
    * see `apriori.py`
* description
    * step 1. get init Cset (items with min_support in all items)
    * step 2. get new Lset by Cset (joinset of Cset)
    * step 3. get new Cset by Lset (items with min_support in Lset)
    * step 4. if Lset is none, goto step 5, or goto step 2
    * step 5. record frequent itemset and rules in each Lset

## Report

### Association Analysis

> Compare with Weka


|  | Weka | this project |
| -------- | -------- | -------- |
| Apriori | ![](https://i.imgur.com/HGDq8tm.png) |  ![](https://i.imgur.com/ZtP7Qp3.png) |
| FP-growth | ![](https://i.imgur.com/oPktqct.png) | ![](https://i.imgur.com/TDbKVMh.png) |

* Bonus: kaggle dataset
    * weka: ` 1. 2612=t 3350=t 153 ==> 6494=t    <conf:(0.9)>`
    * this project: `Rule 1: ('2612', '3350') ==> ('6494',) 90.20%`


### Results Comparison

> comparison for time

* fixed min_support, change number of transactions (on IBM data)

|  | Aprior | FP-growth |
| -------- | -------- | -------- |
| 1000 | 0.04040s | 0.01005s |
| 2000 | 0.07883s | 0.01990s |
| 3000 | 0.12744s | 0.03192s |

* fix number of transactions, change min_support (on IBM data)

|  | Aprior | FP-growth |
| -------- | -------- | -------- |
| 0.02 | 3.46813s | 0.03198s |
| 0.05 | 0.92168s | 0.03214s |
| 0.07 | 0.46378s | 0.03173s |
| 0.10 | 0.13886s | 0.03218s |
| 0.12 | 0.09789s | 0.03145s |
| 0.15 | 0.09113s | 0.03152s |


### Discussion

* Since data from `IBM Quest Data Generator.exe` can not directly be input of WEKA, so I use [IBM-Quest-Data-Converter](https://github.com/mhwong2007/IBM-Quest-Data-Converter) to transform data to WEKA type and conventional csv type (as seen in dataset/)
* Since data from kaggle can not directly be input of WEKA, so I implement an `converter.py` to transform the itemID to number.
* Since FP-growth in this project is slow to kaggle data, most of the experiments is based on IBM data to make observations.
* Here is steps for experiment
    * First, generate IBM data for different number of transcations
    ```
    # change -ntrans and -fname to 1, 2, 3
    IBM Quest Data Generator.exe" lit -ntrans [x] -tlen 10 -nitems 1 -npats 100 -fname test_[x]
    ```
    * Second, transform IBM data to conventional csv
    ```
    java DataConverter -a test_1.data test_1.csv
    ```
    * Third, fixed min_support to test different data
    ```
    python apriori.py test_1.py
    python apriori.py test_2.py
    python apriori.py test_3.py
    ```
    * Last, fixed data to test different min_support
    ```
    python apriori.py test_3.py 0.05 0.90
    python apriori.py test_3.py 0.07 0.90
    python apriori.py test_3.py 0.10 0.90
    ```
### Conclusion and Observation

* In this project, FP-growth always better than Aprior.
* When fixed min_support, time and number of transactions are **positive correlative** (near direct ratio) for both algorithms.
* When fixed number of transactions, time and min_support are **negative correlative** for Apriori algorithm.
* When data are sparse, increase min_support can effectively decrease time.
    * But there is a threshold (about `0.10` for Apriori on IBM data) that no more to decrease.
    * It's because only a few items remain.