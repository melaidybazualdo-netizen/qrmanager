from nicegui import ui, app
from sqlmodel import Session
from app.core.database import engine
from app.services.auth_service import AuthService

def render_login():
    with ui.card().classes('w-96 absolute-center shadow-lg'):
        ui.label('QRManager - Login').classes('text-2xl font-bold mb-4 text-primary')
        username = ui.input('Usuario').classes('w-full')
        password = ui.input('Contraseña', password=True, password_toggle_button=True).classes('w-full')

        def handle_login():
            with Session(engine) as session:
                service = AuthService(session)
                user = service.authenticate_user(username.value, password.value)
                if user:
                    app.storage.user['authenticated'] = True
                    app.storage.user['user_id'] = user.id
                    app.storage.user['username'] = user.username
                    ui.navigate.to('/dashboard')
                else:
                    ui.notify('Credenciales incorrectas', type='negative')

        ui.button('Ingresar', on_click=handle_login).classes('w-full mt-4 bg-blue-600 text-white')
        ui.link('¿No tienes cuenta? Regístrate', '/register').classes('mt-2 text-sm text-center w-full')

def render_register():
    with ui.card().classes('w-96 absolute-center shadow-lg'):
        ui.label('Registro de Cuenta').classes('text-2xl font-bold mb-4 text-primary')
        username = ui.input('Usuario').classes('w-full')
        password = ui.input('Contraseña', password=True, password_toggle_button=True).classes('w-full')

        def handle_register():
            if not username.value or not password.value:
                ui.notify('Complete todos los campos', type='warning')
                return
            with Session(engine) as session:
                service = AuthService(session)
                user = service.register_user(username.value, password.value)
                if user:
                    ui.notify('Registrado con éxito', type='positive')
                    ui.navigate.to('/')
                else:
                    ui.notify('El usuario ya existe', type='negative')

        ui.button('Registrar', on_click=handle_register).classes('w-full mt-4 bg-green-600 text-white')
        ui.link('Volver al Login', '/').classes('mt-2 text-sm text-center w-full')