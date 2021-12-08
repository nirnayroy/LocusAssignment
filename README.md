# Locus Assignment
---
<figure>
  <img
  src="https://github.com/nirnayroy/LocusAssignment/blob/main/dla_251_15000.png"
  alt="251_15k_simulation">
  <figcaption>251x251 Matrix with 15,000 particles</figcaption>
</figure>

## Algorithm for stickiness prediction of Diffusion Latent Aggregation images

### Variable Names

- **M:** size of the *(M,M)* shaped matrix
- **k:** stickiness of a particle
- **N:** total no. of particles in the matrix
- **q:** size of the square shaped section cut from the centre of the matrix
- **N**_q: No. of particles inside the section
- **Central Particle Density:** Density of Particles on the central tile(N_q/q^2)

### Observations

1. When the *stickiness* is high, less *no. of particles* get to the central part of the matrix because they are more likely to have stuck to another particle on their way to the centre. Thus we can expect an **inverse** correlation between No. of particles on the central tile and the stickiness of the particles.
2. After **N** crosses a particular threshold, particles introduced after are less likely to get to the central part of the matrix. Thus, the no. of particles found on the central section of the matrix becomes constant for sufficiently large **N**

### Hypothesis

> Number of particles found at a q(<M) sided square shaped section of the M sized matrix located at its centre varies with the stickiness of the particles on the matrix. 

This is the alternate hyothesis. The null hypothesis is the negation of the above.

### Relationship between Cetral Particle Density and Stickiness

![q35](https://github.com/nirnayroy/LocusAssignment/blob/main/images/q35.png)

We notice a linear relationship between the two variables. So, we go ahead and fit a line to it using linear regression.

### Linear Regression
![linfit](https://github.com/nirnayroy/LocusAssignment/blob/main/images/linfit.png)

But, as we start decreasing q, we see that the correlation breaks apart.
![q20](https://github.com/nirnayroy/LocusAssignment/blob/main/images/q20.png)
![q7](https://github.com/nirnayroy/LocusAssignment/blob/main/images/q7.png)
![q6](https://github.com/nirnayroy/LocusAssignment/blob/main/images/q6.png)

So, we plot the final mean squared error after linear regression for different values of q
![mse](https://github.com/nirnayroy/LocusAssignment/blob/main/images/mse.png)

We observe that the error stops decreasing after q>25. 
But, when the number of particles are less than 625(q^2), we would have to decrease q and make less accurate predictions.

### Statistical significance of the correlation

The **Pearsons** correlation coefficient for Central Particle Density(N_q/q^2) was found to be -0.825 which can be classified as statistically significant correlation
It would be interesting to look at the p-values of the test statistic(against null hypothesis of no correlatioin) of **Pearsons** correlation coefficient, for different values of q to find how low can we set q without disturbing the statistical significance of this correlation.

![pearsonrq](https://github.com/nirnayroy/LocusAssignment/blob/main/images/pearsonrq.png)

We find that the p-value at q=6 is about 6%, which is sufficient to reject the hypothesis that the Central Particle Density and Stickiness are correlated. Thus, we conclude that we can make predictions for a minumum value of q=7.
So, this leads to formation of a low confidence zone between q=7 and q=25, where the correlation is significant but the prediction from Linear Regression gives a lot of error. We may have to predict from this zone if 625>N>49. 
We should not predict anything for N<49 because our feature doesn't have significant correlation with stickiness at these values of q.

### ALgorithm for stickiness prediction

```
if N>625:
  use linear regression,
  stickiness = = -0.1741*Central Particle Density + 0.1233
else if 625>N>49:
  Low Confidence Zone
  use linear regression(but knowing that the predictions contain error),
  stickiness = = -0.1741*Central Particle Density + 0.1233
else:
  It is really difficult to predict the stickiness of particles from the images when there are lesser particles.
```
### Additonal Notes

1. q must be selected such that the central square is covered with particles and if a new particle were to be introduced in the matrix, it would have almost 0 probability of sticking inside the selected q-sized square.
2. The numbers 625 and 49 were picked using the above rationale. 625 is the maximum no. of particles that fit on a 25x25 grid and same for 49 in 7x7 grid.
3. We can improve performance the low confidence zone by further by adjusting q according to the N given.
