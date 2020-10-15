# Artificial Images Generator
This repo contains the software of the Artificial Images Generator (AIG). The AIG was developed to create artificial star images, simulating the star images acquired by the [SPARC4](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/8446/844626/Concept-of-SPARC4--a-simultaneous-polarimeter-and-rapid-camera/10.1117/12.924976.full?SSO=1) CCD cameras in astronomical observations. To create the images, the AIG models the star flux distribution as a 2D-Gaussian Distribution. This result is added to a noise image, created based a set of parameters provided to the software, as the CCD operation mode, the star flux and the sky flux. Figure below presents an example of an image created by the AIG. This READ.ME explains the step-by-step procedure of the AIG to create the imagens, as well as, it presents a simple execution example.


<p align="center">
  <img src="https://github.com/DBernardes/Artificial-Images-Generator/blob/main/artificial_star.png" />
</p>


## Software Description

The AIG is a software developed using the Python 3 language. It is operation can be divided in the parameters configuration step, the creation of a noise image step and, the creation of the star flux step. 

In the parameters configuration step, the AIG will calcute the gain, the dark current noise and the read noise of the CCD. The CCD gain is the converstion factor of the acquired photoelectrons in Analogical-to-Ditial Unit (ADU). The dark current noise is the amount of thermoelectrons per pixel created by the dark current of the CCD, for its respective temperature. The read noise is a fluctuation in the value measured in each pixel of the CCD resulting of the readout process. The calculation of these paramters is given as a function of the operation mode of the CCD. Also, the calculation of the dark current noise and the read noise is based on the characterization of the SPARC4 CCDs, presented by [Bernardes et al. (2018)](https://arxiv.org/abs/1806.02191).

Then, it is created the noise image. To accomplish this, initially it is calculated the backgorund level (B<sub>L</sub>) of the image in ADU, as follows

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?B_L&space;=&space;B&space;&plus;&space;(S_{dc}&space;&plus;&space;S_{sky})&space;\times&space;G_{em}&space;\times&space;B_{in}^2&space;/&space;G." title="B_L = B + (S_{dc} + S_{sky}) \times G_{em} \times B_{in}^2 / G." />
</p>

where B represents the bias level of the CCD in ADU; the S<sub>dc</sub> is the mean of the thermoelectrons created by the CCD dark current, in e-/pix; the G<sub>em</sub> is the Electron Multiplying Gain of the CCD; the Bin is the number of pixels binned in the reading process; the G is the gain of the CCD. Once obtained the brackgroun level, it is calculated the image noise (N), in ADU. This noise is composed by the contibutions of the sky noise, the dark current noise, and the read noise as follows

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?N&space;=&space;\sqrt{(S_{sky}&space;&plus;&space;S_{dc})&space;/&space;G&space;\times&space;\;&space;(N_F&space;\;&space;G_{em}&space;\;&space;B_{in})^2&space;&plus;&space;\sigma_{ADU}^2&space;}" title="N = \sqrt{(S_{sky} + S_{dc}) / G \times \; (N_F \; G_{em} \; B_{in})^2 + \sigma_{ADU}^2 }" />
</p>

where N<sub>F</sub> is an extra noise factor of the use of the Electron Multiplying mode, and it equals 1.4. For the Conventional Mode, N<sub>F</sub> = 1; &sigma;<sub>ADU</sub> is the read noise in ADU. At the end of this process, it is created the noise image, with a backgorund level B<sub>L</sub> and a gaussian distribution for the image pixels with a standard deviation of N.

The next step is the creation of the star flux distribution. To accomplish this, it is used a 2D-Gaussian distribution provided by the [Astropy library](http://dx.doi.org/10.3847/1538-3881/aabc4f) as the star point spread function as follows:

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?f_p(x,y)=&space;C&space;e^{-&space;a(x&space;-&space;x_0)^2&space;\;&space;-&space;\;&space;b(x&space;-&space;x_0)&space;\times&space;(y&space;-&space;y_0)&space;\;&space;-&space;\;&space;c(y&space;-&space;y_0)^2}" title="f_p(x,y)= C e^{- a(x - x_0)^2 \; - \; b(x - x_0) \times (y - y_0) \; - \; c(y - y_0)^2}" />  
</p>

where

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?a&space;=&space;\frac{cos(\theta)^2}{2\delta^2_x}&space;&plus;&space;\frac{sin(\theta)^2}{2\delta^2_y}" title="a = \frac{cos(\theta)^2}{2\delta^2_x} + \frac{sin(\theta)^2}{2\delta^2_y}" />
</p>

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?b&space;=&space;\frac{sin(2&space;\theta)^2}{2\delta^2_x}&space;-&space;\frac{sin(2&space;\theta)^2}{2\delta^2_y}" title="b = \frac{sin(2 \theta)^2}{2\delta^2_x} - \frac{sin(2 \theta)^2}{2\delta^2_y}" />
</p>

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?c&space;=&space;\frac{sin(\theta)^2}{2\delta^2_x}&space;&plus;&space;\frac{cos(\theta)^2}{2\delta^2_y}" title="c = \frac{sin(\theta)^2}{2\delta^2_x} + \frac{cos(\theta)^2}{2\delta^2_y}" />
</p>


f<sub>p</sub>(x,y) is the star intensity in ADU, C represents the maximum amplitude in ADU, x and y are the coordinates over the image in pixels,x<sub>0</sub> and y<sub>0</sub> are the star coordinates in pixels, &delta;<sub>x</sub> and &delta;<sub>y</sub> are the standard deviation of the Gaussian in the directions x and y, respectively; &theta; is the rotation angle of the Gaussian.

The images created by the simulator have 200 x 200 pixels, the center coordinates of the star was fixed in (x<sub>0</sub>, y<sub>0</sub>) = (100,100) pixels; the values &delta;<sub>x</sub> = &delta;<sub>y</sub> and they should be provided to the software, and &theta; = 0. The maximum amplitude C, in ADU, for each mode is calculated through

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?C&space;=&space;\frac{\beta&space;\times&space;t_{exp}&space;\times&space;G_{em}&space;\times&space;Bin^2}{G}" title="C = \frac{\beta \times t_{exp} \times G_{em} \times Bin^2}{G}" />
</p>

where &beta; simulates a constant photon flux over the CCD, and it should be provided to the software. Finally, the image noise and the star flux distribution are added up, and the resulting image is saved in the FITS format.



## Running the AIG

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites
There are some packages that need to be installed before running the software.

[Astropy](https://www.astropy.org/)
```
pip install astropy
```
[Photutils](https://photutils.readthedocs.io/en/stable/)
```
pip install photutils
```
[Collections](https://docs.python.org/3/library/collections.html)
```
pip install collections
```
[JSON](https://www.w3schools.com/python/python_json.asp)
```
pip install json
```

### Installing
Clone this repo using ``` git clone https://github.com/DBernardes/Artificial-Images-Generator.git ```

## Running the tests

To run a simple test, you only need to execute the run.py file and the image would be created at your current directory. The run.py file will provided to the software the basic information for the execution, that are: the star flux, in photons/s; the sky flux, in photons/pix/s, the standard deviation of the guassian, in pixels, and the operation mode of the CCD. In particular, the CCD operation mode should be a python dictonary with the control parameters used ot configure the acquistion of the SPARC4 cameras. They are the Electron Multiplying Mode (em_mode), the Electron Multiplying Gain (em_gain), the Pre-amplification (preamp), the Horizontal Shift Speed (hss), the Pixels Binning (bin), and the Exposure Time (texp). Below, it is presented the accepted values for each parameter previously described.

- em_mode: 0 or 1
- em_gain: from 2 to 300
- preamp: 1 or 2
- hss: 0.1, 1, 10, 20, and 30
- bin: 1 or 2
- texp: greater or equal than 1e-5

## Authors and Contact

* **Denis Bernardes**: 

email: denis.bernardes099@gmail.com 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
