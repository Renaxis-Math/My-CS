#ifndef TRADE_TRIGGER_RULE_H
#define TRADE_TRIGGER_RULE_H

#include "../Order.h"
#include "../SharedGetName.h"

// Rule 1: "After seeing 5 orders with trade price >= 100, output next 3 buys."
class TradeTriggerRule : public SharedGetName {
    enum class State { Waiting, Emitting, Done };

    State _state = State::Waiting;
    int _match_count = 0;
    int _output_count = 0;

    int _threshod_match_count;
    int _threshold_output_count;
    double _threshold_trade_price;

    public:
        TradeTriggerRule(
            int threshold_match_count,
            int threshold_output_count,
            double threshold_trade_price
        ) :
            _threshod_match_count{threshold_match_count},
            _threshold_output_count{threshold_output_count},
            _threshold_trade_price{threshold_trade_price},
            SharedGetName("TradeTriggerRule")
        {}

        bool onOrder(const Order& order) {
            bool ans = false;

            switch (_state) {
                case State::Waiting:
                    ans = false;

                    if (order.type == OrderType::Trade && order.trade_price >= _threshold_trade_price) {
                        ++_match_count;
                        if (_match_count >= _threshod_match_count) {
                            _state = State::Emitting;
                        }
                    }
                    break;

                case State::Emitting:
                    if (order.side == Side::Buy) {
                        ans = true;

                        ++_output_count;
                        if (_output_count >= _threshold_output_count) {
                            _state = State::Done;
                        }
                    } else {
                        ans = false;
                    }
                    break;

                case State::Done:
                    ans = false;
                    break;
            }

            return ans;
        }
};

#endif
