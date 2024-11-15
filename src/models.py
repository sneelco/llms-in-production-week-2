from guardrails.hub import ValidSQL, ValidPython
from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    """
    LLM Response that is validated using Guardrails.ai
    """

    generated_sql: str = Field(
        description="Generate PostgreSQL for the given natural language instruction.",
        validators=[
            ValidSQL(on_fail="reask"),
        ],
    )


class LLMResponseDynamoDB(BaseModel):
    """
    LLM Response that is validated using Guardrails.ai
    """

    generated_query: str = Field(
        description="Generate DynamoDB for the given natural language instruction.",
        validators=[
            ValidPython(on_fail="reask"),
        ],
    )
