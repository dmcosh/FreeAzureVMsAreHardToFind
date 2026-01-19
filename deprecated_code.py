"""
*********************************************************************
This block of code was intial attempt at retrieving VM information.  
It worked but I decided to go with straight API call instead of 
using Azure Python SDK. Had to use API call for part of project 
anyway and SDK didn't prove to be any easier/better IMHO.
- DC 2026-01-15
*********************************************************************
"""
### Use Azure SDK for Python to get VM availability into DataFrame

# Authenticate and pull resource skus using Azure SDK for Python
try:
    client = ComputeManagementClient(
        credential=DefaultAzureCredential(), # Will pull auth from env vars or dev auth
        subscription_id=azure_subscription_id
    )
except Exception as e:
    print(f"Authentication failed: {e}")

# The only built-in filter is on location, which would defeat the point of this project
# ...so we're getting the whole list and it can take a couple minutes to pull!
sdk_response = client.resource_skus.list()

# Returns an ItemPaged object that needs to be iterated.
vm_dict = [] # Init empty list variable to store rows of dictionaries
for page in sdk_response:
    # Only process records related to VMs
    if page.resource_type == 'virtualMachines':
        vm_dict.append(page.as_dict()) # Add dictionary item to list

# Load list of dictionaries into Polars DataFrame
pldf_vms = pl.from_dicts(vm_dict, infer_schema_length=None) # Used once so I could collect schema
# print(pldf_vms.collect_schema()) # Copied schema to speed up future processing
# pldf_vms = pl.from_dicts(vm_dict, schema = "({'resource_type': String, 'name': String, 'tier': String, 'size': String, 'family': String, 'locations': List(String), 'location_info': List(Struct({'location': String, 'zones': List(String), 'zone_details': List(Struct({'capabilities': List(Struct({'name': String, 'value': String}))}))})), 'capabilities': List(Struct({'name': String, 'value': String})), 'restrictions': List(Struct({'type': String, 'values': List(String), 'restriction_info': Struct({'locations': List(String), 'zones': List(String)}), 'reason_code': String}))})")
