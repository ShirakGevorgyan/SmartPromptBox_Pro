#!/bin/bash

LOG_FILE="tests/performance/slow_gpt_log.txt"
MAX_LINES=1000
TRIM_LINES=500

if [ ! -f "$LOG_FILE" ]; then
    echo "⚠️ Լոգ ֆայլը գոյություն չունի։"
    exit 0
fi

total_lines=$(wc -l < "$LOG_FILE")

if [ "$total_lines" -ge "$MAX_LINES" ]; then
    echo "🧹 Trimming log file: $total_lines → $(($total_lines - $TRIM_LINES)) lines"
    tail -n +$((TRIM_LINES + 1)) "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
else
    echo "✅ Լոգ ֆայլը $total_lines տող է, trimming պետք չէ։"
fi
