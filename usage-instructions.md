# ClickUp CSVタスクインポーター 使用方法

このプログラムは、CSVファイルからClickUpにタスクをAPIを使って作成するためのツールです。

## 準備

### 1. 必要なもの

- Python 3.6以上
- 必要なPythonパッケージ（requests, python-dateutil）
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

## 環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/ootakazuhiko/ClickUpTaskImporter.git
cd ClickUpTaskImporter

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化（Windows/Git Bash）
source venv/Scripts/activate

# 必要なパッケージをインストール
pip install -r requirements.txt
```

## CSVファイルの準備

以下のフォーマットでCSVファイルを作成してください：

- 1行目はヘッダー行として以下のフィールドを含める（最低限`name`は必須）
- 使用可能なフィールド:
  - `name`: タスク名（必須）
  - `description`: タスクの説明
  - `due_date`: 期限（YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD形式に対応）
  - `priority`: 優先度（urgent, high, normal, low）
  - `status`: ステータス（to do, in progress, complete など）
  - `tags`: タグ（カンマ区切り）
  - `assignees`: 担当者のユーザーID（カンマ区切り）
  - `subtasks`: サブタスク名（セミコロン区切り）
  - `custom_[ID]`: カスタムフィールド（IDはClickUpのカスタムフィールドID）

テンプレートCSVファイルが `template/tasks_template.csv` にありますので参考にしてください。

## 使用方法

### 基本的な使い方

```bash
# 仮想環境を有効化（まだしていない場合）
source venv/Scripts/activate

# タスクをインポート
python clickup_csv_importer.py --csv-file タスク一覧.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN
```

### 追加オプション

```bash
# ドライラン（実際にタスクを作成せずにテスト実行）
python clickup_csv_importer.py --csv-file タスク一覧.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --dry-run

# 結果をCSVファイルに出力
python clickup_csv_importer.py --csv-file タスク一覧.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --output 結果.csv

# 詳細なログを出力
python clickup_csv_importer.py --csv-file タスク一覧.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --verbose
```

## その他の機能

- タスクの作成に失敗した場合はエラーメッセージが表示されますが、処理は続行されます
- 日付形式は複数のフォーマットに対応（YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD）
- 優先度は文字列（urgent, high, normal, low）からClickUpの数値形式に自動変換されます
- ドライランモード（`--dry-run`）でタスク作成をシミュレーションできます
- 結果出力（`--output`）でインポート結果をCSVファイルに保存できます

## トラブルシューティング

- API認証エラー: APIトークンが正しいか確認してください
- リストIDエラー: リストIDが正しいか、そのリストにアクセス権があるか確認してください
- CSVフォーマットエラー: CSVファイルが正しい形式で、UTF-8でエンコードされているか確認してください
- 日付変換エラー: 日付が正しい形式で入力されているか確認してください
- ネットワークエラー: インターネット接続とClickUp APIの稼働状況を確認してください

## テストの実行

テストを実行するには以下のコマンドを使用します：

```bash
# 仮想環境を有効化（まだしていない場合）
source venv/Scripts/activate

# テストを実行
python -m unittest discover -s tests
```
