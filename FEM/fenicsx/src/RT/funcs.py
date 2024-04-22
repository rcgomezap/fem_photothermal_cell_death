from dolfinx.fem import Function
def set_dofs_optical_properties(V,regions):
    mu_a = Function(V)
    mu_s = Function(V)
    g = Function(V)

    # mu_a.x.array[tumor_dofs] = domain_tumor.mu_a
    # mu_a.x.array[tejido_dofs] = domain_tejido.mu_a

    # mu_s.x.array[tumor_dofs] = domain_tumor.mu_s
    # mu_s.x.array[tejido_dofs] = domain_tejido.mu_s

    # g.x.array[tumor_dofs] = domain_tumor.g
    # g.x.array[tejido_dofs] = domain_tejido.g

    for region, tag in regions.items():
        mu_a.x.array[tag[3]] = tag[2].mu_a
        mu_s.x.array[tag[3]] = tag[2].mu_s
        g.x.array[tag[3]] = tag[2].g

    return mu_a,mu_s,g