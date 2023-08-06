import json
from typing import Dict
from typing import Optional

from terminaltables import AsciiTable

from data.redis import get_key_weekly_price_pct_chg_sd
from data.redis import redis
from data.watchlist import ALL
from robinhood.lib.marketplace.equity import Equity
from robinhood.lib.marketplace.marketplace import marketplace
from scripts.libs.optionsellopportunity import OptionSellOpportunity
from scripts.libs.slack.slackclient import slack_client


class OptionSellScreener(object):

    def __init__(self) -> None:
        pass

    def run(self) -> None:
        equities = marketplace.get_equities(symbols={symbol for symbol in ALL})
        opportunities: Dict[str, OptionSellOpportunity] = {}
        for symbol in ALL:
            if symbol not in equities:
                continue

            opportunity = self._check_symbol_opportunity(
                symbol=symbol,
                equity=equities[symbol],
            )
            if opportunity is None:
                continue

            opportunities[symbol] = opportunity

        self._slack_opportunities(opportunities=opportunities)

    def _check_symbol_opportunity(
        self,
        symbol: str,
        equity: Equity,
    ) -> Optional[OptionSellOpportunity]:
        redis_key = get_key_weekly_price_pct_chg_sd(symbol=symbol)
        weekly_price_pct_chg_sd_raw = redis.get(name=redis_key)
        if weekly_price_pct_chg_sd_raw is None:
            return None

        weekly_price_pct_chg_sd = json.loads(weekly_price_pct_chg_sd_raw)

        this_week_sd = weekly_price_pct_chg_sd['this_week']
        next_week_sd = weekly_price_pct_chg_sd['next_week']
        open_price = weekly_price_pct_chg_sd['first_trading_day_open_price']

        pct_chg_so_far = equity.last_price / open_price - 1
        if abs(pct_chg_so_far) / this_week_sd <= 1:
            return None

        return OptionSellOpportunity(
            symbol=symbol,
            last_price=equity.last_price,
            pct_chg_so_far=pct_chg_so_far,
            sd_this_week=this_week_sd,
            sd_next_week=next_week_sd,
        )

    def _slack_opportunities(self, opportunities: Dict[str, OptionSellOpportunity]) -> None:
        msg = self._construct_slack_msg(opportunities=opportunities)
        slack_client.post_to_option_bot(msg=msg)

    def _construct_slack_msg(self, opportunities: Dict[str, OptionSellOpportunity]) -> str:
        data = [['symbol', 'last', '%', 'z', 'z next']]
        sorted_by_z_score = sorted(
            opportunities.values(),
            key=lambda o: abs(o.z_score_this_week),
            reverse=True,
        )
        for opportunity in sorted_by_z_score:
            if opportunity.last_price <= 10:
                continue

            data.append([
                opportunity.symbol,
                '${:,.2f}'.format(opportunity.last_price),
                '{:.2%}'.format(opportunity.pct_chg_so_far),
                '{:.2f}'.format(opportunity.z_score_this_week),
                '{:.2f}'.format(opportunity.z_score_next_week),
            ])
        t = AsciiTable(data)
        t.inner_column_border = True
        t.inner_footing_row_border = False
        t.inner_heading_row_border = True
        t.inner_row_border = False
        t.outer_border = False
        t.justify_columns = {
            0: 'center',
            1: 'right',
            2: 'right',
            3: 'right',
            4: 'right',
        }

        return f'```\n{str(t.table)}```'
