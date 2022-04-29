from app import config
from app.db.models import Song,User


def test_song_upload_file(application,client):
    """ setup database user and delete """
    resp = client.get('songs/upload', follow_redirects=True)
    user = User("beyzatest@testtest","testtest")
    with application.test_client(user) as client:
        with open(config.Config.BASE_DIR + '/../tests/' + 'music_test.csv', 'rb') as file:
            response = client.post('/songs/upload', data="music_test.csv", follow_redirects=True)
        assert response.status_code == 200
