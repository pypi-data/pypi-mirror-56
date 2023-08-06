from dataverk_vault.connectors.vault import VaultConnector
from dataverk_vault.context.settings import read_environment_settings


def read_secrets():
    secrets = read_environment_settings()
    with VaultConnector(secrets) as vault_conn:
        return vault_conn.secrets()


def get_database_creds(vault_path):
    secrets = read_environment_settings()
    with VaultConnector(secrets) as vault_conn:
        return vault_conn.db_credentials(vault_path)
