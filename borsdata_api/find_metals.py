import quandl
import pandas as pd

def find_metals(list_of_metals):
    metals = []
    try:
        if 'gold' in list_of_metals:
            x = quandl.get("LBMA/GOLD")
            x.rename(columns={'USD (AM)': 'gold'}, inplace=True)
            x.index = x.index.strftime('%Y-%m-%d')
            x = x['gold']
            metals.append(x)
        if 'silver' in list_of_metals:
            s = quandl.get("LBMA/SILVER")
            s.rename(columns={'USD': 'silver'}, inplace=True)
            s.index = s.index.strftime('%Y-%m-%d')
            s = s['silver']
            metals.append(s)
        else:
            return metals
    except quandl.errors.quandl_error.LimitExceededError as e:
        print('error: {}'.format(str(e)))
        return metals

    return metals

if __name__ == '__main__':
    quandl_api()
