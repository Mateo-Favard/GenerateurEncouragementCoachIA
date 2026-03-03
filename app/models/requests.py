from pydantic import BaseModel, Field


class CoachingRequest(BaseModel):
    exercises: list[str] = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Liste des exercices a realiser",
        examples=[["20 jumping jacks", "15 squats", "30s gainage"]],
    )
    theme: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Theme du coaching (pirate, chevalier, etc.)",
        examples=["pirate"],
    )
    duration_hint: str = Field(
        default="1 minute 30",
        max_length=30,
        description="Indication de duree souhaitee",
    )
