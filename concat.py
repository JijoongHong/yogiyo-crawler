import pandas as pd

districts = ["중구"]
categories = ["1인분주문", "프랜차이즈", "치킨", "피자양식", "중국집", "한식", "일식돈까스", "족발보쌈", "야식", "분식", "카페디저트", "편의점마트"]

for district in districts:
    result = pd.read_csv("./"+district+"_"+categories[0]+".csv")
    for i in range(len(categories)-1):
        temp = pd.read_csv("./"+district+"_"+categories[i+1]+".csv")
        result = pd.concat([result, temp])

    result.to_csv("./{}_종합.csv".format(district), encoding='utf-8-sig')


