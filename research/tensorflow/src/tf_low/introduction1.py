import tensorflow as tf

a = tf.constant(3.0, name="const_a", dtype=tf.float32)
b = tf.constant(4.0, name="const_b")
total = a + b
print(a)
print(b)
print(total)

# writer = tf.summary.FileWriter('.')
# writer.add_graph(tf.get_default_graph())
# writer.flush()

sess = tf.Session()
print(sess.run(total))
print(sess.run({'ab':(a, b), 'total':total}))

vec = tf.random_uniform(shape=(3,))
out1 = vec + 1
out2 = vec + 2
print(sess.run(vec))
print(sess.run(vec))
print(sess.run((out1, out2)))

x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)
z = x + y

print(sess.run(z, feed_dict={x: 3, y: 4.5}))
print(sess.run(z, feed_dict={x: [1, 3], y: [2, 4]}))
