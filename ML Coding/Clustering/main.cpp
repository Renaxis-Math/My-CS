#include "clustering.h"
#include <iostream>

using namespace std;

static vector<Point> demo_points() {
    return {
        {{0,0}}, {{0.1,0.2}}, {{-0.1,0}},
        {{5,5}}, {{5.1,4.9}}, {{4.9,5.2}},
        {{2.5,2.5}}
    };
}

static void print_labels(const vector<int>& labels) {
    for (int i = 0; i < (int)labels.size(); i++)
        cout << "Point " << i << " -> " << labels[i] << "\n";
}

int main(int argc, char** argv) {
    string alg = (argc >= 2 ? argv[1] : "kmeans");
    auto points = demo_points();

    if (alg == "kmeans") {
        auto res = run_kmeans(points, 2);
        cout << "[kmeans] centers:\n";
        for (int i = 0; i < (int)res.centers.size(); i++) {
            cout << "  center " << i << ": ";
            for (double v : res.centers[i]) cout << v << " ";
            cout << "\n";
        }
        cout << "[kmeans] labels:\n";
        print_labels(res.labels);
    }
    else if (alg == "dbscan") {
        auto res = run_dbscan(points, 0.5, 2);
        cout << "[dbscan] labels (-1 = noise):\n";
        print_labels(res.labels);
    }
    else if (alg == "hierarchical") {
        auto res = run_hierarchical_single_linkage(points, 2);
        cout << "[hierarchical] labels:\n";
        print_labels(res.labels);
    }
    else if (alg == "gmm") {
        auto res = run_gmm_iso(points, 2);
        cout << "[gmm] means:\n";
        for (int i = 0; i < (int)res.means.size(); i++) {
            cout << "  mean " << i << ": ";
            for (double v : res.means[i]) cout << v << " ";
            cout << "\n";
        }
        cout << "[gmm] labels:\n";
        print_labels(res.labels);
    }
    else {
        cout << "Usage: ./demo kmeans | dbscan | hierarchical | gmm\n";
    }

    return 0;
}
