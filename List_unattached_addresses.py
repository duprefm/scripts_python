"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Compute Engine API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/compute
2. This sample uses Application Default Credentials for authentication.
   If not already done, install the gcloud CLI from
   https://cloud.google.com/sdk and run
   `gcloud beta auth application-default login`.
   For more information, see
   https://developers.google.com/identity/protocols/application-default-credentials
3. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""
from pprint import pprint
from datetime import tzinfo, timedelta, datetime, timezone

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'v1', credentials=credentials)
serviceprojects = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

# Project ID for this request.
#project = 'p-gcp-cloudcostanalysis'  # TODO: Update placeholder value.

# Name of the region for this request.
#region = 'europe-west1'  # TODO: Update placeholder value.

global liste_projects
liste_projects = []

# Lists Projects that are visible to the user
def list_projects():
    tags_filter = '(labels.cost_center_number:*)'
    response = serviceprojects.projects().list(filter=tags_filter).execute()
    for project in response.get('projects', []):
        # TODO: Change code below to process each `project` resource:
        project = project['projectId']
        #pprint(project)
        liste_projects.append(project)
        #print(liste_projects)

# List of Region resources available to the specified project
def list_regions(project):
    #print(r.status_code)
    result = service.regions().list(project=project).execute()
    if 'items' in result:
        return result['items']
        #pprint(items)
    else:
        return []

# List address
def list_address(region):
    result = service.addresses().list(project=project, region=region).execute()
    if 'items' in result:
        return result['items']
        pprint(items)
    else:
        return []

liste_projects = ['p-gcp-cloudcostanalysis', 'padawan-p2']

#Main
list_projects()

#liste_projects = ['p-gcp-cloudcostanalysis', 'padawan-p2']
#liste_projects = ['p-vrd-lai-farmstar-crop-monit']
for project in liste_projects:
    #print(project)
    for regions in list_regions(project):
        #print(regions)
        region_name = regions['name']
        for address in list_address(region_name):
            #pprint(address)
            #Get address creation time
            creationdate = address['creationTimestamp']
            date_creationdate = datetime.fromisoformat(creationdate)
            tz_date_creationdate = date_creationdate.replace(tzinfo=timezone.utc).timestamp()
            #Calcul address duration in month
            now = datetime.now()
            tz_now = now.replace(tzinfo=timezone.utc).timestamp()
            delta_days = (tz_now - tz_date_creationdate)/86400
            delta_months = (tz_now - tz_date_creationdate)/(86400*30)
            #Calculate waste on reserved ip
            prize = delta_months * 7.20

            address_status = address['status']
            address_ip = address['address']
            address_name = address['name']
            #print(address_status)
            if address_status == 'RESERVED':
                print("%s;%s;%s;%s;%.0f days;%.0f months;$ %.0f" % (project, region_name, address_name, address_ip, delta_days, delta_months, prize))
