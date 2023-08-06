[![Travis status](https://img.shields.io/travis/WeFindX/PlanDF/master.svg?style=flat)](https://travis-ci.org/WeFindX/PlanDF)
# PlanDF
DataFrame for computing Value-Over-Time for lists of tuples (Step.investables, Step.deliverables) of a Plan.

Depends on [pandas.DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) and [stepio](https://github.com/wefindx/StepIO).

```
pip install plandf 
# curently only Python 2.7
```
More detailed example is [here](/README.ipynb).
## Examples
Using [hour](https://research.stlouisfed.org/fred2/series/CES0500000003) as currency. The ``time`` is a single reserved word, which is treated differently ONLY when it is added in the ``'input'`` value. The ``time`` is also a required item in all the ``'input'`` values.

### Hello World (1 Step)
```{python}
import plandf

p = plandf.Plan()
p.steps([
    {'input': 'time: 1; carrots: 2; cucumbers: 3',
     'output': 'liters of juice: 0.5; waste material grams: 20'}
])
p.info.df
```
### Hello Valued (1 Step)
```{python}
p.steps([
    {'input': 'time: 1@5h; carrots: 2@1usd; cucumbers: 3@1.5usd',
     'output': 'liters of juice: 0.5@5usd; waste material grams: 20@-0.01usd'}
])
p.df
```

### Hello Loan (Multi-Step)
* The numbers in the brackets denote the most likely value.
```{python}
p.steps(
    [{'input': 'time: 0@1h; cash: 10000@1usd',
      'output': 'loan note: 1'}] +
    [{'input': 'time: 30@24h',
      'output': 'loan payment: 1@320~375[325]usd'}] * 36
)
p.info.df
```

### Simple Ranged (2 Steps)
* The numbers in the brackets denote the most likely value.

```{python}
%matplotlib inline

p = plandf.Plan()
p.steps([
    {'input': 'time: 1~10[2]@1h', 'output': 'relax: 1@25~50[30]usd'},
    {'input': 'time: 4~5@1h', 'output': 'work: 1@200~320usd'},
])

p.plot()
```

### Comparison Example (2 Steps Each)
```{python}
p1 = plandf.Plan()
p1.steps([
    {'input': 'time: 1~10[2]@1h', 'output': 'relax: 1@25~50[30]usd'},
    {'input': 'time: 4~5@1h', 'output': 'work: 1@200~320usd'},
])

p2 = plandf.Plan()
p2.steps([
    {'input': 'time: 1~10[2]@1h', 'output': 'relax: 1@25~50[30]usd'},
    {'input': 'time: 4~5@1h', 'output': 'work: 1@200~320usd'},
])

import pandas as pd
df = pd.concat({'plan1': p1.df,
                'plan2': p2.df}, axis=1)

# Optional: humanize converts times from hours to days/minutes, and currency to USD.
plandf.utils.humanize(df)
```

### Visualizing Multiple Plans
#### All Scenarios
```{python}
import pandas as pd
pd.concat({'plan1': p1.df,
           'plan2': p2.df}, axis=1).fillna(method='bfill').plot()
```
#### Only Chosen Scenarios
```{python}
import pandas as pd
pd.concat({'plan1': p1.df['worst'],
           'plan2': p2.df['best']}, axis=1).fillna(method='bfill').plot()
```

### Breakfast All in Hours, Without any National Currencies :)

Both elapsed time, and the values of commoditites in hours.

```{python}
breakfast = plandf.Plan()
breakfast.steps([
    {'input': 'time: 0.003~0.004@24h; loaf of black bread: 1@0.1h; butter grams: 15@0.01h; tomato: 0.5@0.2h',
     'output': 'sandwitch: 1@0.12h'},

    {'input': 'eggs: 2~5@0.012h; scrambling actions: 50~100; time: 0.003~0.005@24h',
     'output': 'scrambled egg servings: 1@0.16h'},

    {'input': 'coffee teaspoon: 1~2@0.00012h; liters of water: 0.2~0.3@0.0001h; time: 0.003~0.005@24h',
     'output': 'cup of coffee: 1~1.5@0.08h'}
])
```
