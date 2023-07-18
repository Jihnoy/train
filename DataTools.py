import pandas as pd
import numpy as np

df = pd.read_csv("result/FinalResult.csv")
# 假设数据存储在名为df的DataFrame中
new_df = df[df['result'].isin([1, 2])]  # 使用布尔索引选择"result"列中值为1和2的行
print(new_df)
# 将提取的行保存为新的CSV文件
new_df.to_csv('result_mid.csv', index=False)

#
# df['result'] = None
#
# # 根据条件将"A"、"B"、"X"和"Y"列的值映射到"result"列
# conditions = [
#     (df['A'] == 1),
#     (df['B'] == 1),
#     (df['X'] == 1),
#     (df['Y'] == 1)
# ]
# choices = [0, 1, 2, 3]
# df['result'] = np.select(conditions, choices, default=None)
#
# # 将原始列中的1值改为0
# columns_to_replace = ['A', 'B', 'X', 'Y']
# df[columns_to_replace] = df[columns_to_replace].replace(1, 0)
# df.loc[df['Participant zone'] == 3, 'Participant zone'] = 2
# df.loc[df['Participant zone'] == 5, 'Participant zone'] = 3
# # 打印修改后的DataFrame
# print(df)
#
# df.to_csv('TestLeft.csv', index=False)

