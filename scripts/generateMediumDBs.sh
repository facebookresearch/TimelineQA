#!/usr/bin/zsh
for i in {0..999}
do
    echo "Generating medium-$i.json year=2022, seed=$((12345+$i))..."
    \rm -rf benchmark/medium-$i
    mkdir benchmark/medium-$i
    python3 generateDB.py -y 2022 -s $((12345+$i)) -c "medium" -d benchmark/medium-$i -o medium-$i.json
    echo "Done!"
done
