import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from datetime import datetime, date
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Đọc dữ liệu
route = "" # your local folder
df = pd.read_csv(route + 'covid19_2021_by_day.csv')
df.head()

# Loại bỏ cột không cần thiết
df = df[['NGÀY', 'new_cases']]

# Đổi tên cột
df.columns = ['date', 'new_cases']

df['date'] = df['date'].astype(str) + '/2021'
df.head()
# Chuyển đổi 'date' sang kiểu ngày tháng
df['date'] = pd.to_datetime(df['date'], format = '%d/%m/%Y')

# Loại bỏ Null
print('Number of nulls =', df.new_cases.isna().sum())

df = df[~df.new_cases.isna()].reset_index(drop=True)
print('Size sau khi loại nulls:', df.shape)

# Trực quan hóa
plt.figure(figsize=(18,6))
sns.lineplot(x=df.date, y=df.new_cases)

# Tập test: 2^7=128
train_size = len(df)-8
test_size = 8

univariate_df = df[['date', 'new_cases']].copy()
univariate_df.columns = ['ds', 'y']

train = univariate_df.iloc[:train_size, :]

x_train, y_train = pd.DataFrame(univariate_df.iloc[:train_size, 0]), pd.DataFrame(univariate_df.iloc[:train_size, 1])
x_valid, y_valid = pd.DataFrame(univariate_df.iloc[train_size:, 0]), pd.DataFrame(univariate_df.iloc[train_size:, 1])

print(len(train), len(x_valid))

# Build and fit model
# Train the model
model = ExponentialSmoothing(y_train, seasonal_periods=52, seasonal='add')

# Predict on valid set
y_pred = model.fit().predict(start=y_valid.index[0], end=y_valid.index[-1])

# Calculate metrics
score_mae = mean_absolute_error(y_valid, y_pred)
score_rmse = math.sqrt(mean_squared_error(y_valid, y_pred))

print('Exponential Smoothing:\nMAE = {}\nRMSE = {}'.format(score_mae, score_rmse))

# Dự đoán nhiệt độ 8 ngay kế tiếp
plt.figure(figsize=(12,6))
plt.plot(y_train.index, y_train, label='Train')
plt.plot(y_valid.index, y_valid, label='Test')
plt.plot(y_valid.index, y_pred, label='Exponential Smoothing')
plt.legend(loc='best')
