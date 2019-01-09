# AssociationAnalysis
Implement apriori and fp-growth algorithm by python3
[note](https://hackmd.io/s/B1nqM4Vsm)

## How to Install

```
git clone https://github.com/etc276/AssociationAnalysis.git
```

## How to Run

```
python apriori.py ./dataset/IBM.csv
python fp-growth.py ./dataset/IBM.csv
```

* default (min_support, min_confidence) = (0.1, 0.9)
* you can run with custom support or confidence like `python [.py] [data] 0.15 0.92`

## Compare with Weka

### apriori
* Weka
    * ![](https://i.imgur.com/HGDq8tm.png)

* this project
    * ![](https://i.imgur.com/ZtP7Qp3.png)

### fp-growth
* Weka
    * ![](https://i.imgur.com/oPktqct.png)

* this project
    * ![](https://i.imgur.com/TDbKVMh.png)

## Bonus: dataset from kaggle

[kaggle dateset](https://www.kaggle.com/lalalalsa/association-of-shopping-basket/data)

* weka: ` 1. 2612=t 3350=t 153 ==> 6494=t 138    <conf:(0.9)> lift:(1.22) lev:(0.02) [24] conv:(2.49)`
* this project: `Rule 1: ('2612', '3350') ==> ('6494',) 90.20%`
