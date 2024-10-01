import io
from kafka import KafkaProducer
from fdk import response
import oci
import logging
import json
import base64

signer = oci.auth.signers.get_resource_principals_signer()

secret_client = oci.secrets.SecretsClient(config={}, signer=signer)

# Busca o Secret no Vault pelo Secret OCID

def read_secret_value(secret_client, secretid):
    secret_content = secret_client.get_secret_bundle(secretid).data.secret_bundle_content.content.encode('utf-8')
    decrypted_secret_content = base64.b64decode(secret_content).decode("utf-8")
    return decrypted_secret_content

# Handler do fn projetct para functions

def handler(ctx, data: io.BytesIO=None):

    try:
        cfg = ctx.Config()
        server = cfg["server"]
        username = cfg["username"]
        secretid = cfg["secretid"]
    except Exception as e:
        print('Missing function parameters', flush=True)
        raise
    
    password = read_secret_value(secret_client, secretid)
    data = json.loads(data.getvalue())

    topics = [] 
    for keys in data.keys():
        topics.append(keys)

# Gera os dados necessário para o produder kafka

    producer = KafkaProducer(bootstrap_servers = server, 
                         security_protocol = 'SASL_SSL', sasl_mechanism = 'PLAIN',
                         sasl_plain_username = username, 
                         sasl_plain_password = password)
    
# Inicia o processamento do body para inserir nas filas corretas    

    for x in topics:

        for key in data[x].keys():

            values = json.dumps(data[x][key]).encode('UTF-8')

    # Inicia o kafka producer

            try:
                producer.send(x, key=key.encode('utf-8'), value=values)
                producer.flush()
                resp = 'Dados Inseridos com sucesso'
            except (Exception, ValueError) as ex:
                logging.getLogger().error('error parsing json payload: ' + str(ex)) 
                resp = 'error parsing json payload: ' + str(ex)

    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )