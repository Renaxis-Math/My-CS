#ifndef CLUSTERING_H
#define CLUSTERING_H

#include <vector>
#include <functional>
#include <string>

using namespace std;

// requested alias
using Vec = vector<double>;

struct Point { Vec x; };

// ---------- shared helpers ----------
double dist(const Vec& a, const Vec& b);
double dist_sq(const Vec& a, const Vec& b);

// ---------- backbone (python-style) ----------
using AssignFn = function<void()>;
using UpdateFn = function<void()>;
using StopFn   = function<bool(int iter)>;

void run_backbone(AssignFn assign, UpdateFn update, StopFn stop, int max_iters);

// ---------- results + APIs (declared here, implemented in cpp files) ----------
struct KMeansResult {
    vector<Vec> centers;
    vector<int> labels;
};
KMeansResult run_kmeans(const vector<Point>& points, int k);

struct DBSCANResult {
    vector<int> labels; // -1 = noise
};
DBSCANResult run_dbscan(const vector<Point>& points, double eps, int minPts);

struct HierarchicalResult {
    vector<int> labels; // 0..k-1
};
HierarchicalResult run_hierarchical_single_linkage(const vector<Point>& points, int k);

struct GMMResult {
    vector<Vec> means;
    vector<double> var;     // isotropic
    vector<double> pi;      // mixing weights
    vector<int> labels;     // hard label from argmax responsibility
};
GMMResult run_gmm_iso(const vector<Point>& points, int k);

#endif
