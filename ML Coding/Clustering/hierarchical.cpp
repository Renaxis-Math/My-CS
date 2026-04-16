#include "clustering.h"
#include <limits>

static double single_link_dist(const vector<Point>& points,
                               const vector<int>& A,
                               const vector<int>& B) {
    double best = numeric_limits<double>::max();
    for (int i : A) for (int j : B)
        best = min(best, dist(points[i].x, points[j].x));
    return best;
}

HierarchicalResult run_hierarchical_single_linkage(const vector<Point>& points, int k) {
    int n = (int)points.size();
    vector<vector<int>> clusters;
    for (int i = 0; i < n; i++) clusters.push_back({i});

    int merge_i = -1, merge_j = -1;

    auto assign = [&]() {
        double best = numeric_limits<double>::max();
        merge_i = -1; merge_j = -1;

        for (int i = 0; i < (int)clusters.size(); i++) {
            for (int j = i + 1; j < (int)clusters.size(); j++) {
                double d = single_link_dist(points, clusters[i], clusters[j]);
                if (d < best) { best = d; merge_i = i; merge_j = j; }
            }
        }
    };

    auto update = [&]() {
        if (merge_i < 0 || merge_j < 0) return;

        clusters[merge_i].insert(clusters[merge_i].end(),
                                 clusters[merge_j].begin(), clusters[merge_j].end());
        clusters.erase(clusters.begin() + merge_j);
    };

    auto stop = [&](int /*iter*/) {
        return (int)clusters.size() <= k;
    };

    run_backbone(assign, update, stop, 100000);

    vector<int> labels(n, -1);
    for (int c = 0; c < (int)clusters.size(); c++)
        for (int idx : clusters[c]) labels[idx] = c;

    return {labels};
}
