// Gmsh project created on Wed Sep 27 12:36:57 2023
SetFactory("OpenCASCADE");
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {0, 40, 0, 1.0};
//+
Point(3) = {30, 40, 0, 1.0};
//+
Point(4) = {30, 0, 0, 1.0};
//+
Point(5) = {0, 31, 0, 1.0};
//+
Point(6) = {0, 36, 0, 1.0};
//+
Point(7) = {7.75, 36, 0, 1.0};
//+
Point(8) = {7.75, 31, 0, 1.0};
//+
Line(1) = {6, 5};
//+
Line(2) = {5, 8};
//+
Line(3) = {8, 7};
//+
Line(4) = {7, 6};
//+
Line(5) = {1, 4};
//+
Line(6) = {4, 3};
//+
Line(7) = {3, 2};
//+
Line(8) = {2, 6};
//+
Line(9) = {1, 1};
//+
Line(9) = {1, 5};
//+
Curve Loop(1) = {4, 1, 2, 3};
//+
Surface(1) = {1};
//+
Curve Loop(3) = {9, 2, 3, 4, -8, -7, -6, -5};
//+
Plane Surface(2) = {3};
//+
Physical Curve("axis", 10) = {8, 1, 9};
//+
Physical Curve("convection", 11) = {7};
//+//+
Field[1] = AttractorAnisoCurve;
//+
Field[2] = Ball;
//+
Field[3] = Ball;
//+
Field[3].Radius = 5;
//+
Field[3].Thickness = 5;
//+
Field[3].VIn = 0.02;
//+
Field[3].VOut = 0.5;
//+
Field[3].YCenter = 40;
//+
Delete Field [2];
//+
Delete Field [1];
//+
Background Field = 3;
//+
Field[3].VIn = 0.1;
//+
Field[3].VIn = 0.15;
//+
Field[3].VOut = 2;
//+
Field[3].Thickness = 20;
//+
Field[3].Thickness = 15;
//+
Field[3].VOut = 5;
//+
Field[3].VOut = 2;
//+
Field[3].Thickness = 5;
//+
Field[3].Thickness = 10;
//+
Field[3].VOut = 1;
//+
Field[3].Thickness = 1;
//+
Field[3].Thickness = 20;
//+
Field[3].Thickness = 30;
//+
Field[3].VIn = 0.12;
//+
Field[3].VIn = 0.1;
//+
Physical Surface("agar", 12) = {2};
//+
Physical Surface("agarNP", 13) = {1};
//+
Hide "*";
//+
Show {
  Point{1}; Point{2}; Point{5}; Point{6}; Curve{1}; Curve{8}; Curve{9}; 
}
//+
Show "*";
