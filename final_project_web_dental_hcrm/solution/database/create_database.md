# To create the sqlite database. cd to project home
. ./solution/app.env
source venv/bin/activate
python
from dentalhcrm import create_app, db
app = create_app()
ctx = app.app_context()
ctx.push()
db.create_all()
ctx.pop()
exit()
