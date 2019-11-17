import numpy as np
import pandas as pd

np.random.seed(0)

datelist = pd.date_range(start=pd.datetime.today() - pd.DateOffset(months=4),
                         end=pd.datetime.today(),
                         freq='1d')

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
