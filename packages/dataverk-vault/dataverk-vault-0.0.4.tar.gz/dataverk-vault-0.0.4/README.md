# dataverk-vault

Bibliotek med api mot vault for secrets handling og database credential generering for dataverk

### Installasjon

#### Master branch versjon
```
git clone https://github.com/navikt/dataverk-vault.git
cd dataverk-vault
pip install .
```

#### Siste release
```
pip install dataverk-vault
```

## Environment variabler
Følgende environment variabler må være satt i kjøremiljøet:
- K8S_TOKEN_PATH
- POD_NAMESPACE
- VKS_VAULT_ADDR
- VKS_AUTH_PATH
- VKS_KV_PATH

## For NAV-ansatte
Interne henvendelser kan sendes via Slack i kanalen #dataverk