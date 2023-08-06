# coding=utf-8
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


# define W & b
def weight_variable(para):
    # ?????????????stddev?0.1
    initial = tf.truncated_normal(para, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(para):
    initial = tf.constant(0.1, shape=para)
    return tf.Variable(initial)




# ??????
def variable_summaries(var):
    with tf.name_scope('summaries'):  # ???scope??
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean', mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.reduce_mean(tf.square(var - mean))))
        tf.summary.scalar('stddev', stddev)
        tf.summary.scalar('max', tf.reduce_max(var))
        tf.summary.scalar('min', tf.reduce_min(var))  # ????var? ??????????????
        tf.summary.histogram('histogram', var)  # ????var???? - histogram


# ????? - ?????????
#          - ?????????
#          - ????????relu
def nn_layer(in_data, in_dim, out_dim, layer_name, act=tf.nn.relu):
    with tf.name_scope(layer_name):  # ??????????
        with tf.name_scope('weights'):
            weights = weight_variable([in_dim, out_dim])  # ?????????
            variable_summaries(weights)  # ????????
        with tf.name_scope('biases'):
            biases = bias_variable([out_dim])  # ???????biases
            variable_summaries(biases)  # ??????biases
        with tf.name_scope('Wx_plus_b'):
            Wx_plus_b = tf.matmul(in_data, weights) + biases  # ?? wx?b
            tf.summary.histogram('Wx_plus_b', Wx_plus_b)  # ??wx?b?? - histogram
        activations = act(Wx_plus_b, name='activation')  # ??
        tf.summary.histogram('activations', activations)  # ??????? - histogram
        return activations

    # ?????????session


mnist = input_data.read_data_sets("../../data/mnist/", one_hot=True)
sess = tf.InteractiveSession()

# ????????
with tf.name_scope('input'):
    x = tf.placeholder(tf.float32, [None, 784], name='x_input')  # 28*28=784 dim??????name???????
    y_ = tf.placeholder(tf.float32, [None, 10], name='x_input')  # label - 10 dim

# ????reshape
with tf.name_scope('input_reshape'):
    x_shaped = tf.reshape(x, [-1, 28, 28, 1])  # reshape for conv, -1????????1????
    tf.summary.image('input', x_shaped, 10)  # ??input????? - image

# ?????layer
layer1 = nn_layer(x, 784, 500, 'layer1')

with tf.name_scope('dropout'):  # layer1 ??follow??dropout
    keep_prob = tf.placeholder(tf.float32)
    tf.summary.scalar('dropout_keep_probability', keep_prob)
    dropped = tf.nn.dropout(layer1, keep_prob)

# ?????layer
y = nn_layer(dropped, 500, 10, 'layer2', act=tf.identity)

# softmax
# ?????cross_entropy
with tf.name_scope('cross_entropy'):
    diff = tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_)  # diff
    with tf.name_scope('total'):
        cross_entropy = tf.reduce_mean(diff)
tf.summary.scalar('cross_entropy', cross_entropy)



# training
with tf.name_scope('train'):
    train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)
with tf.name_scope('accuracy'):
    with tf.name_scope('correct_prediction'):
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    with tf.name_scope('accuracy'):
        accuracy_op = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('accuracy', accuracy_op)

# ????summary
merge_op = tf.summary.merge_all()
train_writer = tf.summary.FileWriter('./logs/mnist/train', sess.graph)  # ??log????
test_writer = tf.summary.FileWriter('./logs/mnist/test', sess.graph)  # ??log????

# ????
tf.global_variables_initializer().run()  # ???????

# ??tf.train.Saver()????????
saver = tf.train.Saver()
for i in range(1000):
    if i % 10 == 0:  # for test??10?step????
        # ????
        xs, ys = mnist.test.images, mnist.test.labels
        # ??merge_op(????) ? accuracy_op(?????)
        summary, acc = sess.run([merge_op, accuracy_op], feed_dict={x: xs, y_: ys, keep_prob: 1.0})
        print('Accuracy at step %s: %s' % (i, acc))  # ??????

    else:  # for train
        if i == 99:
            # tf.RunOption???????
            # tf.RunMetadata()???????????????????????
            run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
            run_metadata_op = tf.RunMetadata()
            xs, ys = mnist.train.next_batch(100)
            summary, _ = sess.run([merge_op, train_step], feed_dict={x: xs, y_: ys, keep_prob: 0.6},
                                  options=run_options, run_metadata=run_metadata_op)
            train_writer.add_run_metadata(run_metadata_op, 'step % 03d', i)
            train_writer.add_summary(summary, i)
            saver.save(sess, './logs/model.ckpt', i)
            print('Adding run metadata for', i)
        else:
            xs, ys = mnist.train.next_batch(100)
            # ??merged_op?train_step???summary
            summary, _ = sess.run([merge_op, train_step], feed_dict={x: xs, y_: ys, keep_prob: 0.6})
            train_writer.add_summary(summary, i)
        # ???????writer
train_writer.close
test_writer.close