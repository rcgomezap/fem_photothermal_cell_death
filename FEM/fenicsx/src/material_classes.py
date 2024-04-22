class Material_Bioheat():
        def __init__(self, k, rho, c, w, Qmet):
            self.k = k
            self.rho = rho
            self.c = c
            self.w = w
            self.Qmet = Qmet
class Material_Bioheat_Blood():
        def __init__(self, T, rho, cp):
            self.T = T
            self.rho = rho
            self.cp = cp
class Material_Optical():
        def __init__(self, mu_a, mu_s, g):
            self.mu_a = mu_a
            self.mu_s = mu_s
            self.g = g