"""
Best Position for a Service Centre
LeetCode 1638 - Difficulty: Hard

A delivery company wants to build a new service center in a new city. The company knows the positions of all the customers in this city on a 2D-Map and wants to build the new center in a position such that the sum of the euclidean distances to all customers is minimum.

Given an array 'positions' where 'positions[i] = [x_i, y_i]' is the position of the 'ith' customer on the map, return the minimum sum of the euclidean distances to all customers.

In other words, you need to choose the position of the service center '[x_centre, y_centre]' such that the following formula is minimized:

Answers within '10^-5' of the actual value will be accepted.



Constraints:

• '1 <= positions.length <= 50'

• 'positions[i].length == 2'

• '0 <= x_i, y_i <= 100'
"""

double solve(vector<vector<int>>& position) {
    int n = position.size();
    double eps = 1e-20;

    auto diff_dx = [&](double x, double y){
        double dx = 0;
        for (int i = 0; i < n; i++){
            dx +=
                (x - position[i][0]) / sqrt(pow(x - position[i][0], 2) +
                pow(y - position[i][1], 2) + eps); // at the customer’s location (x_i, y_i), avoid denom = 0
        }
        return dx;
    }; 

    auto diff_dy = [&](double x, double y){
        double dy = 0;
        for (int i = 0; i < n; i++){
            dy += 
                (y - position[i][1]) / sqrt(pow(x - position[i][0], 2) +
                pow(y - position[i][1], 2) + eps); // at the customer’s location (x_i, y_i), avoid denom = 0
        }
        return dy;
    }; 
    
    auto loss_f = [&](double x, double y){
        double dist = 0; 
        for (int i = 0; i < n; i++){
            dist += 
                sqrt(pow(x - position[i][0], 2) +
                pow(y - position[i][1], 2)); 
        }
        return dist; 
    };
    
    double x = 0, y = 0, next_x = 0, next_y = 0, stepsize = 1.0; 
    while (stepsize >= eps){
        double dx = diff_dx(x, y), dy = diff_dy(x, y);

        next_x = x - dx * stepsize; next_y = y - dy * stepsize;
        if (loss_f(next_x, next_y) < loss_f(x, y)){
            x = next_x; y = next_y;
        }
        else stepsize *= 0.5; // keep float
    }

    // ans = minimal loss
    return loss_f(x, y); 
}