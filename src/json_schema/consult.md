### Documentation for Using the `consult.py` Script

The `consult.py` script processes JSON Schema and generates preludes, then executes another process on the generated output files. Below is a step-by-step guide on how to use this script:

#### Prerequisites

Ensure you have the following installed:
- Python 3.x
- Required Python libraries (`argparse`, `yaml`, `datamodel_code_generator`, `networkx`, `jinja2`, `subprocess`)

#### Running the Script

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/meta-introspector/pydantic-aws-cloudtrail.git
   cd pydantic-aws-cloudtrail
   ```

2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Prepare Templates**:
   - Create entry and prelude template files if they don't exist.

4. **Execute the Script**:
   Use the following command to run the script. Replace the placeholders with actual paths to your templates and the script to execute.

   ```sh
   poetry run jss-consult \
       --output_path output/ \
       --framework Pydantic \
       --goal "Meta-model of JSON Schema" \
       --entry_template_paths path/to/entry_template1 path/to/entry_template2 \
       --prelude_template_paths path/to/prelude_template1 path/to/prelude_template2 \
       --script_name output/process.sh
   ```

#### Script Parameters

- `--output_path`: Directory where the output files will be saved.
- `--framework`: Framework being used (e.g., Pydantic).
- `--goal`: Purpose or goal of the project.
- `--entry_template_paths`: Paths to the entry template files.
- `--prelude_template_paths`: Paths to the prelude template files.
- `--script_name`: Name of the script to execute on the output files.

#### Understanding the Output

- The script generates multiple output files in the specified `output_path` directory.
- Each output file corresponds to different combinations of prelude and schema entry preludes applied to the cluster nodes.
- The script executes another process on each output file and collects the output, error, and return code from the subprocess.



### Conclusion

By following this documentation, you can effectively use the `consult.py` script to process JSON Schema, generate preludes, and execute additional scripts on the generated output files.
