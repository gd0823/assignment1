#!/bin/bash
set -e

# Compile first
g++ -O2 -o bin/sampler src/sampler.cpp

TIMING_DIR=$(mktemp -d)
COUNT=0

# Run sampler for all date/symbol combinations in marketdata
for date_dir in marketdata/*/; do
    date=$(basename "$date_dir")
    for bin_file in "$date_dir"*.bin; do
        [ -f "$bin_file" ] || continue
        symbol=$(basename "$bin_file" .bin)
        COUNT=$((COUNT + 1))
        echo "$date $symbol $COUNT"
    done
done | xargs -P4 -I{} bash -c '
    set -- {}
    date=$1; symbol=$2; idx=$3
    timing_dir='"\"$TIMING_DIR\""'
    time_output=$(/usr/bin/time -f "%U %S %e" ./bin/sampler "$date" "$symbol" 2>&1 1>/dev/null)
    # last line is the time output: user_s sys_s real_s
    time_line=$(echo "$time_output" | tail -1)
    user_t=$(echo "$time_line" | awk "{print \$1}")
    sys_t=$(echo "$time_line" | awk "{print \$2}")
    real_t=$(echo "$time_line" | awk "{print \$3}")
    # convert user time to ms
    user_ms=$(echo "$user_t" | awk "{printf \"%d\", \$1 * 1000}")
    echo "${user_ms}" > "$timing_dir/${idx}_${date}_${symbol}.time"
    printf "[%s %s] user: %ss  sys: %ss  real: %ss\n" "$date" "$symbol" "$user_t" "$sys_t" "$real_t"
'

# Summary
echo ""
echo "========== Summary =========="
total=0
count=0
for f in "$TIMING_DIR"/*.time; do
    [ -f "$f" ] || continue
    t=$(cat "$f")
    total=$((total + t))
    count=$((count + 1))
done
rm -rf "$TIMING_DIR"

if [ "$count" -gt 0 ]; then
    avg=$((total / count))
    echo "Total runs:     $count"
    echo "Total time:     ${total} ms"
    echo "Average time:   ${avg} ms"
else
    echo "No runs executed."
fi

echo ""
echo "========== Scoring =========="
python3.14 score.py