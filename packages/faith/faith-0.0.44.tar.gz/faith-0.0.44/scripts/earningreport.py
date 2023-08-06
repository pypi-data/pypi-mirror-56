from collections import OrderedDict
from typing import Any

from asciitree import LeftAligned

from report.symbolhistory.symbolhistory import SymbolHistory
from robinhood.lib.account.account import account
from robinhood.lib.helpers import format_price
from scripts.libs.slack.slackclient import slack_client


class EarningReport(object):

    def __init__(self) -> None:
        pass

    def run(self) -> None:
        report_txt = self._gen_earning_report()
        slack_client.post_to_earning(msg=f'```{report_txt}```')

    def _gen_earning_report(self) -> str:
        account.update_in_parallel()
        symbol_history = SymbolHistory(
            stock_orders=account.stock_orders,
            option_orders=account.option_orders,
            option_events=account.option_events,
        )
        (
            _,
            total_profit,
            total_profit_by_exp_date,
            total_profit_by_exp_date_by_symbol,
        ) = symbol_history.get_earning_data()

        total_profit_key = f'Total Profit: {format_price(total_profit)}'
        profit_by_exp_date_tree: OrderedDict[str, Any] = OrderedDict()
        for exp_date in sorted(total_profit_by_exp_date.keys()):
            profit = total_profit_by_exp_date[exp_date]
            symbol_profit = [
                (symbol, symbol_profit)
                for symbol, symbol_profit in total_profit_by_exp_date_by_symbol[exp_date].items()
            ]
            profit_by_exp_date_tree[f'By {exp_date}: {format_price(profit)}'] = {
                '{:5s} ${:.2f}'.format(symbol, symbol_profit): {}
                for symbol, symbol_profit in sorted(symbol_profit, key=lambda x: x[1])
            }
        profit_tree = {total_profit_key: profit_by_exp_date_tree}
        tree = LeftAligned()

        return str(tree(profit_tree))
