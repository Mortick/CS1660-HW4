import boto3
import csv

s3 = boto3.resource('s3',
 aws_access_key_id='',
 aws_secret_access_key=''
)

try:
 s3.create_bucket(Bucket='cs1660', CreateBucketConfiguration={
 'LocationConstraint': 'us-west-2'})
except:
 print("this may already exist")

 bucket = s3.Bucket("cs1660")
 bucket.Acl().put(ACL='public-read')

dyndb =boto3.resource (
    'dynamodb',
    region_name='us-west-2',
    aws_access_key_id='',
    aws_secret_access_key=''
)

try:
 table = dyndb.create_table(
 TableName='DataTable',
 KeySchema=[
 {
 'AttributeName': 'PartitionKey',
 'KeyType': 'HASH'
 },
 {
 'AttributeName': 'RowKey',
 'KeyType': 'RANGE'
 }
 ],
 AttributeDefinitions=[
 {
 'AttributeName': 'PartitionKey',
 'AttributeType': 'S'
 },
 {
 'AttributeName': 'RowKey',
 'AttributeType': 'S'
 },
 ],
 ProvisionedThroughput={
 'ReadCapacityUnits': 5,
 'WriteCapacityUnits': 5
 }
 )
except:
 #if there is an exception, the table may already exist. if so...
 table = dyndb.Table("DataTable")

table.meta.client.get_waiter('table_exists').wait(TableName='DataTable')

print(table.item_count)

import csv
urlbase = "https://s3-us-west-2.amazonaws.com/cs1660/"
with open('master.csv', 'r') as csvfile:
    csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
    for item in csvf:
        print(item)
        body = open('C:/Users/Qing/School/CS1660/' + item[3] + '.csv', 'rb')
        s3.Object('cs1660', item[3]).put(Body=body)
        md=s3.Object('cs1660', item[3]).Acl().put(ACL='public-read')
        
        url = urlbase+item[3]
        metadata_item= {'PartitionKey': item[0], 'RowKey': item[1], 'description': item[4], 'date': item[2], 'url':url}
        try:
            table.put_item(Item=metadata_item)
        except:
            print("Item may already be there or another failure")
    


try:
   response = table.get_item(
    Key={
    'PartitionKey': 'Experiment3',
    'RowKey': 'data3'
    }
    )
except Exception as e:
    sys.exit("Error" + e)

item = response['Item']
print(item)
