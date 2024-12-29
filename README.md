# pydantic-aws-cloudtrail
The low cost aws cloudtrail python api you were always wanted

# notes

## generate schema
`poetry run --verbose pydantic-aws-cloudtrail > json.schema`


## pct-fetch

```
poetry install
export AWS_PROFILE=myprofile
export AWS_DEFAULT_REGION=us-east-1
poetry run --verbose pct-fetch
```
