from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    input: str = Field(min_length=1, max_length=4000)


class FeedbackRequest(BaseModel):
    run_id: str = Field(min_length=1, max_length=80)
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="", max_length=2000)


class ApprovalRequest(BaseModel):
    approved: bool
    reviewer: str = Field(min_length=2, max_length=100)
