from ..lib.quantumics import QUnit, QTUnit, QData

	


def test_qunit_declaration(config):

	#Test Data Declaration
	x0 = (3, "Hello"); y0 = QUnit(3,"Hello")
	x1 = (2, 5); y1 = QUnit(2, 5);
	x2 = (3, (4, 4)); y2 = QUnit(3, (4, 4))
	x3 = (2, (5, 4, 2)); y3 = QUnit(2, (5, 4, 2));
	x4 = (complex(2, 5), ((4, 2), 3)); y4 = QUnit(complex(2, 5), ((4, 2), 3));
	x5 = (2, ((5, 4, 2, 3), {"hello": "world"}, {"machine":"learning"}));
	y5 = QUnit(2, ((5, 4, 2, 3), {"hello": "world"}, {"machine":"learning"}));

	#Checking
	print("(x0, y0): %s", assertEqual(QUnit(x0), y0))
	print("(x1, y1): %s", assertEqual(QUnit(x1), y1))
	print("(x2, y2): %s", assertEqual(QUnit(x2), y2))
	print("(x3, y3): %s", assertEqual(QUnit(x3), y3))
	print("(x4, y4): %s", assertEqual(QUnit(x4), y4))
	print("(x5, y5): %s", assertEqual(QUnit(x5), y5))



def test_qunit_transpose(config):

	#Test Data Declaration
	x0 = QUnit(3, "Hello"); y0 = QTUnit(3, "Hello")
	x1 = QUnit(complex(2, 4), 5); y1 = QTUnit(complex(2, -4), 5);
	x2 = QUnit(complex(3, 3), (4, 4)); y2 = QTUnit(complex(3, -3), (4, 4))
	x3 = QUnit(2, (5, 4, 2)); y3 = QTUnit(2, (5, 4, 2));
	x4 = QUnit(complex(2, 5), (5, (4, 2), 3)); y4 = QTUnit(complex(2, -5), (5, (4, 2), 3));
	x5 = QUnit(complex(4, 7), ((5, 4, 2, 3), {"hello": "world"}, {"machine":"learning"}));
	y5 = QTUnit(complex(4, -7), ((5, 4, 2, 3), {"hello": "world"}, {"machine":"learning"}))

	#Checking
	print("(x0, y0): %s", assertEqual(x0.t(), y0))
	print("(x1, y1): %s", assertEqual(x1.t(), y1))
	print("(x2, y2): %s", assertEqual(x2.t(), y2))
	print("(x3, y3): %s", assertEqual(x3.t(), y3))
	print("(x4, y4): %s", assertEqual(x4.t(), y4))
	print("(x5, y5): %s", assertEqual(x5.t(), y5))



