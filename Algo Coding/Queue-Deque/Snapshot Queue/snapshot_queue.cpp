/*
Implement a queue with:

push(uuid, x)
pop(uuid)
get_mean(uuid)

where each operation is tagged with an increasing UUID, 
and get_mean(uuid) should return the mean of the queue at that snapshot.
*/

#include<vector>
#include<tuple>
#include<unordered_map>
#include<string>
#include<memory>
#include<stdexcept>

using namespace std;

using ll = long long;

struct Node {
    int val;
    shared_ptr<Node> next;
    Node(int val) : val(val), next(nullptr) {}
};

// (head Node, tail Node, size, run_sum)
using Version = tuple<shared_ptr<Node>, shared_ptr<Node>, int, ll>;

class SnapshotQueue {

    private:
        vector<Version> versions;
        unordered_map<string, int> snapshotID_to_versionIndex;

    public:
        SnapshotQueue() : versions{{nullptr, nullptr, 0, 0}} {}

        void push(const string& uuid, int val) {
            auto [head, tail, size, run_sum] = versions.back();

            /* Update new_version */
            Version new_version;

            auto new_node = make_shared<Node>(val);
            if (head == nullptr) {
                // head and tail shared 'new_node', that's why
                // we use shared_ptr in the first plavec
                new_version = {new_node, new_node, 1, val};
            }
            else {
                tail->next = new_node;
                new_version = {head, new_node, size + 1, run_sum + val};
            }

            versions.push_back(new_version);
            snapshotID_to_versionIndex[uuid] = versions.size() - 1;
            /**/
        }

        int pop(const string& uuid) {
            auto [head, tail, size, run_sum] = versions.back();
            if (head == nullptr) throw runtime_error("pop from empty queue");

            int ans = head->val;
            
            /* Update new version */
            Version new_version;
            if (size == 1) new_version = {nullptr, nullptr, 0, 0};
            else new_version = {head->next, tail, size - 1, run_sum - ans};

            versions.push_back(new_version);
            snapshotID_to_versionIndex[uuid] = versions.size() - 1;
            /**/
            
            return ans;
        }

        double get_mean(const string& uuid) const {
            auto it = snapshotID_to_versionIndex.find(uuid);
            if (it == snapshotID_to_versionIndex.end()) throw runtime_error("Unknown uuid");

            auto [head, tail, size, run_sum] = versions[it->second];
            return (size) ? (double) run_sum / size : 0.0;
        }
};

#include <cassert>
#include <stdexcept>

class Test {
public:
    static void run() {
        test_empty_snapshot();
        test_single_push();
        test_pop_empty_throws();
        test_unknown_uuid_throws();
        test_general_sequence();
    }

private:
    static void test_empty_snapshot() {
        SnapshotQueue q;
        q.push("u1", 10);
        q.pop("u2");
        assert(q.get_mean("u2") == 0.0);
    }

    static void test_single_push() {
        SnapshotQueue q;
        q.push("u1", 7);
        assert(q.get_mean("u1") == 7.0);
    }

    static void test_pop_empty_throws() {
        SnapshotQueue q;
        bool thrown = false;
        try {
            q.pop("u1");
        } catch (const runtime_error&) {
            thrown = true;
        }
        assert(thrown);
    }

    static void test_unknown_uuid_throws() {
        SnapshotQueue q;
        bool thrown = false;
        try {
            q.get_mean("does_not_exist");
        } catch (const runtime_error&) {
            thrown = true;
        }
        assert(thrown);
    }

    static void test_general_sequence() {
        SnapshotQueue q;

        q.push("u1", 10);   // [10]
        q.push("u2", 20);   // [10, 20]
        q.push("u3", 30);   // [10, 20, 30]
        q.pop("u4");        // [20, 30]
        q.push("u5", 40);   // [20, 30, 40]
        q.pop("u6");        // [30, 40]

        assert(q.get_mean("u1") == 10.0);
        assert(q.get_mean("u2") == 15.0);
        assert(q.get_mean("u3") == 20.0);
        assert(q.get_mean("u4") == 25.0);
        assert(q.get_mean("u5") == 30.0);
        assert(q.get_mean("u6") == 35.0);
    }
};

int main() {
    Test::run();
}