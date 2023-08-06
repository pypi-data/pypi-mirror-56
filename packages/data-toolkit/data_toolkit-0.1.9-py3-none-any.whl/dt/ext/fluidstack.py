import sys
sys.path.append('/Users/jakub/remote_code')
from fluidstack_auth import credential_id, credential_secret
import requests
from pprint import pprint as pp

def avail_fl_nodes(stats='all', gpu_count=1):
    filtering_call = f"https://worker.api.fluidstack.io/docker/nodes?bandwidth=1M&total_memory=1G&free_storage=10G&gpus=1&cpu_cores=1"

    headers = {
        "X-Fluidstack-ID":  credential_id,
        "X-Fluidstack-Secret": credential_secret
    }

    api_response = requests.get(filtering_call, headers=headers).json()

    if stats=='all' or stats is None:
        import pandas as pd 
        # pd.set_option('display.max_columns', )
        df = pd.DataFrame.from_dict(api_response['nodes'])
        print(df)

    elif stats=='gpus':
        gpus = { x['id']:x['gpus'] for x in api_response['nodes'] } 
        pp(gpus)

    else:
        raise NotImplementedError('Choose one of {gpus, all}')


def start_docker(target_id: str):
    # example target_id = 'cc8bd5fe-07fd-5ea7-b88b-05bf10c57c7c'

    post_url = 'https://worker.api.fluidstack.io/docker/containers'

    headers = {
        "X-Fluidstack-ID":  credential_id,
        "X-Fluidstack-Secret": credential_secret,
        "Content-Type": "application/json"
    }

    # data = '{"node_id":"{target_id}", "image":"sickp/alpine-sshd:latest"}'
    data = {"node_id" : target_id, "image": "sickp/alpine-sshd:latest"}

    data = {
        "node_id" : target_id,
        "image" : "sickp/alpine-sshd:latest"
    }

    reply = requests.post(post_url, headers=headers, data=data)
    print(reply)


def stop_docker():
    pass