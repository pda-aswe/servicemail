from src import mail
from unittest.mock import patch

@patch("os.path.exists")
def test_send(mock_exists,capsys):
    obj = mail.Mail()

    with patch.object(obj, 'service'):
        obj.send("test@test.de","Testsubject",["line 1","line 2"])

        assert capsys.readouterr().out != "gmail error\n"