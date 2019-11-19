import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt

# Functions
def returns(prices):
    """
    Calulates the growth of 1 dollar invested in a stock with given prices
    """
    return (1 + prices.pct_change(1)).cumprod()

def drawdown(prices):
    """
    Calulates the drawdown of a stock with given prices
    """
    rets = returns(prices)
    return (rets.div(rets.cummax()) - 1) * 100

def cagr(prices):
    """
    Calculates the Compound Annual Growth Rate (CAGR) of a stock with given prices
    """
    delta = (prices.index[-1] - prices.index[0]).days / 365.25
    return ((prices[-1] / prices[0]) ** (1 / delta) - 1) * 100

def sim_leverage(proxy, leverage=1, expense_ratio = 0.0, initial_value=1.0):
    pct_change = proxy.pct_change(1)
    pct_change = (pct_change - expense_ratio / 252) * leverage
    sim = (1 + pct_change).cumprod() * initial_value
    sim[0] = initial_value
    return sim

# Now lets graph the adjusted close of TQQQ since its inception versus QQQ.
fig, ax = plt.subplots()
start = datetime.datetime(2010, 2, 9)
end = datetime.datetime.today()

qqq = web.DataReader("QQQ", "yahoo", start, end)["Adj Close"] # yahoo finance API data
tqqq = web.DataReader("TQQQ", "yahoo", start, end)["Adj Close"]

qqq_returns = returns(qqq).rename("QQQ")
tqqq_returns = returns(tqqq).rename("TQQQ")

qqq_returns.plot(title="Growth of $1: QQQ vs TQQQ", legend=True, figsize=(10,6))
tqqq_returns.plot(legend=True)

print("CAGRs")
print(f"QQQ: {cagr(qqq):.2f}%")
print(f"TQQQ: {cagr(tqqq):.2f}%")

# Simulation since inception
fig, ax = plt.subplots()
qqq = web.DataReader("QQQ", "yahoo", start, end)["Adj Close"]
tqqq_sim = sim_leverage(qqq, leverage=3.0, expense_ratio=0.0095).rename("TQQQ Sim")
tqqq_sim.plot(title="Growth of $1: TQQQ vs TQQQ Sim", legend=True, figsize=(10,6))
tqqq_returns.plot(legend=True);

# Simulation of hypothetical historical performance
fig, ax = plt.subplots()
start = datetime.datetime(2007, 6, 1)
qqq = web.DataReader("QQQ", "yahoo", start, end)["Adj Close"]
tqqq_sim = sim_leverage(qqq, leverage=3.0, expense_ratio=0.0095).rename("TQQQ Sim")
tqqq_sim.plot(title="Growth of $1: QQQ vs TQQQ Sim", legend=True, figsize=(10,6))

qqq_returns = returns(qqq).rename("QQQ")
qqq_returns.plot(legend=True, grid=True)

print("CAGRs")
print(f"QQQ: {cagr(qqq):.2f}%")
print(f"TQQQ Sim: {cagr(tqqq_sim):.2f}%")