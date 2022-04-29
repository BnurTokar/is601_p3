from app import db
from app.db.models import User, Song
from app import config


def test_for_accessing_dashboard(application,client):
    with application.app_context():
        assert db.session.query(User).count() == 0

        user = User('beyzatest@test.com', 'testtest')
        db.session.add(user)
        assert user.email == 'beyzatest@test.com'
        db.session.commit()

        assert db.session.query(User).count() == 1

        with application.test_client() as client:
            client.post('/login', data=dict(email='beyzatest@test.com',password='testtest'), follow_redirects=True)
            response_dashboard= client.get('/dashboard')

        assert response_dashboard.status_code == 302

        db.session.delete(user)
        assert db.session.query(User).count() == 0


def test_for_denying_dashboard(application,client):
    assert db.session.query(User).count() == 0
    user = User('beyzatest@test.com', 'testtest')
    db.session.add(user)
    db.session.commit()

    with application.test_client(user) as client:
        client.post('/login', data=dict(email='testuser@test.com',password= 'testtest'), follow_redirects=True)
        response_dashboard= client.get('/dashboard')

    assert response_dashboard.status_code == 302



def test_song_denying_upload_file(application,client):
    """ setup database user and delete """
    with application.test_client() as client:
        with open(config.Config.BASE_DIR + '/../tests/' + "sample_music.csv", 'rb') as file:
            response = client.post('/songs/upload', data='sample_music.csv', follow_redirects=True)

    assert not response.status_code == 404

