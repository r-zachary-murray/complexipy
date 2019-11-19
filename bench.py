import os
import numpy as np
import sys
import subprocess


ngrid = np.logspace(3,6,200).astype(int)
#ngrid = np.linspace(1,10000,10001).astype(int)
dt = 0.01
function = sys.argv[1]
print(ngrid)

directory = str(function)+'_bench'
print(directory)
os.mkdir(directory)


for n in ngrid:
	cmd = 'python mprof.py run -T '+str(dt)+' '+str(function)+'.py bench '+str(n)
	#print(cmd)
	os.system(cmd)
	#os.system('ls')
	#subprocess.call(["python", "mprof.py", "run", "-T", str(dt), str(function), "bench", str(n)])

os.system('mv *.dat '+directory)
