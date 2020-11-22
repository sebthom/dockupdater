from dockupdater.lib.notifiers import StartupMessage
from dockupdater.lib.notifiers import TemplateMessage
from dockupdater.update.container import Container


def test_notifiers_startup_message():
    message = StartupMessage("MyHost")
    assert message.title
    assert message.body


def test_notifiers_template_message(docker_client, hello_world_container):
    message = TemplateMessage(Container(docker_client, hello_world_container))
    assert message.title == f"dockupdater has updated container [{hello_world_container.name}]!"
    assert message.body


def test_notifiers_send(notification, requests_mock):
    requests_mock.post('http://json.server.local', text='data')
    notification.send(StartupMessage("MyHost"), notifiers=["json://json.server.local"])
