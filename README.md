# Python-find-us-str

## 概要 Description
ファイル内文字列検索

UTF-8 の文字コードのテキストファイルを対象に文字列検索

## 特徴 Features

- テキストファイル内の文字列を検索します
- 文字コードが UTF-8 と Shift-JIS のテキストファイルを対象にします  
	混在していても大丈夫です
- ワイルドカードでファイル名を指定できます
- サブフォルダを含めて検索するか指定できます
- 検索から除外するサブフォルダを指定できます
- 検索に含めるサブフォルダを指定できます
- 検索文字、サブフォルダの指定に正規表現を使用できます
- 検索文字の大文字小文字を区別するか指定できます
- 一致した行を行番号とともに出力します
- コマンドプロンプト上で動作します

## 依存関係 Requirement

- Python 3.12.8
- Windows 64ビット OS

## 使い方 Usage
コマンドプロンプトを起動してからコマンドとして実行します。

|使い方|
|---|
|**find-us-str.exe [-h] [-s] [-i] [-r] [--exclude_dir dir] [--include_dir dir] keyword target_path**|

<br>

位置引数|説明
---|---
`keyword`    |検索文字列<br>空白や「`|`」などを含む場合はダブルクォーテーションで括る
`target_path`|検索対象パス（ファイルorフォルダorワイルドカード）<br>例：`test.txt`、`src`、`src\*.py`

検索対象パスは、相対パス、絶対パスのどちらでも指定できます。  
検索対象パスにファイル名を指定した場合、そのファイル内を検索します。  
検索対象パスにフォルダ名を指定した場合、そのフォルダ内のすべてのファイル内を検索します。  
ワイルドカードはファイル名部分に指定できます。

- ワイルドカード文字
	- `*` ：任意の文字0以上
	- `?` ：任意の文字1文字
	- `[]`：カッコ内の文字列のどれか一文字（`-`で範囲指定可）

オプション|説明
---|---
`-s`, `--subdir`     |サブフォルダも検索
`-i`, `--ignore_case`|大文字小文字を同一視
`-r`, `--regx`       |正規表現を使用<br>対象：検索文字列、除外するフォルダ、含めるフォルダ
`--exclude_dir dir`  |除外するフォルダ
`--include_dir dir`  |含めるフォルダ
`-p`, `--plain_text` |装飾しない出力<br>リダイレクトでファイル出力する場合などに使用
`-h`, `--help`       |ヘルプを表示

正規表現について

正規表現は Python の機能をそのまま使用しています。  
記述方法はこちらで確認してください：[re --- 正規表現操作 ? Python 3.13.2 ドキュメント <i class="blogicon-external"></i>](https://docs.python.org/ja/3.13/library/re.html#regular-expression-syntax)

## プログラムの説明サイト Program description site

- 使い方：[ファイル内文字列検索アプリfind-us-str【フリー】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/find-us-str-exe)  
- 作り方：[【準備中】ファイル内文字検索アプリの作り方【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/find-us-str)
  
## 作者 Authors
juu7g

## ライセンス License
このソフトウェアは、MITライセンスのもとで公開されています。LICENSEファイルを確認してください。  
This software is released under the MIT License, see LICENSE file.

