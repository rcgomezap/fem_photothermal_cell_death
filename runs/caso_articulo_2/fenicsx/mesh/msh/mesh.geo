//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {3, 0, 0, 1.0};
//+
Point(3) = {3, 3, 0, 1.0};
//+
Point(4) = {0, 3, 0, 1.0};
//+
Point(5) = {0, 1, 0, 1.0};
//+
Point(6) = {0, 2, 0, 1.0};
//+
Point(7) = {0, 1.5, 0, 1.0};
//+
Circle(1) = {5, 7, 6};
//+
Line(2) = {4, 6};
//+
Line(3) = {6, 7};
//+
Line(4) = {7, 5};
//+
Line(5) = {5, 1};
//+
Line(6) = {1, 2};
//+
Line(7) = {2, 3};
//+
Line(8) = {3, 4};
//+
Curve Loop(1) = {1, 3, 4};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {2, -1, 5, 6, 7, 8};
//+
Plane Surface(2) = {2};
//+
Physical Curve("conv", 9) = {8};
//+
Physical Curve("else", 10) = {7, 6};
//+
Physical Surface("agar", 11) = {2};
//+
Physical Surface("agar_icg", 12) = {1};
//+
Field[1] = Ball;
//+
Field[1].Thickness = 2.5;
//+
Field[1].VIn = 0.01;
//+
Field[1].VOut = 0.2;
//+
Field[1].YCenter = 1.5;
//+
Background Field = 1;
//+
Field[1].Radius = 0.6;
