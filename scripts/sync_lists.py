#!/usr/bin/env python3
"""Sync Checklists/Lists/*.md against Checklists/Practice_Log.md.

Reads every `## YYYY-MM-DD` block in the log, collects `- <num>.` lines,
and marks those problems `[x]` + `✔ <earliest date>` in every list file.
Everything else is unchecked. Idempotent — safe to run after every log edit.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "Checklists", "Practice_Log.md")
LISTS = sorted(glob.glob(os.path.join(ROOT, "Checklists", "Lists", "*.md")))

def parse_log():
    solved = {}
    parts = re.split(r"^## (\d{4}-\d{2}-\d{2})\s*$", open(LOG).read(), flags=re.M)
    for i in range(1, len(parts), 2):
        date, body = parts[i], parts[i + 1]
        for n in re.findall(r"^- (\d+)\.", body, flags=re.M):
            n = int(n)
            solved[n] = min(solved.get(n, date), date)
    return solved

# `- [ ] **1.** [Two Sum](...) — ...`   (master + four source lists)
BOLD = re.compile(r"^- \[[ x]\] \*\*(\d+)\.\*\*(.*)$")
# `- [ ] 1. Two Sum — *Hash Table* · 15 min`   (warmup)
PLAIN = re.compile(r"^- \[[ x]\] (\d+)\. (.*)$")
STAMP = re.compile(r" · <sub>✔ \d{4}-\d{2}-\d{2}</sub>$")
HEADER = re.compile(r"\*\*(?:已刷|進度)：\d+ / (\d+)\*\*")

def sync(path, solved):
    out, cnt, total = [], 0, 0
    for line in open(path).read().split("\n"):
        m = BOLD.match(line)
        if m:
            n, rest = int(m.group(1)), STAMP.sub("", m.group(2))
            total += 1
            if n in solved:
                cnt += 1; line = f"- [x] **{n}.**{rest} · <sub>✔ {solved[n]}</sub>"
            else:
                line = f"- [ ] **{n}.**{rest}"
        else:
            m = PLAIN.match(line)
            if m:
                n, rest = int(m.group(1)), STAMP.sub("", m.group(2))
                total += 1
                if n in solved:
                    cnt += 1; line = f"- [x] {n}. {rest} · <sub>✔ {solved[n]}</sub>"
                else:
                    line = f"- [ ] {n}. {rest}"
        out.append(line)
    text = HEADER.sub(lambda m: f"**已刷：{cnt} / {m.group(1)}**", "\n".join(out))
    open(path, "w").write(text)
    return cnt, total

def main():
    solved = parse_log()
    print(f"Practice_Log: {len(solved)} problems solved")
    for p in LISTS:
        cnt, total = sync(p, solved)
        print(f"  {os.path.basename(p):32s} {cnt:3d} / {total}")

if __name__ == "__main__":
    main()
