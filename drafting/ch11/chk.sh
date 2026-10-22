#!/bin/sh
# usage: sh ch11/chk.sh 11.N  — free in-house check, condensed
cd "$(dirname "$0")/../_pipe" && UDAY_CFG="C:/Users/User/Desktop/Anugrah/OCR2Md/drafting/ch11/cfg_ch11v1.py" python -I -X utf8 inhouse.py check "$1" 2>&1 | python -X utf8 -c "import json,sys;d=json.load(sys.stdin);print(d['section'],d['words'],'CLEAN' if d['clean'] else 'NOT CLEAN');[print('-',p[:260]) for p in d['problems']+d['ledger']+d['style_warnings']]"
