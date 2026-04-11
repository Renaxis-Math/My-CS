/*
You're given an array of sentences and an array of times (both of length n)
sentences[i] represents a previously typed sentence
times[i] represents how many times that sentence was typed
How the System Works:

Users input characters one by one to form a sentence
Each sentence ends with the special character '#'
For each character typed (except '#'), the system returns the top 3 most frequent sentences that start with the prefix typed so far
Ranking Rules:

Sentences are ranked by their "hot degree" (frequency of being typed)
Higher frequency sentences appear first
If two sentences have the same frequency, they're sorted in ASCII order (lexicographically)
If fewer than 3 matching sentences exist, return all available matches
Special Behavior:

When '#' is input, it means the current sentence is complete
The completed sentence is added to the system (increasing its count by 1 if it already exists)
After '#' is input, return an empty list and reset for the next sentence
*/

#include<memory>
#include<string>
#include<unordered_map>
#include<algorithm>
#include<vector>

using namespace std;

struct Node {
    unordered_map<char, unique_ptr<Node>> children;
    bool is_end = false; // is_end = is end of sentence.
    vector<string> top3_strings;

    void add_child(char ch) {
        Node* child = next(ch);
        if (!child) children.emplace(ch, make_unique<Node>());
    }

    Node* next(char ch) {
        return (children.contains(ch)) ? 
            children.at(ch).get() : nullptr;
    }

    void refresh_top3(
        string& new_sentence, 
        unordered_map<string, int>& sentence_count_map) {

        // check if new sentence exists already. if not, add
        bool is_exist = false;
        for (auto& str : top3_strings) {
            is_exist = (str == new_sentence);
            if (is_exist) break;
        }
        if (!is_exist) top3_strings.emplace_back(new_sentence);

        // desc sort
        sort(
            top3_strings.begin(), top3_strings.end(),
            [&](string& a, string& b) {
                if (sentence_count_map[a] != sentence_count_map[b]) {
                    return sentence_count_map[a] > sentence_count_map[b];
                }
                return a < b;
            }
        );
        
        // pop redundant
        if (top3_strings.size() > 3) top3_strings.pop_back();
    }
};

class Trie {
    Node root;
    unordered_map<string, int> sentence_count_map;

    public:
        Trie() {}

        Node* get_root() { return &root; }

        void insert(string& sentence, int insert_count) {

            // update properties
            sentence_count_map[sentence] += insert_count;

            // update trie
            Node* cur = get_root();
            for (char ch : sentence) {
                cur->add_child(ch);
                cur = cur->next(ch);

                // update node property
                cur->refresh_top3(sentence, sentence_count_map);
            }
            cur->is_end = true;
        }
};

class AutoComplete {
    Trie trie;
    string query_sentence;
    Node* cur_node;

public:
    AutoComplete(vector<string>& sentences, vector<int>& times) {
        for (int i = 0; i < sentences.size(); ++i) {
            trie.insert(sentences[i], times[i]);
        }
        cur_node = trie.get_root();
    }

    vector<string> input(char c) {
        if (c != '#') {
            query_sentence.push_back(c);
            cur_node = cur_node ? cur_node->next(c) : nullptr;
            return cur_node ? cur_node->top3_strings : vector<string>{};
        }
        else { // end of sentence
            trie.insert(query_sentence, 1);
            query_sentence = "";
            cur_node = trie.get_root();
            return {};
        }
    }
};