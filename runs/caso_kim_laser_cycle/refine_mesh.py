#!/usr/bin/env python3
"""
Script for refining the mesh with custom tumor refinement parameters.

This script:
1. Reads mesh_refinement_tumor.geo.template
2. Replaces {tumor_refinement} with a value from command line arguments
3. Saves the result to mesh_refinement_tumor.geo
4. Runs gmsh to generate mesh.msh
5. Runs fenicsx_args as a subprocess

Usage Examples:
    # Basic usage with default refinement value (0.1)
    python refine_mesh.py

    # Specify custom tumor refinement value for finer mesh
    python refine_mesh.py --tumor_refinement 0.05

    # Specify custom tumor refinement value for coarser mesh
    python refine_mesh.py --tumor_refinement 0.2

    # Use custom mesh directory
    python refine_mesh.py --tumor_refinement 0.1 --mesh_dir custom/mesh/path

    # Specify custom gmsh executable path
    python refine_mesh.py --tumor_refinement 0.08 --gmsh_executable /usr/local/bin/gmsh

    # Full example with all parameters
    python refine_mesh.py --tumor_refinement 0.03 --mesh_dir fenicsx/mesh/msh --gmsh_executable gmsh

Notes:
    - Lower tumor_refinement values (e.g., 0.01-0.05) create finer meshes with more elements
    - Higher tumor_refinement values (e.g., 0.1-0.5) create coarser meshes with fewer elements
    - The script expects mesh_refinement_tumor.geo.template to exist in the specified mesh directory
    - Gmsh must be installed and accessible in PATH (or specify full path with --gmsh_executable)
    - The script runs fenicsx_args.py from the current working directory after mesh generation to convert the mesh to fenicsx format and run simulations
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Refine mesh with custom tumor refinement value')
    parser.add_argument('--tumor_refinement', type=float, default=0.1,
                        help='Tumor refinement value (default: 0.1)')
    parser.add_argument('--mesh_dir', type=str, default='fenicsx/mesh/msh',
                        help='Directory containing mesh files (default: fenicsx/mesh/msh)')
    parser.add_argument('--gmsh_executable', type=str, default='gmsh',
                        help='Gmsh executable name or path (default: gmsh)')
    
    args = parser.parse_args()
    
    # Define paths
    mesh_dir = Path(args.mesh_dir)
    template_path = mesh_dir / 'mesh_refinement_tumor.geo.template'
    output_geo_path = mesh_dir / 'mesh_refinement_tumor.geo.tmp'
    output_msh_path = mesh_dir / 'mesh.msh'
    
    # Check if template file exists
    if not template_path.exists():
        print(f"Error: Template file not found: {template_path}")
        sys.exit(1)
    
    # Read template file
    print(f"Reading template file: {template_path}")
    try:
        with open(template_path, 'r') as f:
            template_content = f.read()
    except Exception as e:
        print(f"Error reading template file: {e}")
        sys.exit(1)
    
    # Replace placeholder with actual value
    print(f"Replacing {{tumor_refinement}} with {args.tumor_refinement}")
    refined_content = template_content.replace('{tumor_refinement}', str(args.tumor_refinement))
    
    # Write the refined geometry file
    print(f"Writing refined geometry file: {output_geo_path}")
    try:
        with open(output_geo_path, 'w') as f:
            f.write(refined_content)
    except Exception as e:
        print(f"Error writing geometry file: {e}")
        sys.exit(1)
    
    # Run gmsh to generate mesh
    print(f"Running gmsh to generate mesh: {output_msh_path}")
    try:
        gmsh_cmd = [args.gmsh_executable, '-2', str(output_geo_path), '-o', str(output_msh_path)]
        print(f"Executing: {' '.join(gmsh_cmd)}")
        result = subprocess.run(gmsh_cmd, check=True, capture_output=True, text=True)
        print("Gmsh output:")
        print(result.stdout)
        if result.stderr:
            print("Gmsh stderr:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running gmsh: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: gmsh executable not found: {args.gmsh_executable}")
        print("Please make sure gmsh is installed and in your PATH, or specify the path with --gmsh_executable")
        sys.exit(1)
    
    # Check if mesh file was created
    if not output_msh_path.exists():
        print(f"Error: Mesh file was not created: {output_msh_path}")
        sys.exit(1)
    
    print(f"Successfully generated mesh: {output_msh_path}")
    
    # Run fenicsx_args as subprocess
    print("Running fenicsx_args.py as subprocess...")
    try:
        fenicsx_cmd = [sys.executable, 'fenicsx_args.py']
        print(f"Executing: {' '.join(fenicsx_cmd)}")
        result = subprocess.run(fenicsx_cmd, check=True, capture_output=True, text=True)
        print("fenicsx_args output:")
        print(result.stdout)
        if result.stderr:
            print("fenicsx_args stderr:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running fenicsx_args.py: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: fenicsx_args.py not found in current directory")
        sys.exit(1)
    
    print("Mesh refinement process completed successfully!")


if __name__ == '__main__':
    main()