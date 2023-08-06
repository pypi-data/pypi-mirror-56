import pandas as pd
import numpy as np
from bars import bars

df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))

# Register `pandas.progress_apply` and `pandas.Series.map_apply` with `bars`
# (can use `bars.gui.bars`, `bars.notebook.bars`, optional kwargs, etc.)
bars.pandas(desc="my bar!")

# Now you can use `progress_apply` instead of `apply`
# and `progress_map` instead of `map`
df.progress_apply(lambda x: x**2)
# can also groupby:
# df.groupby(0).progress_apply(lambda x: x**2)

# -- Source code for `bars_pandas` (really simple!)
# def bars_pandas(t):
#   from pandas.core.frame import DataFrame
#   def inner(df, func, *args, **kwargs):
#       t.total = groups.size // len(groups)
#       def wrapper(*args, **kwargs):
#           t.update(1)
#           return func(*args, **kwargs)
#       result = df.apply(wrapper, *args, **kwargs)
#       t.close()
#       return result
#   DataFrame.progress_apply = inner
