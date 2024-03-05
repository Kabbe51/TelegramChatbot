import unittest
from unittest.mock import patch, MagicMock
from telegram import Update, Message, Chat
from vscodeBOT import start_command, help_command, req, handle_response, handle_message, error, req_cve
new_update = Update(update_id=1, message=Message(message_id=1, text = "", chat=Chat(id=1, type="private")))

@patch('Telegram.Update')
def test_cveCPE(mock_msg):
    req_cve(new_update, None)
    mock_msg.reply_text.assert_called_once_with("Received")

@patch('Telegram.Update')
def test_handle_message(mock_msg):
    handle_message(new_update, None)
    mock_msg.reply_text.assert_called()

@patch('Telegram.Update')
def test_handle_response(mock_msg):
    handle_response(new_update, None)
    mock_msg.reply_text.assert_called()

test_handle_message()    
test_handle_response()
test_cveCPE()
