# def test_Sign_up_redirect(client):
#     response = client.get('/ID')
#     # Check that there was one redirect response.
#     assert len(response.history) == 0
#     # Check that the second request was to the index page.
#     assert response.request.path == '/ID'
#
#
# def test_Sign_up_redirect(client):
#     response = client.get('/email')
#     # Check that there was one redirect response.
#     assert len(response.history) == 0
#     # Check that the second request was to the index page.
#     assert response.request.path == '/email'
#
#
# def test_Sign_up_redirect(client):
#     response = client.get('/name')
#     # Check that there was one redirect response.
#     assert len(response.history) == 0
#     # Check that the second request was to the index page.
#     assert response.request.path == '/name'
#
#
# # def test_Sign_up_redirect(client):
# #     response = client.get('/password1')
# #     # Check that there was one redirect response.
# #     assert len(response.history) == 0
# #     # Check that the second request was to the index page.
# #     assert response.request.path == '/password2'
#
#
# def test_logout_redirect(client):
#     response = client.get('/Logout')
#     # Check that there was one redirect response.
#     assert len(response.history) == 0
#     # Check that the second request was to the index page.
#     assert response.request.path == '/Logout'
#
#     import pytest
#     from website import create_app
#
#     @pytest.fixture()
#     def app():
#         app = create_app()
#         app.config.update({
#             "TESTING": True,
#         })
#
#         # other setup can go here
#
#         yield app
#
#         # clean up / reset resources here
#
#     @pytest.fixture()
#     def client(app):
#         return app.test_client()
#
#     @pytest.fixture()
#     def runner(app):
#         return app.test_cli_runner()
#
#     def test_login_redirect(client):
#         response = client.get('/Login')
#         # Check that there was one redirect response.
#         assert len(response.history) == 0
#         # Check that the second request was to the index page.
#         assert response.request.path == '/Login'
#
#     def test_Sign_up_redirect(client):
#         response = client.get('/POST')
#         # Check that there was one redirect response.
#         assert len(response.history) == 0
#         # Check that the second request was to the index page.
#         assert response.request.path == '/POST'
