import tensorflow as tf

tf.reset_default_graph()

# Create some variables.
v1 = tf.get_variable("v1", shape=[3])
v2 = tf.get_variable("v2", shape=[5])

# Add ops to save and restore all the variables.
# saver = tf.train.Saver()
saver = tf.train.Saver({"v2": v2})

# Later, launch the model, use the saver to restore variables from disk, and
# do some work with the model.
with tf.Session() as sess:
    # Initialize v1 since the saver will not.
    v1.initializer.run()
    # Restore variables from disk.
    saver.restore(sess, "./models/model1.ckpt")
    print("Model restored.")
    # Check the values of the variables
    print("v1 : %s" % v1.eval())
    print("v2 : %s" % v2.eval())
