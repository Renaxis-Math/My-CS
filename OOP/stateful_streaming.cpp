/*
I gave an Order struct and I asked you to design an OOP interface and implement an event filter feature.
For example, something like: “after seeing 5 orders with trade price >= 100, output the next 3 buy orders.”
*/

#include<iostream>
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

class RuleInterface {
    public:

        /* without this, compiler auto destruct the interface but not the derived class */
        virtual ~RuleInterface() = default; // = default means: “use compiler's implementation, no need child's"

        /*  After moving onOrder() to Rule, child of RuleInterface, 
            these functions no longer be called from outsiders:
                e.g OrderFilter has _rule.is_trigger(order)
            , hence we don't need to force child implementation
        */
        // virtual int trigger_target() const = 0;
        // virtual int output_target() const = 0;
        // virtual bool is_trigger(const Order& order) const = 0;
        // virtual bool can_output(const Order& order) const = 0;
        
        virtual bool onOrder(const Order& order) = 0;
};

class Rule : public RuleInterface {
    int _trigger_target, _output_target;
    int _trigger_count = 0, _output_count = 0;
    bool _is_active = false, _is_done = false;

    public:

        Rule(int trigger_target, int output_target) :
            _trigger_target{trigger_target}, _output_target{output_target}
        {}

        int trigger_target() const { return _trigger_target; }
        int output_target() const { return _output_target; }

        bool is_trigger(const Order& order) const {
            return order.type == OrderType::Trade && order.trade_price >= 100;
        }

        bool can_output(const Order& order) const {
            return order.side == Side::Buy;
        }

        /*  Moved from OrderFilter to enable 'polymorphism', but:

            Make Rule stateful only when the rule must remember past events.
            •	if rule depends only on current input → stateless
	        •	if rule depends on past inputs / progress / phase → stateful
        */
        bool onOrder(const Order& order) {
            if (_is_done) return false;

            if (!_is_active) {
                if (is_trigger(order)) {
                    ++_trigger_count;
                    if (_trigger_count == trigger_target()) {
                        _is_active = true;
                    }
                }
                return false;
            }

            if (can_output(order)) {
                ++_output_count;
                if (_output_count == output_target()) {
                    _is_done = true;
                }
                return true;
            }
            return false;
        }        
};

class OrderFilter {

    // Rule _rule;
    // int _trigger_count = 0, _output_count = 0;
    // bool _is_active = false, _is_done = false;

    /* 1. T& not T* because
        •   no need null handling unlike pointer
	    •	avoids copying
	    •	preserves polymorphism
        2. Why const RuleInterface& here:
	    •	OrderFilter only reads the rule, not changes it
    */
    RuleInterface& _rule; 

    public:
        OrderFilter(RuleInterface& rule) : _rule{rule} {}
        bool onOrder(const Order& order) { return _rule.onOrder(order); }
};

int main() {
    Rule rule(5, 3);
    OrderFilter order_filter(rule);

    vector<Order> stream_orders = {
        {1, Side::Sell, OrderType::Trade, 101},
        {2, Side::Buy,  OrderType::Trade, 120},
        {3, Side::Sell, OrderType::New,     0},
        {4, Side::Sell, OrderType::Trade, 130},
        {5, Side::Buy,  OrderType::Trade, 140},
        {6, Side::Sell, OrderType::Trade, 100}, // 5th trigger
        {7, Side::Sell, OrderType::New,     0},
        {8, Side::Buy,  OrderType::New,     0}, // output
        {9, Side::Buy,  OrderType::Cancel,  0}, // output
        {10, Side::Sell, OrderType::Trade, 110},
        {11, Side::Buy, OrderType::Trade,  90}, // output
        {12, Side::Buy, OrderType::New,     0}        
    };

    for (const auto& order : stream_orders) {
        if (order_filter.onOrder(order)) cout << order.id << '\n';
    }

    return 0;
}

/* DESIGN

+------------------+
|      Order       |
+------------------+
| id               |
| side             |
| type             |
| tradePrice       |
+------------------+


           passes Order to
+----------------------------------+
|         OrderFilter              |
+----------------------------------+
| has a Rule                       |
| processes incoming orders        |
| returns matching output orders   |
+----------------------------------+
                |
                | owns / uses
                v
+----------------------------------+
|              Rule                |
+----------------------------------+
| trigger condition                |
| trigger count target             |
| output condition                 |
| output count target              |
+----------------------------------+
*/