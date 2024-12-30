import yaml
#from pydantic import BaseModel
import json_schema.model as model
from datamodel_code_generator import DataModelType, InputFileType, generate

def main():
#    print("hai")
    print_json_schema()

def print_json_schema():
    schema = model.Model.model_json_schema()
    
    result = generate(schema,
                  disable_timestamp=True,
                  enable_version_header = False,
                  input_file_type=InputFileType.Dict,
                  input_filename=None,
                  #output=output_file,
                  output_model_type=DataModelType.PydanticV2BaseModel,
                  snake_case_field=True
                  )
    print(yaml.dump(schema))
    print(result)
    


if __name__ == "__main__":
    print_json_schema()
    
