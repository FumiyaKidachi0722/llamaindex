import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from dotenv import load_dotenv
import os

# .env ファイルをロードして環境変数に設定
load_dotenv()

# 環境変数から API キーを取得
openai_api_key = os.getenv('OPENAI_API_KEY')

# 永続化するディレクトリの設定
PERSIST_DIR = "./storage"

# インデックスのチェックとロードまたは作成
if not os.path.exists(PERSIST_DIR):
    # ドキュメントを読み込みインデックスを作成
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # インデックスを保存
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # 既存のインデックスをロード
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# 質問エンジンの作成
query_engine = index.as_query_engine()

# 質問と回答の繰り返し入力・表示
while True:
    question = input("質問を入力してください: ")
    if question.lower() in ["終了", "exit", "quit"]:
        print("終了します。")
        break
    response = query_engine.query(question)
    print("回答:", response)
