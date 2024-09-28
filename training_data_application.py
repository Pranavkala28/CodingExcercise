#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
from datetime import datetime, timedelta

with open('trainings (correct).txt', 'r') as f:
    data = json.load(f)


def count_completed_trainings(data):
    training_counts = {}
    for person in data:
        for completion in person.get('completions', []):
            training = completion['name']
            training_counts[training] = training_counts.get(training, 0) + 1
    return training_counts


def list_people_completed_trainings(data, trainings, fiscal_year):
    fiscal_start = datetime(fiscal_year - 1, 7, 1)
    fiscal_end = datetime(fiscal_year, 6, 30)
    result = {training: [] for training in trainings}

    for person in data:
        for completion in person.get('completions', []):
            training_name = completion['name']
            if training_name in trainings:
                completion_date = datetime.strptime(completion['timestamp'], '%m/%d/%Y')
                if fiscal_start <= completion_date <= fiscal_end:
                    result[training_name].append(person['name'])

    return result

def find_expired_or_expiring_trainings(data, reference_date_str):
    reference_date = datetime.strptime(reference_date_str, '%m/%d/%Y')
    soon_expiry_threshold = reference_date + timedelta(days=30)
    result = []

    for person in data:
        person_result = {'name': person['name'], 'trainings': []}
        for completion in person.get('completions', []):
            expiry_str = completion.get('expires')
            if expiry_str:
                expiry_date = datetime.strptime(expiry_str, '%m/%d/%Y')
                if expiry_date < reference_date:
                    person_result['trainings'].append({
                        'name': completion['name'],
                        'status': 'expired'
                    })
                elif reference_date <= expiry_date <= soon_expiry_threshold:
                    person_result['trainings'].append({
                        'name': completion['name'],
                        'status': 'expires soon'
                    })
        if person_result['trainings']:
            result.append(person_result)

    return result


trainings_to_check = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
fiscal_year = 2024
reference_date = "10/1/2023"

print("Task 1: Completed Trainings Count")
print(json.dumps(count_completed_trainings(data), indent=2))

print("\nTask 2: People who completed specific trainings in FY 2024")
print(json.dumps(list_people_completed_trainings(data, trainings_to_check, fiscal_year), indent=2))

print("\nTask 3: People with expired or soon-to-expire trainings (reference date: Oct 1, 2023)")
print(json.dumps(find_expired_or_expiring_trainings(data, reference_date), indent=2))


# In[ ]:




