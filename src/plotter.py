from matplotlib import pyplot as plt

x = [-53,21,41,-42,-38,49,14,-56,-9,53,-40,-41,41,38,-55,-13,56,8,-54,21,41,-42]
y = [-21,-53,40,39,-43,-29,56,12,-57,21,42,-41,-40,43,18,-56,-12,57,-21,-53,40,38]

plt.scatter(x,y)
plt.grid()
plt.xlim(-60,60)
plt.ylim(-60,60)
plt.figsize(300)
plt.show()