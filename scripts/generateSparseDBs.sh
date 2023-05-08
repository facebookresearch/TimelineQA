#!/usr/bin/zsh
for i in {0..999}
do
    echo "Generating sparse-$i.json year=2022, seed=$((12345+$i))..."
    \rm -rf benchmark/sparse-$i
    mkdir benchmark/sparse-$i
    python3 generateDB.py -y 2022 -s $((12345+$i)) -c "sparse" -d benchmark/sparse-$i -o sparse-$i.json
    echo "Done!"
done
