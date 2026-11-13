from typing import List, Optional
from sqlmodel import Session, select
from app.models.qritem import QRItem

class QRRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_user(self, user_id: int) -> List[QRItem]:
        statement = select(QRItem).where(QRItem.user_id == user_id)
        return list(self.session.exec(statement).all())

    def get_by_id(self, item_id: int) -> Optional[QRItem]:
        return self.session.get(QRItem, item_id)

    def create(self, item: QRItem) -> QRItem:
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, item_id: int) -> None:
        item = self.session.get(QRItem, item_id)
        if item:
            self.session.delete(item)
            self.session.commit()