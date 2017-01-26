"""Tutorial on how to create a convolutional autoencoder w/ Tensorflow.

Parag K. Mital, Jan 2016
"""
import tensorflow as tf
import numpy as np
import math
from libs.activations import lrelu
from libs.utils import corrupt
import pickle 
from xml.sax.handler import feature_external_ges
import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data
import matplotlib.pyplot as plt

# %%
def autoencoder(input_shape=[None, 3072],
                n_filters=[3, 40, 40, 2 ],
                filter_sizes=[3, 3, 3, 3 ],
                corruption=False):
    """Build a deep denoising autoencoder w/ tied weights.

    Parameters
    ----------
    input_shape : list, optional
        Description
    n_filters : list, optional
        Description
    filter_sizes : list, optional
        Description

    Returns
    -------
    x : Tensor
        Input placeholder to the network
    z : Tensor
        Inner-most latent representation
    y : Tensor
        Output reconstruction of the input
    cost : Tensor
        Overall cost to use for training

    Raises
    ------
    ValueError
        Description
    """
    # %%
    # input to the network
    x = tf.placeholder(
        tf.float32, input_shape, name='x')


    # %%
    # ensure 2-d is converted to square tensor.
    if len(x.get_shape()) == 2:
        x_dim = 32
        x_tensor = tf.reshape(
            x, [-1, x_dim, x_dim, n_filters[0]])
    elif len(x.get_shape()) == 4:
        x_tensor = x
    else:
        raise ValueError('Unsupported input dimensions')
    current_input = x_tensor

    # %%
    # Optionally apply denoising autoencoder
    if corruption:
        current_input = corrupt(current_input)

    # %%
    # Build the encoder
    encoder = []
    shapes = []
    for layer_i, n_output in enumerate(n_filters[1:]):
        n_input = current_input.get_shape().as_list()[3]
        shapes.append(current_input.get_shape().as_list())
        print shapes 
        W = tf.Variable(
            tf.random_uniform([
                filter_sizes[layer_i],
                filter_sizes[layer_i],
                n_input, n_output],
                -1.0 / math.sqrt(n_input),
                1.0 / math.sqrt(n_input)))
        b = tf.Variable(tf.zeros([n_output]))
        encoder.append(W)
        output = lrelu(
            tf.add(tf.nn.conv2d(
                current_input, W, strides=[1, 2, 2, 1], padding='SAME'), b))
        print output          
        current_input = output

    # %%
    # store the latent representation
    z = current_input
    
    print shapes
    print encoder
    
    encoder.reverse()
    shapes.reverse()
    print "------------------"
    print z
    

    # %%
    # Build the decoder using the same weights
    for layer_i, shape in enumerate(shapes):
        W = encoder[layer_i]
        b = tf.Variable(tf.zeros([W.get_shape().as_list()[2]]))
        output = lrelu(tf.add(
            tf.nn.conv2d_transpose(
                current_input, W,
                tf.pack([tf.shape(x)[0], shape[1], shape[2], shape[3]]),
                strides=[1, 2, 2, 1], padding='SAME'), b))
        current_input = output

    # %%
    # now have the reconstruction through the network
    y = current_input
    # cost function measures pixel-wise difference
    cost = tf.reduce_sum(tf.square(y - x_tensor))

    # %%
    return {'x': x, 'z': z, 'y': y, 'cost': cost}


# %%
def traing_cifar(feat, labels):
    """Test the convolutional autoencder using CIFAR."""
    # %%


    # %%
    # load MNIST as before
#     mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
    n = len(labels)
    print n,"XXXXXXXXXXXXXXXXXXxxx"
    

    feat = np.array(feat)/(255.0)
    mean_img = np.mean(feat, axis=0)
    Xdata = (feat - mean_img)
    
    
    ae = autoencoder()

    # %%
    learning_rate = 0.01
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(ae['cost'])

    # %%
    # We create a session to use the graph
    sess = tf.Session()
    sess.run(tf.initialize_all_variables())

    # %%
    # Fit all training data
    batch_size = 100
    n_epochs = 200
    for epoch_i in range(n_epochs):
        for batch_i in range(n // batch_size):
#         for   batch_i in range( 1):
            train  = Xdata[0:batch_size,:]
#             train = np.array([img - mean_img for img in batch_xs])
            sess.run(optimizer, feed_dict={ae['x']: train})
        print("COSt ",   epoch_i, sess.run(ae['cost'], feed_dict={ae['x']: train}))

    # %%
    # Plot example reconstructions
    
    fo = open('../python/OurMethod/src/CIFAR5.txt','w')
    foi = open('../python/OurMethod/src/CIFAR5_images.txt','w')
    
    n_examples = 100
    for k in xrange(n/n_examples):
        print k
        test_xs = Xdata[k*n_examples:(k+1)*n_examples, :]
        test_ys = labels[k*n_examples:(k+1)*n_examples]
        
#         test_xs_norm = np.array([img - mean_img for img in test_xs])
        
        
        recon = sess.run(ae['y'], feed_dict={ae['x']: test_xs})
        
        reconZ = sess.run(ae['z'], feed_dict={ae['x']: test_xs})
        
        
        for sj in xrange(n_examples):
            out=[]
            for i in   reconZ[sj]:
                for j in i:
                    for k in j:
                        out+= [k]
            yy = test_ys[sj]
            label = yy
            if (label == 0 or label==1 or label==2):
                fo.write(str(int(label))+':'+' '.join([str(kk) for kk in out])+'\n')
                foi.write(' '.join(  [str(kk) for kk in (test_xs[sj]+mean_img  ) ]   )+'\n')
    fo.close() 
    foi.close()
 
    if False:           
        print(recon.shape)
        fig, axs = plt.subplots(2, n_examples, figsize=(10, 2))
        for example_i in range(n_examples):
            axs[0][example_i].imshow(
                np.reshape(test_xs[example_i, :], (28, 28)))
            axs[1][example_i].imshow(
                np.reshape(
                    np.reshape(recon[example_i, ...], (784,)) + mean_img,
                    (28, 28)))
        fig.show()
        plt.draw()
        plt.waitforbuttonpress()


# %%
if __name__ == '__main__':
    cifar  = pickle.load( open( "cifar/5classCFAR100.pickle", "rb" ) )
    
    feat = cifar['data']
    labels = cifar['labels']
    
    print feat 
    print labels 
    
    pic = feat[1]
    
    pic2 = np.reshape(pic, (32,32,3), order='F')
    pic2 = pic.reshape(3,32,32).transpose(1,2,0)
    
    traing_cifar(feat, labels)
#     print pic2
#     
#     
#     fig, axs = plt.subplots(2, 2 )
#     axs[0][0].imshow( pic2  )
#     fig.show()
#     plt.draw()
#     plt.waitforbuttonpress()
    
