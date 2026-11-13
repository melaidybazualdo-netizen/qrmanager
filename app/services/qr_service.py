import io
import base64
import qrcode
from typing import List
from sqlmodel import Session
from app.models.qritem import QRItem
from app.repositories.qr_repository import QRRepository

class QRService:
    def __init__(self, session: Session):
        self.repo = QRRepository(session)

    def get_user_qrs(self, user_id: int) -> List[QRItem]:
        return self.repo.get_by_user(user_id)

    def create_qr(self, title: str, data_content: str, category: str, user_id: int) -> QRItem:
        item = QRItem(title=title, data_content=data_content, category=category, user_id=user_id)
        return self.repo.create(item)

    def remove_qr(self, item_id: int) -> None:
        self.repo.delete(item_id)

    @staticmethod
    def generate_qr_base64(data: str) -> str:
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{img_str}"