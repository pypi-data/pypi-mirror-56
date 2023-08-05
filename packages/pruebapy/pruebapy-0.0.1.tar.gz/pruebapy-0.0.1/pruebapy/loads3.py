import boto3
import pandas as pd
import io

def s3csv_to_df(REGION, ACCESS_KEY_ID, SECRET_ACCESS_KEY, SESSION_TOKEN, KEY, BUCKET_NAME):

	s3c = boto3.client(
        	's3', 
	        region_name = REGION,
        	aws_access_key_id = ACCESS_KEY_ID,
	        aws_secret_access_key = SECRET_ACCESS_KEY,
	        aws_session_token = SESSION_TOKEN
	    )

	obj = s3c.get_object(Bucket= BUCKET_NAME , Key = KEY)
	s3File = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8')
	return s3File