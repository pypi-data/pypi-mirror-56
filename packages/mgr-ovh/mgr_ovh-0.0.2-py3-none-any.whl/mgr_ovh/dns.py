# -*- encoding: utf-8 -*-
'''
First, install the latest release of Python wrapper: $ pip install ovh
'''
import json
import ovh

# fieldType : A, AAA, CA, CNAME, ....
def createRecord(client, dnsZone, fieldType, name, target, ttl):
 result = client.post('/domain/zone/'+dnsZone+'/record', 
    fieldType=fieldType, # Resource record Name (type: zone.NamedResolutionFieldTypeEnum)
    subDomain=name, # Resource record subdomain (type: string)
    target=target, # Resource record target (type: string)
    ttl=ttl, # Resource record ttl (type: long)
 )
 print(json.dumps(result, indent=4))
 return result

def getRecords(client, dnsZone, fieldType, name):
 result = client.get('/domain/zone/'+dnsZone+'/record', 
    fieldType=fieldType, # Resource record Name (type: zone.NamedResolutionFieldTypeEnum)
    subDomain=name, # Resource record subdomain (type: string)
 )
 print(json.dumps(result, indent=4))
 return result

def getRecordDetails(client, dnsZone, recordId):
 result = client.get('/domain/zone/'+dnsZone+'/record/'+recordId)
 print(json.dumps(result, indent=4))
 return result
 
def deleteRecord(client, dnsZone,recordId ):
 result = client.delete('/domain/zone/'+dnsZone+'/record/'+recordId)
 print(json.dumps(result, indent=4))
 return result
 

