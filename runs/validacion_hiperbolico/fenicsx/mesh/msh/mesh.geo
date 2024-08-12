//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {10, 0, 0, 1.0};
//+
Point(3) = {10, 30, 0, 1.0};
//+
Point(4) = {0, 30, 0, 1.0};
//+
Line(1) = {4, 1};
//+
Line(2) = {1, 2};
//+
Line(3) = {2, 3};
//+
Line(4) = {3, 4};
//+
Curve Loop(1) = {1, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Physical Curve("surface", 5) = {4};
//+
Physical Curve("dirichlet", 6) = {3,2};
//+
Physical Surface("domain", 7) = {1};
