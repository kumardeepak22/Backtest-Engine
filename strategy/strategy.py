import os
from typing import Union
from backtest.utils import utils
from backtest.utils.utils import get_instrument_lot_size


class Strategy:
    def __init__(self, strat_name, start_date, end_date, instrument, is_intraday,
                 start_time, end_time, capital, lots, stoploss_mtm_points = None,
                 target= None, per_trade_commission= 0,
                 re_entry_count=0, re_execute_count=0, stoploss_mtm_rupees=None,
                 timeframe = "1min", opt_timeframe = "1min", move_sl_to_cost = False,
                 trading_days_before_expiry=None, how_far_otm_hedge_point=None,
                 how_far_otm_short_point=None, expiry_week=0, stoploss_pct = None,
                 buffer: float = 0, close_half_on_mtm_rupees=None,
                 is_trail_sl = False, tsl = None):
        self.strat_name = strat_name
        self.start_date = start_date
        self.end_date = end_date
        self.instrument = instrument
        self.is_intraday = is_intraday
        self.start_time = utils.str_to_time_obj(start_time)
        self.end_time = utils.str_to_time_obj(end_time)
        self.stoploss_pct = stoploss_pct
        self.stoploss_mtm_points = -1 * stoploss_mtm_points if stoploss_mtm_points is not None else stoploss_mtm_points
        self.stoploss_mtm_rupees = -1 * stoploss_mtm_rupees if stoploss_mtm_rupees is not None else stoploss_mtm_rupees
        self.target = target
        self.per_trade_commission = per_trade_commission
        self.re_entry_count = re_entry_count
        self.re_execute_count = re_execute_count
        self.timeframe = timeframe
        self.opt_timeframe = opt_timeframe
        self.move_sl_to_cost = move_sl_to_cost
        self.trading_days_before_expiry = trading_days_before_expiry
        self.how_far_otm_hedge_point = how_far_otm_hedge_point
        self.how_far_otm_short_point = how_far_otm_short_point
        self.expiry_week = expiry_week
        self.capital = capital
        self.lots = lots
        self.position_size = get_instrument_lot_size(instrument) * lots
        self.buffer = buffer
        self.is_trail_sl = is_trail_sl
        self.tsl = tsl
        self.close_half_on_mtm_rupees = close_half_on_mtm_rupees
        self.create_strat_dir()
    def create_strat_dir(self):
        # Create a directory for the strategy if it doesn't exist.
        
        curr_dir = os.path.dirname(os.path.dirname(__file__))
        strategy_dir = os.path.join(curr_dir, self.strat_name)
        if not os.path.exists(strategy_dir):
            os.mkdir(strategy_dir)