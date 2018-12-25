import tensorflow as tf
from tensorflow.contrib import autograph
import matplotlib.pyplot as plt

(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()


def mlp_model(input_shape):
    model = tf.keras.Sequential((
        tf.keras.layers.Dense(100, activation='relu', input_shape=input_shape),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')))
    model.build()
    return model


def predict(m, x, y):
    y_p = m(tf.reshape(x, (-1, 28 * 28)))
    losses = tf.keras.losses.categorical_crossentropy(y, y_p)
    l = tf.reduce_mean(losses)
    accuracies = tf.keras.metrics.categorical_accuracy(y, y_p)
    accuracy = tf.reduce_mean(accuracies)
    return l, accuracy


def fit(m, x, y, opt):
    l, accuracy = predict(m, x, y)
    # Autograph automatically adds the necessary
    # <a href="./../api_docs/python/tf/control_dependencies"><code>tf.control_dependencies</code></a> here.
    # (Without them nothing depends on `opt.minimize`, so it doesn't run.)
    # This makes it much more like eager-code.
    opt.minimize(l)
    return l, accuracy


def setup_mnist_data(is_training, batch_size):
    if is_training:
        ds = tf.data.Dataset.from_tensor_slices((train_images, train_labels))
        ds = ds.shuffle(batch_size * 10)
    else:
        ds = tf.data.Dataset.from_tensor_slices((test_images, test_labels))

    ds = ds.repeat()
    ds = ds.batch(batch_size)
    return ds


def get_next_batch(ds):
    itr = ds.make_one_shot_iterator()
    image, label = itr.get_next()
    x = tf.to_float(image) / 255.0
    y = tf.one_hot(tf.squeeze(label), 10)
    return x, y


# Use `recursive = True` to recursively convert functions called by this one.
@autograph.convert(recursive=True)
def train(train_ds, test_ds, hp):
    m = mlp_model((28 * 28,))
    opt = tf.train.AdamOptimizer(hp.learning_rate)

    # We'd like to save our losses to a list. In order for AutoGraph
    # to convert these lists into their graph equivalent,
    # we need to specify the element type of the lists.
    train_losses = []
    autograph.set_element_type(train_losses, tf.float32)
    test_losses = []
    autograph.set_element_type(test_losses, tf.float32)
    train_accuracies = []
    autograph.set_element_type(train_accuracies, tf.float32)
    test_accuracies = []
    autograph.set_element_type(test_accuracies, tf.float32)

    # This entire training loop will be run in-graph.
    i = tf.constant(0)
    while i < hp.max_steps:
        train_x, train_y = get_next_batch(train_ds)
        test_x, test_y = get_next_batch(test_ds)

        step_train_loss, step_train_accuracy = fit(m, train_x, train_y, opt)
        step_test_loss, step_test_accuracy = predict(m, test_x, test_y)
        if i % (hp.max_steps // 10) == 0:
            print('Step', i, 'train loss:', step_train_loss, 'test loss:',
                  step_test_loss, 'train accuracy:', step_train_accuracy,
                  'test accuracy:', step_test_accuracy)
        train_losses.append(step_train_loss)
        test_losses.append(step_test_loss)
        train_accuracies.append(step_train_accuracy)
        test_accuracies.append(step_test_accuracy)
        i += 1

    # We've recorded our loss values and accuracies
    # to a list in a graph with AutoGraph's help.
    # In order to return the values as a Tensor,
    # we need to stack them before returning them.
    return (autograph.stack(train_losses), autograph.stack(test_losses),
            autograph.stack(train_accuracies), autograph.stack(test_accuracies))


with tf.Graph().as_default() as g:
    hp = tf.contrib.training.HParams(
        learning_rate=0.005,
        max_steps=500,
    )
    train_ds = setup_mnist_data(True, 50)
    test_ds = setup_mnist_data(False, 1000)
    (train_losses, test_losses, train_accuracies,
     test_accuracies) = train(train_ds, test_ds, hp)

    init = tf.global_variables_initializer()

with tf.Session(graph=g) as sess:
    sess.run(init)
    (train_losses, test_losses, train_accuracies,
     test_accuracies) = sess.run([train_losses, test_losses, train_accuracies,
                                  test_accuracies])

plt.title('MNIST train/test losses')
plt.plot(train_losses, label='train loss')
plt.plot(test_losses, label='test loss')
plt.legend()
plt.xlabel('Training step')
plt.ylabel('Loss')
plt.show()
plt.title('MNIST train/test accuracies')
plt.plot(train_accuracies, label='train accuracy')
plt.plot(test_accuracies, label='test accuracy')
plt.legend(loc='lower right')
plt.xlabel('Training step')
plt.ylabel('Accuracy')
plt.show()
