#ifndef ORDER_ENGINE_H
#define ORDER_ENGINE_H

#include <utility>
#include <variant>
#include <vector>

#include "./strategies/BuySellAlertRule.h"
#include "./strategies/TradeTriggerRule.h"

using Rule = std::variant<TradeTriggerRule, BuySellAlertRule>;

class OrderEngine {
    std::vector<Rule> _rules;

    public:
        template<typename... Rules>
        OrderEngine(Rules&&... rules) {
            std::ios::sync_with_stdio(false); // faster cout
            (add_rule(std::forward<Rules>(rules)), ...);
        }

        void add_rule(Rule rule) {
            _rules.emplace_back(std::move(rule));
        }

        void onOrder(const Order& order) {
            for (auto& rule : _rules) {
                std::visit(
                    [&order](auto& concrete_rule) {
                        if (concrete_rule.onOrder(order)) {
                            std::cout
                            << concrete_rule.get_name() 
                            << " Order ID: " 
                            << order.id << '\n';
                        }
                    },
                    rule
                );
            }
        }
};

#endif
