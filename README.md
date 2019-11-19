Python scripy for getting the time and space complexity of algorithyms.

bench.py does a benchmark of the function preformance using memory profiler's 'mprof.py' as a dependency (See documentation here https://pypi.org/project/memory-profiler/) 

analyze.py does a fit of the resulting data from a preset suite of asymtotic complexities and estimates coefficients and intercepts and produces a png output. 

run.sh executes both of the above files sequentially and compiles the data results into a .7z file for futher analysis. 


Some examples of the script are below:


for pollardrho factorization: 

![factor_pollardrho](factor_pollardrho.png)

for karatsuba multiplication: 

![multiplication_karatsuba](multiplication_karatsuba.png)

for the binary split algorithym for factorials: 

![factorial_binarysplit](factorial_binarysplit.png)
