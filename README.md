# ClickUp Task Importer

[English](#english) | [日本語](#japanese)

<a id="english"></a>
## English

A Python tool for importing tasks from CSV files to ClickUp.

### Features

- Bulk import tasks from CSV files to ClickUp
- Set task names, descriptions, due dates, priorities, statuses, tags, and assignees
- Create subtasks
- Configure custom fields
- Detailed logging
- Support for multiple date formats
- Dry run mode (to check without actually creating tasks)
- Export import results to CSV

### Requirements

- Python 3.6 or later
- Requests library
- Python-dateutil library
- ClickUp API token
- ClickUp list ID

### Installation

1. Clone this repository:
```bash
git clone https://github.com/ootakazuhiko/ClickUpTaskImporter.git
```

2. Create and activate a virtual environment:
```bash
cd ClickUpTaskImporter
python -m venv venv
source venv/Scripts/activate  # Windows/Git Bash
# source venv/bin/activate  # Linux/Mac
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

### Usage

1. Prepare a CSV file (see [template example](./template/tasks_template.csv))
2. Run the following command:

```bash
python clickup_csv_importer.py --csv-file your_tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN
```

Additional options:
```bash
# Dry run mode (test without actually creating tasks)
python clickup_csv_importer.py --csv-file your_tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --dry-run

# Save results to output file
python clickup_csv_importer.py --csv-file your_tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --output results.csv

# Enable detailed logging
python clickup_csv_importer.py --csv-file your_tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --verbose
```

For detailed usage instructions, see the [Usage Guide](./usage-instructions.md).

### CSV Format

The tool supports the following columns:

| Column Name | Description | Required | Format |
|-------------|-------------|----------|--------|
| name | Task name | Yes | Text |
| description | Task description | No | Text |
| due_date | Due date | No | YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD |
| priority | Priority | No | urgent, high, normal, low |
| status | Status | No | to do, in progress, complete, etc. |
| tags | Tags | No | Comma-separated text |
| assignees | Assignees | No | Comma-separated user IDs |
| subtasks | Subtasks | No | Semicolon-separated text |
| custom_[ID] | Custom field | No | Value according to the custom field ID |

### How to Get API Token

1. Log in to ClickUp
2. Click on your profile avatar in the bottom left
3. Select "Settings"
4. Click on "Apps" in the left sidebar
5. Click "Generate" to create an API token

### How to Get List ID

1. Open the list in ClickUp web interface where you want to import tasks
2. Find the "list/XXXXXXXXX" part in the URL (XXXXXXXXX is the list ID)

Example: For `https://app.clickup.com/123456/v/li/789012345`, the list ID is `789012345`

### Security Notes

- **API tokens are sensitive information**. Do not include them directly in your source code or commit them to version control systems.
- When using the `--api-token` option on the command line, be aware that it may be stored in your command history.
- For production environments, it's recommended to use environment variables:
  ```bash
  export CLICKUP_API_TOKEN="your_api_token"
  python clickup_csv_importer.py --csv-file your_tasks.csv --list-id YOUR_LIST_ID --api-token $CLICKUP_API_TOKEN
  ```
- When running the script in automated processes, ensure proper permission management.

### Testing

To run tests:

```bash
python -m unittest discover -s tests
```

### License

[MIT License](./LICENSE)

### Contributing

Please report bugs and feature requests in [Issues](https://github.com/ootakazuhiko/ClickUpTaskImporter/issues).
Pull requests are welcome.

---

<a id="japanese"></a>
## 日本語

CSVファイルからClickUpにタスクを一括インポートするためのPythonツールです。

### 機能

- CSVファイルからClickUpにタスクを一括作成
- タスク名、説明、期限、優先度、ステータス、タグ、担当者の設定
- サブタスクの作成
- カスタムフィールドの設定
- 詳細なログ出力
- 複数の日付形式に対応
- ドライランモード（実際にタスクを作成せずに確認）
- インポート結果のCSV出力

### 必要条件

- Python 3.6以上
- requestsライブラリ
- python-dateutilライブラリ
- ClickUp APIトークン
- ClickUpのリストID

### インストール方法

1. このリポジトリをクローン：
```bash
git clone https://github.com/ootakazuhiko/ClickUpTaskImporter.git
```

2. 仮想環境を作成し有効化：
```bash
cd ClickUpTaskImporter
python -m venv venv
source venv/Scripts/activate  # Windows/Git Bash
# source venv/bin/activate  # Linux/Mac
```

3. 必要なパッケージをインストール：
```bash
pip install -r requirements.txt
```

### 使用方法

1. CSVファイルを準備（[テンプレート例](./template/tasks_template.csv)を参照）
2. 以下のコマンドを実行：

```bash
python clickup_csv_importer.py --csv-file your_tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN
```

追加オプション：
```bash
# ドライランモード（実際にタスクを作成せずにテスト）
python clickup_csv_importer.py --csv-file your_tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --dry-run

# 結果を出力ファイルに保存
python clickup_csv_importer.py --csv-file your_tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --output results.csv

# 詳細なログ出力
python clickup_csv_importer.py --csv-file your_tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --verbose
```

詳細な使用方法については[使用方法ガイド](./usage-instructions.md)を参照してください。

### CSV形式

以下の列に対応しています：

| 列名 | 説明 | 必須 | 形式 |
|-----|------|-----|-----|
| name | タスク名 | はい | テキスト |
| description | タスクの説明 | いいえ | テキスト |
| due_date | 期限 | いいえ | YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD |
| priority | 優先度 | いいえ | urgent, high, normal, low |
| status | ステータス | いいえ | to do, in progress, complete など |
| tags | タグ | いいえ | カンマ区切りのテキスト |
| assignees | 担当者 | いいえ | カンマ区切りのユーザーID |
| subtasks | サブタスク | いいえ | セミコロン区切りのテキスト |
| custom_[ID] | カスタムフィールド | いいえ | カスタムフィールドIDに応じた値 |

### API トークンの取得方法

1. ClickUpにログインする
2. 左下のプロフィールアバターをクリック
3. 「設定」を選択
4. 左サイドバーで「Apps」をクリック
5. 「Generate」をクリックしてAPIトークンを生成

### リストIDの取得方法

1. ClickUpのWebインターフェースでタスクをインポートしたいリストを開く
2. URLから「list/XXXXXXXXX」の部分を見つける（XXXXXXXXXがリストID）

例： `https://app.clickup.com/123456/v/li/789012345`の場合、リストIDは`789012345`

### セキュリティ上の注意

- **APIトークンは機密情報です**。APIトークンをソースコードに直接記述したり、バージョン管理システムにコミットしたりしないでください。
- コマンドラインで`--api-token`オプションを使用する場合、コマンド履歴に残る可能性があります。
- 本番環境では環境変数を使用することをお勧めします：
  ```bash
  export CLICKUP_API_TOKEN="your_api_token"
  python clickup_csv_importer.py --csv-file your_tasks.csv --list-id YOUR_LIST_ID --api-token $CLICKUP_API_TOKEN
  ```
- スクリプトを自動化プロセスで実行する場合は、適切な権限管理を行ってください。

### テスト

テストを実行するには：

```bash
python -m unittest discover -s tests
```

### ライセンス

[MIT License](./LICENSE)

### 貢献

バグ報告や機能リクエストは[Issues](https://github.com/ootakazuhiko/ClickUpTaskImporter/issues)にお願いします。
プルリクエストも歓迎します。