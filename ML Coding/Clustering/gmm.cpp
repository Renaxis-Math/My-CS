#include "clustering.h"
#include <cmath>
#include <limits>

static double gaussian_iso_pdf(const Vec& x, const Vec& mu, double var) {
    int d = (int)x.size();
    double denom = pow(2.0 * M_PI * var, d / 2.0);
    double num = exp(-0.5 * dist_sq(x, mu) / var);
    return num / (denom + 1e-300);
}

GMMResult run_gmm_iso(const vector<Point>& points, int k) {
    int n = (int)points.size();
    int d = (int)points[0].x.size();

    vector<Vec> means;
    for (int i = 0; i < k; i++) means.push_back(points[i].x); // init

    vector<double> var(k, 1.0);
    vector<double> pi(k, 1.0 / k);
    vector<vector<double>> r(n, vector<double>(k, 1.0 / k));

    double prev_ll = -numeric_limits<double>::infinity();
    double curr_ll = prev_ll;

    auto assign = [&]() {
        for (int i = 0; i < n; i++) {
            double s = 0.0;
            for (int c = 0; c < k; c++) {
                r[i][c] = pi[c] * gaussian_iso_pdf(points[i].x, means[c], var[c]);
                s += r[i][c];
            }
            s = max(s, 1e-300);
            for (int c = 0; c < k; c++) r[i][c] /= s;
        }
    };

    auto update = [&]() {
        // M-step
        for (int c = 0; c < k; c++) {
            double Nk = 0.0;
            Vec mu(d, 0.0);

            for (int i = 0; i < n; i++) {
                Nk += r[i][c];
                for (int j = 0; j < d; j++) mu[j] += r[i][c] * points[i].x[j];
            }
            Nk = max(Nk, 1e-12);
            for (int j = 0; j < d; j++) mu[j] /= Nk;
            means[c] = mu;

            double sse = 0.0;
            for (int i = 0; i < n; i++)
                sse += r[i][c] * dist_sq(points[i].x, means[c]);
            var[c] = max(sse / (Nk * d), 1e-6);

            pi[c] = Nk / n;
        }

        // log-likelihood
        prev_ll = curr_ll;
        curr_ll = 0.0;
        for (int i = 0; i < n; i++) {
            double s = 0.0;
            for (int c = 0; c < k; c++)
                s += pi[c] * gaussian_iso_pdf(points[i].x, means[c], var[c]);
            curr_ll += log(s + 1e-300);
        }
    };

    auto stop = [&](int /*iter*/) {
        return fabs(curr_ll - prev_ll) < 1e-6;
    };

    run_backbone(assign, update, stop, 100);

    // hard labels from argmax responsibility
    vector<int> labels(n, 0);
    for (int i = 0; i < n; i++) {
        int best = 0;
        for (int c = 1; c < k; c++)
            if (r[i][c] > r[i][best]) best = c;
        labels[i] = best;
    }

    return {means, var, pi, labels};
}
