// Gmsh project created on Tue Dec 10 09:43:14 2024
SetFactory("OpenCASCADE");
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {10, 0, 0, 1.0};
//+
Point(3) = {10, 10, 0, 1.0};
//+
Point(4) = {0, 10, 0, 1.0};
//+
Point(5) = {0, 8, 0, 1.0};
//+
Point(6) = {2, 8, 0, 1.0};
//+
Point(7) = {2, 10, 0, 1.0};
//+
Point(8) = {2, 8.82, 0, 1.0};
//+
Point(9) = {10, 8.82, 0, 1.0};
//+
Point(10) = {2, 9.42, 0, 1.0};
//+
Point(11) = {10, 9.42, 0, 1.0};
//+
Point(12) = {2, 9.92, 0, 1.0};
//+
Point(13) = {10, 9.92, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 9};
//+
Line(3) = {9, 11};
//+
Line(4) = {11, 13};
//+
Line(5) = {13, 3};
//+
Line(6) = {3, 7};
//+
Line(7) = {7, 4};
//+
Line(9) = {5, 1};
//+
Line(10) = {5, 6};
//+
Line(11) = {6, 8};
//+
Line(12) = {8, 10};
//+
Line(13) = {10, 12};
//+
Line(14) = {12, 7};
//+
Line(15) = {8, 9};
//+
Line(16) = {11, 10};
//+
Line(17) = {12, 13};
//+
Circle(18) = {0, 9, 0, 0.5, 1.5*Pi, 2.5*Pi};
//+
Line(19) = {4, 15};
//+
Line(20) = {15, 14};
//+
Line(21) = {14, 5};
//+
Curve Loop(1) = {18, 20};
//+
Surface(1) = {1};
//+
Curve Loop(3) = {10, 11, 12, 13, 14, 7, 19, -18, 21};
//+
Surface(2) = {3};
//+
Curve Loop(5) = {1, 2, -15, -11, -10, 9};
//+
Surface(3) = {5};
//+
Curve Loop(7) = {12, -16, -3, -15};
//+
Surface(4) = {7};
//+
Curve Loop(9) = {13, 17, -4, 16};
//+
Surface(5) = {9};
//+
Curve Loop(11) = {6, -14, 17, 5};
//+
Surface(6) = {11};
//+
Field[1] = Box;
//+
Field[1].Thickness = 10;
//+
Field[1].VIn = 0.1;
//+
Field[1].VOut = 1;
//+
Field[1].XMax = 4;
//+
Field[1].XMin = -1;
//+
Field[1].YMax = 10;
//+
Field[1].YMin = 8;
//+
Background Field = 1;
//+
Field[2] = Ball;
//+
Field[2].Radius = 0.5;
//+
Field[2].Thickness = 1;
//+
Field[2].VIn = 1;
//+
Field[2].VOut = 1;
//+
Field[2].YCenter = 9;
//+
Background Field = 2;
//+
Field[3] = Box;
//+
Field[3].Thickness = 5;
//+
Field[3].VIn = 0.2;
//+
Field[3].VOut = 1;
//+
Field[3].XMax = 10;
//+
Field[3].XMin = -1;
//+
Field[3].YMax = 10;
//+
Field[3].YMin = 9.42;
//+
Field[4] = MathEval;
//+
Field[4].F = "F1*F2*F3";
//+
Background Field = 4;
//+
Physical Curve("convection", 22) = {7, 6};
//+
Physical Curve("tissue", 23) = {2, 3, 4, 5, 1};
//+
Physical Surface("tumor", 24) = {2};
//+
Physical Surface("tumorNP", 25) = {1};
//+
Physical Surface("epidermis", 26) = {6};
//+
Physical Surface("p-dermis", 27) = {5};
//+
Physical Surface("r-dermis", 28) = {4};
//+
Physical Surface("fat", 29) = {3};
