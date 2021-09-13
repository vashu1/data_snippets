"""
The rejection may affect your reputation as a Requester and the approval rate of the Worker who submitted the results.

# override rejection
import boto3
session = boto3.Session(profile_name='root')
mturk = session.client('mturk', 'us-east-1')
client.approve_assignment(
    AssignmentId='string',  # put actual id and reason
    RequesterFeedback='string',
    OverrideRejection=True
)
"""
import boto3
import shelve
import random

session = boto3.Session(profile_name='root')
mturk = session.client('mturk', 'us-east-1')

print('Balance', mturk.get_account_balance()['AvailableBalance'])


def test_for_copypaste(txt):
    for substr_len in [10]:
        for _ in range(15):
            r = random.random()
            r = int(r * (len(txt) - substr_len))
            substr_val = txt[r:r+substr_len]
            if txt.count(substr_val) > 1:
                print('REPEATS:', txt.count(substr_val), substr_val)


def shelve_save(db, key, elem):
    a = db[key]
    if isinstance(a, set):
        a.add(elem)
    elif isinstance(a, list):
        a.append(elem)
    else:
        raise Exception(f'shelve_save(): {key=} unsupported {type(a)=}')
    db[key] = a


with shelve.open('state') as db:
    if 'HITId' not in db:
        print('run "start_hit" first')
        exit(1)
    if 'accepted' not in db:
        db['accepted'] = []
    if 'rejected' not in db:
        db['rejected'] = []
    if 'workers' not in db:
        db['workers'] = set()


with shelve.open('state') as db:
    hit_id = db['HITId']
    paginator = mturk.get_paginator('list_assignments_for_hit')  # ? list_reviewable_hits
    for response in paginator.paginate(HITId=hit_id, AssignmentStatuses=['Submitted']):
        for assignment in response['Assignments']:
            assignment_id = assignment['AssignmentId']
            worker_id = assignment['WorkerId']
            answer = assignment['Answer']
            answer = answer[answer.find('<FreeText>') + len('<FreeText>'):]
            answer = answer[:answer.find('</FreeText>')]
            requester_feedback = assignment.get('RequesterFeedback', None)
            print(f'ANSWER:\n{answer}')
            if requester_feedback:
                print(f'RequesterFeedback {requester_feedback}')
            # test
            if worker_id in db['workers']:
                print('\n\nWorker repeating!')
            test_for_copypaste(answer)
            # decide
            print('1. Approve / 2. Reject')
            user_answer = input()
            if user_answer == '1':
                mturk.approve_assignment(AssignmentId=assignment_id)
                mturk.create_worker_block(WorkerId=worker_id, Reason='temporary')
                shelve_save(db, 'accepted', assignment)
                shelve_save(db, 'workers', worker_id)
            elif user_answer == '2':
                print(f'{worker_id=} {assignment_id=} {answer=}')
                print('input rejection reason:')  #TODO selection + automation
                mturk.reject_assignment(AssignmentId=assignment_id, RequesterFeedback=input())
                mturk.create_worker_block(WorkerId=worker_id, Reason='bad_worker')
                shelve_save(db, 'rejected', assignment)
                shelve_save(db, 'workers', worker_id)
            else:
                print(f'Skipping assignment for now.')





