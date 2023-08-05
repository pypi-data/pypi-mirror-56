=======================
Powerfit scipion plugin
=======================

Program from Alexandre Bonvin and Gydo van Zundert (Utrecht University) for rigid body fitting of an atomic structure into a 3D volume. See `Powerfit home page <http://www.bonvinlab.org/education/powerfit>`_ for details).


===================
Install this plugin
===================

You will need to use `2.0.0 <https://github.com/I2PC/scipion/releases/tag/v2.0>`_ version of Scipion to run these protocols. To install the plugin, you have two options:

- **Stable version**  

.. code-block:: 

      scipion installp -p scipion-em-powerfit
      
OR

  - through the plugin manager GUI by launching Scipion and following **Configuration** >> **Plugins**
      
- **Developer's version** 

1. Download repository: 

.. code-block::

            git clone https://github.com/scipion-em/scipion-em-powerfit.git
            
2. Install:

.. code-block::

           scipion installp -p path_to_scipion-em-powerfit --devel
 
 
- **Binary files** 

Powerfit binary file is installed with the plugin. 


- **Tests**

Tested with Powerfit version: 2.0.

To check the installation, simply run the following Scipion test: 

* scipion test powerfit_scipion.tests.test_powerfit


- **Supported versions of Powerfit**

2.0



=========
Protocols
=========

* powerfit-scipion: *Powerfit* program functionality. 



========
Examples
========

See `Model Building Tutorial <https://github.com/I2PC/scipion/wiki/tutorials/tutorial_model_building_basic.pdf>`_

Additionally, `here <http://www.bonvinlab.org/education/powerfit/>`_ you have the *Tutorial* from the original developer.


===============
Buildbot status
===============

Status devel version: 

.. image:: http://scipion-test.cnb.csic.es:9980/badges/powerfit_devel.svg

Status production version: 

.. image:: http://scipion-test.cnb.csic.es:9980/badges/powerfit_prod.svg

