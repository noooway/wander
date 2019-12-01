# Wander
Mobile app analytics dashboard

Installation:
``` shell
git clone https://github.com/noooway/wander
cd wander
pip3 install -r requirements.txt
```

For testing, start server with:
``` shell
flask run
```

To make server visible to the outside world:
``` shell
flask run --host='0.0.0.0' --port='5000'
```

Run using `gunicorn`:
``` shell
gunicorn -w 4 --bind 0.0.0.0:5000 wander.wsgi:app
```
