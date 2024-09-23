from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from os import getcwd, path, makedirs, getenv
from dotenv import load_dotenv

load_dotenv()

cwd = getcwd()
uploads_dir = path.join(cwd, "uploads")
if not path.exists(uploads_dir):
    makedirs(uploads_dir)


app = Flask(__name__)
app.url_map.strict_slashes = False

babel = Babel(app)

app.config["BABEL_DEFAULT_LOCALE"] = "ar"
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "./translations"
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["UPLOAD_DIRECTORY"] = uploads_dir
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}?charset=utf8mb4"
)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(14), primary_key=True)
    password = db.Column(db.String(224))
    name = db.Column(db.String(128))
    phone = db.Column(db.String(16))
    email = db.Column(db.String(48))
    address = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
# Added for email verification
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verification_code = db.Column(db.String(6))  # Assuming a 6-digit code


class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(432))
    readme = db.Column(db.Text)


class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(432))
    readme = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    department = db.relationship("Department", backref="services")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    details = db.Column(db.String(4096))
    file_paths = db.Column(db.String(4096))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_done = db.Column(db.Boolean, default=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"))
    service = db.relationship("Service", backref="orders")
    user_id = db.Column(db.String(14), db.ForeignKey("users.id"))
    user = db.relationship("User", backref="orders")


class CertificateDesign(db.Model):
    __tablename__ = 'certificate_designs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
class SiteDesign(db.Model):
    __tablename__ = 'site_design'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    logo_url = db.Column(db.String(255))
    navbar_color = db.Column(db.String(7))  # Storing color as HEX code
    font_style = db.Column(db.String(50))
if __name__ == "__main__":
    with app.app_context():
        db.create_all()


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(14), db.ForeignKey('users.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    amount = db.Column(db.Float)
    type = db.Column(db.String(50))  # 'bank' or 'points'
    timestamp = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', backref='transactions')
    service = db.relationship('Service', backref='transactions')

class ServicePricing(db.Model):
    __tablename__ = 'service_pricing'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    price = db.Column(db.Float)
    currency = db.Column(db.String(10), default='SAR')

    service = db.relationship('Service', backref='pricing')
