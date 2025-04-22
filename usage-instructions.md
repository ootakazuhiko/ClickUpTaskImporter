# ClickUp CSVタスクインポーター 使用方法

このプログラムは、CSVファイルからClickUpにタスクをAPIを使って作成するためのツールです。

## 準備

### 1. 必要なもの

- Python 3.6以上
- 必要なPythonパッケージ（requests）
- ClickUp API トークン
- インポート先のClickUpリストID

### 2. API トークンの取得

1. ClickUpにログインする
2. 左下のプロフィールアバターをクリック
3. 「設定」を選択
4. 左サイドバーで「Apps」をクリック
5. 「Generate」をクリックしてAPIトークンを生成
6. 作成されたトークンをコピーする

### 3. リストIDの取得

1. ClickUpのWebインターフェースでタスクをインポートしたいリストを開く
2. URLから「list/XXXXXXXXX」の部分を見つける（XXXXXXXXXがリストID）

例： `https://app.clickup.com/123456/v/li/789012345`の場合、リストIDは`789012345`

## CSVファイルの準備

以下のフォーマットでCSVファイルを作成してください：

- 1行目はヘッダー行として以下のフィールドを含める（最低限`name`は必須）
- 使用可能なフィールド:
  - `name`: タスク名（必須）
  - `description`: タスクの説明
  - `due_date`: 期限（YYYY-MM-DD形式）
  - `priority`: 優先度（urgent, high, normal, low）
  - `status`: ステータス（to do, in progress, complete など）
  - `tags`: タグ（カンマ区切り）
  - `assignees`: 担当者のユーザーID（カンマ区切り）
  - `subtasks`: サブタスク名（セミコロン区切り）
  - `custom_[ID]`: カスタムフィールド（IDはClickUpのカスタムフィールドID）

## 使用方法

1. スクリプトを実行する:

```bash
python clickup_csv_importer.py --csv-file タスク一覧.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN
```

2. スクリプトが実行され、各タスクの作成状況がログに出力されます。

## その他の機能

- タスクの作成に失敗した場合はエラーメッセージが表示されますが、処理は続行されます
- 日付形式は複数のフォーマットに対応（YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD）
- 優先度は文字列（urgent, high, normal, low）からClickUpの数値形式に自動変換されます

## トラブルシューティング

- API認証エラー: APIトークンが正しいか確認してください
- リストIDエラー: リストIDが正しいか、そのリストにアクセス権があるか確認してください
- CSVフォーマットエラー: CSVファイルが正しい形式で、UTF-8でエンコードされているか確認してください

## 拡張方法

- カスタムフィールドの取得と設定の機能を追加
- エラー発生時のリトライ機能
- 一括インポート用のプログレスバー表示
