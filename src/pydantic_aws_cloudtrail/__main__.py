import yaml
from datamodel_code_generator import DataModelType, InputFileType, generate
#from pydantic import BaseModel
import pydantic_aws_cloudtrail.aws.cloudtrail.events as model

def main():
#    print("hai")
    print_json_schema()

def print_json_schema():
    schema = model.Model.model_json_schema()
    print(yaml.dump(schema))
    result = generate(schema,
                  disable_timestamp=True,
                  enable_version_header = False,
                  input_file_type=InputFileType.Dict,
                  input_filename=None,
                  #output=output_file,
                  output_model_type=DataModelType.PydanticV2BaseModel,
                  snake_case_field=True
                  )
    print(result)



if __name__ == "__main__":
    print_json_schema()
    
