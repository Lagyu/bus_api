iot-dojoで使ったバス乗車人数記録用のAPIサーバです。

# Setup
1. Install Python3.
1. Clone this repository.
1. Modify "settngs.py" in bus_count directory.
1. Run following commands.
```python
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

- You can start server with:
```python
python manage.py runserver
```
- You can create admin user (can login from /admin/) with:
```python
python manage.py createsuperuser
```

# Usage
- /api/ride_record/
乗車データを登録できます。
- /api/bus_route/
現在の路線ごとの状況（待ち人数、次のバスの時間など）がわかります。

運用の際は、公開するAPIに気を付けてください。

# Caution
- 時間なかったので、かなりやっつけな部分が多いです。特に画面に表示する色のところとか
