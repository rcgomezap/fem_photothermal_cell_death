//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {0, 1, 0, 1.0};
//+
Point(3) = {2, 1, 0, 1.0};
//+
Point(4) = {2, 0, 0, 1.0};
//+
Point(5) = {0, 0.5, 0, 1.0};
//+
Point(6) = {1, 0.5, 0, 1.0};
//+
Point(7) = {1, 1, 0, 1.0};
//+
Line(1) = {2, 7};
//+
Line(2) = {2, 7};
//+
Line(3) = {7, 6};
//+
Line(4) = {6, 5};
//+
Line(5) = {2, 5};
//+
Curve Loop(1) = {1, 3, 4, -5};
//+
Surface(1) = {1};
//+
Line(6) = {5, 1};
//+
Line(7) = {1, 4};
//+
Line(8) = {4, 3};
//+
Line(9) = {3, 7};
//+
Curve Loop(2) = {7, 8, 9, 3, 4, 6};
//+
Surface(2) = {2};
//+
Surface(2) = {2};
//+
Plane Surface(2) = {2};
//+
Physical Surface("tumor", 10) = {1};
//+
Surface(3) = {2};
//+
Physical Surface("tejido", 11) = {2};
//+
Physical Curve("axis", 12) = {5};
//+
Physical Curve("neu", 13) = {7, 8};
//+
Physical Curve("rob", 14) = {9, 1};
//+//+
Field[1] = Box;
//+
Field[1].Thickness = 6;
//+
Field[1].VIn = 0.01;
//+
Field[1].VOut = 0.5;
//+
Field[1].XMax = 1;
//+
Field[1].YMax = 1;
//+
Field[1].YMin = 0.995;
//+
Background Field = 1;
