===================
Django Image Field
===================

Overview
========

- This Image field Provides functionality for **Compression** and **Dimension** of image at uploading time.


Installation
=============

- Installation -
   * Run ::

      pip install djimage

   * Add 'djimage' to your INSTALLED_APPS ::

      'djimage',

   * Import CompressImageField in your models.py file ::

      from djimage.field import CompressImageField

      image = CompressImageField(upload_to='images/')

                  **OR**

      # dim parameter is optional for convert image into specific dimension
      image = CompressImageField(upload_to='images/', dim=(100, 100))

