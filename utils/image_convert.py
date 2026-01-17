import numpy as np
import nibabel as nib

def convert_jnii_to_nii_jdata(input_path, output_path=None):
    """
    Convert a JNIfTI (.jnii) file to standard NIfTI (.nii) format using jdata library.
    Requires: pip install jdata
    
    Parameters:
    -----------
    input_path : str
        Path to the input .jnii file
    output_path : str, optional
        Path for the output .nii file. If None, will replace .jnii with .nii
    
    Returns:
    --------
    str
        Path to the output file
    """
    try:
        import jdata as jd
    except ImportError:
        raise ImportError("jdata library required. Install with: pip install jdata")
    
    # Load JNIfTI file
    data = jd.load(input_path)
    
    # Extract NIfTI data and header
    if 'NIFTIData' in data:
        img_data = np.array(data['NIFTIData'])
    else:
        # Data might be at root level
        img_data = np.array(data)
    
    print(f"Original shape: {img_data.shape}")
    
    # Remove only the last singleton dimension to get (400, 400, 100, 1)
    # MC_interp expects imgdata[mid_L, :, :, 0]
    if img_data.ndim == 5 and img_data.shape[-1] == 1:
        img_data = img_data.squeeze(axis=-1)
        print(f"Squeezed shape: {img_data.shape}")
    
    # Create affine (identity matrix as default)
    affine = np.eye(4)
    
    # Try to get voxel size if available
    if 'NIFTIHeader' in data and 'Pixdim' in data['NIFTIHeader']:
        pixdim = data['NIFTIHeader']['Pixdim']
        if len(pixdim) >= 4:
            affine[0, 0] = pixdim[1]
            affine[1, 1] = pixdim[2]
            affine[2, 2] = pixdim[3]
    
    # Create NIfTI image
    nii_img = nib.Nifti1Image(img_data, affine)
    
    # Generate output path if not provided
    if output_path is None:
        output_path = input_path.rsplit('.jnii', 1)[0] + '.nii'
    
    # Save as NIfTI
    nib.save(nii_img, output_path)
    
    print(f"Converted {input_path} to {output_path}")
    print(f"Image shape: {img_data.shape}")
    print(f"Data type: {img_data.dtype}")
    
    return output_path