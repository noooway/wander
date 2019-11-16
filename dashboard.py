from app_pkg import app, db
from app_pkg.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
