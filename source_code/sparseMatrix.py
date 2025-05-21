#!/usr/bin/python3
import ast
import os

class SparseMatrix:
    """ This class holds a sparse matrix implementation for adding, subtracting,
    multiplying of sparse matrices and writing the sparse_result to a file
    """
    def __init__(self, sample_file='', row_count=0, col_count=0):
        self.row_count = row_count
        self.col_count = col_count
        self.sparse_elems = {}

        if sample_file:
            self.load_sample_file(sample_file)

    def load_sample_file(self, sample_file):
        """ imports the matrix dataset from the given file """
        try:
            with open(sample_file, 'r') as file_lines:
                # read number of row and col in the file
                all_rows = file_lines.readline()[5:]
                all_cols = file_lines.readline()[5:]

                self.row_count, self.col_count = int(all_rows), int(all_cols)

                for read_line in file_lines:
                    read_line = read_line.strip()
                    if read_line:
                        # handle wrong formats: float values or different brackets
                        try:
                            data = ast.literal_eval(read_line)
                            if (
                                isinstance(data, tuple)
                                and len(data) == 3
                                and all(isinstance(i, int) for i in data)
                            ):
                                row, col, value = data

                                if value != 0:
                                    self.sparse_elems[(row, col)] = value
                            else:
                                raise ValueError
                        except (ValueError):
                            raise SyntaxError('Input file has wrong format')
        except FileNotFoundError:
            raise FileNotFoundError("Input file not found")

    def get_matrix_element(self, row, col):
        """ Get the value at the specified position """
        return self.sparse_elems.get((row, col), 0)

    def set_matrix_element(self, row, col, value):
        """ Set the value at the specified position """
        if value == 0:
            # Remove the element if it exists
            self.sparse_elems.pop((row, col), None)
        else:
            self.sparse_elems[(row, col)] = value

    def apply_operation(self, other_matrix, operation):
        """
        Applies addition or subtraction operation, element-wise
        to two sparse matrices of the same dimensions.
        Args:
            other_matrix (SparseMatrix): The second matrix to operate with.
            operation (callable): A function that takes two arguments and returns a value,
            like lambda x, y: x + y for addition.

        Returns a new SparseMatrix containing the result of the operation.
        """
        # Ensure proper dimension for the operation
        if self.row_count != other_matrix.row_count or self.col_count != other_matrix.col_count:
            raise ValueError("Matrix dimensions must match")

        #  new SparseMatrix to store the result
        sparse_result = SparseMatrix(row_count=self.row_count, col_count=self.col_count)

        # Combine all unique positions where non-zero values may exist
        all_positions = set(self.sparse_elems.keys()) | set(other_matrix.sparse_elems.keys())

        for row, col in all_positions:
            # Apply the given operation on corresponding elements
            value = operation(
                self.get_matrix_element(row, col),
                other_matrix.get_matrix_element(row, col)
            )
            # Only store non-zero results
            if value != 0:
                sparse_result.set_matrix_element(row, col, value)

        return sparse_result

    def add(self, other_matrix):
        """
        Add another sparse matrix to this matrix and return the sum.
        Args:
            other_matrix (SparseMatrix): The matrix to add.
        """
        return self.apply_operation(other_matrix, lambda x, y: x + y)

    def subtract(self, other_matrix):
        """
        Subtract another sparse matrix from this matrix and return the result.
        Args:
            other_matrix (SparseMatrix): The matrix to subtract.
        """
        return self.apply_operation(other_matrix, lambda x, y: x - y)

    def multiply(self, other_matrix):
        """ Multiply this matrix by another matrix """
        # Check if dimensions are compatible for multiplication
        if self.col_count != other_matrix.row_count:
            raise ValueError("First matrix column count must match second matrix row count")

        # Create result matrix
        sparse_result = SparseMatrix(row_count=self.row_count, col_count=other_matrix.col_count)
        # Organize the second matrix by row for efficient multiplication
        row_elements = {}

        for (row, col), value in other_matrix.sparse_elems.items():
            if row not in row_elements:
                row_elements[row] = []
            row_elements[row].append((col, value))

        # Perform multiplication
        for (row_a, col_a), value_a in self.sparse_elems.items():
            # If this column index from matrix A exists as a row in matrix B
            if col_a in row_elements:
                # Multiply and add to the result
                for col_b, value_b in row_elements[col_a]:
                    current_value = sparse_result.get_matrix_element(row_a, col_b)
                    new_value = current_value + (value_a * value_b)

                    sparse_result.set_matrix_element(row_a, col_b, new_value)
        return sparse_result

    def write_to_file(self, out_file):
        """ Write the sparse matrix to a file """
        with open(out_file, 'w') as output_file:
            # write the dimension of the matrix
            output_file.write(f'rows={self.row_count}\n')
            output_file.write(f'cols={self.col_count}\n')
            # Sort by row, then by column for consistent output
            sorted_elems = sorted(self.sparse_elems.items())
            for (row, col), value in sorted_elems:
                output_file.write(f'({row}, {col}, {value})\n')
