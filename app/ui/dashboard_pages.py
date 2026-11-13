from nicegui import ui, app
from sqlmodel import Session
from app.core.database import engine
from app.services.qr_service import QRService

def render_dashboard():
    if not app.storage.user.get('authenticated', False):
        ui.navigate.to('/')
        return

    user_id = app.storage.user.get('user_id')
    username = app.storage.user.get('username')

    def logout():
        app.storage.user.clear()
        ui.navigate.to('/')

    with ui.header().classes('justify-between items-center bg-gray-800 text-white p-4 shadow'):
        ui.label(f'QRManager | Sesión: {username}').classes('text-lg font-bold')
        ui.button('Cerrar Sesión', on_click=logout).props('flat color=white')

    with ui.column().classes('w-full max-w-4xl mx-auto p-4 gap-4'):
        with ui.card().classes('w-full p-4'):
            ui.label('Generar Nuevo Código QR').classes('text-xl font-bold mb-2')
            with ui.row().classes('w-full gap-4'):
                title_input = ui.input('Título / Referencia').classes('flex-1')
                category_input = ui.select(['General', 'URL', 'WiFi', 'Contacto'], value='General').classes('w-32')
            content_input = ui.input('Contenido o URL del QR (ej. https://...)').classes('w-full mt-2')

            def create_qr():
                if not title_input.value or not content_input.value:
                    ui.notify('Complete el título y el contenido', type='warning')
                    return
                with Session(engine) as session:
                    service = QRService(session)
                    service.create_qr(title_input.value, content_input.value, category_input.value, user_id)
                title_input.value = ''
                content_input.value = ''
                refresh_grid()
                ui.notify('Código QR generado con éxito', type='positive')

            ui.button('Generar y Guardar QR', on_click=create_qr).classes('mt-3 bg-blue-600 text-white')

        ui.label('Mis Códigos QR Guardados').classes('text-xl font-bold mt-4')
        grid_container = ui.row().classes('w-full wrap gap-4')

        def refresh_grid():
            grid_container.clear()
            with Session(engine) as session:
                service = QRService(session)
                items = service.get_user_qrs(user_id)

            with grid_container:
                if not items:
                    ui.label('No hay códigos QR generados aún.').classes('text-gray-500 italic')
                for item in items:
                    with ui.card().classes('w-72 p-4 items-center shadow border'):
                        ui.label(item.title).classes('font-bold text-lg text-center truncate w-full')
                        ui.badge(item.category).classes('mb-2')
                        
                        qr_base64 = QRService.generate_qr_base64(item.data_content)
                        ui.image(qr_base64).classes('w-40 h-40 object-contain my-2')
                        
                        ui.label(item.data_content).classes('text-xs text-gray-500 truncate w-full text-center mb-2')
                        
                        with ui.row().classes('w-full justify-between items-center mt-2'):
                            ui.button('Descargar', on_click=lambda c=item.data_content, t=item.title: ui.download(qr_base64, f"{t}.png")).props('flat sm color=primary')
                            ui.button(icon='delete', on_click=lambda i_id=item.id: delete_item(i_id)).props('flat sm color=red')

        def delete_item(item_id: int):
            with Session(engine) as session:
                QRService(session).remove_qr(item_id)
            refresh_grid()
            ui.notify('QR eliminado', type='info')

        refresh_grid()