#ifndef ORDER_H
#define ORDER_H

enum class Side { Buy, Sell };
enum class OrderType { New, Cancel, Trade };

struct Order {
    int id;
    Side side;
    OrderType type;
    double trade_price; // meaningful when type == Trade
};

#endif
