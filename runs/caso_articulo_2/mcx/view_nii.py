import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt


img = "base/caso_Gnyawali.nii"
nii = nib.load(img)
nii_data = nii.get_fdata()


# center of the image
nii_data = nii_data[:,299,::-1,0].T*1000**2


plt.imshow(nii_data, cmap='turbo')
plt.colorbar()