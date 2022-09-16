from flask_lan.utils import is_f_param_required


def test_is_f_param_required():
    def t(a: int, b: str = "test"):
        pass

    assert is_f_param_required(t, "a")
    assert not is_f_param_required(t, "b")
