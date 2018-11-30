# Expand a collection of problems into a set of SGFs.

COLLECTION=../"minigo/collection.csv"
COLLECTION_SRC=~/"Projects/training/badukmovies-pro-75komi-1000/"
COLLECTION_DIR=~/"Projects/training/problem-collection2/"

echo "collection: $COLLECTION"
echo "dir: $COLLECTION_DIR"

if [ ! -f "$COLLECTION" ]; then
    cd ../minigo/
    BOARD_SIZE=19 python3 oneoffs/subsample_pro.py --sgf_dir "$COLLECTION_SRC" --num_positions 10
    cd -
fi

# Copy each SGF into a new directory
mkdir -p "$COLLECTION_DIR"
if [ -z "$(ls -A "$COLLECTION_DIR")" ]; then
    echo "Moving SGFs to dir"
    cat "$COLLECTION" | cut -f1 -d',' | sort -u | xargs cp -t "$COLLECTION_DIR"

    # new dir + filename for each line
    sed -i "s#^.*/\([^/]*sgf\)#$COLLECTION_DIR\1#" "$COLLECTION"
fi

# Count number of files
echo "SGFS: $(ls "$COLLECTION_DIR" | wc -l)"

# Remove hard sgfs
sgfcheck -nokfn -r "$COLLECTION_DIR" 2>/dev/null > badfiles.txt
find "$COLLECTION_DIR" -iname "*'*" >> badfiles.txt
grep --color=never -rL 'KM\[7.5\]' "$COLLECTION_DIR" >> badfiles.txt
grep --color=never -rL 'RE\[[BW]+[0-9.R]\{1,\}]' "$COLLECTION_DIR" >> badfiles.txt
BAD_COUNT="$(cat badfiles.txt | wc -l)"
echo "badfiles: $BAD_COUNT in badfiles.txt"

echo
sgfinfo -m "$COLLECTION_DIR"* | sort -n | cut -f1 -d' ' | ministat
#      N           Min           Max        Median           Avg        Stddev
# x 9940             0           340           101     107.90624     69.931731

# For each file split and truncate
if [ 0 -eq $BAD_COUNT ]; then
    echo "Expanding"
    cat "$COLLECTION" | tr -d ',' | tqdm | xargs -P 3 -I{} sh -c "python truncate.py {}"
fi

cat "$COLLECTION" | cut -f1 -d',' | grep "\.sgf$" | sort -u | wc -l
