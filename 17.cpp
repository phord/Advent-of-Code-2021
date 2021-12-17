// Try day 17 from scratch.  My python code got stuck somewhere.

#include <iostream>

using namespace std;
struct Point {
    int x;
    int y;
};

struct Velocity {
    int dx;
    int dy;
};

struct Rect {
    Point tl, br;
    int top, left, bottom, right;
    Rect(int x1, int x2, int y1, int y2) {
        top = max(y1,y2);
        left = min(x1,x2);
        bottom = min(y1,y2);
        right = max(x1,x2);
    }

    bool hit(Point p) const
    {
        return left <= p.x && right >= p.x && top >= p.y && bottom <= p.y;
    }

    bool missed(Point const &p, Velocity const &v) const
    {
        return  (v.dx >= 0 && p.x > right) ||
                (v.dx <= 0 && p.x < left) ||
                (v.dy < 0 && p.y < bottom);
    }
};

void step(Point &p, Velocity &v)
{
    p.x += v.dx;
    p.y += v.dy;

    v.dx -= !!v.dx;
    v.dy -= 1;
}

bool track_probe(Rect const & target, Point &p, Velocity &v)
{
    while (true) {
        step(p, v);
        if (target.hit(p))       return true;
        if (target.missed(p, v)) return false;
    }
}

// Just a hack to make track_probe simpler
int apex(Velocity v)
{
    if (v.dy < 0) return 0;
    Point p{0, 0};
    while (v.dy > 0) {
        step(p, v);
    }
    return p.y;
}

int main() {
    Rect target(20, 30, -10,-5);
    target = {175, 227, -134, -79};

    Point pos;
    Velocity vel;

    // If dy is positive at 0 , it will be negative the same value when we reach zero again.
    // If it is greater than target.bottom at that point, we will miss the target.  So upper bound
    // for dy is abs(target.bottom). But target is always negative, so...
    int DYMAX = -target.bottom;

    int highest = 0;
    int count = 0;
    for (int dx = 0; dx <= target.right; dx++ ) {
        for (int dy = target.bottom; dy <= DYMAX; dy++) {
            pos = {0,0};
            vel = {dx, dy};
            if (track_probe(target, pos, vel)) {
                ++count;
                int h = apex({dx, dy});
                if (h > highest) {
                    highest = h;
                }
            }
        }
    }
    cout << "Highest = " << highest << "\n";
    cout << "total = " << count << "\n";
    return 0;
}