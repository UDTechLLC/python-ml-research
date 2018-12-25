import tensorflow as tf

rank_three_tensor = tf.ones([3, 4, 5])

t = tf.ones([3, 4, 5])
tf.Print(t, [t])  # This does nothing
t = tf.Print(t, [t])  # Here we are using the value returned by tf.Print
result = t + 1  # Now when result is evaluated the value of `t` will be printed.

matrix = tf.reshape(rank_three_tensor, [6, 10])  # Reshape existing content into
                                                 # a 6x10 matrix
print(matrix)

matrixB = tf.reshape(matrix, [3, -1])  #  Reshape existing content into a 3x20
                                       # matrix. -1 tells reshape to calculate
                                       # the size of this dimension.
print(matrixB)

matrixAlt = tf.reshape(matrixB, [4, 3, -1])  # Reshape existing content into a
                                             #4x3x5 tensor
print(matrixAlt)

# Note that the number of elements of the reshaped Tensors has to match the
# original number of elements. Therefore, the following example generates an
# error because no possible value for the last dimension will match the number
# of elements.
# yet_another = tf.reshape(matrixA  lt, [13, 2, -1])  # ERROR!

# constant = tf.constant([1, 2, 3])
# tensor = constant * constant
# print(tensor.eval())
