import click

from scripts.calcstockweeklypctchgsd import CalcStockWeeklyPctChgSd
from scripts.earningreport import EarningReport
from scripts.optionsellscreener import OptionSellScreener


@click.group()
def manage() -> None:
    pass


@click.command()
def calc_stock_weekly_pct_chg_sd() -> None:
    CalcStockWeeklyPctChgSd().run()


@click.command()
def run_option_sell_screener() -> None:
    OptionSellScreener().run()


@click.command()
def slack_earning_report() -> None:
    EarningReport().run()


manage.add_command(calc_stock_weekly_pct_chg_sd)
manage.add_command(run_option_sell_screener)
manage.add_command(slack_earning_report)

if __name__ == '__main__':
    manage()
