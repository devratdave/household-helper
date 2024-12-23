from main import app
from application.sec import datastore
from application.models import db, Role, Service, Professional, Customer, ServiceRequest
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.session.commit()
    service = Service(name="Cleaning", description="Cleaning of any part of the house.", base_price=10000, time_required=6)
    service2 = Service(name="Plumbing", description="Repair of any water leakage or plumbing related problem.", base_price=1000, time_required=2)
    db.session.add(service)
    db.session.add(service2)
    db.session.commit()
    datastore.find_or_create_role(name="admin", description="User is an admin")
    datastore.find_or_create_role(name="cust", description="User is a Customer")
    datastore.find_or_create_role(name="prof", description="User is a Service Professional")
    db.session.commit()
    if not datastore.find_user(email="admin@email.com"):
        datastore.create_user(name="Admin",
            email="admin@email.com", password=generate_password_hash("pass123"), role="admin")
    if not datastore.find_user(email="professional_1@email.com"):
        datastore.create_user(name="Professional 1",
                              email="professional_1@email.com", password=generate_password_hash("pass123"), role="prof",
                              active=True)
    if not datastore.find_user(email="professional_2@email.com"):
        datastore.create_user(name="Professional 2",
                              email="professional_2@email.com", password=generate_password_hash("pass123"), role="prof",
                              active=True)
    if not datastore.find_user(email="customer_1@email.com"):
        datastore.create_user(
            name="Customer 1",
            email="customer_1@email.com", password=generate_password_hash("pass123"), role="cust")
    if not datastore.find_user(email="customer_2@email.com"):
        datastore.create_user(
            name="Customer 2",
            email="customer_2@email.com", password=generate_password_hash("pass123"), role="cust")
    db.session.commit()

    customer_1_info=datastore.find_user(email="customer_1@email.com")
    customer_1=Customer(user_id=customer_1_info.id, pincode=201310)

    customer_2_info=datastore.find_user(email="customer_2@email.com")
    customer_2=Customer(user_id=customer_2_info.id, pincode=201310)

    professional_1_info=datastore.find_user(email="professional_1@email.com")
    professional_1=Professional(user_id=professional_1_info.id, service_id=service.id, experience="I have 10 years of experience in deep cleaning of houses.", pincode=201310)

    professional_2_info=datastore.find_user(email="professional_2@email.com")
    professional_2=Professional(user_id=professional_2_info.id, service_id=service2.id, experience="I have 7 years of experience in providing plumbing services.", pincode=201210)

    db.session.add(customer_1)
    db.session.add(customer_2)
    db.session.add(professional_1)
    db.session.add(professional_2)
    db.session.commit()