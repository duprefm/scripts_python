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

global liste_projects
liste_projects = []

# The name of the zone for this request.
#zone = 'europe-west1-b'  # TODO: Update placeholder value.

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
    
  
# List of Zone resources available to the specified project
def list_zones(project):
    #print(r.status_code)
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
list_projects()

#liste_projects = ['p-gcp-cloudcostanalysis', 'padawan-p2']
#liste_projects = ['p-vrd-lai-farmstar-crop-monit']
for project in liste_projects:
    #print(project)
    for zones in list_zones(project):
        #print(zones)
        zone_name = zones['name']
        for disks in list_disks(zone_name):
            #Get disks with detach time
            if 'lastDetachTimestamp' in disks:
                last_detach_time = disks['lastDetachTimestamp']
                date_last_detach_time = datetime.fromisoformat(last_detach_time)
                tz_date_last_detach_time = date_last_detach_time.replace(tzinfo=timezone.utc).timestamp()
                #Get disk size
                sizeGb = 0
                sizeGb = disks['sizeGb']
                #Calculate delta in days and months      
                now = datetime.now()
                tz_now = now.replace(tzinfo=timezone.utc).timestamp()
                delta_days = (tz_now - tz_date_last_detach_time)/86400
                delta_months = (tz_now - tz_date_last_detach_time)/(86400*30)
                #Get disk name
                disk_name = disks['name']
                #Get disk type
                disk_type_str = disks['type'].split("/")
                disk_type = disk_type_str[-1]
                #print(disk_type)
                #Calculate cost of unattached disks
                if disk_type == 'pd-standard':
                    prize = delta_months * 0.04 * int(sizeGb)
                if disk_type == 'pd-ssd':
                    prize = delta_months * 0.17 * int(sizeGb)
                #Outputs
                print("%s;%s;%s;%.0f days;%.0f months;%s Gb;$ %.0f" % (project, zone_name, disk_name, delta_days, delta_months, sizeGb, prize))
