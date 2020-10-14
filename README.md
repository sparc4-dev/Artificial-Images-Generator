# Artificial Images Generator
This repo contains the Artificial Images Generator (AIG). The AIG creates artificial images of stars, simulating the images acquired by CCD cameras. To accomplish this, the AIG models the star flux distribution as a 2D-Gaussian Distribution. 

The artificial image is created, then, by adding the Gaussian Distribution model to a noise image
that would be acquired by a CCD camera. It is used a Gaussian 2D, implemented in Python Language by the Astropy library \cite{Astropy2018}, as the star point spread function:

<p align="center">
  <img src="https://github.com/DBernardes/Artificial-Images-Generator/blob/main/artificial_star.png" />
</p>
