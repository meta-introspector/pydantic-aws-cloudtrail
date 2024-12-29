import yaml
from pydantic import BaseModel
import pydantic_aws_cloudtrail.aws.cloudtrail.events

def main():
#    print("hai")
    print_json_schema()

def print_json_schema():
    print(yaml.dump(pydantic_aws_cloudtrail.aws.cloudtrail.events.Model.model_json_schema()))


if __name__ == "__main__":
    print_json_schema()
    
