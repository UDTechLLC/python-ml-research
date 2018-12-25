import tensorflow as tf

layers = tf.keras.layers
from tensorflow.contrib import autograph

import numpy as np
import matplotlib.pyplot as plt

tf.enable_eager_execution()


def square_if_positive(x):
    if x > 0:
        x = x * x
    else:
        x = 0.0
    return x


print(autograph.to_code(square_if_positive))

print('Eager results: %2.2f, %2.2f' % (square_if_positive(tf.constant(9.0)),
                                       square_if_positive(tf.constant(-9.0))))

tf_square_if_positive = autograph.to_graph(square_if_positive)

with tf.Graph().as_default():
    # The result works like a regular op: takes tensors in, returns tensors.
    # You can inspect the graph using tf.get_default_graph().as_graph_def()
    g_out1 = tf_square_if_positive(tf.constant(9.0))
    g_out2 = tf_square_if_positive(tf.constant(-9.0))

    with tf.Session() as sess:
        print('Graph results: %2.2f, %2.2f\n' % (sess.run(g_out1), sess.run(g_out2)))


# Continue in a loop
def sum_even(items):
    s = 0
    for c in items:
        if c % 2 > 0:
            continue
        s += c
    return s


print('Eager result: %d' % sum_even(tf.constant([10, 12, 15, 20])))

tf_sum_even = autograph.to_graph(sum_even)

with tf.Graph().as_default(), tf.Session() as sess:
    print('Graph result: %d\n\n' % sess.run(tf_sum_even(tf.constant([10, 12, 15, 20]))))

print(autograph.to_code(sum_even))
