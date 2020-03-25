# Wander
Mobile app analytics dashboard

Installation:
``` shell
git clone https://github.com/noooway/wander
cd wander
pip3 install -r requirements.txt
sqlite3 data_sources_example/regs_pur.db < data_sources_example/regs_purchases.sql 
mkdir instance
sqlite3 instance/wander.sqlite < wander/schema.sql
```

For testing, start server with:
``` shell
flask run
```

Visit [localhost:5000](http://localhost:5000) in a browser.
 
To make the server visible to outside world:
``` shell
flask run --host='0.0.0.0' --port='5000'
```

Run using `gunicorn`:
``` shell
gunicorn -w 4 --bind 0.0.0.0:5000 wander.wsgi:app
```
