import os
import matplotlib.pyplot as plt

os.environ['TRIDENT_BACKEND']='cntk'
from cntk.internal import *

fig=plt.figure()
fn= layers.cntk_activations.selu
n=1
for k,v in fn.__globals__.items():
    try:
        if not isinstance(v,str) and v.__module__=='trident.backend.cntk_activations' and hasattr(v, '__call__'):
            #if int(v.__code__.co_argcount)>0:
                # for att in dir(v):
                #     print(att, getattr(v, att))
            print(k)
            f_name=k
            x = np.arange(-10, 10, 0.1).astype(np.float32)
            exposed_methods = {'v': v}
            y=eval('v()(x)',{'x': x}, exposed_methods)
            if hasattr(y,'value'):
                y = y.value
            elif hasattr(y,'asarray'):
                y = y.asarray()
            else:
                y=y.eval()

            ax1 = fig.add_subplot(3, 6, n)
            ax1.plot(x,y)
            ax1.plot(x[1:], np.diff(y) /(np.diff(x)+1e-8),ls=':')
            ax1.set_title(k)



            n+=1
    except Exception as e:
        print(e)
        pass

plt.show()
plt.savefig('{0}.png'.format(k), dpi=300, format='png')
plt.clf()
