from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, backref
from saleapp import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    STAFF = 3
    IMPORTER = 4


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), default='https://image.thanhnien.vn/1200x630/Uploaded/2022/xdrkxrvekx/2015_11_18/anonymous-image_fgnd.jpg')
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    diachi = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    comment = relationship('Comment', backref='user', lazy=True)
    user_receipt = relationship('UserReceipt', backref='user', lazy=True)


    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ = 'category'
    __table_args__ = {'extend_existing': True}
    name = Column(String(50), nullable=False)
    products = relationship('models.Product', backref='category', lazy=True)

    def __str___(self):
        return self.name


class Product(BaseModel):
    __tablename__ = 'product'
    # __table_args__ = {'extend_existing': True}
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(255))
    active = Column(Boolean, default=True)
    quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    receipt_details = relationship('ReceiptDetail', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)
    sach_tacgia = relationship('SachTacGia', backref='product', lazy=True)
    chitietnhapsach = relationship('ChiTietNhapSach', backref='product', lazy=True)

    def __str___(self):
        return self.name

class Note(BaseModel):
    __abstract__ = True
    # __table_args__ = {'extend_existing': True}
    created_date = Column(DateTime, default= datetime.now())

    def __str___(self):
        return self.created_date

class Receipt(Note):
    __tablename__ = 'receipt'
    # __table_args__ = {'extend_existing': True}
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)
    user_receipt = relationship('UserReceipt', backref='receipt', lazy=True)
    payment = Column(Boolean, default=True)

    def __str___(self):
        return self.created_date

class UserReceipt(db.Model):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)

class PhieuNhapSach(Note):
    __tablename__ = 'phieunhapsach'
    chitietnhapsach = relationship('ChiTietNhapSach', backref='phieunhapsach', lazy=True)

    def __str___(self):
        return self.created_date


class ReceiptDetail(db.Model):
    __tablename__ = 'receiptdetail'
    __table_args__ = {'extend_existing': True}
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


class ChiTietNhapSach(db.Model):
    __tablename__ = 'chitietnhapsach'
    quantity = Column(Integer, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    phieunhapsach_id = Column(Integer, ForeignKey(PhieuNhapSach.id), nullable=False, primary_key=True)


class Comment(BaseModel):
    content = Column(String(255), nullable = False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())

    def __str___(self):
        return self.content


class TacGia(BaseModel):
    name = Column(String(100), nullable=False)
    sach_tacgia = relationship('SachTacGia', backref='tacgia', lazy=True)

    def __str___(self):
        return self.name


class SachTacGia(db.Model):
    tacgia_id = Column(Integer, ForeignKey(TacGia.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)

class Rule(BaseModel):
    name = Column(String(100), nullable=False, unique=True)
    value = Column(Integer, nullable=False)
    description = Column(Text)

if __name__ == '__main__':
    with app.app_context():

        # db.drop_all()
        # db.create_all()


        # cates = untils.read_json(os.path.join(app.root_path, 'data/categories.json'))
        # products = untils.read_json(os.path.join(app.root_path, 'data/products.json'))


        # for i in cates:
        #     c = Category(name=i['name'])
        #     db.session.add(c)
        #
        # for i in products:
        #     c = Product(name=i['name'], category_id=i['category_id'], description=i['description'],
        #                 price=i['price'], image=i['image'])
        #     db.session.add(c)

        # c = Category(name = 'Lap Trinh')
        # db.session.add(c)
        db.session.commit()
