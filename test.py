import numpy as np

# Assuming you have two matrices, matrix_1 and matrix_2, each containing 2D vectors
# For demonstration purposes, creating dummy matrices

# Create dummy matrices with 2D vectors
matrix_1 = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
matrix_2 = np.array([[[9, 10], [11, 12]], [[13, 14], [15, 16]]])

# Concatenate the matrices along the specified axis (axis=2 in this case)
concatenated_matrix = np.concatenate((matrix_1, matrix_2), axis=2)

# Print the concatenated matrix
print(concatenated_matrix)