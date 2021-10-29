import numpy as np
import pandas_datareader as pdr
import datetime as dt
import pandas as pd

# The tickets of the business we wanna research.
tickers = ['AMZN', 'MSFT', 'GOOGL', 'BABA']
# The start and end date
start = dt.datetime(2015, 12, 1)
end = dt.datetime(2021, 1, 1)

# This function gets the Beta of every Stock in the given list
def getBetas (stocks, start_date, end_date):
    data = pdr.get_data_yahoo(stocks, start_date, end_date, interval="m")
    data1 = pdr.get_data_yahoo("^GSPC", start_date, end_date, interval="m")
    data = data['Adj Close']
    data1 = data1["Adj Close"]
    data = pd.concat([data, data1], axis=1)
    log_returns = np.log(data/data.shift())
    cov = log_returns.cov()
    var = log_returns["Adj Close"].var()
    betas = pd.DataFrame(columns=["Stock", "Beta"])
    i = 0
    for x in stocks:
        beta = cov.loc[str(x), "Adj Close"]/var
        betas.at[i, "Stock"] = str(x)
        betas.at[i, "Beta"] = beta
        i = i + 1
    return betas

# This function gets the CAPM of a single stock
def CAPM (beta, marketreturn, riskfreereturn):
    CAPM = riskfreereturn + beta*(marketreturn - riskfreereturn)
    return CAPM

# This Functios gets the CAPM of various stocks
def VariousCAPM (dataframeofstockbeta, marketreturn, riskfreereturn):
    index = dataframeofstockbeta.index
    print(range(len(index)))
    for x in range(len(index)):
        dataframeofstockbeta.at[x, "CAPM"] = CAPM(dataframeofstockbeta.at[x, "Beta"], marketreturn, riskfreereturn)
    return dataframeofstockbeta



all_betas = getBetas(tickers, start, end)
risk_free_return = 0.1
market_return = .105
AmazonCAPM = VariousCAPM(all_betas, market_return, risk_free_return)
AmazonCAPM.to_csv("AmazonCAPM.csv")
