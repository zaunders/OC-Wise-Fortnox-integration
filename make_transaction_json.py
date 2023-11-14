import json
import os

def makeJson(transferId, created, value, AccountSlug, Description, LegacyId, Tags, invoiceFiles, Items):
    relative_path=os.getenv("relative_path")

    transaction_json = {
        "transferId": transferId,
        "createDate": created,
        "value": value,
        "AccountSlug": AccountSlug,
        "Description": Description,
        "LegacyId": LegacyId,
        "Tags": Tags,
        "invoiceFiles": invoiceFiles,
        "Items": Items   
    }
    
    # Specify the name of the file you want to write to
    filename = f'{relative_path}json_files/{transferId}.json'

    # Write the JSON object to a file
    with open(filename, 'w') as file:
        json.dump(transaction_json, file, indent=4)

    return filename


#json_file = makeJson(807463894, "2023-09-18 08:46:50", 18861.0, "org-overhead-costs", "Talk AWS server costs", 161710, "", "", "https://opencollective-production.s3.us-west-1.amazonaws.com/expense-item/57c27b74-b83d-4e2f-b748-3927b7c61e0e/summary.pdf")
#print(json_file)