import matplotlib.pyplot as plt
from datetime import datetime
import os
import re

LOG_FILE = "tests/performance/slow_gpt_log.txt"

if not os.path.exists(LOG_FILE):
    print("❌ Լոգ ֆայլը չի գտնվել։ Նախ թեստը վազեցրու։")
    exit()

timestamps = []
durations = []

with open(LOG_FILE, "r", encoding="utf-8") as f:
    for line in f:
        try:
            timestamp_match = re.search(r"^([0-9\-: T]+)", line)
            duration_match = re.search(r"\|\s*(OK|SLOW|FAIL)\s*\|\s*([\d.]+)\s*sec", line)

            if timestamp_match and duration_match:
                timestamp_str = timestamp_match.group(1).strip()
                duration_str = duration_match.group(2).strip()

                timestamp = datetime.fromisoformat(timestamp_str)
                duration = float(duration_str)

                timestamps.append(timestamp)
                durations.append(duration)
        except Exception as e:
            print(f"❌ Վերլուծության սխալ՝ {e}")

if not timestamps:
    print("⚠️ Չկան GPT արձագանքներ։")
    exit()

plt.figure(figsize=(10, 6))
plt.plot(timestamps, durations, marker="o", linestyle="-", color="blue", label="Response Time")

plt.axhline(y=4.0, color='orange', linestyle='--', label="⚠️ 4.0 sec threshold")
plt.axhline(y=15.0, color='red', linestyle='--', label="❌ 15.0 sec FAIL")

plt.xlabel("Ժամանակ")
plt.ylabel("Պատասխանի տևողություն (վրկ)")
plt.title("GPT արձագանքների ժամանակային գրաֆիկ")
plt.legend()
plt.grid(True)
plt.tight_layout()

output_path = "tests/performance/gpt_response_graph.png"
plt.savefig(output_path)
print(f"📈 Գրաֆիկը հաջողությամբ պահպանվեց՝ {output_path}")
plt.show()
