import pandas as pd
import pandas_market_calendars as mcal
import yaml


class TradeEventParser:
    def __init__(self):
        self.nyse = mcal.get_calendar('NYSE')
        self.df = pd.DataFrame({"date": []})
        self.df.set_index("date", inplace=True)

    def get_trade_events(self):
        early = self.nyse.schedule(tz='UTC', start_date='2023-01-26', end_date='2023-06-09')
        date_index = mcal.date_range(early, frequency='1D')
        df = pd.DataFrame({"date": date_index})
        df.set_index("date", inplace=True)

        with open("config/config.yaml", "r") as config:
            trade_calendar = yaml.safe_load(config)
            for item in trade_calendar:
                self._parse_trade_item(item)

        self.df.index = self.df.index.tz_convert('Asia/Taipei')
        self.df.index += pd.Timedelta(hours=-8)
        return self.df

    def _parse_trade_item(self, item: dict):
        index_range = self.nyse.schedule(start_date=item["from"], end_date=item["to"])
        date_index = mcal.date_range(index_range, frequency='1D')
        tmp = pd.DataFrame({"date": date_index})
        tmp.set_index("date", inplace=True)
        # tmp.index.tz_convert('Asia/Taipei')

        slope = item["shares"] / len(date_index)
        tmp[item["target"]] = [int((i + 1) * slope) - int(i * slope) for i in range(len(date_index))]
        self.df = self.df.merge(tmp, on="date", how="outer")
