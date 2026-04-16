#include "clustering.h"
#include <limits>

// k-means: assign = nearest center, update = mean, stop = centers stop moving
KMeansResult run_kmeans(const vector<Point>& points, int k) {
    int n = (int)points.size();
    int dim = (int)points[0].x.size();

    vector<Vec> centers;
    for (int i = 0; i < k; i++) centers.push_back(points[i].x); // simple init

    vector<int> labels(n, -1);
    vector<Vec> new_centers;
    bool moved = true;

    auto assign = [&]() {
        for (int i = 0; i < n; i++) {
            double best = numeric_limits<double>::max();
            int best_k = -1;
            for (int c = 0; c < k; c++) {
                double d = dist(points[i].x, centers[c]);
                if (d < best) { best = d; best_k = c; }
            }
            labels[i] = best_k;
        }
    };

    auto update = [&]() {
        new_centers.assign(k, Vec(dim, 0.0));
        vector<int> cnt(k, 0);

        for (int i = 0; i < n; i++) {
            int c = labels[i];
            cnt[c]++;
            for (int j = 0; j < dim; j++) new_centers[c][j] += points[i].x[j];
        }
        for (int c = 0; c < k; c++) {
            if (cnt[c] == 0) continue;
            for (int j = 0; j < dim; j++) new_centers[c][j] /= (double)cnt[c];
        }

        // movement check for stop()
        moved = false;
        for (int c = 0; c < k; c++) {
            if (dist(centers[c], new_centers[c]) > 1e-6) { moved = true; break; }
        }
        centers = new_centers;
    };

    auto stop = [&](int /*iter*/) {
        return !moved;
    };

    run_backbone(assign, update, stop, 100);

    return {centers, labels};
}
