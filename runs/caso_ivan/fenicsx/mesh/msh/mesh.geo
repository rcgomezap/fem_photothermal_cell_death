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
Point(8) = {1, 0, 0, 1.0};
//+
Point(9) = {2, 0.5, 0, 1.0};
//+
Line(1) = {2, 7};
//+
Line(2) = {2, 5};
//+
Line(3) = {5, 6};
//+
Line(4) = {6, 7};
//+
Line(5) = {5, 1};
//+
Line(6) = {1, 8};
//+
Line(7) = {8, 6};
//+
Line(8) = {7, 3};
//+
Line(9) = {3, 9};
//+
Line(10) = {9, 6};
//+
Line(11) = {8, 4};
//+
Line(12) = {4, 9};
//+
Curve Loop(1) = {3, 4, -1, 2};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {5, 6, 7, -3};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {10, -7, 11, 12};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {8, 9, 10, 4};
//+
Plane Surface(4) = {4};
//+
Physical Surface("tumor", 10) = {1};
//+
Physical Surface("tejido", 11) = {2,3,4};
//+
Physical Curve("axis", 12) = {2,5};
//+
Physical Curve("neu", 13) = {6, 11, 12, 9};
//+
Physical Curve("rob", 14) = {1, 8};
//+
Transfinite Surface {1} = {2, 5, 6, 7};
//+
Transfinite Surface {2} = {5, 1, 8, 6};
//+
Transfinite Surface {4} = {7, 6, 9, 3};
//+
Transfinite Surface {3} = {6, 8, 4, 9};
