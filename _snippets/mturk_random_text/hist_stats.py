import boto3
import shelve

session = boto3.Session(profile_name='root')
mturk = session.client('mturk', 'us-east-1')

print('Balance', mturk.get_account_balance()['AvailableBalance'])

hit_id = None
with shelve.open('state') as db:
    hit_id = db['HITId']
    response = mturk.get_hit(HITId=hit_id)
    hit_status = response['HIT']['HITStatus']
    finished = hit_status in set(['Disposed'])
    print(f'{hit_id=} {hit_status=}')
    print(f'{response.get("NumberOfAssignmentsPending","")=}\n{response.get("NumberOfAssignmentsAvailable","")=}\n{response.get("NumberOfAssignmentsCompleted","")=}\n')
    #for i in response['HIT']:
    #    print(i, response['HIT'][i])

# list processed assignments
paginator = mturk.get_paginator('list_assignments_for_hit')
for response in paginator.paginate(HITId=hit_id, AssignmentStatuses=['Approved']):
    for assignment in response['Assignments']:
        print('Approved', assignment['AssignmentId'])
        print(assignment)
for response in paginator.paginate(HITId=hit_id, AssignmentStatuses=['Rejected']):
    for assignment in response['Assignments']:
        print('Rejected', assignment['AssignmentId'])
# list blocks
paginator = mturk.get_paginator('\n\nlist_worker_blocks')
for response in paginator.paginate():
    for worker_block in response['WorkerBlocks']:
        print(worker_block)