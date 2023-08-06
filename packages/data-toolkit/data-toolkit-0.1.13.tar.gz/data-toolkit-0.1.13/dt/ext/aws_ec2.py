import boto3
import pandas as pd

def get_ec2(status: str, profile: str):
    ec2 = boto3.session.Session(profile_name=profile, region_name='eu-west-1').client('ec2')
    live_inst = ec2.describe_instances(Filters=[{"Name":"instance-state-name", "Values":["running"] }])
    # live_inst['Reservations']
    # live_inst['Reservations'][1]['Instances'][0]['PublicIpAddress']
    df = pd.DataFrame(live_inst['Reservations'])
    df_list = [ pd.DataFrame.from_dict(x[0], orient='index') for x in df['Instances'].values ]
    full_df = pd.concat(df_list,axis=1, sort=True)
    pd.set_option('display.max_colwidth', 40)
    print(full_df)