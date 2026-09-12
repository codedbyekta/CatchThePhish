"""Pydantic models for request validation and response shaping."""

from pydantic import BaseModel, Field, field_validator


class EmailInput(BaseModel):
    """
    Required inputs match the dataset's actual columns used for
    training: subject and body. Nothing else is required by the model.
    """

    subject: str = Field(
        default="",
        max_length=2000,
        description="Email subject line. Optional — may be empty.",
    )
    body: str = Field(
        ...,
        min_length=1,
        max_length=20000,
        description="Email body text. Required.",
    )

    @field_validator("body")
    @classmethod
    def body_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("body must not be blank")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "subject": "Urgent: Verify your account immediately",
                "body": "Dear customer, click the link below immediately to verify your account or it will be suspended.",
            }
        }


class PredictionResponse(BaseModel):
    label: str
    is_phishing: bool
    phishing_probability: float
    legitimate_probability: float


class HealthResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    status: str
    model_loaded: bool
