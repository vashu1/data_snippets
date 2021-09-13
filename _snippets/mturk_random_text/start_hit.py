"""
If a HIT is created with 10 or more maximum assignments, there is an additional fee.
For more information, see Amazon Mechanical Turk Pricing.

Mechanical Turk Fee
20% fee on the reward and bonus amount (if any) you pay Workers.
Tasks with 10 or more assignments will be charged an additional 20% fee on the reward you pay Workers.
The minimum fee is $0.01 per assignment or bonus payment.
"""
import boto3
import shelve

REWARD = '0.03'  # The US Dollar amount
TITLE = 'Print random text for at least 3 minutes.'
DESCRIPTION = '''Print random text for at least 3 minutes and at least 600 characters.

Must contain numbers, special characters (like "!@#$%^*()"), uppercase and lowercase letters.

Use minimal effort to mix types of characters - typing numbers for a minute, then uppercase for a minute, etc. is not acceptable.

Copy-pasting output of random text generator is not acceptable.

Only one assignment per worker will be accepted.'''

QUESTION = f"""<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">
    <Overview>
        <Title>{TITLE}</Title>
        <Text>
          {DESCRIPTION}
          
          EXAMPLE: LKAFmnwiohjT#U3098oejzh_oijJILjw4tr_iy576wuiKLM ...
        </Text>
    </Overview>
    <Question>
        <QuestionIdentifier>random_text</QuestionIdentifier>
        <DisplayName>Random text.</DisplayName>
        <IsRequired>true</IsRequired>
        <QuestionContent>
          <Text>
            Type it here:
          </Text>
        </QuestionContent>
        <AnswerSpecification>
            <FreeTextAnswer>
              <Constraints>
                <Length minLength="600"/>
              </Constraints>
              <NumberOfLinesSuggestion>10</NumberOfLinesSuggestion>
            </FreeTextAnswer>
        </AnswerSpecification>
    </Question>
</QuestionForm>"""

session = boto3.Session(profile_name='root')
mturk = session.client('mturk', 'us-east-1')

print('Balance', mturk.get_account_balance()['AvailableBalance'])

with shelve.open('state') as db:
    if 'HITId' in db:
        print(f'Clean "state" by hand before starting another HIT.')
        exit(1)

MINUTE = 60  # seconds
response = mturk.create_hit(
    MaxAssignments=1,  # The number of times the HIT can be accepted and completed before the HIT becomes unavailable.
    AutoApprovalDelayInSeconds=30*MINUTE,
    LifetimeInSeconds=15*MINUTE,
    AssignmentDurationInSeconds=6*MINUTE,
    Reward=REWARD,
    Title=TITLE,
    Keywords='short,easy,fast approve',
    Description=DESCRIPTION,
    Question=QUESTION,
)

print(response)
with shelve.open('state') as db:
    db['HITId'] = response['HIT']['HITId']