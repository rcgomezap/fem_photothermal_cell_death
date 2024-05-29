//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {3.5, 0, 0, 1.0};
//+
Point(3) = {3.5, 7.8, 0, 1.0};
//+
Point(4) = {0, 7.8, 0, 1.0};
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
Physical Curve("side", 6) = {3};
//+
Field[1] = Box;
//+
Field[1].Thickness = 3;
//+
Field[1].VIn = 0.125;
//+
Field[1].VOut = 0.5;
//+
Field[1].XMax = 1.5;
//+
Field[1].YMax = 7.8;
//+
Field[1].YMin = 6;
//+
Background Field = 1;
//+
Physical Surface("domain", 7) = {1};
