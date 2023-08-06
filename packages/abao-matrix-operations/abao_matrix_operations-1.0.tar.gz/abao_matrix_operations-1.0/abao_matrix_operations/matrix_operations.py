import numpy as np


class MatrixOperations:
    """
    This class was created for Udacity ML Nanodegree 1st Portfolio Exercise : Upload a Package to Pypi
    by Bilgehan Kılınç.

    Basic Matrix Operations calls for adding, subtracting, unequal addition, matrix multiplication,
    matrix transpose calculation and scalar multiplication.

    Attributes:
    Class assumes operations will be applied on two distinct matrices. Therefore 2 attributes are created.
    matrix_one: numpy(array) representing first matrix inputed by user.
    matrix_two: numpy(array) representing second matrix inputed by user.

    """

    def __init__(self, matrix_one, matrix_two):
        self.matrix_one = matrix_one
        self.matrix_two = matrix_two

    def adding_matrices(self):
        """
        Function to add two matrices.
        Args: None
        Returns: a list or error massage.
        Note: Controls also matrix shapes for math accuracy.
        """
        if self.matrix_one.shape == self.matrix_two.shape:
            return [[self.matrix_one[i, j] + self.matrix_two[i, j] for j in range(self.matrix_two.shape[1])] for i in
                    range(self.matrix_one.shape[0])]
        else:
            print('Math Error')
            print('Addition cannot be performed. Shape of the matrices must be the same!')

    def subtracting_matrices(self):
        """
        Function to subtract two matrices.
        Args: None
        Returns: a list or error massage.
        Note: Controls also matrix shapes for math accuracy.
        """
        if self.matrix_one.shape == self.matrix_two.shape:
            return [[self.matrix_one[i, j] - self.matrix_two[i, j] for j in range(self.matrix_two.shape[1])] for i in
                    range(self.matrix_one.shape[0])]
        else:
            print('Math Error')
            print('Subtraction cannot be performed. Shape of the matrices must be the same!')

    def unequal_dimensions_matrix_addition(self):
        """
        Function to add two different-shaped matrices with special method of unequal matrix addition.
        Args: None
        Returns: a numpy(array) or error massage.
        Note: Controls also matrix shapes for math accuracy.
        """
        if self.matrix_one.shape != self.matrix_two.shape:
            unequal_matrix = np.zeros((self.matrix_one.shape[0] + self.matrix_two.shape[0],
                                       self.matrix_one.shape[1] + self.matrix_two.shape[1]))
            for i in range(self.matrix_one.shape[0]):
                for j in range(self.matrix_one.shape[1]):
                    unequal_matrix[i, j] = self.matrix_one[i, j]
            for k in range(self.matrix_one.shape[0], unequal_matrix.shape[0]):
                for l in range(self.matrix_one.shape[1], unequal_matrix.shape[1]):
                    unequal_matrix[k, l] = self.matrix_two[k - self.matrix_one.shape[0], l - self.matrix_one.shape[1]]
            return unequal_matrix
        else:
            print('Math Error')
            print('Use adding_matrices method. Your matrices have the same shape!')

    def multiplying_two_matrices(self):
        """
        Function to multiply/dot product two matrices.
        Args: None
        Returns: a numpy(array) or error massage.
        Note: Controls also matrix shapes for math accuracy.
        """
        multiplied_matrix = np.zeros((self.matrix_one.shape[0], self.matrix_two.shape[1]))
        if self.matrix_one.shape[1] == self.matrix_two.shape[0]:
            for i in range(self.matrix_one.shape[0]):
                for j in range(self.matrix_two.shape[0]):
                    multiplied_matrix[i] += self.matrix_one[i, j] * self.matrix_two[j, i]
            return multiplied_matrix
        else:
            print('Math Error')
            print('Multiplication cannot be performed. # of columns on the first matrix should be equal to # of rows '
                  'on the second matrix!')

    @staticmethod
    def transpose_of_matrix(given_matrix):
        """
        Static Method to transpose a matrix.
        Args: given_matrix: numpy(array) or a list
        Returns: a list
        """
        return [[given_matrix[j, i] for j in range(given_matrix.shape[0])] for i in range(given_matrix.shape[1])]

    @staticmethod
    def scalar_multiplication(given_matrix, multiplier):
        """
        Static Method to multiply a matrix with a numeric value.
        Args: given_matrix: numpy(array) or a list
              multiplier: an int or a float
        Returns: a list
        """
        return [[(multiplier * given_matrix[i, j]) for j in range(given_matrix.shape[1])] for i in
                range(given_matrix.shape[0])]
