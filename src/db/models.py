from sqlalchemy import MetaData, Table
from src.db.session import engine

metadata = MetaData()
metadata.reflect(bind=engine)

repos = metadata.tables["accounts_repository"]
repo_files = metadata.tables["preview_repositoryfile"]
code_states = metadata.tables["preview_repositorycodestate"]
code_embeddings = metadata.tables["aihub_codeembedding"]
