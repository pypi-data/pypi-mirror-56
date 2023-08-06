from redscope.project.project import Folders
from redscope.database.models import Catalog
import pandas as pd


class IntroSchema:

    def __init__(self, db_connection, catalog: Catalog, folders: Folders):
        self.db_connection = db_connection
        self.data = pd.DataFrame()
        self.catalog = catalog
        self.folders = folders

    def execute(self):
        self.fetch_data()
        self._set_create_schema()
        self._set_paths()
        self._make_dirs()
        self._make_files()

    def fetch_data(self):
        self.data = self.catalog.fetch_schema(self.db_connection)

    def _set_create_schema(self):
        self.data['create_schema_sql'] = self.data['schema_name'].apply(lambda x: f"CREATE SCHEMA IF NOT EXISTS {x};")

    def _set_paths(self):
        self.data['paths'] = self.data['schema_name'].apply(lambda x: self.folders.schema_path / x / "schema")

    def _make_dirs(self):
        self.data['paths'].apply(lambda x: x.mkdir(exist_ok=True, parents=True))

    def _make_files(self):
        self.data.apply(lambda x: x['paths'].joinpath(f"{x['paths'].parent.name}.sql").write_text(x['create_schema_sql']), axis=1)
