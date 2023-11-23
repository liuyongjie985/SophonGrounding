import pandas as pd

# 创建一个简单的DataFrame  
data = {
    'Name': ['刘勇杰', 'Nick', 'John', 'Peter'],
    'Age': [20, 21, 19, 18]
}
df = pd.DataFrame(data)

# 将DataFrame保存为.xlsx文件  
df.to_excel(r'C:\Users\Admin\Desktop\liuyongjie.xlsx', index=False)
