from app import db
from app.db.models import User, Song


def test_for_login(application,client):
    with application.app_context():
        assert db.session.query(User).count() == 0

        user = User('beyzatest@test.com', 'testtest')
        db.session.add(user)
        assert user.email == 'beyzatest@test.com'
        db.session.commit()

        assert db.session.query(User).count() == 1

        with application.test_client() as client:
            response_login = client.post('/login', data=dict(email='beyzatest@test.com',password='testtest'), follow_redirects=True)

        assert response_login.status_code == 200
        response = client.get("/login")
        assert response.status_code == 200

        db.session.delete(user)
        assert db.session.query(User).count() == 0


def test_for_register(application,client):
    with application.app_context():
        assert db.session.query(User).count() == 0

        user = User('beyzatest@test.com', 'testtest')
        db.session.add(user)
        assert user.email == 'beyzatest@test.com'
        db.session.commit()
        assert db.session.query(User).count() == 1

        with application.test_client() as client:
            response_register= client.post('/register', data=dict(email='beyzatest@test.com',password='testtest'), follow_redirects=True)

        assert response_register.status_code == 200
        response = client.get("/register")
        assert response.status_code == 200

        db.session.delete(user)
        assert db.session.query(User).count() == 0
