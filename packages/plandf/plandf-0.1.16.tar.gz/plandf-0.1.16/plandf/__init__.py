import fred
import requests
import pandas as pd
import copy
import datetime

from plandf.plan_maker import PlanMaker
from plandf import settings


def read(plan_tuples, conversion_rates=True, scenarios=True):

    if not isinstance(conversion_rates, bool):
        try:
            p = PlanMaker(plan_tuples, conversion_rates)
        except:
            print("Could not retrieve currency conversion rates.")
            p = False

    else:
        if conversion_rates is True:
            p = PlanMaker(plan_tuples, constants.rates)
        else:
            p = PlanMaker(plan_tuples)

    if p:
        if scenarios:
            return p.get_scenarios()
        else:
            return p
    else:
        print("Could not read the plan_tuples.")
        return False


class Constants(object):

    def set_defaults(self):
        self.hour = settings.DEFAULT_HOUR_VALUE_IN_USD

        self.rates = pd.DataFrame({
            'h':   [settings.DEFAULT_HOUR_VALUE_IN_USD],
            'usd': [1.],
            'eur': [1.101473],
            'cny': [0.142244],
            'rub': [0.015642],
            'jpy': [0.009174]})

    def update(self):
        self.set_hour_rate()
        self.set_currenc_rates()

    def set_currenc_rates(self):
        if not settings.FIXER_API_KEY:
            print("Set settings FIXER_KEY. Get one at https://fixer.io")

        currency_rates = requests.get('http://data.fixer.io/api/latest?access_key={}&format=1'.format(settings.FIXER_API_KEY)).json()['rates']

        self.rates = pd.DataFrame( dict({'h': [self.hour], 'eur': 1.}, **{key.lower(): 1/currency_rates[key] for ix, key in enumerate(currency_rates)} ) )

        print("Currency values had been set from FIXER IO, check the .rates attribute.\nThe currency 'h' means the time of 1 hour labor, based on FRED API.")

    def set_hour_rate(self, h=None):
        if h:
            self.hour = h
            print("Hour value of work (self.hour) was set to %s usd from FRED API. Retrieving currency rates.." % self.hour)
            self.set_currenc_rates()
            print("Done.")

        else:
            if not settings.FRED_KEY:
                print("Set settings FRED_KEY. Get one at https://fred.stlouisfed.org")

            fred.key(settings.FRED_KEY)

            last_observation = fred.observations(settings.FRED_SERIES)['observations'][-1]

            h = last_observation['value']

            try:
                self.hour = float(h)
                print("Hour value of work (self.hour) was set to %s usd from FRED API." % self.hour)
            except:
                self.hour = 28.18
                print("Failed to retrieve rates from FRED API. Assuming 1h = 28.18 usd.")

constants = Constants()

update_rates = constants.update

constants.set_defaults()


class Plan(object):
    def __init__(self):
        if constants:
            self.rates = constants.rates
            self.hour = constants.hour
        else:
            print('No currencies or hour value. Run plandf.init() to load constants.')

    def from_records(self, plan_dicts):
        self.info = read(
            [
                (step['input'], step['output']) for step in plan_dicts
            ],
            conversion_rates=self.rates,
            scenarios=False
        ) # * (rates['h'] / rates['gbp']).values[0]
        self.df = self.info.get_scenarios()
        return self.df

    def steps(self, plan_dicts):
        ''' Shorthands '''

        records = []

        for step in plan_dicts:
            i = ''
            if 'i' in step.keys():
                i = step['i']
            elif 'in' in step.keys():
                i = step['in']
            elif 'input' in step.keys():
                i = step['input']

            o = ''
            if 'o' in step.keys():
                o = step['o']
            elif 'out' in step.keys():
                o = step['out']
            elif 'output' in step.keys():
                o = step['output']

            records.append({'input': i, 'output': o})

        return self.from_records(records)

    def convert(self, currency='h', convert_time=True):
        df = copy.deepcopy(self.df)

        if currency in self.rates.columns:
            # Currency
            df = df * self.rates['h'].values[0] / self.rates[currency].values[0]

        if convert_time:
            # Time
            df.index = df.index.map(lambda x: datetime.timedelta(hours=x))

        return df

    def plot(self, currency='h', dates=False, figsize=(10,4.5)):
        self.pf = self.convert(currency, convert_time=dates)

        if dates:
            p = self.pf.interpolate().plot(marker='.', figsize=figsize)
        else:
            self.pf['worst'].dropna().plot(marker='.', figsize=figsize)
            self.pf['mean'].dropna().plot(marker='.', figsize=figsize)
            p = self.pf['best'].dropna().plot(marker='.', figsize=figsize)

        p.set_ylabel('value (%s)' % (currency.upper(),))
        if dates:
            label = ''
        else:
            label = 'h, '
        p.set_xlabel('time (%selapsed)' % (label,));
        p.grid(True)
