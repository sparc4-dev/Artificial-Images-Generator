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
<img src="https://latex.codecogs.com/svg.latex?B_L&space;=&space;B&space;&plus;&space;\frac{(DC&space;&plus;&space;Sky)&space;\times&space;T_{exp}&space;\times&space;G_{em}&space;\times&space;Bin^2}{G}" title="B_L = B + \frac{(DC + Sky) \times T_{exp} \times G_{em} \times Bin^2}{G}" /></a>
</p>

where B represents the bias level of the CCD in ADU; the DC is dark current of the CCD in e-/pix/s; the Sky is the sky flux in photons/pix/s; T<sub>exp</sub> is the exposure time in seconds; the G<sub>em</sub> is the Electron Multiplying Gain of the CCD; the Bin is the number of pixels binned in the reading process; the G is the gain of the CCD. Once obtained the brackgroun level, it is calculated the image noise (N), in ADU. This noise is composed by the contibutions of the sky noise, the dark current noise, and the read noise as follows

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?N&space;=&space;\sqrt{(S_{sky}&space;&plus;&space;S_{dc})&space;/&space;G&space;\times&space;\;&space;(N_F&space;\;&space;G_{em}&space;\;&space;B_{in})^2&space;&plus;&space;\sigma_{ADU}^2&space;}" title="N = \sqrt{(S_{sky} + S_{dc}) / G \times \; (N_F \; G_{em} \; B_{in})^2 + \sigma_{ADU}^2 }" />
</p>

where S<sub>sky</sub> is the sky flux in photons/pix; the S<sub>dc</sub> is the mean of the thermoelectrons created by the CCD dark current, in e-/pix; N<sub>F</sub> is an extra noise factor of the use of the Electron Multiplying mode, and it equals 1.4. For the Conventional Mode, N<sub>F</sub> = 1; &sigma;<sub>ADU</sub> is the read noise in ADU.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites
There are some packages that need to be installed before running the software. The first one is the Software Development Kit (SDK) developed by Andor Technology to control the CCDs. The second one is the GFITSIO package, used to save the data acquired by the camera in FITS format. 

![Software Development Kit (SDK)](https://andor.oxinst.com/products/software-development-kit/)

![GFITSIO](https://github.com/USNavalResearchLaboratory/GFITSIO)


### Installing
Clone this repo using ``` git clone https://github.com/DBernardes/SPARC4_ACS.git ```

## Running the tests
1. Before running the software, you need EMCCD to be connected to your PC.
2. Open the project SPARC4_AC.lvproj.
3. Run the VI SPARC4_GUI.vi.
4. Wait until the camera starts.
5. Set the night directory where the acquired images should be saved.
6. Press the Acquire button to start an acquisition. This would allow you to obtain a FITS files in your directory with the data acquired by the camera.

## Authors and Contact

* **Denis Bernardes**: 

email: denis.bernardes099@gmail.com 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
