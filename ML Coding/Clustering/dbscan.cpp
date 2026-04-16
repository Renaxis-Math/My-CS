#include "clustering.h"

static vector<int> neighbors_of(const vector<Point>& points, int i, double eps) {
    vector<int> nb;
    for (int j = 0; j < (int)points.size(); j++) {
        if (dist(points[i].x, points[j].x) <= eps) nb.push_back(j);
    }
    return nb;
}

DBSCANResult run_dbscan(const vector<Point>& points, double eps, int minPts) {
    int n = (int)points.size();

    // -2 = unvisited, -1 = noise, >=0 = cluster id
    vector<int> labels(n, -2);
    int cid = 0;

    auto assign = [&]() {
        // process one unvisited point per iteration (fits backbone cleanly)
        int i0 = -1;
        for (int i = 0; i < n; i++) if (labels[i] == -2) { i0 = i; break; }
        if (i0 == -1) return;

        auto nb = neighbors_of(points, i0, eps);
        if ((int)nb.size() < minPts) {
            labels[i0] = -1; // noise
            return;
        }

        // start/expand cluster
        labels[i0] = cid;
        vector<int> seeds = nb;

        for (int s = 0; s < (int)seeds.size(); s++) {
            int p = seeds[s];

            if (labels[p] == -1) labels[p] = cid; // previously noise -> now included
            if (labels[p] != -2) continue;         // already processed

            labels[p] = cid;

            auto nb2 = neighbors_of(points, p, eps);
            if ((int)nb2.size() >= minPts) {
                seeds.insert(seeds.end(), nb2.begin(), nb2.end());
            }
        }

        cid++;
    };

    auto update = [&]() {
        // DBSCAN has no center update
    };

    auto stop = [&](int /*iter*/) {
        for (int i = 0; i < n; i++) {
            if (labels[i] == -2) return false; // still unvisited exists
        }
        return true;
    };

    run_backbone(assign, update, stop, 100000);

    // finalize any leftover unvisited -> noise (shouldn't happen)
    for (int i = 0; i < n; i++) if (labels[i] == -2) labels[i] = -1;

    return {labels};
}
