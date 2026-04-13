/*
I gave an Order struct and I asked you to design an OOP interface and implement an event filter feature.
For example, something like: “after seeing 5 orders with trade price >= 100, output the next 3 buy orders.”
*/

#include<iostream>
#include<variant>
#include<vector>
using namespace std;

enum class Side { Buy, Sell };
enum class OrderType { New, Cancel, Trade };

struct Order {
    int id;
    Side side;
    OrderType type;
    double trade_price; // meaningful when type == Trade
};

// Rule 1: "After seeing 5 orders with trade price >= 100, output next 3 buys."
class TradeTriggerRule {
    enum class State { Waiting, Emitting, Done };

    State _state = State::Waiting;
    int _match_count = 0, _output_count = 0;

    int _threshod_match_count, _threshold_output_count;
    double _threshold_trade_price;

    public:
        TradeTriggerRule(
            int threshold_match_count,
            int threshold_output_count,
            double threshold_trade_price
        ) :
            _threshod_match_count{threshold_match_count},
            _threshold_output_count(threshold_output_count),
            _threshold_trade_price{threshold_trade_price}
        {}
        
        // return True if we output
        bool onOrder(const Order& order) {
            bool ans = false;

            switch (_state) {
                case State::Waiting:
                    ans = false;

                    if (order.type == OrderType::Trade && order.trade_price >= _threshold_trade_price) {
                        if (++_match_count >= _threshod_match_count) {
                            _state = State::Emitting;
                        }
                    }
                    break;

                case State::Emitting:
                    if (order.side == Side::Buy) {
                        ans = true;

                        if (++_output_count >= _threshold_output_count) {
                            _state = State::Done;
                        }
                    }
                    else ans = false;
                    break;
        
                case State::Done:
                    ans = false;
                    break;
            }
            
            if (ans) cout << "Emitted Order ID: " << order.id << '\n';
            return ans;
        }
};

// Rule 2: "Anytime if 3 buys and 2 sells happen in any order, alert once."
class BuySellAlertRule {
    int _buy_count = 0, _sell_count = 0;

    int _threshold_buy_count, _threshold_sell_count;

    void reset() {
        _buy_count = 0; _sell_count = 0;
    }

    public:
        BuySellAlertRule(int threshold_buy_count, int threshold_sell_count) :
            _threshold_buy_count{threshold_buy_count},
            _threshold_sell_count{threshold_sell_count}
        {}

        bool onOrder(const Order& order) {
            if (order.side == Side::Buy) ++_buy_count;
            if (order.side == Side::Sell) ++_sell_count;

            if (_buy_count >= _threshold_buy_count && _sell_count >= _threshold_sell_count) {
                reset();
                return true; // Emit this specific order as the alert
            }
            return false;
        }
};

using Rule = variant<TradeTriggerRule, BuySellAlertRule>;

class OrderEngine {
    vector<Rule> _rules;

    public:
        template<typename... Rules>
        OrderEngine(const Rules&... new_rules) {
            (add_rule(new_rules), ...);
        }

        void add_rule(const Rule& new_rule) {
            _rules.emplace_back(new_rule);
        }

        bool onOrder(const Order& order) {
            for (auto& rule : _rules) {
                bool is_match = std::visit( // to figure out type for std::variant
                    [&order](auto& found_rule) {
                        return found_rule.onOrder(order);
                    }, 
                    rule
                );
                // rule.onOrder(order);
                if (is_match) {
                    cout << "ALERT Order ID: " << order.id << '\n';
                    return true;
                }
            }
            return false;
        }
};

int main() {
    OrderEngine engine(
        TradeTriggerRule(5, 3, 100.0),
        BuySellAlertRule(3, 2)
    );

    // Test Stream
    vector<Order> stream = {
        {1,  Side::Sell, OrderType::Trade, 101.0}, // R1 Trigger 1
        {2,  Side::Buy,  OrderType::Trade, 120.0}, // R1 Trigger 2 (Also R2 Buy 1)
        {3,  Side::Sell, OrderType::New,     0.0}, // R2 Sell 1
        {4,  Side::Sell, OrderType::Trade, 130.0}, // R1 Trigger 3 (Also R2 Sell 2)
        {5,  Side::Buy,  OrderType::Trade, 140.0}, // R1 Trigger 4 (Also R2 Buy 2)
        {6,  Side::Sell, OrderType::Trade, 100.0}, // R1 Trigger 5 -> State transitions to Emitting
        {7,  Side::Sell, OrderType::New,     0.0}, 
        {8,  Side::Buy,  OrderType::New,     0.0}, // R1 Emit 1 (Also R2 Buy 3 -> R2 ALERT triggers here!)
        {9,  Side::Buy,  OrderType::Cancel,  0.0}, // R1 Emit 2 
        {10, Side::Sell, OrderType::Trade, 110.0}, 
        {11, Side::Buy,  OrderType::Trade,  90.0}, // R1 Emit 3 -> State transitions to Done
        {12, Side::Buy,  OrderType::New,     0.0}  
    };

    for (const auto& order : stream) {
        engine.onOrder(order);
    }

    return 0;
}