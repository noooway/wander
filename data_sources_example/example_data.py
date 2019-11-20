import numpy as np
import pandas as pd
from datetime import datetime, timedelta


np.random.seed(0)

datelist = pd.date_range(start=pd.datetime.today() - pd.DateOffset(months=4),
                         end=pd.datetime.today(),
                         freq='1d')
weekstart = [x.date() - timedelta(days=x.weekday()) for x in datelist]
monthstart = [x.date().replace(day=1) for x in datelist]
# todo: make into dataframe


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
revenue_df['weekstart'] = weekstart
revenue_df['monthstart'] = monthstart


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
regs_df['weekstart'] = weekstart
regs_df['monthstart'] = monthstart


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
inst_to_regs_conv_df = pd.DataFrame(list(zip(datelist, inst_to_regs)),
                                    columns=["date","inst_to_regs_conv"])
inst_to_regs_conv_df['weekstart'] = weekstart
inst_to_regs_conv_df['monthstart'] = monthstart


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
first_sales_df['weekstart'] = weekstart
first_sales_df['monthstart'] = monthstart


regs_to_first_sales_conv_df = pd.DataFrame(
    list(zip(datelist,
             first_sales_df["first_sales"] / regs_df["regs"])),
    columns=["date","regs_to_first_sales_conv"])
regs_to_first_sales_conv_df['weekstart'] = weekstart
regs_to_first_sales_conv_df['monthstart'] = monthstart





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
sales_df['weekstart'] = weekstart
sales_df['monthstart'] = monthstart




second_sales_start = 10
second_sales_end = 20
n_points = len(datelist)
k = (second_sales_end - second_sales_start) / n_points
av_second_sales = [second_sales_start + k * x for x in range(n_points)]
daily_conv = [x + int(np.random.uniform(-0.1 * x, 0.1 * x)) for x in av_second_sales]
second_sales = pd.Series(daily_conv)
second_sales_df = pd.DataFrame(list(zip(datelist, second_sales)),
                                   columns=["date", "second_sales"])
first_sales_to_second_sales_conv_df = pd.DataFrame(
    list(zip(datelist,
             second_sales_df["second_sales"] / first_sales_df["first_sales"])),
    columns=["date", "first_sales_to_second_sales_conv"])
first_sales_to_second_sales_conv_df['weekstart'] = weekstart
first_sales_to_second_sales_conv_df['monthstart'] = monthstart
