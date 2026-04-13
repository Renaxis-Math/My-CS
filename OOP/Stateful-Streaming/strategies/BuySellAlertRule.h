#ifndef BUY_SELL_ALERT_RULE_H
#define BUY_SELL_ALERT_RULE_H

#include "../Order.h"
#include "../SharedGetName.h"

// Rule 2: "Anytime if 3 buys and 2 sells happen in any order, alert once."
class BuySellAlertRule : public SharedGetName {
    int _buy_count = 0;
    int _sell_count = 0;

    int _threshold_buy_count;
    int _threshold_sell_count;

    void reset() {
        _buy_count = 0;
        _sell_count = 0;
    }

    public:
        BuySellAlertRule(int threshold_buy_count, int threshold_sell_count) :
            _threshold_buy_count{threshold_buy_count},
            _threshold_sell_count{threshold_sell_count},
            SharedGetName("BuySellAlertRule")
        {}

        bool onOrder(const Order& order) {
            if (order.side == Side::Buy) {
                ++_buy_count;
            }
            if (order.side == Side::Sell) {
                ++_sell_count;
            }

            if (_buy_count >= _threshold_buy_count && _sell_count >= _threshold_sell_count) {
                reset();
                return true;
            }
            return false;
        }
};

#endif
