import baostock as bs
import pandas as pd
from datetime import datetime

# 获取今天的日期
today = datetime.today().strftime('%Y-%m-%d')

# 登录Baostock
lg = bs.login()
print('登录状态：', '成功' if lg.error_code == '0' else '失败')

# 获取上证100指数数据 (代码：sh.000132)
rs = bs.query_history_k_data_plus(
    code='sh.000132',
    fields='date,code,open,high,low,close,volume,amount',
    start_date=today,
    end_date=today,
    frequency='d',
    adjustflag='3'
)

# 处理数据
data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())

if data_list:
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 保存数据到CSV文件
    result.to_csv(f'sse100_data_{today}.csv', index=False, encoding='utf-8')
    print(f'数据已保存至 sse100_data_{today}.csv')
else:
    print('未获取到数据，请检查代码或日期是否正确')

# 登出
bs.logout()