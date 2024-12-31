class Validation(BaseModel):
    title: str
    type: str

class Property(BaseModel):
    validation: Validation

class FlagSchema(BaseModel):
    properties: Property
    required: List[str]
    title: str
    type: str

class Reference(BaseModel):
    field_reference: str = Field(..., alias='$ref')

class PropertyRoot(BaseModel):
    reference: Reference

class HierarchicalSchema(BaseModel):
    properties: PropertyRoot
    required: List[str]
    title: str
    type: str

class Detail(BaseModel):
    field_reference: str = Field(..., alias='$ref')

class PropertyDetail(BaseModel):
    validation: Validation
    detail: Detail

class ListSchema(BaseModel):
    properties: PropertyDetail
    required: List[str]
    title: str
    type: str

class EvaluationPathSchema(BaseModel):
    title: str
    type: str

class SchemaLocationSchema(BaseModel):
    format: str
    min_length: int = Field(..., alias='minLength')
    title: str
    type: str

class InstanceLocationSchema(BaseModel):
    title: str
    type: str

class AnyOfSchemaItem(BaseModel):
    field_reference: Optional[str] = Field(None, alias='$ref')
    type: Optional[str] = None

class DetailItem(BaseModel):
    any_of: List[AnyOfSchemaItem] = Field(..., alias='anyOf')
    default: None

class AnnotationItem(BaseModel):
    type: str

class Annotation(BaseModel):
    any_of: List[AnnotationItem] = Field(..., alias='anyOf')
    default: None
    title: str

class DroppedAnnotation(BaseModel):
    any_of: List[AnnotationItem] = Field(..., alias='anyOf')
    default: None
    title: str

class AdditionalProperty(BaseModel):
    type: str

class AnyOfAdditionalProperty(BaseModel):
    additional_property: Optional[AdditionalProperty] = Field(None, alias='additionalProperties')
    type: str

class ErrorSchema(BaseModel):
    any_of: List[AnyOfAdditionalProperty] = Field(..., alias='anyOf')
    default: None
    title: str

class PropertyDetailSchema(BaseModel):
    validation: Validation
    evaluation_path: EvaluationPathSchema = Field(..., alias='evaluationPath')
    schema_location: SchemaLocationSchema = Field(..., alias='schemaLocation')
    instance_location: InstanceLocationSchema = Field(..., alias='instanceLocation')
    detail_item: DetailItem
    annotation: Annotation
    dropped_annotation: DroppedAnnotation = Field(..., alias='droppedAnnotations')
    error: ErrorSchema

class OutputSchema(BaseModel):
    properties: PropertyDetailSchema
    required: List[str]
    title: str
    type: str

class ItemReference(BaseModel):
    field_reference: str = Field(..., alias='$ref')

class RootItem(BaseModel):
    items: ItemReference
    title: str
    type: str

class PropertyRootItem(BaseModel):
    root: RootItem

class OutputArraySchema(BaseModel):
    properties: PropertyRootItem
    required: List[str]
    title: str
    type: str

class FieldDefinitions(BaseModel):
    flag_schema: FlagSchema = Field(..., alias='Flag')
    hierarchical_schema: HierarchicalSchema = Field(..., alias='Hierarchical')
    list_schema: ListSchema = Field(..., alias='ListModel')
    output_schema: OutputSchema = Field(..., alias='OutputUnit')
    output_array_schema: OutputArraySchema = Field(..., alias='OutputUnitArray')

class AnyOfRootItem(BaseModel):
    field_reference: str = Field(..., alias='$ref')

class RootSchema(BaseModel):
    any_of: List[AnyOfRootItem] = Field(..., alias='anyOf')
    description: str
    title: str

class PropertyRootSchema(BaseModel):
    root: RootSchema

class ModelSchema(BaseModel):
    field_definitions: FieldDefinitions = Field(..., alias='$defs')
    properties: PropertyRootSchema
    required: List[str]
    title: str
    type: str
