# Claude Code Windows通知システム

WSL2環境のClaude CodeからWindows側に通知を送信するシステムです。

## 概要

このプロジェクトは、WSL2のUbuntu環境で動作するClaude CodeからWindows側に通知を送る仕組みを提供します。タスク完了時やエラー発生時に、Windows側にバルーン通知を表示できます。

## 必要な環境

- Windows 10/11
- WSL2 (Ubuntu 24.04)
- PowerShell（Windows標準搭載）
- Python 3.x

## ファイル構成

```
.
├── README.md              # このファイル
├── notification.py        # 通知送信メインモジュール
└── test_notification.py   # テストファイル
```

## インストール・セットアップ

### 1. リポジトリのクローン

```bash
git clone <このリポジトリのURL>
cd claude-code-windows-alert
```

### 2. 通知システムのテスト

```bash
# テスト実行
python3 test_notification.py

# 実際の通知テスト
python3 notification.py "テスト通知" "システムが正常に動作しています"
```

## 使用方法

### 基本的な使用方法

#### 1. デフォルト通知

```bash
python3 notification.py
```

#### 2. タスク名を指定した通知

```bash
python3 notification.py "データベース移行"
```

#### 3. カスタム通知

```bash
python3 notification.py "カスタムタイトル" "カスタムメッセージ"
```

### Python環境での使用

```python
from notification import WindowsNotifier

# 通知オブジェクトを作成
notifier = WindowsNotifier()

# 基本的な通知
notifier.send_notification("タイトル", "メッセージ")

# Claude Code完了通知
notifier.send_claude_completion("タスク名")

# エラー通知
notifier.send_error_notification("エラーの詳細")
```

## Claude Codeでの活用方法

### 1. CLAUDE.mdに設定を追加

`~/.claude/CLAUDE.md`に以下を追加します：

```markdown
## ユーザへのアテンション

- ユーザの許可や確認が必要な場合は、下記のスクリプトを実行して通知を発信してください。
- 応答の完了時、下記のスクリプトを実行して通知を発信してください。

```bash
# 通知スクリプトのパス
NOTIFICATION_SCRIPT="~/git/claude-code-windows-alert/notification.py"

# タスク完了時の通知例
python3 $NOTIFICATION_SCRIPT "Claude Code 完了" "タスクが正常に完了しました"
```
```

### 2. シェルエイリアスの設定

`~/.bashrc`または`~/.zshrc`に追加：

```bash
# Claude Code通知エイリアス
alias claude-notify='python3 /path/to/claude-code-windows-alert/notification.py'
alias claude-done='python3 /path/to/claude-code-windows-alert/notification.py "Claude Code 完了" "タスクが正常に完了しました"'
```

### 3. Claude Codeでの使用例

#### タスク完了時の通知

```bash
# ビルド実行後に通知
npm run build && claude-notify "ビルド完了" "プロジェクトのビルドが正常に完了しました"

# テスト実行後に通知  
python -m pytest && claude-notify "テスト完了" "全てのテストが通過しました"

# デプロイ後に通知
./deploy.sh && claude-notify "デプロイ完了" "本番環境への配信が完了しました"
```

#### エラー発生時の通知

```bash
# エラー時のみ通知
npm run build || claude-notify "ビルドエラー" "ビルド処理でエラーが発生しました"
```

### 4. Gitフックでの自動通知

`.git/hooks/post-commit`を作成：

```bash
#!/bin/bash
python3 /path/to/claude-code-windows-alert/notification.py "Git Commit" "コミットが完了しました"
```

## トラブルシューティング

### 通知が表示されない場合

1. **PowerShellのパス確認**
   ```bash
   ls -la /mnt/c/windows/System32/WindowsPowerShell/v1.0/powershell.exe
   ```

2. **Windows側の通知設定確認**
   - Windows設定 > システム > 通知とアクション
   - 「アプリやその他の送信者からの通知を取得する」がオンになっていることを確認

3. **WSL2とWindows間の通信確認**
   ```bash
   /mnt/c/windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "Get-Date"
   ```

### よくあるエラー

#### 「通知送信に失敗しました」と表示される場合

- PowerShellのパスが正しいか確認
- Windows側の実行ポリシーを確認：
  ```powershell
  Get-ExecutionPolicy
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

#### タイムアウトエラーが発生する場合

- notification.pyの`timeout`値を増やしてください（現在15秒）

## 開発・テスト

### テスト実行

```bash
# 全テスト実行
python3 test_notification.py

# 特定のテストのみ実行
python3 -m unittest test_notification.TestWindowsNotification.test_send_notification_basic
```

### モックテストの無効化（実際の通知テスト）

テストファイル内の`@patch('subprocess.run')`をコメントアウトして実行することで、実際の通知送信をテストできます。

## ライセンス

MIT License

## 貢献

プルリクエストやイシューの報告を歓迎します。

---

**Note**: このシステムはWSL2環境でのみ動作します。ネイティブLinux環境では使用できません。