def test_qunit_add(config):
	
	#Test Data Declaration
	x0 = QUnit(complex(3),); y0 = QUnit(complex(3),); z0 = QData([QUnit(complex(6),)]);
	x1 = QUnit(complex(2), 5); y1 = QUnit(complex(2), 2); z1 = QData([QUnit(complex(2), 5), QUnit(complex(2), 2)]); 
	x2 = QUnit(complex(3), (4, 4)); y2 = QUnit(complex(3), (4, 4)); z2 = QData([QUnit(complex(6), (4, 4))])
	x3 = QUnit(complex(2), (5, 4, 2)); y3 = QUnit(complex(2), (5, 4, 1)); 
	z3 = QData([QUnit((complex(2), (5, 4, 2))), QUnit(complex(2), (5, 4, 1))]);
	x4 = QUnit(complex(2), (5, 4, 2, 3)); y4 = QUnit(complex(2, 6) (5, 4, 2, 3));
	z4 = QData([QUnit(complex(4, 6), (5, 4, 2, 3))]);
	x5 = QUnit(complex(2, 3), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	y5 = QUnit(complex(2, 5), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	z5 = QUnit(complex(4, 8), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	x6 = QUnit(complex(1), 5); y6 = QUnit(complex(3),5); z6 = QData([QUnit(complex(4),5)]);
	x7 = QUnit(complex(1), 3); y7 = QUnit(complex(3),5); z7 = QData([QUnit(complex(1),3), QUnit(complex(3),5)]);

	#Checking 
	print("(x0, y0, z0): %s", assertEqual(x0+y0, z0))
	print("(x1, y1, z1): %s", assertEqual(x1+y1, z1))
	print("(x2, y2, z2): %s", assertEqual(x2+y2, z2))
	print("(x3, y3, z3): %s", assertEqual(x3+y3, z3))
	print("(x4, y4, z4): %s", assertEqual(x4+y4, z4))
	print("(x5, y5, z5): %s", assertEqual(x5+y5, z5))
	print("(x6, y6, z6): %s", assertEqual(x6+y6, z6))
	print("(x7, y7, z7): %s", assertEqual(x7+y7, z7))



def test_qunit_sub(config):
	#Test Data Declaration
	x0 = QUnit(complex(3),); y0 = QUnit(complex(3),); z0 = QData([QUnit(0,)]);
	x1 = QUnit(complex(2), 5); y1 = QUnit(complex(2), 2); z1 = QData([QUnit(complex(2), 5), QUnit(complex(-2), 2)]); 
	x2 = QUnit(complex(3), (4, 4)); y2 = QUnit(complex(3), (4, 4)); z2 = QData([QUnit(0, (4, 4))])
	x3 = QUnit(complex(2), (5, 4, 2)); y3 = QUnit(complex(2), (5, 4, 1)); 
	z3 = QData([QUnit(complex(2), (5, 4, 2)), QUnit(complex(-2), (5, 4, 1))]);
	x4 = QUnit(complex(2), (5, 4, 2, 3)); y4 = QUnit(complex(2, 6) (5, 4, 2, 3));
	z4 = QData([QUnit(complex(0, -6), (5, 4, 2, 3))]);
	x5 = QUnit(complex(2, 3), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	y5 = QUnit(complex(2, 5), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	z5 = QUnit(complex(0, -2), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	x6 = QUnit(complex(1), 5); y6 = QUnit(complex(3),5); z6 = QData([QUnit(complex(-2),5)]);
	x7 = QUnit(complex(1), 3); y7 = QUnit(complex(3),5); z7 = QData([QUnit(complex(1),3), QUnit(complex(-3),5)]);

	#Checking 
	print("(x0, y0, z0): %s", assertEqual(x0-y0, z0))
	print("(x1, y1, z1): %s", assertEqual(x1-y1, z1))
	print("(x2, y2, z2): %s", assertEqual(x2-y2, z2))
	print("(x3, y3, z3): %s", assertEqual(x3-y3, z3))
	print("(x4, y4, z4): %s", assertEqual(x4-y4, z4))
	print("(x5, y5, z5): %s", assertEqual(x5-y5, z5))
	print("(x6, y6, z6): %s", assertEqual(x6-y6, z6))
	print("(x7, y7, z7): %s", assertEqual(x7-y7, z7))



def test_qunit_outer_product(config):

	#Test Data Declaration
	x0 = QUnit(complex(3), "Hello"); y0 = QTUnit(complex(3), "Hi"); z0 = QOperator(complex(9), "Hello", "Hi")
	x1 = QUnit(complex(2), 5); y1 = QTUnit(complex(2), 2); z1 = QOperator(complex(4), 5, 2)
	x2 = QUnit(complex(3), (4, 4)); y2 = QTUnit(3, (4, 4)); z2 = QOperator(complex(9), (4,4), (4,4))
	x3 = QUnit(complex(2), (5, 4, 2)); y3 = QTUnit(complex(2), (5, 4, 1)); 
	z3 = QOperator(complex(6), (5, 4, 2), (5, 4, 1));
	x4 = QUnit(complex(2), (5, 4, 2, 3)); y4 = QTUnit(complex(2, 6), (5, 4, 2, 3));
	z4 = QOperator(complex(2, 12), (5, 4, 2, 3), (5, 4, 2, 3))
	x5 = QUnit(complex(2, 3), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	y5 = QTUnit(complex((2, 5), (4, 2, 3, {"hello": "world"}, {"machine":"learning"})));
	z5 = QOperator(complex(-9, 16), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}), 
		(4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	x6 = QUnit(complex(1),5); y6 = QTUnit(complex(3),5); z6 = QOperator(complex(3), 5, 5)
	x7 = QUnit(complex(1),3); y7 = QTUnit(complex(3),5); z7 = QOperator(complex(3), 3, 5)

	#Checking 
	print("(x0, y0, z0): %s", assertEqual(x0*y0, z0))
	print("(x1, y1, z1): %s", assertEqual(x1*y1, z1))
	print("(x2, y2, z2): %s", assertEqual(x2*y2, z2))
	print("(x3, y3, z3): %s", assertEqual(x3*y3, z3))
	print("(x4, y4, z4): %s", assertEqual(x4*y4, z4))
	print("(x5, y5, z5): %s", assertEqual(x5*y5, z5))
	print("(x6, y6, z6): %s", assertEqual(x6*y6, z6))
	print("(x7, y7, z7): %s", assertEqual(x7*y7, z7))



def test_qunit_inner_product(config):
	#Test Data Declaration
	x0 = QTUnit(complex(3), "Hello"); y0 = QUnit(complex(3), "Hello"); z0 = complex(9)
	x1 = QTUnit(complex(2), 5); y1 = QUnit(complex(2), 2); z1 = 0; 
	x2 = QTUnit(complex(3), (4, 4)); y2 = QUnit(complex(3), (4, 4)); z2 = 9;
	x3 = QTUnit(complex(2), (5, 4, 2)); y3 = QUnit(complex(2), (5, 4, 1)); z3 = 0;
	x4 = QTUnit(complex(2), (5, 4, 2, 3)); y4 = QUnit(complex(2, 6) (5, 4, 2, 3));
	z4 = complex(4, 12)
	x5 = QTUnit(complex(2, 3), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	y5 = QUnit(complex(2, 5), complex(4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	z5 = complex(-9, 16)
	x6 = QTUnit(complex(1), 5); y6 = QUnit((3,5)); z6 = complex(3)
	x7 = QTUnit(complex(1), 3); y7 = QUnit((3,5)); z7 = complex(3)

	#Checking
	print("(x0, y0, z0): %s", assertEqual(x0*y0, z0))
	print("(x1, y1, z1): %s", assertEqual(x1*y1, z1))
	print("(x2, y2, z2): %s", assertEqual(x2*y2, z2))
	print("(x3, y3, z3): %s", assertEqual(x3*y3, z3))
	print("(x4, y4, z4): %s", assertEqual(x4*y4, z4))
	print("(x5, y5, z5): %s", assertEqual(x5*y5, z5))
	print("(x6, y6, z6): %s", assertEqual(x6*y6, z6))
	print("(x7, y7, z7): %s", assertEqual(x7*y7, z7))



def test_qunit_tensor_product(config):
	#Test Data Declaration
	x0 = QUnit(3, "Hello"); y0 = QUnit(3,"Hi"); z0 = QUnit(complex(3), ("Hello", "Hi"))
	x1 = QUnit(2, 5); y1 = QUnit(2, 2); z1 = QUnit(complex(4), (5, 2)); 
	x2 = QUnit(3, (4, 4)); y2 = QUnit(3, (4, 4)); z2 = QUnit(complex(9), ((4,4), (4,4)));
	x3 = QUnit(2, (5, 4, 2)); y3 = QUnit(2, (5, 4, 1)); 
	z3 = QUnit(complex(4), ((5,4,2), (5,4,1)));
	x4 = QUnit(complex(2), (5, 4, 2, 3)); y4 = QUnit(complex(2, 6) (5, 4, 2, 3));
	z4 = QData([QUnit((complex(4, 12), (5, 4, 2, 3), (5, 4, 2, 3)))]);
	x5 = QUnit(complex(2, 3), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	y5 = QUnit(complex(2, 5), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	z5 = QUnit(complex(-9, 16), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	x6 = QUnit(complex(1), 5); y6 = QUnit(complex(3), 5); z6 = QUnit(complex(3), (5, 5));
	x7 = QUnit(complex(1), 3); y7 = QUnit(complex(3), 5); z7 = QUnit(complex(3), (3, 5));

	#Checking
	print("(x0, y0, z0): %s", assertEqual(x0*y0, z0))
	print("(x1, y1, z1): %s", assertEqual(x1*y1, z1))
	print("(x2, y2, z2): %s", assertEqual(x2*y2, z2))
	print("(x3, y3, z3): %s", assertEqual(x3*y3, z3))
	print("(x4, y4, z4): %s", assertEqual(x4*y4, z4))
	print("(x5, y5, z5): %s", assertEqual(x5*y5, z5))
	print("(x6, y6, z6): %s", assertEqual(x6*y6, z6))
	print("(x7, y7, z7): %s", assertEqual(x7*y7, z7))




def test_qunit_split(config):
	#Test Data Declaration
	x0 = QUnit(3, "Hello"); y0 = QUnit(3, "Hi"); z0 = QUnit(complex(9), ("Hello","Hi"))
	x1 = QUnit(2, 5); y1 = QUnit(2, 2); z1 = QUnit(complex(4), (5, 2)); 
	x2 = QUnit(3, (4, 4)); y2 = QUnit(3, (4, 4)); z2 = QUnit(complex(9), ((4,4), (4,4)));
	x3 = QUnit(2, (5, 4, 2)); y3 = QUnit(2, (5, 4, 1)); 
	z3 = QUnit(complex(4), ((5,4,2), (5,4,1)));
	x4 = QUnit(complex(2), (5, 4, 2, 3)); y4 = QUnit(complex(2, 6) (5, 4, 2, 3));
	z4 = QData([QUnit(complex(4, 12), (5, 4, 2, 3), (5, 4, 2, 3))]);
	x5 = QUnit(complex(2, 3), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	y5 = QUnit(complex(2, 5), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	z5 = QUnit(complex(-9, 16), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}), (4, 2, 3, {"hello": "world"}, {"machine":"learning"}));
	x6 = QUnit(complex(1), 5); y6 = QUnit((complex(3), 5)); z6 = QUnit(complex(3), (5, 5));
	x7 = QUnit(complex(1), 3); y7 = QUnit((complex(3), 5)); z7 = QUnit(complex(3), (3, 5));

	#Checking
	print("(x0, y0, z0): %s", assertEqual((x0, y0), z0.split((1,1))))
	print("(x1, y1, z1): %s", assertEqual((x1, y1), z1.split((1,1))))
	print("(x2, y2, z2): %s", assertEqual((x2, y2), z2.split((1,1))))
	print("(x3, y3, z3): %s", assertEqual((x3, y3), z3.split((1, 1))))
	print("(x4, y4, z4): %s", assertEqual((x4, y4), z4.split((2, complex(2, 6)))))
	print("(x5, y5, z5): %s", assertEqual((x5, y5), z5.split((complex(2, 3), complex(2, 5)))))
	print("(x6, y6, z6): %s", assertEqual((x6, y6), z6.split((1, 3))))
	print("(x7, y7, z7): %s", assertEqual((x7, y7), z7.split((1, 3))))





if __name__ == "__main__":
	config = {};
	test_qunit_declaration(config);
	test_qunit_transpose(config);
	test_qunit_add(config);
	test_qunit_sub(config);
	test_qunit_outer_product(config);
	test_qunit_inner_product(config);
	test_qunit_tensor_product(config);
	test_qunit_split(config);




