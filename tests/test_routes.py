from app import app

# This could be improved by creating an instance of app instead of using the actual app, this would be better practice.
# If I had more time this would have been refactored, I would have done as I had started it and can be seen on a branch,
# in Github Branch: restruct/project

def test_home_page():
    flask_app = app

    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        #looking for a redirect as the base url either redirects to dashboard or login
        assert response.status_code == 302



