#!/bin/bash

LOG_FILE="tests/performance/slow_gpt_log.txt"
TEST_FILE="tests/performance/test_gpt_response_time.py"
TRIM_SCRIPT="tests/performance/trim_log_file.sh"


if [ -f "$TRIM_SCRIPT" ]; then
    bash "$TRIM_SCRIPT"
else
    echo "⚠️ trim_log_file.sh ֆայլը բացակայում է։"
fi

echo ""
echo "🚀 Վազեցնում ենք GPT performance թեստը 10 անգամ..."
for i in {1..10}
do
    echo "👉 Թեստ $i/10"
    PYTHONPATH=. pytest "$TEST_FILE" > /dev/null
    sleep 1
done

echo ""
echo "📊 Վերլուծում ենք վերջին 10 արդյունքները..."

if [ ! -f "$LOG_FILE" ]; then
    echo "❌ Լոգ ֆայլը չի գտնվել։"
    exit 1
fi

durations=$(tail -n 10 "$LOG_FILE" | awk -F '|' '{gsub(/ sec/, "", $3); print $3}' | tr -d ' ')

count=0
sum=0

while read -r value; do
    if [[ $value =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
        sum=$(echo "$sum + $value" | bc)
        count=$((count + 1))
    fi
done <<< "$durations"

if [ "$count" -lt 5 ]; then
    echo "⚠️ Չկա բավարար տվյալ միջինը հաշվելու համար։"
    exit 1
fi

avg=$(echo "scale=3; $sum / $count" | bc)
echo ""
echo "📈 Միջին պատասխան ժամանակը՝ $avg վայրկյան"

if (( $(echo "$avg < 7.0" | bc -l) )); then
    echo "✅ GPT performance թեստը համարվում է **անցած** ✅"
    exit 0
else
    echo "❌ GPT performance թեստը **չանցավ**։ Պատասխանները չափազանց դանդաղ են։"
    exit 1
fi
