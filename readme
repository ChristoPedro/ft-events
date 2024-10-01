# FT Stream + Queue + Service Connector Hub

Lab mostrando a utilização de serviços Oracle para eventos e comunicação assíncrona.

## Pré Requisitos

### Dynamic Group

Cria um Dynamic Group para as funções em determinado compartment.

```bash
ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1..aaaaaaaa23______smwa'}
```

### Policies

Criar política para o Dynamic Group da Function ter acesso a outros recursos de OCI

```bash
allow dynamic-group functions to use secret-family in tenancy
allow dynamic-group functions to use queue-push in tenancy
```

### Criar Functions Application

1. Via console criar uma aplicação do functions usando VCN criada anteriormente.
2. Abrir o Code editor e fazer o **Getting Stated** do Functions
3. Salvar o Token Gerado para fazer o Docker loging

### Criar um Secret no OCI Vault

1. Criar um OCI Vault
2. Criar uma Chave de encriptação
3. Criar um secret com o Token gerado anteriormente

## Kafka Producer

1. Fazer o clone do Github
2. Alterar as variáveis do arquivo func.yaml
3. fazer o deploy da function
   ```bash
   fn deploy -v --app Functions
   ```
4. Chamar a Função Criada
   ```
   echo -n '{"Teste":"Producer Kafka"}' | fn invoke Functions producer --content-type application/json

## Queue Producer

1. Fazer o clone do Github
2. Alterar as variáveis do arquivo func.yaml
3. fazer o deploy da function
   ```bash
   fn deploy -v --app Functions
   ```
4. Chamar a Função Criada
   ```
   echo -n '{"Teste":"Producer Queue"}' | fn invoke Functions producer-queue --content-type application/json