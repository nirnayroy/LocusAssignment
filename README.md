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
- 

### Observations

1. When the *stickiness* is high, less *no. of particles* get to the central part of the matrix because they are likely to have stuck to another particle on its way to the centre. Thus we can expect an **inverse** correlation between No. of particles on the central tile and the stickiness of the particles.
2. After **N** crosses a particular threshold, particles introduced after are less likely to get to the central part of the matrix. Thus, the no. of particles found on the central section of the matrix becomes constant for sufficiently large **N**
