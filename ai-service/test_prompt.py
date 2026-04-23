# Read prompt file
with open("prompts/describe_prompt.txt", "r") as file:
    prompt = file.read()

# Create 5 sample test inputs
test_inputs = [
    {
        "recordType": "Employee Data",
        "retentionPeriod": "5 years",
        "riskLevel": "High"
    },
    {
        "recordType": "Financial Records",
        "retentionPeriod": "7 years",
        "riskLevel": "Medium"
    },
    {
        "recordType": "Customer Data",
        "retentionPeriod": "3 years",
        "riskLevel": "High"
    },
    {
        "recordType": "Legal Documents",
        "retentionPeriod": "10 years",
        "riskLevel": "Low"
    },
    {
        "recordType": "Medical Records",
        "retentionPeriod": "8 years",
        "riskLevel": "High"
    }
]

# Loop through each input and print the full prompt
for item in test_inputs:

    print("\n-----------------------------")

    print(prompt)

    print(f"Record Type: {item['recordType']}")
    print(f"Retention Period: {item['retentionPeriod']}")
    print(f"Risk Level: {item['riskLevel']}")
