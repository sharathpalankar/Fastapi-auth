import json
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # TODO implement 
    print(event)
    
    instance_id = event['detail']['instance-id']
    
    print(f"Processing instance: {instance_id}")

    # Step 1: Get instance details
    response = ec2.describe_instances(InstanceIds=[instance_id])

    volumes = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for mapping in instance.get('BlockDeviceMappings', []):
                volume_id = mapping['Ebs']['VolumeId']
                volumes.append(volume_id)

    print(f"Attached volumes: {volumes}")

    # Step 2: Check each volume
    for volume_id in volumes:
        vol_response = ec2.describe_volumes(VolumeIds=[volume_id])
        
        volume = vol_response['Volumes'][0]
        volume_type = volume['VolumeType']

        print(f"Volume {volume_id} type: {volume_type}")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda, Event logged!')
    }
