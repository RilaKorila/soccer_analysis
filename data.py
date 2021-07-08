import pandas as pd
import numpy as np

soccer = pd.read_csv('./soccer_data.csv')

teams = ['イタリア', 'フランス', 'ドイツ', 'ポルトガル', 'アルゼンチン', 'ブラジル', 'イングランド',
    'ウクライナ', 'スペイン', 'エクアドル', 'メキシコ', 'オーストラリア', 'スイス', 'ガーナ',
    'スウェーデン', 'オランダ', 'コートジボアール', 'コスタリカ', 'チェコ', '韓国', 'チュニジア',
    'サウジアラビア', 'ポーランド', 'イラン', '日本', 'セルビア モンテネグロ', 'クロアチア', 'アンゴラ',
    'パラグアイ', 'トーゴ', 'アメリカ', 'トリニダードトバコ']

def get_data(rows):
    tmp = soccer
    # 列順を変える
    tmp = tmp.drop(['順位'], axis=1)
    tmp.insert(1, '順位', soccer['順位'])

    # 任意の行をとる
    # delete = teams - rows
    tmp = tmp[tmp['チーム'].isin(rows)]
    # tmp = tmp.drop(rows, axis=0)
    
    # データの処理はあとでここに書く

    return tmp

# 1試合あたりに換算
def get_data_per_game(rows):
    df_per_game = pd.DataFrame()
    tmp = soccer 

    # ['チーム', '順位']以外を試合数でわる
    tmp = tmp.drop(['チーム', '順位'], axis=1)
    df_per_game = tmp.div(tmp['試合'], axis=0).round(2)

    # ['チーム', '順位']を元に戻す
    # df_per_game = df_per_game.assign(順位=soccer['順位'])
    df_per_game.insert(0, '順位', soccer['順位'])
    df_per_game.insert(0, 'チーム', soccer['チーム'])

    # 任意の行をとる
    # delete = teams - rows
    tmp = tmp[tmp['チーム'].isin(rows)]

    return df_per_game


def get_lat_lon():
    countries = pd.DataFrame(soccer['チーム'])
    # 本当はindex番号消したい、、
    # lon, latのdataが作れれば、map表示ができる

    games = soccer['試合数'].values

    val = [
        '試合',
        '得点数',
        '失点',
        'PKゴール数',
        'アシスト数',
        '枠内シュート数',
        'シュート',
        'CK数',
        'FK数',
        'オフサイド数',
        'ショートパス数',
        'ロングパス数',
        'クロス数',
        'タックル数',
        '被タックル数',
        'ファウル数',
        '被ファウル数',
        'イエロー数',
        'レッド数'
    ]

    for game_num in  games:
        for elem in val:
            soccer[elem] = soccer[elem] /  game_num


    # 転置：countries.T
    return countries

def get_corrcoef(x_label, y_label):
    cor = np.corrcoef(soccer[x_label], soccer[y_label])
    return cor[0,1].round(4)


def get_label_list():
    # textデータを削
    df = soccer[[
        '得点数',
        '失点',
        'PKゴール数',
        'アシスト数',
        '枠内シュート数',
        'シュート',
        'CK数',
        'FK数',
        'オフサイド数',
        'ショートパス数',
        'ロングパス数',
        'クロス数',
        'タックル数',
        '被タックル数',
        'ファウル数',
        '被ファウル数',
        'イエロー数',
        'レッド数']]

    # '失点','PKゴール数','アシスト数', '枠内シュート数', 'シュート', 'CK数', 'FK数','オフサイド数','ショートパス数','ロングパス数']]
        # 'クロス数',
        # 'タックル数',
        # '被タックル数',
        # 'ファウル数',
        # '被ファウル数',
        # 'イエロー数',
        # 'レッド数']]
    # dataのcolumn名を取得
    return list(df.columns)
