
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 

pp_ = """

安装完成后支持 提示重启 VSCode， 且有 重新启动扩展 按钮
"""



x = np.arange(100)
y = np.sin(x/180 * np.pi)

plt.plot(x, y)
plt.show()