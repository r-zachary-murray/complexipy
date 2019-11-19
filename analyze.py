import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import csv
from scipy.optimize import curve_fit
import sys

algo = str(sys.argv[1]).split('.')[0]
path = './'+algo+'_bench/'
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

def parse(file):
    col0 = []
    col1 = []
    col2 = []
    ns = []

    with open(path+file, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            col0.append(row[0])
            col1.append(row[1])
            col2.append(row[2])
            try:
                ns.append(row[4])
            except:
                IndexError           
    #print(col2)

    indexes = []
    for i in range(len(col0)):
        if col0[i] == 'CMDLINE':
            indexes.append(i)

    indexes.append(len(col0))

    def getarray(n,m):
        res = []
        for i in range(n+1,m):
            res.append([col1[i],col2[i]])
        return np.asarray(res).astype(np.float64)

    arrays = []
    for i in range(len(indexes)-1):
        arrays.append(getarray(indexes[0],indexes[1]))
    return np.asarray(ns).astype(int),arrays
#############

ns = []
data = []
for i in range(len(onlyfiles)):
    n,a = parse(onlyfiles[i])
    for i in range(len(n)):
        ns.append(n[i])
        data.append(a[i])
ns=np.asarray(ns)

#Shows the individual memory/time graphs
# alphas = np.log10(ns)/np.max(np.log10(ns))
# for i in range(len(ns)):
#     mem = data[i].T[0]
#     times = data[i].T[1]
#     times = times - np.min(times)
#     plt.plot(times,mem,c='k',alpha=alphas[i])


memmax = []
tmax = []
for i in range(len(ns)):
    mem = data[i].T[0] 
    times = data[i].T[1]
    mem = mem - np.min(mem)
    times = times - np.min(times)
    memmax.append(np.max(mem))
    tmax.append(np.max(times))
    
memmax = np.asarray(memmax)

memmin = np.min(memmax)
tmin = np.min(tmax)
dM = memmax - memmin
dT = tmax - tmin
aray = [ns,dM,dT]
naray = np.sort(aray)
ns = naray[0].astype(int)
dM = naray[1]
dT = naray[2]

fmt = lambda x: '%.2E' % x


def constant(x,a):
    return a*np.ones(len(x))
def logarithmic(x,a):
    return a*np.log2(x)
def root(x,a):
    return a*np.sqrt(x)
def linear(x,a):
    return x*a
def loglinear(x,a):
    return a*x*np.log2(x)
def square(x,a):
    return a*(x**2)
def cube(x,a):
    return a*(x**3)
def exponential(x,a):
    return a*(2**x)
functions = [constant,logarithmic,root,linear,loglinear,square,cube,exponential]
fname = [r"$\mathcal{O}(1)$",r"$\mathcal{O}(\log_2{n})$",r"$\mathcal{O}(\sqrt{n})$",
          r"$\mathcal{O}(n)$",r"$\mathcal{O}(n\log_2{n})$",r"$\mathcal{O}(n^2)$",
          r"$\mathcal{O}(n^3)$",r"$\mathcal{O}(2^n)$"]


merr = np.inf
terr = np.inf
mparms = 0
tparms = 0
for i in range(len(functions)):
    
    xs = ns
    popt_m, pcov = curve_fit(functions[i], xs, dM)
    popt_t, pcov = curve_fit(functions[i], xs, dT)
    ys_m = functions[i](xs,popt_m[0])
    ys_t = functions[i](xs,popt_t[0])
    rms_m = np.sqrt(np.mean((ys_m-dM)**2))
    rms_t = np.sqrt(np.mean((ys_t-dT)**2))
    
    #plot individual fits
#     plt.scatter(xs,dM,c='b')
#     plt.plot(xs,ys_m,c='b')
#     plt.scatter(xs,dT,c='r')
#     plt.plot(xs,ys_t,c='r')
#     plt.show()
#     print(rms_m,rms_t)

    if rms_m < merr:
        mparms = [popt_m,functions[i],fname[i]]
        merr = rms_m
    if rms_t < terr:
        tparms = [popt_t,functions[i],fname[i]]
        terr = rms_t


fig,ax = plt.subplots(ncols=2,figsize=(15,7))

ax[0].scatter(ns,dM+memmin)
ax[0].plot(ns,mparms[1](ns,mparms[0])+memmin,c='r')
ax[0].set_title(mparms[2]+r': $C_1$='+str(fmt(mparms[0][0]))+' min='+str(fmt(memmin)))
ax[0].set_xlabel('N')
ax[0].set_ylabel('Memory [MB]')

ax[1].scatter(ns,dT+tmin)
ax[1].plot(ns,tparms[1](ns,tparms[0])+tmin,c='r')
ax[1].set_title(tparms[2]+r': $C_1$='+str(fmt(tparms[0][0]))+' min='+str(fmt(tmin)))
ax[1].set_xlabel('N')
ax[1].set_ylabel('Execution Time [S]')
#plt.savefig(path+algo+'.png')
plt.savefig(algo+'.png')
#plt.show()











































