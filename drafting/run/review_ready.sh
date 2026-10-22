#!/usr/bin/env bash
# Start judge + verify (default model, medium) for every section marked .ready that has not been reviewed yet.
cd "C:/Users/User/Desktop/Anugrah/OCR2Md" || exit 1
declare -A CFG=([1]=drafting/ch01/cfg_ch01v5.py [2]=drafting/ch02/cfg_ch02v3.py [3]=drafting/ch03/cfg_ch03v2.py)
for f in drafting/run/ch*/*.ready; do
  [ -e "$f" ] || continue
  sec=$(basename "$f" .ready); ch=${sec%%.*}; d=drafting/run/ch$ch
  [ -e "$d/$sec.review_started" ] && continue
  touch "$d/$sec.review_started"
  echo "review $sec $(date +%H:%M:%S)"
  (UDAY_CFG=${CFG[$ch]} python -I -X utf8 drafting/_pipe/inhouse.py judge "$sec" > "$d/${sec}_judge.out" 2>&1 &)
  (UDAY_CFG=${CFG[$ch]} python -I -X utf8 drafting/_pipe/inhouse.py verify "$sec" > "$d/${sec}_verify.out" 2>&1 &)
done
