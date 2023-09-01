# A Generative Model for 5D Points

## Project Description
* This repository contains the code and resources for the “Colored Pi Generator” project.
* The goal of this project is to build a generative model that can generate 5-dimensional points, represented as [x, y, r, g, b], from the same distribution as the points in a provided dataset.
* The dataset is derived from an image, where each data point corresponds to a pixel in the image.
* The ‘x’ and ‘y’ values represent the location of the pixel in the image, while ‘r’, ‘g’, and ‘b’ represent the color of the pixel in RGB color space.
* This project demonstrates how to formulate the problem, devise a solution, organize code, and explain the problem and solution. It also includes a demonstration of how the output points come from the same distribution as the input points.
---
### Step 1, Data Preparation: Load and Preprocess the Data
The first step is to prepare the data. This involves loading the data from the provided sources and preprocessing it to create a suitable dataset for our model.
The data preparation step involves loading the x, y coordinates and the RGB values, combining them into a 5-dimensional dataset to prepare it for training the model.

Provided with the x and y coordinates of the points in numpy arrays. Also have a colored image from which can extract the RGB values of the points. 

To load the data, read the x and y coordinates from the numpy arrays and the RGB values from the colored image. Image pixel coordinates are treated in '(y,x)' order because the first index refers to rows (height) and the second index refers to columns (width). So, the convention may be needed while extracting the RGB values.

Once I have the x, y coordinates and the RGB values, I can combine them into a single array. Each item in this array will be a 5-dimensional vector [x, y, r, g, b], representing a point in the dataset.

### Step 2, Normalize the Data
The second step is to normalize the data. Normalization may be a needed step that may help improve the performance of the model.
The normalization step involves scaling the values in the dataset to a specific range (typically between 0 and 1) or standardizing the distribution of the data. This helps to ensure that the scale or distribution of the data does not negatively impact the learning process of the model.

#### Method 1 (min-max normalization):
Scale the data to a specific range. In this case, normalize the x and y coordinates to be between 0 and 1 by dividing by the size of the image (300, as the image size is 300x300). Similarly, normalize the RGB values to be between 0 and 1 by dividing by 255, as RGB values range from 0 to 255. This method ensures that all values in the dataset are on the same scale, which can help the model to converge faster and lead to better performance.
#### Method 2 (z-score normalization):

Normalize the data to have zero mean and unit variance. This is also a practice when working with neural networks. It involves subtracting the mean of the dataset from each value (to center the data around zero) and then dividing by the standard deviation (to scale the data to unit variance). This method ensures that the distribution of the data is standardized, which may be beneficial when training neural networks.


### Step 3, Define / Build the Model

The third step is to define and build the generative model. Model will take a 5-dimensional point as input and output a 5-dimensional point. The model will be trained to minimize the difference between its output and the true point.

The model-building step involves defining the architecture of the model, which can be an Autoencoder, GPT-2, Transformer-based Variational Autoencoder, or Variational Autoencoder, depending on the chosen approach. The model is then trained to generate points that have the same distribution as the points in the dataset.


#### Solution 1: Autoencoder (AE)

An Autoencoder is a type of generative model that may be effective at capturing the underlying distribution of the data. The AE consists of an encoder and a decoder. The encoder takes the input data and outputs a lower-dimensional representation, while the decoder takes this representation and reconstructs the original data. In this case, use an AE that has a 5-dimensional input (for the given [x, y, r, g, b] data), a specified latent space dimension, and a 5-dimensional output.


#### Solution 2: GPT-2

Another approach is to use a transformer-based model for sequence generation, such as GPT-2, and adapt it to generate sequences of 5-dimensional points. Treat the sequence of 5D points as a "text" and each 5D point as a sequence of “words”. The model is then trained to generate the new sequence of "words" based on the previous ones, similar to how GPT-2 generates new words based on the previous words in a text.


#### Solution 3: Transformer Variational Autoencoder (trm-VAE)

