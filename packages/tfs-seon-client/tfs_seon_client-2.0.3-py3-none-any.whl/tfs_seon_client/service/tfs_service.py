import pika
import uuid
import os
import json
from pprint import pprint
from rabbitmqX.patterns.client.work_queue_task_client import Work_Queue_Task_Client
from rabbitmqX.journal.journal import Journal
import json 

class TFS_Service (Work_Queue_Task_Client):
    
    def __init__(self, type):
        Work_Queue_Task_Client.__init__(self,'integration.tfs')
        self.type = type

    def integrate(self, organization_id, tfs_key, tfs_url, application):

        data = {'organization_id': organization_id, 
                "tfs_key": tfs_key, 
                "tfs_url": tfs_url,
                "application": application}      
        journal = Journal(organization_id,self.type,data,"integration")
        self.send(journal)
        

