import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


np.random.seed(0)

datelist = pd.date_range(start=pd.datetime.today() - pd.DateOffset(months=4),
                         end=pd.datetime.today(),
                         freq='1d')
week_start = [x.date() - timedelta(days=x.weekday()) for x in datelist]
month_start = [x.date().replace(day=1) for x in datelist]
# todo: make into dataframe

regions = ['america', 'europe', 'asia']
platforms = ['web_mobile', 'web_desktop', 'android', 'ios']


#av_rev = rev_start + k * x^2;
#daily_rev = av_rev +- 20%;
rev_start = 300
rev_end = 1000
n_points = len(datelist)
k = (rev_end - rev_start) / n_points**2
av_rev = [rev_start + k * x**2 for x in range(n_points)]
daily_rev = [x + np.random.uniform(-0.2*x, 0.2*x) for x in av_rev]
rev = pd.Series(daily_rev)
revenue_df = pd.DataFrame(list(zip(datelist, rev)), columns=["date","revenue"])
revenue_df['week_start'] = week_start
revenue_df['month_start'] = month_start
revenue_df['region'] = revenue_df.apply(lambda row: random.choice(regions),
                                        axis=1)
revenue_df['platform'] = revenue_df.apply(lambda row: random.choice(platforms),
                                          axis=1)


# regs = regs_start + k * x
# daily_regs = av_regs +- 10%
regs_start = 30
regs_end = 300
n_points = len(datelist)
k = (regs_end - regs_start) / n_points
av_regs = [regs_start + int(k * x) for x in range(n_points)]
daily_regs = [x + int(np.random.uniform(-0.1 * x, 0.1 * x)) for x in av_regs]
regs = pd.Series(daily_regs)
regs_df = pd.DataFrame(list(zip(datelist, regs)), columns=["date","regs"])
regs_df['week_start'] = week_start
regs_df['month_start'] = month_start
regs_df['region'] = regs_df.apply(lambda row: random.choice(regions),
                                  axis=1)
regs_df['platform'] = regs_df.apply(lambda row: random.choice(platforms),
                                    axis=1)




# online = online + k * x
# daily_online = av_online +- 10%
online_start = 50
online_end = 5000
n_points = len(datelist)
k = (online_end - online_start) / n_points
av_online = [online_start + int(k * x) for x in range(n_points)]
daily_online = [x + int(np.random.uniform(-0.1 * x, 0.1 * x)) for x in av_online]
online = pd.Series(daily_online)
online_df = pd.DataFrame(list(zip(datelist, online)), columns=["date","online"])
online_df['week_start'] = week_start
online_df['month_start'] = month_start
online_df['region'] = online_df.apply(lambda row: random.choice(regions),
                                      axis=1)
online_df['platform'] = online_df.apply(lambda row: random.choice(platforms),
                                        axis=1)



# TODO: Should be step instead of linear
# inst_to_regs = inst_to_regs_start + k * x
# daily_conv = inst_to_regs +- 10%
inst_to_regs_start = 0.7
inst_to_regs_end = 0.9
n_points = len(datelist)
k = (inst_to_regs_end - inst_to_regs_start) / n_points
av_inst_to_regs = [inst_to_regs_start + k * x for x in range(n_points)]
daily_conv = [x + np.random.uniform(-0.1 * x, 0.1 * x) for x in av_inst_to_regs]
inst_to_regs = pd.Series(daily_conv)
installs_count = [reg * conv for (reg, conv) in zip (regs, inst_to_regs)]
installs_df = pd.DataFrame(list(zip(datelist, installs_count)),
                           columns=["date", "installs"])
installs_df['week_start'] = week_start
installs_df['month_start'] = month_start
installs_df['region'] = regs_df.apply(lambda row: random.choice(regions),
                                      axis=1)
installs_df['platform'] = regs_df.apply(lambda row: random.choice(platforms),
                                        axis=1)



# TODO: Should be step instead of linear
# inst_to_regs = inst_to_regs_start + k * x
# daily_conv = inst_to_regs +- 10%
first_sales_start = 30
first_sales_end = 60
n_points = len(datelist)
k = (first_sales_end - first_sales_start) / n_points
av_first_sales = [first_sales_start + k * x for x in range(n_points)]
daily_conv = [x + int(np.random.uniform(-0.1 * x, 0.1 * x)) for x in av_first_sales]
first_sales = pd.Series(daily_conv)
first_sales_df = pd.DataFrame(list(zip(datelist, first_sales)),
                                   columns=["date","first_sales"])
first_sales_df['week_start'] = week_start
first_sales_df['month_start'] = month_start
first_sales_df['region'] = first_sales_df.apply(
    lambda row: random.choice(regions), axis=1)
first_sales_df['platform'] = first_sales_df.apply(
    lambda row: random.choice(platforms), axis=1)


regs_to_first_sales_df = pd.DataFrame(
    list(zip(datelist, first_sales_df["first_sales"], regs_df["regs"])),
    columns=["date", "first_sales", "regs"])
regs_to_first_sales_df['week_start'] = week_start
regs_to_first_sales_df['month_start'] = month_start





# TODO: Should be step instead of linear
# inst_to_regs = inst_to_regs_start + k * x
# daily_conv = inst_to_regs +- 10%
sales_start = 80
sales_end = 100
n_points = len(datelist)
k = (sales_end - sales_start) / n_points
av_sales = [sales_start + k * x for x in range(n_points)]
daily_sales = [x + int(np.random.uniform(-0.15 * x, 0.15 * x)) for x in av_sales]
sales = pd.Series(daily_sales)
sales_df = pd.DataFrame(list(zip(datelist, sales)), columns=["date","sales"])
sales_df['week_start'] = week_start
sales_df['month_start'] = month_start
sales_df['region'] = first_sales_df.apply(lambda row: random.choice(regions),
                                          axis=1)
sales_df['platform'] = first_sales_df.apply(lambda row: random.choice(platforms),
                                            axis=1)




second_sales_start = 10
second_sales_end = 20
n_points = len(datelist)
k = (second_sales_end - second_sales_start) / n_points
av_second_sales = [second_sales_start + k * x for x in range(n_points)]
daily_conv = [x + int(np.random.uniform(-0.1 * x, 0.1 * x)) for x in av_second_sales]
second_sales = pd.Series(daily_conv)
second_sales_df = pd.DataFrame(list(zip(datelist, second_sales)),
                                   columns=["date", "second_sales"])
first_sales_to_second_sales_df = pd.DataFrame(
    list(zip(datelist,
             second_sales_df["second_sales"],
             first_sales_df["first_sales"])),
    columns=["date", "second_sales", "first_sales"])
first_sales_to_second_sales_df['week_start'] = week_start
first_sales_to_second_sales_df['month_start'] = month_start



# virtual_currency_spent = online * 50 +- 10%
av_virtual_currency_spent = online_df['online'] * 50
daily_virtual_currency_spent = \
    [x + np.random.uniform(-0.1 * x, 0.1 * x) for x in av_virtual_currency_spent]
virtual_currency_spent = pd.Series(daily_virtual_currency_spent)
virtual_currency_spent_df = \
    pd.DataFrame(list(zip(datelist, virtual_currency_spent)),
                 columns=["date","virtual_currency_spent"])
virtual_currency_spent_df['week_start'] = week_start
virtual_currency_spent_df['month_start'] = month_start
virtual_currency_spent_df['region'] = \
    virtual_currency_spent_df.apply(lambda row: random.choice(regions), axis=1)
virtual_currency_spent_df['platform'] = \
    virtual_currency_spent_df.apply(lambda row: random.choice(platforms), axis=1)
