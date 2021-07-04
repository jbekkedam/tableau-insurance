
import pandas as pd
import random

df = pd.read_csv('./names.csv')
print(df)

# first year of business in 2010
# coverages D&O E&O
# company revenue $5M-$20M
# Coverage is minimum 1M, + 0.5M for 10M, 15M, 20M, max 2.5M for D&O
# Coverage is minimum 0.5M, + 0.5M for 10M, 15M, 20M, max 2M for E&O
# Coverage cost $12K-18K per M of D&O
# Coverage cost $30K-40K per M of E&O
# market will harden around 2018
# 50% chance of 2% increase from 2010 to 2018
# 80% chance of 7-11% increase from 2018-2021

# broker change fees in 2016 to 0.05
# market hardens in 2014


def gen_broker_fee(price, year):
    if year <= 2014:
        return price*0.1, 0.1
    if year >= 2014 and year < 2018:
        return price*0.05, 0.05
    else:
        return price*0.1, 0.1


def random_start():
    return random.randint(0, 9) <= 0


def nine_in_ten():
    return random.randint(0, 9) != 0


def revenue_changes(prev_rev):
    return (1 + (random.randint(-2, 13)/100)) * prev_rev


def do_coverage_generator(revenue):
    if revenue >= 20000000:
        return 2000000
    if revenue >= 15000000:
        return 1500000
    if revenue >= 10000000:
        return 1000000
    else:
        return 500000


def eo_coverage_generator(revenue):
    if revenue >= 20000000:
        return 1000000
    if revenue >= 15000000:
        return 500000
    if revenue >= 10000000:
        return 250000
    else:
        return 100000


def initial_price(revenue):
    if revenue >= 20000000:
        price = 120000
        broker_fee, broker_fee_percentage = gen_broker_fee(price, year)
        price = price + broker_fee
        return price, broker_fee, broker_fee_percentage
    if revenue >= 15000000:
        price = 80000
        broker_fee, broker_fee_percentage = gen_broker_fee(price, year)
        price = price + broker_fee
        return price, broker_fee, broker_fee_percentage
    if revenue >= 10000000:
        price = 55000
        broker_fee, broker_fee_percentage = gen_broker_fee(price, year)
        price = price + broker_fee
        return price, broker_fee, broker_fee_percentage
    else:
        price = 40000
        broker_fee, broker_fee_percentage = gen_broker_fee(price, year)
        price = price + broker_fee
        return price, broker_fee, broker_fee_percentage


def price_change(prev_price, revenue, previous_revenue, year, previous_broker_fee):
    multiplier = 0
    if year >= 2014:
        multiplier += 0.07
    if revenue > previous_revenue*1.10:
        multiplier += 0.03

    price = prev_price*(1 + multiplier) - previous_broker_fee
    broker_fee, broker_fee_percentage = gen_broker_fee(price, year)
    price = price + broker_fee
    return price, broker_fee, broker_fee_percentage

    return prev_price*(1 + multiplier)


year_list = [2010, 2011, 2012, 2013, 2014,
             2015, 2016, 2017, 2018, 2019, 2020, 2021]
cols = ['Company', "Year", "Revenue"]
df_main = pd.DataFrame(columns=cols)
print(df_main)

n = 0
# add years
for index, row in df.iterrows():
    for year in year_list:

        # 30# of becoming a client
        if random_start() and row["Company Names"] not in df_main.values:
            company = row["Company Names"]
            year = year
            revenue = int(random.randint(1000000, 20000000))
            do_coverage = int(do_coverage_generator(revenue))
            eo_coverage = int(eo_coverage_generator(revenue))
            price, broker_fee, broker_fee_percentage = initial_price(revenue)

            company_dict = {"Company": int(company), "Year": int(year), "Revenue": float(revenue), "D&O Limit": do_coverage,
                            "E&O Limit": eo_coverage, "Price": price, "Broker_fee": broker_fee,
                            "Broker_fee_percentage": broker_fee_percentage, "Broker": "Broker C"}
            df_main = df_main.append(company_dict, ignore_index=True)

        # 90% chance of continuing
        if year-1 in df_main[df_main['Company'] == row["Company Names"]].values and nine_in_ten():
            # generate revenue based off of last year
            previous_year_df = df_main[(df_main['Company'] == row["Company Names"]) & (
                df_main['Year'] == year-1)]
            prev_rev = previous_year_df['Revenue'].iloc[0]
            prev_price = previous_year_df['Price'].iloc[0]
            prev_broker_fee = previous_year_df['Broker_fee'].iloc[0]
            prev_broker_fee_percentage = previous_year_df['Broker_fee_percentage'].iloc[0]

            revenue = int(revenue_changes(prev_rev))
            do_coverage = int(do_coverage_generator(revenue))
            eo_coverage = int(eo_coverage_generator(revenue))
            price, broker_fee, broker_fee_percentage = price_change(
                prev_price, revenue, prev_rev, year, prev_broker_fee)

            # Coverage
            #hard market
            if year >= 2014 and year < 2018 and broker_fee_percentage >= 0.1:
                if random.randint(0, 9) >= 5:
                    company_dict = {"Company": int(company), "Year": int(year), "Revenue": float(
                        revenue),  "D&O Limit": do_coverage, "E&O Limit": eo_coverage, "Price": price, "Broker_fee": broker_fee, 
                                    "Broker_fee_percentage": broker_fee_percentage, "Broker": "Broker C"}
                    df_main = df_main.append(company_dict, ignore_index=True)
                else:
                    pass
            else:
                if random.randint(0, 9) <= 8:
                    company_dict = {"Company": int(company), "Year": int(year), "Revenue": float(
                        revenue),  "D&O Limit": do_coverage, "E&O Limit": eo_coverage, "Price": price, "Broker_fee": broker_fee, 
                                    "Broker_fee_percentage": broker_fee_percentage, "Broker": "Broker C"}
                    df_main = df_main.append(company_dict, ignore_index=True)


df_main['Year'] = df_main['Year'].astype(int)
df_main['Company'] = df_main['Company'].astype(int)
df_main['Revenue'] = df_main['Revenue'].astype(int)
df_main['Broker_fee'] = df_main['Broker_fee'].astype(int)
df_main['D&O Limit'] = df_main['D&O Limit'].astype(int)
df_main['E&O Limit'] = df_main['E&O Limit'].astype(int)
df_main['Price'] = df_main['Price'].astype(int)
df_main['Year'] = df_main['Year'].astype(str) + "/01/01"
df_main.to_csv("./insurance_data_broker_C.csv")




















