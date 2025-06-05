#!/usr/bin/env python3
"""
Windows通知機能のテスト

期待される動作:
1. 通知送信関数が存在する
2. タイトルとメッセージを指定して通知を送信できる
3. 通知送信が成功したかどうかを返す
4. PowerShellコマンドが適切に構築される
"""

import unittest
import subprocess
from unittest.mock import patch, MagicMock
import sys
import os

# テスト対象モジュールのパスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from notification import WindowsNotifier
except ImportError:
    # まだ実装されていない場合はスキップ
    WindowsNotifier = None


class TestWindowsNotification(unittest.TestCase):
    """Windows通知機能のテストクラス"""
    
    def setUp(self):
        """テストの前準備"""
        if WindowsNotifier is None:
            self.skipTest("WindowsNotifier not implemented yet")
        self.notifier = WindowsNotifier()
    
    def test_notifier_exists(self):
        """通知クラスが存在することを確認"""
        self.assertIsNotNone(WindowsNotifier)
        self.assertIsInstance(self.notifier, WindowsNotifier)
    
    def test_send_notification_method_exists(self):
        """send_notificationメソッドが存在することを確認"""
        self.assertTrue(hasattr(self.notifier, 'send_notification'))
        self.assertTrue(callable(getattr(self.notifier, 'send_notification')))
    
    @patch('subprocess.run')
    def test_send_notification_basic(self, mock_subprocess):
        """基本的な通知送信のテスト"""
        # モックの設定
        mock_subprocess.return_value = MagicMock(returncode=0)
        
        # テスト実行
        result = self.notifier.send_notification("Test Title", "Test Message")
        
        # 検証
        self.assertTrue(result)
        mock_subprocess.assert_called_once()
        
        # PowerShellコマンドが呼び出されていることを確認
        call_args = mock_subprocess.call_args[0][0]
        self.assertIn('powershell.exe', call_args)
    
    @patch('subprocess.run')
    def test_send_notification_with_custom_message(self, mock_subprocess):
        """カスタムメッセージでの通知送信テスト"""
        mock_subprocess.return_value = MagicMock(returncode=0)
        
        title = "Claude Code Complete"
        message = "タスクが正常に完了しました"
        
        result = self.notifier.send_notification(title, message)
        
        self.assertTrue(result)
        mock_subprocess.assert_called_once()
        
        # コマンドにタイトルとメッセージが含まれていることを確認
        call_args = str(mock_subprocess.call_args)
        self.assertIn(title, call_args)
        self.assertIn(message, call_args)
    
    @patch('subprocess.run')
    def test_send_notification_failure(self, mock_subprocess):
        """通知送信失敗時のテスト"""
        # エラーを返すモック
        mock_subprocess.return_value = MagicMock(returncode=1)
        
        result = self.notifier.send_notification("Title", "Message")
        
        self.assertFalse(result)
    
    @patch('subprocess.run')
    def test_powershell_command_structure(self, mock_subprocess):
        """PowerShellコマンドの構造をテスト"""
        mock_subprocess.return_value = MagicMock(returncode=0)
        
        self.notifier.send_notification("Test", "Message")
        
        call_args = mock_subprocess.call_args[0][0]
        
        # PowerShellが呼び出されていることを確認
        self.assertTrue(any('powershell.exe' in str(arg) for arg in call_args))
        
        # BurntToastコマンドが含まれていることを確認
        command_str = ' '.join(str(arg) for arg in call_args)
        self.assertIn('New-BurntToastNotification', command_str)
    
    def test_default_notification_method(self):
        """デフォルト通知メソッドのテスト"""
        if hasattr(self.notifier, 'send_claude_completion'):
            with patch.object(self.notifier, 'send_notification', return_value=True) as mock_send:
                result = self.notifier.send_claude_completion()
                self.assertTrue(result)
                mock_send.assert_called_once()


if __name__ == '__main__':
    # テスト実行
    unittest.main(verbosity=2)