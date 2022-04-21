import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def p_ii_t(k):
    return  0.25 + 0.75 * np.exp(-4*k)


def p_ij_t(k):
    return  0.25 - 0.25 * np.exp(-4*k)
plt.figure(dpi=150,figsize=(3,3))

k = np.arange(0,2,0.001)

p_ii = p_ii_t(k)
p_ij = p_ij_t(k)

plt.plot(k,p_ii,"g",label="p_ii")
plt.plot(k,p_ij,"r",label="p_ij")

plt.xlabel("αt")
plt.ylabel("p(αt)")
plt.title("time ~ p(αt)")

plt.legend()
