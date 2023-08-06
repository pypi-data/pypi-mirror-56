from redis import StrictRedis


redis = StrictRedis(
    host='localhost',
    port='7001',
    db='0',
)


def get_key_weekly_price_pct_chg_sd(symbol: str) -> str:
    return f'weekly_price_pct_chg_sd_{symbol}'
