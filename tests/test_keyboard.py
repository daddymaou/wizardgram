from wizardgram import Keyboard


def test_inline_single_button() -> None:
    markup = Keyboard.inline().button("Open", callback_data="open").build()
    assert markup["inline_keyboard"] == [[{"text": "Open", "callback_data": "open"}]]


def test_inline_row_breaks() -> None:
    markup = (
        Keyboard.inline()
        .button("A", callback_data="a")
        .row()
        .button("B", callback_data="b")
        .build()
    )
    assert len(markup["inline_keyboard"]) == 2


def test_reply_resize_flag() -> None:
    markup = Keyboard.reply().button("A").resize().build()
    assert markup["resize_keyboard"] is True


def test_callback_data_vs_url() -> None:
    markup = (
        Keyboard.inline()
        .button("Callback", callback_data="go")
        .button("Link", url="https://example.com")
        .build()
    )
    assert "callback_data" in markup["inline_keyboard"][0][0]
    assert "url" in markup["inline_keyboard"][0][1]
