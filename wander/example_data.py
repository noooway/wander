import numpy as np
import pandas as pd

np.random.seed(0)

datelist = pd.date_range(start=pd.datetime.today() - pd.DateOffset(months=4),
                         end=pd.datetime.today(),
                         freq='1d')
#av_rev = rev_start + k * x^2;
#daily_rev = av_rev +/- 20%;
rev_start = 300
rev_end = 1000
n_points = len(datelist)
k = (rev_end - rev_start) / n_points**2
av_rev = [rev_start + k * x**2 for x in range(n_points)]
daily_rev = [x + np.random.uniform(-0.2*x, 0.2*x) for x in av_rev]
rev = pd.Series(daily_rev)

revenue_df = pd.DataFrame(list(zip(datelist, rev)), columns=["date","revenue"])
