#include <iostream>
#include <fstream>
#include <sstream>

#include <vector>
#include <set>
#include <unordered_set>
#include <algorithm>

using namespace std;

struct Point {
    int x, y, z;

    bool operator==(const Point& rhs) const {
        return rhs.x == x && rhs.y ==y && rhs.z == z;
    }

    bool operator<(const Point& rhs) const {
        return rhs.x < x ||
            (rhs.x == x && rhs.y < y) ||
            (rhs.y == y && rhs.z < z);
    }

    Point operator+(const Point& rhs) const {
        return {rhs.x + x, rhs.y + y, rhs.z + z};
    }

    Point operator-(const Point& rhs) const {
        return {x - rhs.x , y - rhs.y , z - rhs.z };
    }

    int manhattan_dist(Point q) {
        auto diff = *this - q;
        return abs(diff.x) + abs(diff.y) + abs(diff.z);
    }
};

ostream& operator<<(ostream& os, const Point& p)
{
    os << p.x << ',' << p.y << ',' << p.z;
    return os;
}


using Beacons = set<Point>;
struct Scanner {
    int id;
    Point offset;
    Beacons beacons;
    set<Beacons> rotations;
    set<int> fingerprint;

    Scanner() {
        rotations.insert({});
    }

    // Fingerprint is a quick and dirty discriminator for potential overlapping scanner cubes.  An overlapping cube has
    // to have at least 12 points in common.  This fingerprint holds all the distances between every pair of beacons. If
    // our cube overlaps another, we should have at least 11 + 10 + 9 + ... + 2 + 1 = 12 * 5.5 = 66 distances in common.
    // But we keep a set and some distances may be duplicated. So this could be quite wrong. Fortunately for my puzzle
    // input, it was not.
    // Someone else had the clever idea to record triangles (3 distances?).  This would probably be safer.
    void gen_fingerprint() {
        for (auto a : beacons) {
            for (auto b : beacons) {
                auto d = a.manhattan_dist(b);
                if (d) fingerprint.insert(d);
            }
        }
    }

    bool maybe_has_overlap(Scanner const &rhs) const {
        set<int> result;
        set_intersection(fingerprint.begin(), fingerprint.end(), rhs.fingerprint.begin(), rhs.fingerprint.end(),
                        std::inserter(result, result.begin()));
        return result.size() > 50;
    }
};

using Scanners = vector<Scanner>;

Scanners parse() {
    Scanners inp;
    ifstream infile("19.txt");
    // ifstream infile("sample.txt");
    string line;

    while (getline(infile, line)) {
        if (line.empty()) {
            continue;
        } else if (line.find("scanner") != string::npos) {
            inp.push_back({});
            continue;
        }

        stringstream ss;
        ss << line;
        int x, y, z;
        char comma;

        ss >> x >> comma >> y >> comma >> z;
        // cout << line << "   " << x << ", " << y << ", " <<z  <<"\n";
        auto beac = inp.back().beacons.insert({x, y, z});
        inp.back().id = inp.size()-1;
    }
    return inp;
}

Point rotate_x(Point p) {
    return {p.x, p.z, -p.y};
}
Point rotate_y(Point p) {
    return {-p.z, p.y, p.x};
}
Point rotate_z(Point p) {
    return {-p.y, p.x, p.z};
}
Beacons rotate_x(Beacons const & b) {
    Beacons nb;
    for ( auto const p : b )
        nb.insert(rotate_x(p));
    return nb;
}
Beacons rotate_y(Beacons const & b) {
    Beacons nb;
    for ( auto const p : b )
        nb.insert(rotate_y(p));
    return nb;
}
Beacons rotate_z(Beacons const & b) {
    Beacons nb;
    for ( auto const p : b )
        nb.insert(rotate_z(p));
    return nb;
}

// Generate all the rotations of the beacons in the scanner range
void rotate_all(Scanner & scan) {
    Beacons const & b = scan.beacons;

    Beacons r = b;
    // cout << "rotate_all " << r.size() << endl;
    for (int x=0; x < 4; x++) {
        for (int y=0; y < 4; y++) {
            for (int z=0; z < 4; z++) {
                scan.rotations.insert(r);
                r = rotate_z(r);
            }
            r = rotate_y(r);
        }
        r = rotate_x(r);
    }
}

// This is complex (big-O) because we repeatedly translate beacons for trials.  A faster
// method is to fingerprint the beaconspace by calculating distances between beacons and then
// deciding if there are 12 beacons' worth of common distances.
Beacons translate(Beacons & b, Point tx) {
    Beacons ans;
    // cout << tx << endl;
    for (auto const p : b) {
        // cout << "  " << p << "   ->   " << p + tx << endl;
        ans.insert(p + tx);
    }
    return ans;
}

// If two scanners have 12 beacons in common when translated and rotated, return the whole translated and rotated set from t
Scanner overlap(Scanner const & s, Scanner const & t) {
    if (!s.maybe_has_overlap(t))
        return {};

    auto const & sb = s.beacons;
    for (auto sp : sb) {
        for (auto tb: t.rotations) {
            for (auto tp : tb) {
                auto torigin = sp - tp;
                auto trial = translate(tb, torigin);
                Beacons result;
                set_intersection(sb.begin(), sb.end(), trial.begin(), trial.end(),
                                std::inserter(result, result.begin()));
                if (result.size() >= 12) {
                    cout << "Found match between "<< s.id << "-"<< t.id << " at " << torigin << "\n";
                    Scanner ns = t;
                    ns.beacons = std::move(trial);
                    ns.offset = torigin;
                    ns.rotations.clear();
                    return ns;
                }
            }
        }
    }
    // cout << "  no match: "<< s.id << "-"<< t.id << "\n";
    return {};
}

int main() {
    auto scanners = parse();
    for (auto & s: scanners) {
        rotate_all(s);
        s.gen_fingerprint();
    }

    // Pick a scanner to be the "real" coordinates
    auto const & s0 = scanners[0];

    vector<Scanner> fixed = {s0};
    vector<Scanner> unknown;
    for (int i = 1; i < scanners.size(); i++) {
        unknown.push_back(scanners[i]);
    }

    Beacons map = s0.beacons;

    // Hack: store scanner locations in this faux scanner structure so we can use fingerprint for part 2.
    Scanner scanner_positions;
    while (unknown.size()) {
        vector<Scanner> new_unknown;
        vector<Scanner> new_fixed;
        for (auto const & t : unknown) {
            bool found = false;
            for (auto const & s : fixed) {

                auto match = overlap(s, t);

                if (!match.beacons.empty()) {
                    map.insert(match.beacons.begin(), match.beacons.end());
                    scanner_positions.beacons.insert(match.offset);
                    new_fixed.push_back(std::move(match));
                    found = true;
                    break;
                }
            }
            if (!found) new_unknown.push_back(std::move(t));
        }
        unknown = std::move(new_unknown);
        fixed = std::move(new_fixed);
        if (fixed.empty() && !unknown.empty()) {
            cout << "Error: still have " << unknown.size() << " scanners to map\n";
        }
    }

    scanner_positions.gen_fingerprint();
    cout << map.size() << " " << *scanner_positions.fingerprint.crbegin() << endl;
    return 0;
}