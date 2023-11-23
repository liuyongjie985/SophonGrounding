# 1.导入pandas模块
import json

import pandas as pd

# 2.把Excel文件中的数据读入pandas
df = pd.read_excel(r'C:\Users\Admin\Desktop\电商&幸福里-字段.xlsx')
temp_dict = {}
for indexs in df.index:
    temp_dict[df.loc[indexs].values[0]] = df.loc[indexs].values[6]
# print(temp_dict)
result = {}
for k, v in temp_dict.items():
    # print("k", k, "v", v)
    if isinstance(v, str) and "condition_name" in v and "column" in v and "condition_value" in v:
        temp_list = v.replace("：", ":").replace("column:", "").replace("condition_name:", "").replace(
                "condition_value:", "").split("#")
        print(k, temp_list)
        assert len(temp_list) == 3
        condition_n_list = None
        condition_v_list = None
        column_list = None
        for i, x in enumerate(temp_list):
            x = x.replace("，", ",").replace(" ","")
            if i == 0:
                column_list = x.split(",")
            else:
                if i == 1:
                    condition_n_list = x.split(",")
                else:
                    condition_v_list = x.split(",")
        if k == 343:
            condition_n_list = ["主营四级类目【近60天，截止当前】", "p_date"]
        assert len(condition_n_list) == len(condition_v_list)
        result[k] = {"column": column_list, "condition_n": condition_n_list, "condition_v": condition_v_list}
print(result)
num = 0
for indexs in df.index:
    if df.loc[indexs].values[0] in result:
        df.iloc[indexs, 6] = str(result[df.loc[indexs].values[0]])
        num += 1
print(num)
df.to_excel(r'C:\Users\Admin\Desktop\output.xlsx', index=False)
