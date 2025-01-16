# Z, A, B = 10, C = 12
import numpy as np
import matplotlib.pyplot as plt


def liner(nums):
    
    def build(x):
        z = list(sorted(x))
        y = []
        for i in range(1, len(z)):
            dx = (z[i] - z[i-1])/(nums - 1)
            for k in range(nums):
                y.append(z[i-1] + k*dx)
        return y

    def stats(x):
        trades = len(x)
        mu = np.mean(x)
        sd = np.std(x)
        sharpe = mu / sd
        return mu, sd, sharpe, trades
                
    def solver(f):
        def handle(*a, **b):
            pre, post = f(*a, **b)
            bpre =  build(pre)
            bpost = build(post)
            pre_mu, pre_sd, pre_sharpe, pre_trades = stats(pre)
            pos_mu, pos_sd, pos_sharpe, pos_trades = stats(post)

            pre_title = 'Pre-Train Trades {}: Mu: {} | Vol: {} | Sharpe: {}'.format(pre_trades, '{0:.4f}'.format(pre_mu), '{0:.4f}'.format(pre_sd), '{0:.2f}'.format(pre_sharpe)) 
            pos_title = 'ML Trades {}: Mu: {} | Vol: {} | Sharpe: {}'.format(pos_trades, '{0:.4f}'.format(pos_mu), '{0:.4f}'.format(pos_sd), '{0:.2f}'.format(pos_sharpe)) 
            
            return bpre, bpost, pre_title, pos_title

        return handle
    
    return solver


@liner(50)   
def analyze_log(log, place):
    data = open(f'{log}.csv','r').readlines()
    returns = [float(i.replace('\n','')) for i in data if i != '\n']

    pre_ml = returns[:place]
    post_ml = returns[place:]

    return pre_ml, post_ml


logs = ['TradingLogZ','TradingLogA','TradingLogB','TradingLogC']
places = [10, 10, 10, 12]

fig = plt.figure(figsize=(9, 5))
ax = [fig.add_subplot(2, 2, i+1) for i in range(len(logs))]

for lx, px, bx in zip(logs, places, ax):
    bpre, bpost, pre_title, post_title = analyze_log(lx, px)
    bx.hist(bpre, bins=15, color='red', alpha=0.8, edgecolor='black', label=pre_title)
    bx.hist(bpost, bins=15, color='green', alpha=0.8, edgecolor='black', label=post_title) 
    bx.set_title(lx)
    bx.legend()

plt.show()





      

