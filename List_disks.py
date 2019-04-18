'''
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
   `pip install --upgrade google-api-python-client oauth2client`
'''
from datetime import tzinfo, timedelta, datetime, timezone
import time
from datetime import timedelta
from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'beta', credentials=credentials)
serviceprojects = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

# Project ID for this request.
project = 'p-gcp-cloudcostanalysis'  # TODO: Update placeholder value.

# The name of the zone for this request.
#zone = 'europe-west1-b'  # TODO: Update placeholder value.

# Lists Projects that are visible to the user
def list_projects():
    #serviceprojects = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
    response = serviceprojects.projects().list().execute()
    for project in response.get('projects', []):
        # TODO: Change code below to process each `project` resource:
        projectId = project['projectId']
        print(projectId)
        
    
  
# List of Zone resources available to the specified project
def list_zones(project):
    result = service.zones().list(project=project).execute()
    if 'items' in result:
        return result['items']
        #pprint(items)
    else:
        return []

# List disks in zone
def list_disks(zone):
    result = service.disks().list(project=project, zone=zone).execute()
    if 'items' in result:
        return result['items']
    else:
        return []
#Main
#list_projects()

list_projects()

for zones in list_zones(project):
    #pprint(zone)
    zone_name = zones['name']
    #print(zone_name)
    for disks in list_disks(zone_name):
        #Get disks with detach time
        if 'lastDetachTimestamp' in disks:
            last_detach_time = disks['lastDetachTimestamp']
            date_last_detach_time = datetime.fromisoformat(last_detach_time)
            tz_date_last_detach_time = date_last_detach_time.replace(tzinfo=timezone.utc).timestamp()
            #Get disk size
            sizeGb = disks['sizeGb']
            #Calculate delta in days       
            now = datetime.now()
            tz_now = now.replace(tzinfo=timezone.utc).timestamp()
            delta = (tz_now - tz_date_last_detach_time)/86400             
            #Get disk name
            disk_name = disks['name']
            #Outputs
            #print(delta)
            #pprint(disks)
            print("%s;%s;%s;%.0f;%s" % (project, zone_name, disk_name, delta, sizeGb))
#zones = list_zones(project)
#pprint(zones)
