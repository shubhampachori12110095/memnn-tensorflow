import tensorflow as tf

import data
import memn2n_model
from model import Model

flags = tf.app.flags

flags.DEFINE_integer("train_batch_size", 32, "Batch size during training [32]")
flags.DEFINE_integer("memory_size", 50, "Memory size [50]")
flags.DEFINE_integer("hidden_size", 20, "Embedding dimension [20]")
flags.DEFINE_integer("num_layers", 3, "Number of memory layers (hops) [3]")
flags.DEFINE_float("init_mean", 0, "Initial weight mean [0]")
flags.DEFINE_float("init_std", 0.1, "Initial weight std [0.1]")
flags.DEFINE_float("init_lr", 0.005, "Initial learning rate [0.005]")
flags.DEFINE_boolean("ls", True, "Start training with linear model? [True]")
flags.DEFINE_float("anneal_ratio", 0.5, "Annealing ratio [0.5]")
flags.DEFINE_integer("anneal_period", 25, "Number of epochs for every annealing [25]")
flags.DEFINE_float("max_grad_norm", 40, "Max gradient norm; above this number is clipped [40]")
flags.DEFINE_integer("num_epochs", 100, "Total number of epochs for training [100]")
flags.DEFINE_boolean("te", True, "Temporal encoding enabled? 'True' or 'False' [True]")
flags.DEFINE_boolean("pe", True, "Position encoding enabled? 'True' or 'False' [True]")
flags.DEFINE_string("tying", 'adj', "Indicate tying method: 'adj' or 'rnn' [adj]")

flags.DEFINE_string("data_dir", 'data/tasks_1-20_v1-2/en/', "Data folder directory [data/tasks_1-20_v1-2/en]")
flags.DEFINE_string("data_prefix", "qa1_", "Prefix for file names to fetch in data_dir [qa1_]")
flags.DEFINE_string("data_suffix", "", "Suffix (before '_train.txt' or '_test.txt') for file names to fetch in data dir []")

FLAGS = flags.FLAGS


def main(_):
    train_ds, test_ds = data.read_babi(FLAGS.data_dir, prefix=FLAGS.data_prefix, suffix=FLAGS.data_suffix)
    FLAGS.vocab_size = train_ds.vocab_size
    FLAGS.max_sentence_size = train_ds.max_sentence_size
    FLAGS.test_data_size = test_ds.num_examples
    FLAGS.val_data_size = test_ds.num_examples

    print "vocab size: %d, max sentence length: %d" % (FLAGS.vocab_size, FLAGS.max_sentence_size)

    graph = tf.Graph()
    model = Model(graph, FLAGS, logdir="logs/")
    with tf.Session(graph=graph) as sess:
        sess.run(tf.initialize_all_variables())
        model.train(sess, train_ds, test_ds)

if __name__ == "__main__":
    tf.app.run()