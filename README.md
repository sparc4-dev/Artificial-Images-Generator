# Artificial Images Generator
This repo contains the software of the Artificial Images Generator (AIG). The AIG was developed to create artificial star images, simulating the star images acquired by CCD cameras in astronomical. To create the images, the AIG models the star flux distribution as a 2D-Gaussian Distribution. This result is added to a noise image, created based a set of parameters provided to the software, as the CCD operation mode, the star flux and the sky flux. Figure below presents an example of an image created by the AIG

This READ.ME explains step-by-step procedure of the AIG to create the imagens, as well as, it presents a simple execution example.


<p align="center">
  <img src="https://github.com/DBernardes/Artificial-Images-Generator/blob/main/artificial_star.png" />
</p>


## Software Description

The AIG is a software developed using the Python 3 language. It is operation can be divided in the parameters configuration step, the creation of a noise image step and, the creation of the star flux step. In the parameters configuration step, the AIG will calcute the gain, dark current noise and read noise of the CCD. The CCD gain is the converstion value of the acquired photoelectrons in Analogical-to-Ditial Unit (ADU). The dark current noise, in electrons, is the amount of thermoelectrons created by the dark current of the CCD, for its respective temperature. The read noise is a fluctuation in the value measured in each pixel of the CCD resulting of the readout process. The calculation of these paramters is given as a function of the operation mode of the CCD. Also, the calculation of the dark current noise and the read noise is bases on the characterization of the SPARC4 CCDs, presented by [Bernardes et al. (2018)](https://arxiv.org/abs/1806.02191).

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
