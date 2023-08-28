import cohere
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="The prompt to send to the API")
#parser.add_argument("file_name", help="Name of the file to save Python script")
args = parser.parse_args()

co = cohere.Client('Zmz7oSN242GFTiGisumtHI1YJue4RpbiJMgyXc4T')

response = co.generate(
    prompt = f"Write python script to {args.prompt}. Provide only code, no text",
)

print (response)
