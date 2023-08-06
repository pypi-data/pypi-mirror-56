import json
from datetime import datetime
from time import sleep
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pandas import DataFrame
from pandas import Series

from alphavantage.alphavantageclient import AlphaVantageClient
from alphavantage.pricehistory.pricehistory import PriceHistory
from data.redis import get_key_weekly_price_pct_chg_sd
from data.redis import redis
from data.watchlist import ALL


class CalcStockWeeklyPctChgSd(object):

    def __init__(self) -> None:
        self._alphavantage = AlphaVantageClient()

    def run(self) -> None:
        for symbol in ALL:
            if symbol in {'RHT'}:
                continue

            print(symbol)
            weekly_pct_chg_sd = self._get_weekly_pct_chg_sd(symbol=symbol)
            if weekly_pct_chg_sd is None:
                continue

            redis.set(
                name=get_key_weekly_price_pct_chg_sd(symbol=symbol),
                value=json.dumps(weekly_pct_chg_sd),
            )

    def _get_price_history(self, symbol: str) -> Optional[PriceHistory]:
        try:
            price_history = self._alphavantage.get_price_history(
                symbol=symbol,
                time_window='daily',
                output_size='full',
            )

            return price_history
        except KeyError:
            sleep(5)
            return self._get_price_history(symbol=symbol)

    def _get_time_series_df(self, symbol: str) -> Optional[DataFrame]:
        price_history = self._get_price_history(symbol=symbol)
        if price_history is None:
            return None

        data: List[Dict[str, Any]] = []
        for ds, item in price_history.time_series.items():
            row: Dict[str, Any] = {
                'ds': ds,
                'open_price': item.adjusted_open_price,
                'close_price': item.adjusted_close_price,
            }
            data.append(row)

        return DataFrame(data)

    def _enrich_time_series_df(self, df: DataFrame) -> DataFrame:
        df['dow'] = df.ds.map(self._get_dow)
        df['woy'] = df.ds.map(self._get_woy)
        df['woy_full'] = df.apply(self._get_woy_full, axis=1)
        df['next_woy_full'] = df.apply(self._get_next_woy_full, axis=1)
        return df

    def _get_last_trading_day_df(self, df: DataFrame) -> DataFrame:
        idx = df.dow == df.groupby('woy_full').dow.transform(max)
        last_trading_day_df = df[idx][['close_price', 'woy_full']].set_index('woy_full')

        return last_trading_day_df

    def _get_first_trading_day_df(self, df: DataFrame) -> DataFrame:
        idx = df.dow == df.groupby('woy_full').dow.transform(min)
        first_trading_day_df = df[idx][['ds', 'open_price', 'woy_full']].set_index('woy_full')

        return first_trading_day_df

    def _get_weekly_pct_chg_sd(self, symbol: str) -> Optional[Dict[str, Any]]:
        df = self._get_time_series_df(symbol=symbol)
        if df is None:
            return None

        if df.shape[0] >= 360:
            n = 180
        elif df.shape[0] >= 180:
            n = 90
        else:
            return None

        enriched_df = self._enrich_time_series_df(df=df)
        last_trading_day_df = self._get_last_trading_day_df(df=df)

        joined = enriched_df.join(
            other=last_trading_day_df,
            on='woy_full',
            rsuffix='_this_week',
        ).join(
            other=last_trading_day_df,
            on='next_woy_full',
            rsuffix='_next_week',
        )

        joined['to_weekend_pct_chg'] = joined.close_price_this_week / joined.open_price - 1
        joined['to_next_weekend_pct_chg'] = joined.close_price_next_week / joined.open_price - 1

        joined['rolling_nd_to_weekend_pct_chg_std'] = joined.to_weekend_pct_chg.rolling(window=n).std()
        joined['rolling_nd_to_next_weekend_pct_chg_std'] = joined.to_next_weekend_pct_chg.rolling(window=n).std()

        print(joined['rolling_nd_to_next_weekend_pct_chg_std'])
        print(joined.to_next_weekend_pct_chg.tail(100))
        print(n)
        print(joined.tail(60))

        this_week = joined.iloc[-1].rolling_nd_to_weekend_pct_chg_std
        this_week_ds = joined.iloc[-1].ds
        next_week_idx = joined.rolling_nd_to_next_weekend_pct_chg_std.last_valid_index()
        if next_week_idx is None:
            next_week = None
            next_week_ds = None
        else:
            next_week = joined.iloc[next_week_idx].rolling_nd_to_next_weekend_pct_chg_std
            next_week_ds = joined.iloc[next_week_idx].ds

        first_trading_day_df = self._get_first_trading_day_df(df=df)
        first_trading_day_ds = first_trading_day_df.iloc[-1].ds
        first_trading_day_open_price = first_trading_day_df.iloc[-1].open_price

        return {
            'this_week': this_week,
            'this_week_ds': this_week_ds,
            'next_week': next_week,
            'next_week_ds': next_week_ds,
            'first_trading_day_open_price': first_trading_day_open_price,
            'first_trading_day_ds': first_trading_day_ds,
        }

    def _get_dow(self, ds: str) -> int:
        return datetime.strptime(ds, '%Y-%m-%d').weekday()

    def _get_woy(self, ds: str) -> int:
        return datetime.strptime(ds, '%Y-%m-%d').isocalendar()[1]

    def _get_woy_full(self, row: Series) -> str:
        year = row.ds[:4]
        woy = str(row.woy)
        return f'{year}/{woy}'

    def _get_next_woy_full(self, row: Series) -> str:
        new_woy = (row.woy + 1) % 52
        if new_woy == 0:
            new_woy = 52

        new_year = int(row.ds[:4])
        if new_woy == 1:
            new_year += 1

        return f'{new_year}/{new_woy}'
