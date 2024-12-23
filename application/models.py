from flask_login import current_user
from flask_security import RoleMixin, UserMixin, current_user, auth_required
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    address = db.Column(db.Text, nullable=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column('role_name', db.String(), db.ForeignKey('role.name'))


class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('users.id'))
    pincode = db.Column(db.Integer)


class Professional(db.Model):
    __tablename__ = 'professionals'
    professional_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('users.id'))
    service_id = db.Column('service_id', db.Integer(), db.ForeignKey('services.service_id'))
    experience = db.Column(db.Text)
    pincode = db.Column(db.Integer)


class Service(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    base_price = db.Column(db.Integer)
    time_required = db.Column(db.Integer)
    description = db.Column(db.Text())


class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    service_request_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    professional_id = db.Column('professional_id', db.Integer, db.ForeignKey('professional.professional_id'))
    customer_id = db.Column('customer_id', db.Integer, db.ForeignKey('customer.customer_id'))
    service_id = db.Column('service_id', db.Integer, db.ForeignKey('service.service_id'))
    is_approved = db.Column(db.Boolean, default=False, nullable=True)
    is_responded = db.Column(db.Boolean, default=False, nullable=True)
    is_revoked = db.Column(db.Boolean, default=False, nullable=True)
    is_completed = db.Column(db.Boolean, default=False, nullable=True)
    rejection_reason = db.Column(db.String(100), nullable=True)
    issue_date = db.Column(db.Date, nullable=True)


# class Feedback(db.Model):
#     __tablename__ = 'feedbacks'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
#     feedback = db.Column(db.String)
#     rating = db.Column(db.Integer(5))

    @property
    def num_of_service_requests_pending(self):
        rqs = ServiceRequest.query.filter_by(customer_id=current_user.id, is_approved=True,
                                          is_responded=True, is_revoked=False).count()
        rqs2 = ServiceRequest.query.filter_by(customer_id=current_user.id, is_approved=False,
                                          is_responded=True, is_revoked=False).count()
        return rqs+rqs2

    @property
    def is_approved_for_me(self):
        rqs = ServiceRequest.query.filter_by(service_id=self.service_id, professional_id=self.professional_id, is_approved=True, is_responded=True, is_completed=False, is_revoked=False).all()
        return True if current_user.id in [request.customer_id for request in rqs] else False

    @property
    def request_id(self):
        if self.is_approved_for_me:
            qs = ServiceRequest.query.filter_by(service_id=self.service_id, professional_id=self.professional_id, is_responded=True, is_completed=False, is_revoked=False,
                                             customer_id=current_user.id).first()
            return qs.id
        else:
            return None

    # @property
    # def wrote_review(self):
    #     rqs = Feedback.query.filter_by(book_id=self.book_id).all()
    #     return True if current_user.id in [request.user_id for request in rqs] else False

    @property
    def is_pending_for_me(self):
        rqs = ServiceRequest.query.filter_by(service_id=self.service_id, professional_id=self.professional_id, is_completed=False,
                                          is_revoked=False).all()
        return True if current_user.id in [request.user_id for request in rqs] else False