## secret-manager
Secret manager for Python

### How to use 

****Add dependency -****  
secrets-manager==0.0.2

****Set environment variable -****  
APP_ENV = prod/staging    
APP_NAME = IAMservice

**In config file:**  
from secretmanager import secrets

redshift_secrets = secrets['redshift']   
REDSHIFT_HOST = redshift_secrets['host']     
REDSHIFT_PORT = redshift_secrets['port']     
REDSHIFT_USER = redshift_secrets['username']    
REDSHIFT_PASS = redshift_secrets['password']    
REDSHIFT_DB = redshift_secrets['dbname'] 

****Secret manager changes -****  
Secret format is -     
`APP_NAME + "_" + APP_ENV + "_" + SECRET_NAME`

Go to secret manager and add secret name in above defined format eg(IAMservice_prod_redshift)     
Add key value pair inside as -       
    host = <redshift_host>         
    port = <redshift_host>   

SECRET_NAME will be used to access secret in your code.    
In above example SECRET_NAME = redshift 

