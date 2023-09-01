# Description
* Given image has a size of (300,300). You can think of this image as a tensor pi of shape (300,300,3). However, only 5000 out of the 300x300=90000 points in the image are not black (i.e. the point pi[y,x]is not equal to [0,0,0])
* You can consider these 5000 points as a dataset. Each item in this dataset is a 5-dimensional array: [x,y,r,g,b] where [r,g,b] is the color of the pixel [x,y] in the given image.
* `pi_xs.npy` - A numpy array of length 5000 - the x-coordinates of each of the points in the dataset
* `pi_ys.npy` - A numpy array of length 5000 - the y-coordinates of each of the points in the dataset
* You can get the x and y locations for each of the 5000 points by doing something like:
  ```
  xs = np.load(pi_xs.npy) // xs.shape is (5000,)
  ys = np.load(pi_ys.npy) // ys.shape is (5000,)
  image_array = np.array(Image.open(‘sparse_pi_colored.jpg’))
  rgb_values = image_array[xs, ys] // rgb_values.shape is (5000,3)
  ```  
