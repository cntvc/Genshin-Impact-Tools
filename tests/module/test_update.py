from genshin import __version__ as version
from genshin.module import update


class TestUpdate:
    def test_get_latest_tag(self, mocker):
        update.request_get = mocker.MagicMock()
        update.request_get.return_value = '{"test":"hello"}'
        tag = update.get_latest_tag(update.GITHUB_RELEASE_URL)
        assert tag == ""

        update.request_get.return_value = '{"tag_name":"0.1.0"}'
        tag = update.get_latest_tag(update.GITHUB_RELEASE_URL)
        assert tag == "0.1.0"

    def test_check_update(self, mocker):
        update.get_latest_tag = mocker.MagicMock()

        update.get_latest_tag.return_value = ""
        assert update.check_update() is False

        update.get_latest_tag.return_value = version
        assert update.check_update() is True

        update.get_latest_tag.return_value = "0.0.0"
        assert update.check_update() is False
