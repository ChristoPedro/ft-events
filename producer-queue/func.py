import io
import oci
import os
import json
from fdk import response

signer = oci.auth.signers.get_resource_principals_signer()

def put_message (queue_id, service_endpoint ,message):
    try:

        queue_client = oci.queue.QueueClient(config={}, signer=signer, service_endpoint=service_endpoint)

        put_messages_response = queue_client.put_messages(
            queue_id= queue_id,
            put_messages_details=oci.queue.models.PutMessagesDetails(
                messages=[
                    oci.queue.models.PutMessagesDetailsEntry(
                        content=json.dumps(message),
                    metadata=oci.queue.models.MessageMetadata(
                      ))]))
        return put_messages_response.data.messages[0]
    except Exception as e:
        return {"Error" : e}

def handler(ctx, data: io.BytesIO=None):

    try:
        cfg = ctx.Config()
        service_endpoint = cfg["service_endpoint"]
        queue_id = cfg["queue_id"]

    except Exception as e:
        print('Missing function parameters', flush=True)
        raise

    message = json.loads(data.getvalue())
    retorno = put_message(queue_id,service_endpoint, message )
    return response.Response(
        response_data=str(retorno),
        headers={"Content-Type": "application/json"}
    )
