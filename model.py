import tensorflow as tf
import utils


def get_model(is_train=False, keep_prob=0.8, alpha=0.8):
    with tf.compat.v1.variable_scope("model", reuse=not is_train):
        tf_x = tf.compat.v1.placeholder(tf.compat.v1.float32, shape=[None, utils.IMAGE_HEIGHT, utils.IMAGE_WIDTH, utils.IMAGE_CHANNEL])
        tf_y = tf.compat.v1.placeholder(tf.compat.v1.int32, shape=[None])
        tf_y_onehot = tf.compat.v1.one_hot(tf_y, utils.IMAGE_CLASSIFY)

        # conv 1
        filter_1 = tf.compat.v1.Variable(tf.compat.v1.truncated_normal(shape=[5, 5, 3, 32], mean=utils.mu, stddev=utils.sigma))
        bias_1 = tf.compat.v1.Variable(tf.compat.v1.constant(0.1, shape=[32]))
        conv_1 = tf.compat.v1.nn.conv2d(tf_x, filter=filter_1, strides=[1, 2, 2, 1], padding='SAME') + bias_1
        leaky_relu_1 = tf.compat.v1.nn.leaky_relu(conv_1, alpha=alpha)

        # conv 2
        filter_2 = tf.compat.v1.Variable(tf.compat.v1.truncated_normal(shape=[3, 3, 32, 48], mean=utils.mu, stddev=utils.sigma))
        bias_2 = tf.compat.v1.Variable(tf.compat.v1.constant(0.1, shape=[48]))
        conv_2 = tf.compat.v1.nn.conv2d(leaky_relu_1, filter=filter_2, strides=[1, 2, 2, 1], padding='SAME') + bias_2
        leaky_relu_2 = tf.compat.v1.nn.leaky_relu(conv_2, alpha=alpha)

        # conv 3
        filter_3 = tf.compat.v1.Variable(tf.compat.v1.truncated_normal(shape=[3, 3, 48, 64], mean=utils.mu, stddev=utils.sigma))
        bias_3 = tf.compat.v1.Variable(tf.compat.v1.constant(0.1, shape=[64]))
        conv_3 = tf.compat.v1.nn.conv2d(leaky_relu_2, filter=filter_3, strides=[1, 2, 2, 1], padding='SAME') + bias_3
        leaky_relu_3 = tf.compat.v1.nn.leaky_relu(conv_3, alpha=alpha)

        dropout = tf.compat.v1.nn.dropout(leaky_relu_3, rate=1-keep_prob)

        # flatten
        shape = dropout.get_shape().as_list()
        flatten_size = shape[1] * shape[2] * shape[3]
        flatten = tf.compat.v1.reshape(dropout, [-1, flatten_size])

        # fc 1
        filter_4 = tf.compat.v1.Variable(tf.compat.v1.truncated_normal(shape=[flatten.get_shape().as_list()[1], 100],
                                                   mean=utils.mu, stddev=utils.sigma))
        bias_4 = tf.compat.v1.Variable(tf.compat.v1.constant(0.1, shape=[100]))
        fc_1 = tf.compat.v1.matmul(flatten, filter_4) + bias_4
        leaky_relu_4 = tf.compat.v1.nn.leaky_relu(fc_1, alpha=alpha)

        # fc 2
        filter_5 = tf.compat.v1.Variable(tf.compat.v1.truncated_normal(shape=[100, 50], mean=utils.mu, stddev=utils.sigma))
        bias_5 = tf.compat.v1.Variable(tf.compat.v1.constant(0.1, shape=[50]))
        fc_2 = tf.compat.v1.matmul(leaky_relu_4, filter_5) + bias_5
        leaky_relu_5 = tf.compat.v1.nn.leaky_relu(fc_2, alpha=alpha)

        # fc 3
        filter_6 = tf.compat.v1.Variable(tf.compat.v1.truncated_normal(shape=[50, 10], mean=utils.mu, stddev=utils.sigma))
        bias_6 = tf.compat.v1.Variable(tf.compat.v1.constant(0.1, shape=[10]))
        fc_3 = tf.compat.v1.matmul(leaky_relu_5, filter_6) + bias_6
        leaky_relu_6 = tf.compat.v1.nn.leaky_relu(fc_3, alpha=alpha)

        # result
        filter_7 = tf.compat.v1.Variable(tf.compat.v1.truncated_normal(shape=[10, utils.IMAGE_CLASSIFY],
                                                   mean=utils.mu, stddev=utils.sigma))
        bias_7 = tf.compat.v1.Variable(tf.compat.v1.constant(0.1, shape=[utils.IMAGE_CLASSIFY]))
        result = tf.compat.v1.matmul(leaky_relu_6, filter_7) + bias_7
        
        last_layer = result if is_train else tf.compat.v1.nn.softmax(result)
        return tf_x, tf_y, tf_y_onehot, last_layer
