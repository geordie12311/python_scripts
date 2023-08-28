import openai
import json

openai.api_key = "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"

# Set up the prompt
prompt = ("""
            Generate a Cisco switch configuration file for a Cisco {model} switch with the following parameters:
            - {interfaces}
            - {vlan_id}
            - {routing_protocol}
            - {ip_address}
          """)

# Set the parameters for the configuration file
model = "Catalyst 2960X-48FPD-L"
interfaces = "GigabitEthernet1/0/1-24"
vlan_id = "10,20,30"
routing_protocol = "OSPF"
ip_address = "192.168.1.1"

api_endpoint = "https://api.openai.com/v1/completions"
api_key = "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"

request_headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key
}

completion = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt.format(model=model, interfaces=interfaces, vlan_id=vlan_id, routing_protocol=routing_protocol, ip_address=ip_address),
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7
)

# Retrieve the generated configuration file
output = completion.choices[0].text

# Save the configuration file to a text file
with open("switch_config.txt", "w") as f:
    f.write(output)
    
# Print the generated configuration file
print(output)