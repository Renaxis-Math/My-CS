#include "clustering.h"
#include <cmath>

double dist_sq(const Vec& a, const Vec& b) {
    double s = 0.0;
    for (int i = 0; i < (int)a.size(); i++) {
        double d = a[i] - b[i];
        s += d * d;
    }
    return s;
}

double dist(const Vec& a, const Vec& b) {
    return sqrt(dist_sq(a, b));
}

// The universal loop:
// assign() -> update() -> stop()
void run_backbone(AssignFn assign, UpdateFn update, StopFn stop, int max_iters) {
    for (int iter = 0; iter < max_iters; iter++) {
        assign();
        update();
        if (stop(iter)) break;
    }
}
