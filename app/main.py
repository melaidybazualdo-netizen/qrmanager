from nicegui import ui
from app.core.config import settings
from app.core.database import init_db
from app.ui.auth_pages import render_login, render_register
from app.ui.dashboard_pages import render_dashboard

init_db()

@ui.page('/')
def login_page():
    render_login()

@ui.page('/register')
def register_page():
    render_register()

@ui.page('/dashboard')
def dashboard_page():
    render_dashboard()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title=settings.APP_NAME,
        port=settings.PORT,
        storage_secret=settings.STORAGE_SECRET,
        reload=False
    )