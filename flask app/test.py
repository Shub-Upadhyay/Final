import json

data = "{\n  \"letter_date\": \"04/18/2017\",\n  \"days_to_respond\": \"60\",\n  \"sender\": \"Blue Cross Blue Shield of Michigan\",\n  \"recipient\": \"MCLAREN BAY REGIONAL\",\n  \"letter_subject\": \"Notice of Review Findings\",\n  \"contact_info\": \"HMS Provider Service Representative at (866) 875-1749\",\n  \"recipient_address\": \"1900 COLUMBUS AVE BAY CITY, MI 48708\",\n  \"insurance_provider\": \"Blue Cross Blue Shield of Michigan\"\n}"

# Parse the JSON data from the string
parsed_data = json.loads(data)

# Create lists of keys and values
keys_list = list(parsed_data.keys())
values_list = list(parsed_data.values())

# Print the lists
print("Keys:", keys_list)
print("Values:", values_list)



# Create a dictionary using keys and values lists
data_dict = dict(zip(keys_list, values_list))

# Print the dictionary
print(data_dict)

file_path = 'webroot\\json\\output_data.json'

# Write the dictionary to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(data_dict, json_file)

print("Data written to JSON file.")