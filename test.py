import json
from tkinter import Label, Tk, Entry, END
from tktooltip import ToolTip

# Open the JSON file
with open(r'C:\Users\Admin\PycharmProjects\frreqinter\config.json', 'r') as f:
    data = json.load(f)

# Access the data in the JSON file
print(data['unfilledtimeout'])

# Create a Tkinter window
root = Tk()
label_max_open_trades = Label(root, text="max_open_trades")
label_stake_currency = Label(root, text="stake_currency")
label_stake_amount = Label(root, text="stake_amount")
label_tradable_balance_ratio = Label(root, text="tradable_balance_ratio")
label_fiat_display_currency = Label(root, text="fiat_display_currency")
label_dry_run = Label(root, text="dry_run")
label_dry_run_wallet = Label(root, text="dry_run_wallet")
label_cancel_open_orders_on_exit = Label(root, text="cancel_open_orders_on_exit")
label_trading_mode = Label(root, text="trading_mode")
label_margin_mode = Label(root, text="margin_mode")
label_unfilledtimeout_entry = Label(root, text="unfilledtimeout.entry ")
label_unfilledtimeout_exit = Label(root, text="unfilledtimeout.exit")
label_unfilledtimeout_exexit_timeout_countit = Label(root, text="unfilledtimeout.exexit_timeout_countit")
label_unfilledtimeout_unit = Label(root, text="unfilledtimeout.unit")

ToolTip(label_max_open_trades,
        msg="Required. Number of open trades your bot is allowed to have. Only one open trade per pair is possible, "
            "so the length of your pairlist is another limitation that can apply. If -1 then it is ignored "
            "(i.e. potentially unlimited open trades, limited by the pairlist)"
            "Datatype: Positive integer or -1.")

ToolTip(label_stake_currency,
        msg="Required. Crypto-currency used for trading. Datatype: String")

label_max_open_trades.grid(row=0, column=0)
label_stake_currency.grid(row=1, column=0)
label_stake_amount.grid(row=2, column=0)
label_tradable_balance_ratio.grid(row=3, column=0)
label_fiat_display_currency.grid(row=4, column=0)
label_dry_run.grid(row=5, column=0)
label_dry_run_wallet.grid(row=6, column=0)
label_cancel_open_orders_on_exit.grid(row=7, column=0)
label_trading_mode.grid(row=8, column=0)
label_margin_mode.grid(row=9, column=0)
label_unfilledtimeout_entry.grid(row=10, column=0)
label_unfilledtimeout_exit.grid(row=11, column=0)
label_unfilledtimeout_exexit_timeout_countit.grid(row=12, column=0)
label_unfilledtimeout_unit.grid(row=13, column=0)

entry_max_open_trades = Entry(root)
entry_stake_currency = Entry(root)
entry_stake_amount = Entry(root)
entry_tradable_balance_ratio = Entry(root)
entry_fiat_display_currency = Entry(root)
entry_dry_run = Entry(root)
entry_dry_run_wallet = Entry(root)
entry_cancel_open_orders_on_exit = Entry(root)
entry_trading_mode = Entry(root)
entry_margin_mode = Entry(root)
entry_unfilledtimeout_entry = Entry(root)
entry_unfilledtimeout_exit = Entry(root)
entry_unfilledtimeout_exit_timeout_countit = Entry(root)
entry_unfilledtimeout_unit = Entry(root)

entry_max_open_trades.grid(row=0, column=1)
entry_stake_currency.grid(row=1, column=1)
entry_stake_amount.grid(row=2, column=1)
entry_tradable_balance_ratio.grid(row=3, column=1)
entry_fiat_display_currency.grid(row=4, column=1)
entry_dry_run.grid(row=5, column=1)
entry_dry_run_wallet.grid(row=6, column=1)
entry_cancel_open_orders_on_exit.grid(row=7, column=1)
entry_trading_mode.grid(row=8, column=1)
entry_margin_mode.grid(row=9, column=1)
entry_unfilledtimeout_entry.grid(row=10, column=1)
entry_unfilledtimeout_exit.grid(row=11, column=1)
entry_unfilledtimeout_exit_timeout_countit.grid(row=12, column=1)
entry_unfilledtimeout_unit.grid(row=13, column=1)

entry_max_open_trades.insert(END, data['max_open_trades'])
entry_stake_currency.insert(END, data['stake_currency'])
entry_stake_amount.insert(END, data['stake_amount'])
entry_tradable_balance_ratio.insert(END, data['tradable_balance_ratio'])
entry_fiat_display_currency.insert(END, data['fiat_display_currency'])
entry_dry_run.insert(END, data['dry_run'])
entry_dry_run_wallet.insert(END, data['dry_run_wallet'])
entry_cancel_open_orders_on_exit.insert(END, data['cancel_open_orders_on_exit'])
entry_trading_mode.insert(END, data['trading_mode'])
entry_margin_mode.insert(END, data['margin_mode'])
entry_unfilledtimeout_entry.insert(END, data['unfilledtimeout']['entry'])
entry_unfilledtimeout_exit.insert(END, data['unfilledtimeout']['exit'])
entry_unfilledtimeout_exit_timeout_countit.insert(END, data['unfilledtimeout']['exit_timeout_count'])
entry_unfilledtimeout_unit.insert(END, data['unfilledtimeout']['unit'])

root.mainloop()
