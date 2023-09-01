# Create Generative Models for 5D Points Project

## Step 5, Generate New Points

After training, generate new points by sampling from the latent space and passing the samples through the decoder. 

New point generation step involves using the trained model to generate new points that have the same distribution as the points in the dataset. This is done by sampling from the latent space (for AE, trm-VAE, and VAE) or by feeding a sequence of tokens into the model and having it generate the next token (for GPT-2).


### Solution 1, 3 & 4: Autoencoder (AE), Transformer Variational Autoencoder (trm-VAE), Variational Autoencoder (VAE)

For these models, generate new points by sampling from the latent space of the model and then decoding these samples to get new points. This process should give new 5-dimensional points that come from the same distribution as the points in the dataset. 


### Solution 2: GPT-2

For the GPT-2 model solution, generate new points by feeding a sequence of tokens into the model and having it generate the next token. This token is then converted back into a 5D point. Start with a random point (i.e., a sequence of float strings) and ask the model to predict the next point. This point is added to the sequence and the process is repeated.


## Step 6, Validate the Model and Evaluate its Results: Demonstrate the Distribution

The sixth step is to validate the model and evaluate its results. Model validation step involves generating new points using the trained model and comparing their distribution to the distribution of the original points. If the model has learned correctly, the generated points should come from the same distribution as the original points. This can be done using various methods such as scatter plots, histograms, or statistical measures.


### Method 1: Scatter Plot

One way to validate the model is to visualize the generated points and compare them with the original image. Creating a scatter plot of the generated points, with their corresponding colors. If the model has learned the distribution correctly, the plot should resemble the original image distribution.


### Method 2: Histogram

Another way to validate the model is to compare the histograms of the generated points and the original points. If the two histograms are similar, this indicates that the generated points come from the same distribution as the original points.


### Method 3: Statistical Measures

Validate the model by computing statistical measures (like mean and variance) of the original and generated points and comparing them. If the statistical measures are similar, this indicates that the generated points come from the same distribution as the original points.
