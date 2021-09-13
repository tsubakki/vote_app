# サークル用の特殊な投票アプリ

# 動作確認済みのPythonバージョン
python3.7.11

# 環境構築
1. GitHubのコードをクローン
```
git clone https://github.com/tsubakki/vote_app.git
```
2. 仮想環境を構築
```
python -m venv vote_app
```
3. 仮想環境をアクティブにする
```
cd vote_app
source bin/activate
```
4. パッケージのインストール
```
pip install -r requirements.txt
```
5. プロジェクトに移動
```
cd myproject
```
6. データベースの作成
```
python manage.py makemigrations   
python manage.py migrate          
```
7. スーパーユーザの登録
```
python manage.py createsuperuser
```