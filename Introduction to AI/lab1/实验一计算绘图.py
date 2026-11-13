import sys, platform, importlib.metadata as md
print("OS:", platform.system(), platform.mac_ver()[0])
print("Architecture:", platform.machine())
print("Python:", platform.python_version())
print("Interpreter:", sys.executable)
for name in ["conda", "notebook", "numpy", "pandas", "matplotlib"]:
    print(f"{name}: {md.version(name)}")

print("hello,world")
print("test")
print("6 + 7 =", 6 + 7)

import numpy as np
x = np.array([1, 2, 3, 4, 5])
print("x =", x)
print("x squared =", x ** 2)
print("sum =", x.sum())
print("mean =", x.mean())

import pandas as pd
df = pd.DataFrame({"x": x, "square": x ** 2})
print(df.to_string(index=False))
print("square mean =", df["square"].mean())

import matplotlib.pyplot as plt
plt.figure(figsize=(6, 3.2))
plt.plot(df["x"], df["square"], marker="o", label="y = x^2")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Simple Calculation and Plot")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("calculation_plot.png", dpi=180)
plt.show()