Define a Variational Autoencoder with a transformer-based encoder and decoder. The encoder takes the 5-dimensional points as input and outputs a mean and a log variance, which define a distribution in the latent space. The decoder takes a sample from this distribution and outputs a reconstruction of the original points. The model is trained using the reparameterization trick and the ELBO loss, which is the sum of the reconstruction loss and the KL divergence.


#### Solution 4: Variational Autoencoder (VAE)

Variational AutoEncoder is also a type of generative model that may be good at modeling complex, high-dimensional data. It works by encoding the input data into a lower-dimensional representation, and then decoding this representation back into the original format. The encoder outputs a mean and variance for each point in the latent space, and the decoder takes points from the latent space and tries to reconstruct the original input data.


### Step 4, Train the Model

The fourth step is to train the model. This involves feeding the data to the model and optimizing the model's parameters to minimize the loss function. The choice of optimizer and loss function can vary depending on the model and the nature of the data.


#### Solution 1: Autoencoder (AE)

Can use the Adam optimizer and the reconstruction loss (e.g., Mean Square Error (MSE)).


#### Solution 2: GPT-2

For the GPT-2 model, use the _GPT2LMHeadModel_ class from the Transformers library, which is a GPT-2 model with a language modeling head. This model is trained to generate the new sequence of "words" (5D points) based on the previous ones.


#### Solution 3: Transformer Variational Autoencoder (trm-VAE)

For the Transformer Variational Autoencoder, the training process involves feeding the data to the model and optimizing the model's parameters to minimize the reconstruction loss and the KL divergence loss. The loss may measure the difference between the original data and the data reconstructed by the model.


#### Solution 4: Variational Autoencoder (VAE)

For the Variational Autoencoder, use the Adam optimizer and a combination of a reconstruction loss and a KL divergence loss. The reconstruction loss can be Mean Square Error (MSE) loss, which measures the average squared difference between the actual and predicted values. The KL divergence loss measures the difference between the actual data distribution and the distribution predicted by the model.


### Step 5, Generate New Points

After training, generate new points by sampling from the latent space and passing the samples through the decoder. 

New point generation step involves using the trained model to generate new points that have the same distribution as the points in the dataset. This is done by sampling from the latent space (for AE, trm-VAE, and VAE) or by feeding a sequence of tokens into the model and having it generate the next token (for GPT-2).


#### Solution 1, 3 & 4: Autoencoder (AE), Transformer Variational Autoencoder (trm-VAE), Variational Autoencoder (VAE)

For these models, generate new points by sampling from the latent space of the model and then decoding these samples to get new points. This process should give new 5-dimensional points that come from the same distribution as the points in the dataset. 


#### Solution 2: GPT-2

For the GPT-2 model solution, generate new points by feeding a sequence of tokens into the model and having it generate the next token. This token is then converted back into a 5D point. Start with a random point (i.e., a sequence of float strings) and ask the model to predict the next point. This point is added to the sequence and the process is repeated.


## Step 6, Validate the Model and Evaluate its Results: Demonstrate the Distribution

The sixth step is to validate the model and evaluate its results. Model validation step involves generating new points using the trained model and comparing their distribution to the distribution of the original points. If the model has learned correctly, the generated points should come from the same distribution as the original points. This can be done using various methods such as scatter plots, histograms, or statistical measures.


### Method 1: Scatter Plot

One way to validate the model is to visualize the generated points and compare them with the original image. Creating a scatter plot of the generated points, with their corresponding colors. If the model has learned the distribution correctly, the plot should resemble the original image distribution.


### Method 2: Histogram

Another way to validate the model is to compare the histograms of the generated points and the original points. If the two histograms are similar, this indicates that the generated points come from the same distribution as the original points.


### Method 3: Statistical Measures

Validate the model by computing statistical measures (like mean and variance) of the original and generated points and comparing them. If the statistical measures are similar, this indicates that the generated points come from the same distribution as the original points.

## Corresponding organized Colab notebooks
[link](https://drive.google.com/drive/folders/120DSzBZVsXIfzuwO9hHI-EjFtNPfma9x?usp=sharing)
