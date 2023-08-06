import unittest
import numpy as np
from abao_matrix_operations import MatrixOperations


class TestMatrixOperations(unittest.TestCase):
    def setUp(self):
        self.matrix_one = np.zeros((3, 3))
        self.matrix_two = np.ones((3, 3))
        self.matrix_three = 3 * np.ones((3, 1))
        self.matrix_four = 5 * np.ones((1, 3))
        self.operation_1 = MatrixOperations(self.matrix_one, self.matrix_two)
        self.operation_2 = MatrixOperations(self.matrix_two, self.matrix_three)
        self.operation_3 = MatrixOperations(self.matrix_three, self.matrix_four)
        self.operation_4 = MatrixOperations(self.matrix_two, self.matrix_four)

    def test_adding_matrices(self):
        self.assertEqual(self.operation_1.adding_matrices(), np.add(self.matrix_one, self.matrix_two).tolist(),
                         'Correct Add Operation')
        self.assertEqual(self.operation_2.adding_matrices(), None, 'Correct Add Operation')

    def test_subtracting_matrices(self):
        self.assertEqual(self.operation_1.subtracting_matrices(),
                         np.subtract(self.matrix_one, self.matrix_two).tolist(), 'Correct Sub Operation')
        self.assertEqual(self.operation_2.subtracting_matrices(), None, 'Correct Sub Operation')

    def test_unequal_dimensions_matrix_addition(self):
        self.assertMultiLineEqual(str(self.operation_2.unequal_dimensions_matrix_addition()),
                                  "[[1. 1. 1. 0.]\n [1. 1. 1. 0.]\n [1. 1. 1. 0.]\n [0. 0. 0. 3.]\n [0. 0. 0. 3.]\n "
                                  "[0. 0. 0. 3.]]",
                                  'Correct Unqeual Add Operation')
        self.assertEqual(self.operation_1.unequal_dimensions_matrix_addition(), None, 'Correct Unqeual Add Operation')

    def test_multiplying_two_matrices(self):
        self.assertMultiLineEqual(str(self.operation_3.multiplying_two_matrices()),
                                  str(np.dot(self.matrix_three, self.matrix_four)), 'Correct Multiplication Operation')
        self.assertEqual(self.operation_4.multiplying_two_matrices(), None, 'Correct Multiplication Operation')

    def test_transpose_of_matrix(self):
        self.assertMultiLineEqual(str(self.operation_2.transpose_of_matrix(self.matrix_three)),
                                  str(np.transpose(self.matrix_three).tolist()), 'Correct Transpose Operation')

    def test_scalar_multiplication(self):
        self.assertEqual(self.operation_2.scalar_multiplication(self.matrix_two, 3),
                         np.multiply(3, self.matrix_two).tolist(), 'Correct Scalar Operation')


tests = TestMatrixOperations()
tests_loaded = unittest.TestLoader().loadTestsFromModule(tests)
unittest.TextTestRunner().run(tests_loaded)
