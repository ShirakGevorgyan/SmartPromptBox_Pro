#!/bin/bash

mkdir -p logs/test_check_logs

cd "$(dirname "$0")"

TEST_DIR="./"
LOG_DIR="./logs/test_check_logs"
SUMMARY_FILE="./logs/test_runs_summary.log"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_FILE="${LOG_DIR}/${TIMESTAMP}.log"
FAIL_FILE="${LOG_DIR}/${TIMESTAMP}_fail_only.log"

mkdir -p "$LOG_DIR"

test_files=$(find "$TEST_DIR" -type f -name "test_*.py" ! -path "*/__pycache__/*")

echo "🚀 Սկսում ենք բոլոր թեստերի ընթացքը..." > "$LOG_FILE"
echo "Թեստերի սկան՝ $TIMESTAMP" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

total=0
passed=0
failed=0

start_all=$(date +%s)

for file in $test_files; do
    ((total+=1))
    relative_path="${file#./}"
    echo -n "🚧 $relative_path ... " | tee -a "$LOG_FILE"

    start_test=$(date +%s)

    if PYTHONPATH="$(pwd)/.." pytest "$file" --maxfail=1 --disable-warnings -q; then

        result="✅ OK"
        ((passed+=1))
    else
        result="❌ FAIL"
        echo "❌ $relative_path" >> "$FAIL_FILE"
        ((failed+=1))
    fi

    end_test=$(date +%s)
    duration=$((end_test - start_test))
    echo "$result (${duration}s)" | tee -a "$LOG_FILE"
done

end_all=$(date +%s)
total_duration=$((end_all - start_all))

echo "==========================================" >> "$LOG_FILE"
echo "✔️ Ընդամենը թեստեր: $total" >> "$LOG_FILE"
echo "✅ Հաջողված: $passed" >> "$LOG_FILE"
echo "❌ Չհաջողված: $failed" >> "$LOG_FILE"
echo "🕒 Ընդհանուր տևողություն: ${total_duration}s վայրկյան" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

if [ $failed -gt 0 ]; then
    echo "🔴 ❗ Ունենք FAILED թեստեր, ստուգիր այս ֆայլը → $FAIL_FILE"
else
    echo "🟢 ✔️ Բոլոր թեստերը անցել են հաջողությամբ"
fi

echo "🟢 Լրիվ ավարտվեց։ Արդյունքները՝ $LOG_FILE"

echo "$TIMESTAMP | 🧪 Թեստեր՝ $total | ✅ $passed | ❌ $failed | 🕒 ${total_duration}s | 📄 $LOG_FILE" >> "$SUMMARY_FILE"

if [ ! -f "$LOG_FILE" ]; then
    echo "❗ Չկան թեստեր կամ լոգեր, սա placeholder ֆայլ է GitHub-ի համար" > "$LOG_FILE"
fi

if [ ! -f "$FAIL_FILE" ]; then
    touch "$FAIL_FILE"
fi


if [ $failed -gt 0 ]; then
    exit 1
else
    exit 0
fi
