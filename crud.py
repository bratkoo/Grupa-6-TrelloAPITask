from sqlalchemy.orm import Session
from models import Board, List, Card, Comment

def create_board(db: Session, name: str):
    db_board = Board(name=name)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

def get_board(db: Session, board_id: int):
    return db.query(Board).filter(Board.id == board_id).first()

def create_list(db: Session, name: str, board_id: int):
    db_list = List(name=name, board_id=board_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

def create_card(db: Session, name: str, description: str, list_id: int):
    db_card = Card(name=name, description=description, list_id=list_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def get_card(db: Session, card_id: int):
    return db.query(Card).filter(Card.id == card_id).first()

def create_comment(db: Session, text: str, card_id: int):
    db_comment = Comment(text=text, card_id=card_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
