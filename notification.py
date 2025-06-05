#!/usr/bin/env python3
"""
WSL2からWindows側へ通知を送るモジュール

PowerShellのBurntToastNotificationを使用してWindows通知を送信
"""

import subprocess
import shlex
from typing import Optional


class WindowsNotifier:
    """WSL2からWindows側に通知を送信するクラス"""
    
    def __init__(self):
        """通知クラスの初期化"""
        self.powershell_path = "/mnt/c/windows/System32/WindowsPowerShell/v1.0/powershell.exe"
    
    def send_notification(self, title: str, message: str, 
                         duration: Optional[str] = "Short") -> bool:
        """
        Windows通知を送信する
        
        Args:
            title (str): 通知のタイトル
            message (str): 通知メッセージ
            duration (str): 通知の表示時間 (使用されません)
            
        Returns:
            bool: 送信成功時True、失敗時False
        """
        try:
            # Windows標準のpowershell通知を使用
            notification_script = f"""
Add-Type -AssemblyName System.Windows.Forms
$notification = New-Object System.Windows.Forms.NotifyIcon
$notification.Icon = [System.Drawing.SystemIcons]::Information
$notification.BalloonTipTitle = '{title}'
$notification.BalloonTipText = '{message}'
$notification.Visible = $true
$notification.ShowBalloonTip(5000)
Start-Sleep -Seconds 6
$notification.Dispose()
"""
            
            # 通知送信
            result = subprocess.run([
                self.powershell_path,
                "-Command",
                notification_script
            ], capture_output=True, check=False, timeout=15)
            
            return result.returncode == 0
            
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, Exception) as e:
            print(f"通知送信エラー: {e}")
            return False
    
    def send_claude_completion(self, task_name: Optional[str] = None) -> bool:
        """
        Claude Code完了通知を送信する
        
        Args:
            task_name (str, optional): 完了したタスク名
            
        Returns:
            bool: 送信成功時True、失敗時False
        """
        title = "Claude Code 完了"
        
        if task_name:
            message = f"タスク「{task_name}」が完了しました"
        else:
            message = "タスクが正常に完了しました"
        
        return self.send_notification(title, message)
    
    def send_error_notification(self, error_message: str) -> bool:
        """
        エラー通知を送信する
        
        Args:
            error_message (str): エラーメッセージ
            
        Returns:
            bool: 送信成功時True、失敗時False
        """
        title = "Claude Code エラー"
        message = f"エラーが発生しました: {error_message}"
        
        return self.send_notification(title, message, duration="Long")


# コマンドライン実行時の処理
if __name__ == "__main__":
    import sys
    
    notifier = WindowsNotifier()
    
    if len(sys.argv) == 1:
        # 引数なしの場合はデフォルト通知
        success = notifier.send_claude_completion()
    elif len(sys.argv) == 2:
        # タスク名指定
        success = notifier.send_claude_completion(sys.argv[1])
    elif len(sys.argv) == 3:
        # タイトルとメッセージ指定
        success = notifier.send_notification(sys.argv[1], sys.argv[2])
    else:
        print("使用方法: python3 notification.py [タスク名] または python3 notification.py [タイトル] [メッセージ]")
        sys.exit(1)
    
    if success:
        print("通知を送信しました")
    else:
        print("通知送信に失敗しました")
        sys.exit(1)