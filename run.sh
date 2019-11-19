python3 bench.py $1
python3 analyze.py $1
cd $1"_bench"
7z a -r ../$1"_bench" *
cd .. 

rm -r $1"_bench"
