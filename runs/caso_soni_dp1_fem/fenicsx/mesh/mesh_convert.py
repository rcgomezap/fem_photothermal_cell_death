import meshio
# Read mesh
msh = meshio.read("FEM/fenicsx/mesh/msh/malla.msh")


def create_mesh(mesh, cell_type, prune_z=False):
    cells = mesh.get_cells_type(cell_type)
    cell_data = mesh.get_cell_data("gmsh:physical", cell_type)
    points = mesh.points[:,:2] if prune_z else mesh.points
    out_mesh = meshio.Mesh(points=points, cells={cell_type: cells}, cell_data={"name_to_read":[cell_data]})
    return out_mesh


triangle_mesh = create_mesh(msh, "triangle")
line_mesh = create_mesh(msh, "line")
meshio.write("FEM/fenicsx/mesh/xdmf/mesh_triangle.xdmf", triangle_mesh)
meshio.write("FEM/fenicsx/mesh/xdmf/mesh_line.xdmf", line_mesh)