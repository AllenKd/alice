from __future__ import print_function
from src.trade.schedule import TradeEventParser
from src.google.client import CalendarClient


def main():
    df_events = TradeEventParser().get_trade_events()

    for date, row in df_events.iterrows():
        if not row.sum():
            # no stocks to buy
            continue
        event = {
            'summary': 'Daily Trading Hint',
            'description': '',
            'start': {
                'dateTime': date.isoformat(),
            },
            'end': {
                'dateTime': date.isoformat(),
            },
        }
        for target, amount in row.items():
            event["description"] += f"{target}: {amount}\n" if amount else ''

        print(f"create event on {date}, content: \n{event['description']}")
        CalendarClient().create_event(event)


if __name__ == '__main__':
    main()
