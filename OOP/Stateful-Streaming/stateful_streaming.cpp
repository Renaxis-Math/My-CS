/*
I gave an Order struct and I asked you to design an OOP interface and implement an event filter feature.
For example, something like: "after seeing 5 orders with trade price >= 100, output the next 3 buy orders."
*/

#include <fstream>
#include <iostream>
#include <string>

#include "Order.h"
#include "OrderEngine.h"

using namespace std;

Side parse_side(const string& side_text) {
    if (side_text == "Buy") return Side::Buy;
    return Side::Sell;
}

OrderType parse_type(const string& type_text) {
    if (type_text == "New") return OrderType::New;
    if (type_text == "Cancel") return OrderType::Cancel;
    return OrderType::Trade;
}

int main() {
    OrderEngine engine(
        TradeTriggerRule(5, 3, 100.0),
        BuySellAlertRule(3, 2)
    );

    ifstream input_file("orders.txt");
    if (!input_file.is_open()) {
        cerr << "Failed to open orders.txt\n";
        return 1;
    }

    int id;
    string side_text, type_text;
    double trade_price;
    while (input_file >> id >> side_text >> type_text >> trade_price) {
        Order order{
            id,
            parse_side(side_text),
            parse_type(type_text),
            trade_price
        };
        engine.onOrder(order);
    }

    return 0;
}
