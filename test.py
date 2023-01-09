import pytest
from website import create_app


from flask import template_rendered
from contextlib import contextmanager

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    # other setup can go here
    yield app
    # clean up / reset resources here
@pytest.fixture()
def client(app):
    return app.test_client()
@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_login_redirect1(client):
    response = client.get("/login")
    # Check that there was one redirect response.
    assert len(response.history) == 0
    # Check that the second request was to the index page.
    assert response.request.path == "/login"

def test_Sign_up_redirect2(client):
    response = client.get('/ID')
    # Check that there was one redirect response.
    assert len(response.history) == 0
    # Check that the second request was to the index page.
    assert response.request.path == '/ID'

def test_Sign_up_redirect3(client):
    response = client.get('/name')
    # Check that there was one redirect response.
    assert len(response.history) == 0
    # Check that the second request was to the index page.
    assert response.request.path == '/name'
    #
    #
def test_Sign_up_redirect4(client):
    response = client.get('/password1')
    # Check that there was one redirect response.
    assert len(response.history) == 0
    # Check that the second request was to the index page.
    assert response.request.path == '/password2'
    #
    #
def test_logout_redirect5(client):
    response = client.get('/Logout')
    # Check that there was one redirect response.
    assert len(response.history) == 0
    # Check that the second request was to the index page.
    assert response.request.path == '/Logout'
    #


def test_login_redirect6(client):
    response = client.get('/Login')
    # Check that there was one redirect response.
    assert len(response.history) == 0
    # Check that the second request was to the index page.
    assert response.request.path == '/Login'


def test_Sign_up_redirect7(client):
    response = client.get('/POST')
    # Check that there was one redirect response.
    assert len(response.history) == 0
    # Check that the second request was to the index page.
    assert response.request.path == '/POST'


def test_Sign_up_redirect8(client):
    response = client.get('/email')
    # Check that there was one redirect response.
    assert len(response.history) == 0
    # Check that the second request was to the index page.
    assert response.request.path == '/email'

def test_Login(app, client):
    res = client.get('/')
    assert res.status_code == 302
    expected = {"login.html"}
    assert "You should be redirected automatically" in res.get_data(as_text=True)

def test_render_login(app, client):
    with captured_templates(app) as templates:
        res = client.get('/Login')
        assert res.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'login.html'

def test_not_existing_page(app, client):
    res = client.get('/blah')
    assert res.status_code == 404

def test_patients(app, client):
    with captured_templates(app) as templates:
        res = client.get('/patients')
        assert res.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'patients.html'
        assert 'patients' in context.keys()

def test_logout_redirect(app,client):
    with captured_templates(app) as templates:
        res = client.get('/Logout')
        assert res.status_code == 302
        assert '/Login' in str(res.data)

def test_signup(app, client):
    with captured_templates(app) as templates:
        res = client.get('/Sign_up')
        assert res.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'sign_up.html'


def test_signup_illegal_id(app, client):
    with captured_templates(app) as templates:
        res = client.post('/Sign_up', data={"ID": 1234})
        # Test flash text
        assert "ID card length should be 9 digits" in res.get_data(as_text=True)

def test_signup_illegal_id_wrong(app, client):
    with captured_templates(app) as templates:
        res = client.post('/Sign_up', data={"ID": 123456789})
        assert "ID card length should be 9 digits" in res.get_data(as_text=True)

def test_patients_for_secretary(app, client):
    with captured_templates(app) as templates:
        res = client.get('/patients_for_secretary')
        assert res.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'patiensts_for_secretary.html'
        assert 'patients' in context.keys()


def test_chat(app, client):
    with captured_templates(app) as templates:
        res = client.get('/chat')
        assert res.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'chat.html'
        assert 'messages' in context.keys()


def test_add_message_get(app, client):
    with captured_templates(app) as templates:
        res = client.get('/message_for_patient')
        assert res.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'secretary_write_message.html'


def test_add_message_fails_with_non_existent_id(app, client):
    with captured_templates(app) as templates:
        with pytest.raises(AttributeError):
            client.post('/message_for_patient', data={"ID": "I Dont exist nahnah", "message": "testing"})


def test_home(app, client):
    with captured_templates(app) as templates:
        res = client.get('/')
        assert res.status_code == 302
        assert 'Login' in res.get_data(as_text=True)


def test_home2(app, client):
    with captured_templates(app) as templates:
        res = client.get('/home')
        assert res.status_code == 302
        assert 'Login' in res.get_data(as_text=True)

def test_nurse_action_one(app, client):
    with captured_templates(app) as templates:
        res = client.post('/nurse', data={"n_action": 1})
        assert res.status_code == 302
        assert "/patients" in res.get_data(as_text=True)

def test_nurse_action_three(app, client):
    with captured_templates(app) as templates:
        res = client.post('/nurse', data={"n_action": 3})
        assert res.status_code == 302
        assert "/chat" in res.get_data(as_text=True)

def test_secretary_action_two(app, client):
    with captured_templates(app) as templates:
        res = client.post('/Secretary', data={"s_action": 2})
        assert res.status_code == 302
        assert "/patients_for_secretary" in res.get_data(as_text=True)

def test_secretary_action_three(app, client):
    with captured_templates(app) as templates:
        res = client.post('/Secretary', data={"s_action": 3})
        assert res.status_code == 302
        assert "/message_for_patient" in res.get_data(as_text=True)


def test_patient(app, client):
    with captured_templates(app) as templates:
        res = client.get('/patient')
        assert res.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'patient.html'
        assert 'message' in context.keys()
        assert 'user_name' in context.keys()
        assert context['message'] is None
        assert context['user_name'] is None


def test_forgot_password_get(app, client):
    with captured_templates(app) as templates:
        res = client.get('/forgot_password')
        assert res.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'forgot_password.html'
