#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import re

# パッケージのルートディレクトリを取得
root_dir = os.path.abspath(os.path.dirname(__file__))

# __init__.pyからバージョン情報を取得
with open(os.path.join(root_dir, '__init__.py'), encoding='utf-8') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("バージョン情報が見つかりません")

# READMEを読み込む
with open(os.path.join(root_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# 依存関係を読み込む
with open(os.path.join(root_dir, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name="clickup-task-importer",
    version=version,
    description="CSVファイルからClickUpにタスクを一括インポートするツール",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kazuhiko Oota",
    author_email="your.email@example.com",  # 実際のメールアドレスを設定してください
    url="https://github.com/ootakazuhiko/ClickUpTaskImporter",
    packages=find_packages(),
    py_modules=["clickup_csv_importer"],
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "clickup-importer=clickup_csv_importer:main",
        ],
    },
    python_requires=">=3.6",
)