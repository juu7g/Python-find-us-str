"""
ファイル内文字列検索
コマンド オプション 検索文字列 ファイル名
    オプション  -s:サブフォルダ、-r:正規表現、-i:大文字小文字区別せず

    他の例: grep -r abc work/*    -r:サブフォルダ、-E:正規表現、-i:大文字小文字区別せず
            findstr /s abc ./*    /s:サブフォルダ、/r:正規表現、/i大文字小文字区別せず
"""

import re
import os
from pathlib import Path

COLOR_RED = "\033[31m"      # 赤色文字エスケープシーケンス
COLOR_END = "\033[0m"       # 色付け終了エスケープシーケンス
COLOR_UDL = "\033[4m"       # 下線エスケープシーケンス

def find_text_in_dir(target_path:str, keyword:str, subdir:bool, is_icase:bool, 
                     is_regx:bool, exculde_dir:str, include_dir:str, plain_text:bool):
    """
    フォルダ内のファイルを取得してファイル内の文字列を検索して出力
    ファイルの抽出にはpathlib.glob()を使用
    文字列検索には正規表現を使用。オプションで正規表現未使用の場合、特殊文字をエスケープする

    Args:
        target_path(str):   ファイル名、フォルダ名、ワイルドカード
        keyword(str):       検索文字列
        subdir(bool):       サブフォルダも検索
        is_icase(bool):     大文字と小文字を区別しない
        is_regx(bool):      正規表現を使用
        exclude_dir(str):   除外するフォルダ
        include_dir(str):   含めるフォルダ
        plain_text(bool):   装飾しない出力
    """
    p = Path(target_path)
    
    # 正規表現初期化(繰り返し使用するのでcompile()する)
    # 正規表現未使用の場合、特殊文字をエスケープ
    if not is_regx:
        keyword = re.escape(keyword)
        exculde_dir = re.escape(exculde_dir)
        include_dir = re.escape(include_dir)
    
    # 大文字と小文字を区別するかどうかは正規表現のフラグで対応
    f_re = 0
    if is_icase: f_re = re.IGNORECASE

    # 正規表現を使用する場合、記述に誤りがあるときは例外
    try:
        regk = re.compile(rf"({keyword})", flags=f_re)  # 置換で色付けするためグループ化
        rege = re.compile(rf"{exculde_dir}", flags=re.IGNORECASE)  # 常に大文字と小文字を区別しない
        regi = re.compile(rf"{include_dir}", flags=re.IGNORECASE)  # 常に大文字と小文字を区別しない
    except re.error as e:
        print(f"正規表現の記述誤り:'{keyword}' {e}")
        return
    
    # 検索範囲
    wc = ''
    if subdir: wc = '**/'       # サブフォルダも検索する場合glob()で再帰的検索にする
    
    # 対象ファイルの抽出
    if p.is_file():     # ファイル名指定
        files = [p]
    elif p.is_dir():    # フォルダ名指定
        files = p.glob(wc + '*')
    else:               # ワイルドカード指定
        files = p.parent.glob(wc + p.name)

    # ファイルごとに文字列の抽出と出力
    # 内包表記で対象のファイルを選別し、find_text()を実行
    [find_text(file_path, regk, plain_text) for file_path in files
        if ((not exculde_dir or 
             not [dir for dir in str(file_path).split(os.sep) if rege.fullmatch(dir)]) and 
             (not include_dir or 
              [dir for dir in str(file_path).split(os.sep) if regi.fullmatch(dir)]))]
            
def find_text(file_path:Path, regx:re.Pattern, plain_text:bool):
    """
    ファイル内の文字列を検索して出力
    一致する行の内容と行番号を出力
    一致する行がある場合、ファイル名を出力
    一致部分を赤色で出力

    Args:
        file_path(Path):    対象ファイル
        regx(re.Pattern):   コンパイル済み正規表現オブジェクト
        plain_text(bool):   装飾しない出力
    """
    # print(file_path)
    # return

    # 修飾用文字の設定
    if plain_text:  # 修飾なしは空文
        cr = ce = cu = ''
    else:           # 修飾ありはエスケープ文字
        cr = COLOR_RED  # 赤
        ce = COLOR_END  # 終了
        cu = COLOR_UDL  # 下線

    try:
        with open(file_path, encoding="utf-8") as f:
            data_lines = f.readlines()
    except PermissionError:     # 参照権限がない場合は飛ばす
        return
    except UnicodeDecodeError:  # UTF-8でない場合はShift-JISで試す
        try:
            with open(file_path, encoding="shift-jis") as f:
                data_lines = f.readlines()
        except UnicodeDecodeError:  # UTF-8でもShift-JISでもない場合は飛ばす
            return

    # 各行から改行文字を除いてリスト化
    lines_no_lf = [line.strip() for line in data_lines]
    # 検索文字列を含んだ行だけをリスト化
        # リスト内は行番号と内容のタプル
        # 一致部分の色を赤に変更するためエスケープシーケンスを追加
        # \1は正規表現で一致部分の内容
    lines = [(i, regx.sub(rf"{cr}\1{ce}", line))
             for i, line in enumerate(lines_no_lf, 1) if regx.search(line)]
    # 出力
    if lines:
        print(f"\n{cu}{file_path}{ce}")     # ファイル名の出力
    for i, v in lines:
        print(f"{i:>4}: {v}")               # 一致行の出力。行番号に4桁確保

if __name__ == '__main__':
    # コマンドライン引数の定義
    import argparse
    paser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    paser.add_argument('keyword', help='検索文字列')
    paser.add_argument('target_path', help='検索対象のパス(ファイルorフォルダorワイルドカード)\n例：file.txt、dir、dir\\*.py')
    paser.add_argument('-s', '--subdir', action='store_true', help='サブフォルダも検索')
    paser.add_argument('-i', '--ignore_case', action='store_true',
                        help='大文字小文字を同一視')
    paser.add_argument('-r', '--regx', action='store_true',
        help='正規表現を使用(対象：検索文字列、除外するフォルダ、含めるフォルダ)')
    paser.add_argument('--exclude_dir', default='', metavar= 'dir',
                        help='除外するフォルダ')
    paser.add_argument('--include_dir', default='', metavar= 'dir',
                        help='含めるフォルダ')
    paser.add_argument('-p', '--plain_text', action='store_true', help='装飾しない出力')
    args = paser.parse_args()
    print(args)
    
    os.system("")   # Windowsコマンドプロンプトでエスケープシーケンスを機能させるための処理

    try:
        find_text_in_dir(args.target_path, args.keyword, args.subdir, args.ignore_case, 
                         args.regx, args.exclude_dir, args.include_dir, args.plain_text)
    except KeyboardInterrupt:
        print("Ctrl + C が押されたので中断しました")
