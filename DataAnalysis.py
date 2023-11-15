import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("result/left.csv")
filtered_df = df[df['Participant zone'].isin([5, 6])]

time_stats = filtered_df['Time'].describe()
print(time_stats)

time_bins = [4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5,8, 8.5,9]  # 您可以根据需要修改时间区间的范围


# 使用cut函数将时间分成不同的区间，并统计每个区间内的数据数量
time_distribution = pd.cut(filtered_df['Time'], bins=time_bins).value_counts()
time_distribution = time_distribution.sort_index()
print("时间分布统计：")
print(time_distribution)

# 修改标签格式
time_labels = time_distribution.index.astype(str).str.replace('(', '').str.replace(']', '').str.replace(', ','-')
plt.figure(figsize=(10, 6))
# 绘制时间分布的折线图
plt.plot(time_labels, time_distribution.values, marker='o')

# 添加标题和轴标签
plt.title('Time Distribution')
plt.xlabel('Time Interval')
plt.ylabel('Count')
plt.savefig('time_zone56.png', format='png')
# 显示图形
plt.show()
