import os
from simple_salesforce import Salesforce

DEFAULT_API_VERSION = '57.0'

class SalesforceConnection:
    """Create new connection to Salesforce"""

    def __init__(
        self,
        username=None,
        password=None,
        security_token=None,
        domain=None,
        version=DEFAULT_API_VERSION):
        self.conn = None

        # Use environment variables in case if username was not given
        if username is None:
            self.username = os.environ["SF_USER"]
            self.password = os.environ["SF_PASS"]
            self.security_token = os.environ["SF_SECURITY_TOKEN"]
            self.domain = os.environ["SF_DOMAIN"]
        else:
            self.username = username
            self.password = password
            self.security_token = security_token
            self.domain = domain
        
        self.version = version

    def get_conn(self):
        """
        Sign into Salesforce, only if we are not already signed in.
        """
        if not self.conn:
            self.conn = Salesforce(
                username=self.username, 
                password=self.password, 
                security_token=self.security_token, 
                domain=self.domain,
                version=self.version,
            )
        return self.conn

    def get_object_field_info(self, object_name):
        sf = self.get_conn()
        field_info = {}
        desc = getattr(sf, object_name).describe()
        
        for fld in desc['fields']:
            field_info[fld['name']] = {
                'label': fld['label'],
                'type': fld['type'],
                'length': fld['length'],
                'referenceTo': fld['referenceTo'],
                'precision': fld['precision'],
                'digits': fld['digits']
            }
        return field_info