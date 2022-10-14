# This utility was developed in October of 2022 by Alex Clark of Clark Management Consulting. 
# It is released to the public under the Creative Commons CC0 Universal Public Domain Dedication


import json
import sys
import csv
import datetime

if len(sys.argv) == 1:
    print('You must supply the filename for the json file to be processed as a parameter')
    exit()

message_store_filename = sys.argv[1]
sms_messages = list()
headers = ['id','to','to_name','to_location','to_multiple','from','from_name','from_location','type','creationTime','readStatus','priority','lastModifiedTime','direction','subject','conversationId','availability','messageStatus', 'attachmentId']
sms_messages.insert(0,headers)
csv_output_file = "csv_output_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') + ".csv"

f = open(message_store_filename)
data = json.load(f)

for i in data['records']:
    sms_message = list()
    sms_message.append(i['id'])
    sms_message.append(i['to'][0]['phoneNumber'])
    if 'name' in i['to'][0]:
        sms_message.append(i['to'][0]['name'])
    else:
        sms_message.append(' ')
    if 'location' in i['to'][0]:
        sms_message.append(i['to'][0]['location'])
    else:
        sms_message.append(' ')
    if len(i['to']) > 1:
        sms_message.append('multiple recipients - check json')
    else:
        sms_message.append('single recipient')
    sms_message.append(i['from']['phoneNumber'])
    if 'name' in i['from']:
        sms_message.append(i['from']['name'])
    else:
        sms_message.append(' ')
    if 'location' in i['from']:
        sms_message.append(i['from']['location'])
    else:
        sms_message.append(' ')
    sms_message.append(i['type'])
    sms_message.append(i['creationTime'])
    sms_message.append(i['readStatus'])
    sms_message.append(i['priority'])
    sms_message.append(i['lastModifiedTime'])
    sms_message.append(i['direction'])
    sms_message.append(i['subject'])
    sms_message.append(i["conversationId"])
    sms_message.append(i["availability"])
    sms_message.append(i["messageStatus"]) 
    #can there be multiple conversationIds for a message? I did not include the conversation key which contains a nested id element
    attachments_space_separated = ""
    for attachment in i['attachments']:
        attachments_space_separated = attachment['id'] + " "
    sms_message.append(attachments_space_separated)
    sms_messages.append(sms_message)


f.close()

with open(csv_output_file, "w", newline="") as c:
    writer = csv.writer(c, quoting=csv.QUOTE_ALL)
    writer.writerows(sms_messages)

