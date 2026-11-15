import requests
from collections import deque
import numpy as np


def pair_buy(price, quantity, orderbook, target, original_balance, currency_accumulated, spending, fees):
                seen = set()
                for price, quantity in orderbook:
                        price, quantity = float(price), float(quantity)
                        if price not in seen:
                                seen.add(price)
                        else:
                                continue
                        target = float(original_balance / price)
                        if quantity < target:
                                currency_accumulated += quantity
                                spending += quantity * price
                                original_balance -= quantity * price
                        else:
                                currency_accumulated += target
                                spending += target * price
                                original_balance -= target * price
                                original_balance = 0
                                break

                if original_balance > 0.00001:
                        print("target buy not filled", float(target))
                        return None
                else:   
                        return currency_accumulated * (1 - fees)


def pair_sell(price, quantity, orderbook, original_balance, currency_accumulated, fees):
                seen = set()
                for price, quantity in orderbook:
                        price, quantity = float(price), float(quantity)
                        if price not in seen:
                                seen.add(price)
                        else:
                                continue
                        if quantity < original_balance:
                                currency_accumulated += quantity * price
                                original_balance -= quantity
                        else:
                                currency_accumulated += original_balance * price
                                original_balance -= quantity
                                original_balance = 0
                        break

                if original_balance > 0.00001:
                        print("target sell not filled", float(original_balance))
                        return None
                else:
                        return currency_accumulated * (1 - fees)

def spread_deque(currency, deque):
        spread = abs((currency / 10000) * 100)
        deque.append(spread)
        return deque

def deque_mean(deque):
        return np.mean(deque)

def deque_std_dev(deque):
        return float(std) if (std := float(np.std(deque))) != 0 else 0.0

def deque_z_score(deque, mean, std_dev):
        for sample in deque:
                try:
                        if std_dev == 0:
                                return None
                        z_score = (sample - mean) / std_dev
                except ZeroDivisionError:
                        return None
        return z_score

#signal achat veut dire qu'on est a plus de 10000
def signal(window, last_cost, margin, mean, std_dev, signal_achat, attente, budget, final_balance):
        if len(window) != 20:
                return "Window length inadequate, should be 10"
        if std_dev == 0:
                return "Standard deviation is equal to 0"
        
        last_z_score = (last_cost - mean) / std_dev
        profit =  final_balance - budget

        if last_z_score >= 3 and profit >= budget + margin:
                return signal_achat, float(last_z_score), float(profit), float(budget + margin)
        elif last_z_score >= 3 and profit >= budget + margin:
                return attente, float(last_z_score), float(profit), float(budget + margin)
        else:
                return attente, float(last_z_score), float(profit), float(budget + margin)
        
def main():
        spread_dq = deque(maxlen=20)
        np.set_printoptions(legacy='1.25')
        z_score_list = list()
        sell_total_list = list()
        signal_achat = "SIGNAL_ACHAT"
        attente = "ATTENTE"



        while True:
                try:
                        btcusd_resp = requests.get(
                                "https://api.binance.com/api/v3/depth",
                                params={"symbol": "BTCUSDT", "limit":50}, timeout=10
                                )
                        resp_lat1 = btcusd_resp.elapsed
                        #print("last btcusd update id", btcusd_resp.json()["lastUpdateId"])

                        ethbtc_resp = requests.get(
                                "https://api.binance.com/api/v3/depth",
                                params={"symbol": "ETHBTC", "limit":50}, timeout=10
                                )
                        resp_lat2 = ethbtc_resp.elapsed
                        #print("last ethbtc update id", ethbtc_resp.json()["lastUpdateId"])

                        ethusd_resp = requests.get(
                                "https://api.binance.com/api/v3/depth",
                                params={"symbol": "ETHUSDT", "limit":50}, timeout=10
                                )    
                        resp_lat3 = ethusd_resp.elapsed
                        #print("last ethusd update id", ethusd_resp.json()["lastUpdateId"])

                        total_lat = (resp_lat1 + resp_lat2 + resp_lat3).total_seconds() * 1000
                        print(f"[Total Latency: {round(float(total_lat))} Milliseconds]")
                                  
                        btcusd_asks = btcusd_resp.json()["asks"][:100]
                        ethbtc_asks = ethbtc_resp.json()["asks"][:100] 
                        ethusdt_bids = ethusd_resp.json()["bids"][:100] 

                        btc_asks = btcusd_resp.json().get("asks", [])
                        eth_asks = ethbtc_resp.json().get("asks", [])
                        eth_bids = ethusd_resp.json().get("bids", [])

                        if not btc_asks or not eth_asks or not eth_bids:
                                print("Orderbook incomplete, missing a key")
                                break

                        btc_budget = 100.0
                        fees = 0.001
                        bitcoin_accumulated = pair_buy(0, 0, btcusd_asks, 0, btc_budget, 0, 0, fees)
                        if bitcoin_accumulated == None:
                                        continue
                        else:
                                print(bitcoin_accumulated)
                                eth_budget = bitcoin_accumulated
                                eth_accumulated = pair_buy(0,0, ethbtc_asks, 0, eth_budget, 0, 0, fees)
                                if eth_accumulated == None:
                                        continue
                                else:
                                        print(eth_accumulated)

                                        usdt_budget = eth_accumulated                      
                                        usdt_accumulated = pair_sell(0, 0, ethusdt_bids, usdt_budget, 0, fees)
                                        if usdt_accumulated == None:
                                                continue
                                        else: 
                                                print(usdt_accumulated)
                                                sell_total_list.append(usdt_accumulated)
                                                if len(spread_deque(usdt_accumulated, spread_dq)) == 20:
                                                        mean, std_deviation = deque_mean(spread_dq), deque_std_dev(spread_dq)
                                                        print(mean, std_deviation)
                                                        z_score = deque_z_score(spread_dq, mean, std_deviation)
                                                        if z_score == None:
                                                                continue
                                                        z_score_list.append(z_score)
                                                        buy_decision = signal(spread_dq, spread_dq[-1], btc_budget * 0.0001, mean, std_deviation, signal_achat, attente, btc_budget, usdt_accumulated)
                                                        print(buy_decision)
                                                else:
                                                        print("window length", len(spread_dq))
        
                except requests.exceptions.Timeout as e:
                        print("Request timed out", e)
                        break
                except requests.exceptions.ConnectionError as e:
                        print("Your Connection might have a problem, check if you're connected to a working network and retry", e)
                        break
                except requests.exceptions.RequestException as e:
                        print("Request exception",e)
                        break
if __name__ == "__main__":
        main()