import json
from datetime import datetime

from flask import Flask, render_template, redirect, request

application = Flask(__name__)

DATA_FILE = 'norilog.json'

def save_data(start, finish, memo, created_at):
    """記録データを保存
    :param start: 乗った駅
    :type start: str
    :param finish: 降りた駅
    :type finish: str
    :param memo: 乗り降りのメモ
    :type memo: str
    :param created_at: 乗り降りの日付
    :type created_at: datetime.datetime
    :return: None
    """
    try:
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []
    
    database.insert(0, {
        "start": start,
        "finish": finish,
        "memo": memo,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M")
    })

    json.dump(database, open(DATA_FILE, mode="w", encoding="utf-8"), indent=4, ensure_ascii=False)


def load_data():
    # 記録データを返す
    try:
        # json モジュールでデータベースファイルを開く
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileExistsError:
        database = []
    return database


@application.route('/')
def index():
    """トップページ
    テンプレートを使用してページを表示
    """
    rides = load_data()
    return render_template('index.html', rides=rides)


@application.route('/save', methods=['POST'])
def save():
    # 記録用URL
    # 記録されたデータを取得します
    start = request.form.get('start')
    finish = request.form.get('finish')
    memo = request.form.get('memo')
    created_at = datetime.now()
    save_data(start, finish, memo, created_at)
    # 保存後はトップページにリダイレクト
    return redirect('/')


if __name__ == '__main__':
    # IPアドレス0.0.0.0の8000番ポートでアプリケーションを実行
    application.run('0.0.0.0', 8000, debug=True)