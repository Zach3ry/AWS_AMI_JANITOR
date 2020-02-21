"""
Use At Your Own Risk - This Script Will Deregister ALL Private AMIs Created BEFORE 1-1-2020 If Used As Is
_author_ = "Zachery DeGraffenreid"
_version_ = "1.0"
"""
import datetime
import boto3
from botocore.exceptions import ClientError

# Initialize Boto3 Session and EC2 Client
session = boto3.Session(profile_name='YOUR_AWS_ACCOUNT_NAME_HERE')
ec2_client = session.client('ec2', region_name='us-east-1')

# Define function to deregister all AMIs older than Janurary 1st 2020
def ami_janitor():
    """ The ami_bucket function compiles a list of private AMIs and filters out all AMIs older than 2020-1-1 """
    print('###################### DEREGISTERING AMIs CREATED BEFORE 2020-1s-1 ######################')

    # Get a list of all private AMIs
    ami_client = ec2_client.describe_images(Filters=[{
        'Name': 'is-public',
        'Values': [
            'false',
        ]
    }])
    # Loop through list of private AMIs compiled above
    for ami in ami_client['Images']:
        # Initialize local variables to assign data extracted from the list of private AMIs
        ami_id = ami['ImageId']
        ami_name = ami['Name']
        ami_state = ami['State']
        # Initialize variable below to cut off date for comparison
        cut_off_date = datetime.datetime(2020,1,1)
        # Now we need a to extract the AMI creation date. 
        # Example of raw output of ami['CreationDate'] is "2018-08-03T15:00:26.000Z
        # The Year, Month and Day will suffice - the rest of the information is not needed
        # Initialize variable below to extract the creation date using the split method on the 
        # 'T' to extract the date and selecting the 1st element of the resulting list from the split method
        ami_creation_date = ami['CreationDate'].split('T')[0]
        # This is sufficient for the function output - but for comparison purposes, we need 
        # to split up the year, month and day and assign each value to discrete variables   
        ami_creation_year = ami['CreationDate'].split('T')[0].split('-')[0]
        ami_creation_month = ami['CreationDate'].split('T')[0].split('-')[1]
        ami_creation_day = ami['CreationDate'].split('T')[0].split('-')[2]
        # Initialize variable below and pass in the year, moth and day variables 
        comparison_ami_creation_date = datetime.datetime(int(ami_creation_year), int(ami_creation_month), int(ami_creation_day))
        # Filter out all AMIs older than
        if comparison_ami_creation_date <= cut_off_date:
            print(f"AMI NAME: {ami_name}    AMI ID: {ami_id}    CREATION DATE: {ami_creation_date}  AMI STATE: {ami_state}")
            ami_dustami_dust_pan
            

def ami_dust_pan(ami_id):
    """ The ami_dust_pan fucntion deregisters AMIs """
    while True:
        try:
            # DryRun is a boolean...it checks to see if you have permission to degreister an AMI before actually performing the action
            # If you do not have permission, you will get an UnauthorizedOperation error. 
            ec2_client.deregister_image(ImageId=ami_id, DryRun=True)
            break
        except ClientError as e:
            if e.response['UnauthorizedOperation']:
                print(' You do not have the appropriate permissions to deregister AMIs...change IAM roles and try again...')
                break
            else:
                print(f'{ami_id} operation returned the following error: {e}')
                raise Exception(e)

if __name__ == '__main__':
    ami_janitor()
