from docupdater.lib.notifiers import StartupMessage, TemplateMessage
from docupdater.update.container import Container


def test_notifiers_startup_message():
    message = StartupMessage("MyHost")
    assert message.title
    assert message.body


def test_notifiers_template_message(docker_client, hello_world_container):
    message = TemplateMessage(Container(docker_client, hello_world_container))
    assert message.title
    assert message.body


def test_notifiers_send(notification, requests_mock):
    requests_mock.post('http://json.server.local', text='data')
    notification.send(StartupMessage("MyHost"), notifiers=["json://json.server.local"])
