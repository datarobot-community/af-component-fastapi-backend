#!/usr/bin/env bash

# Run from the app dir so `app.main` and PYTHONPATH resolve.
cd "$(dirname "$0")" || exit 1

# Get the number of CPU cores
if [ -f /sys/fs/cgroup/cpu.max ] && ! grep -q "max" /sys/fs/cgroup/cpu.max; then
    read -r max period < /sys/fs/cgroup/cpu.max
    cpu_cores=$((max / period))
else
    cpu_cores=$(nproc)
fi

# Calculate the recommended number of workers
workers=$((cpu_cores * 2 + 1))

# Ensure at least 2 workers are started
if [[ $workers -lt 2 ]]; then
  workers=2
fi

# core isn't pip-installed (cached build installs third-party deps only), so
# put it on PYTHONPATH and launch system Python instead of `uv run`.
export PYTHONPATH="$PWD/core/src${PYTHONPATH:+:$PYTHONPATH}"

echo "Starting App with ${workers} workers"
python3 -m uvicorn app.main:app --workers "$workers" --host 0.0.0.0 --port 8080 --proxy-headers --timeout-keep-alive 300
