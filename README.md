# PyKeyMacro
Python製マウス・キーボード操作マクロツール

単キー押下のみ対応しています。
長押しや同時押し、ダブルクリックやスクロールは未対応です。
また `Esc` キーは再生停止キーとして扱っているため登録できません。

## 動作確認環境

* Windows 12
* Python 3.10.8
* pynput 1.7.6

## How to use

1. install [pynput](https://pypi.org/project/pynput/)
```bash
pip install pynput
```

2. execute
```bash
python .\pykeymacro
```
