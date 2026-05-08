"""
Authentication and user-related Pydantic schemas.
"""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class UserRegisterRequest(BaseModel):
    """Registration request payload."""
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number")
    age: int = Field(..., ge=8, le=25, description="Age (8-25)")
    address: str | None = Field(None, max_length=500, description="Address")
    password: str = Field(..., min_length=6, max_length=128, description="Password")
    preferred_language: str = Field("en", description="Preferred language code")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = v.strip().replace(" ", "").replace("-", "")
        if not cleaned.replace("+", "").isdigit():
            raise ValueError("Phone number must contain only digits and optional + prefix")
        return cleaned

    @field_validator("preferred_language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        valid_languages = {"en", "hi", "mr", "bn", "ta", "te", "kn", "gu"}
        if v not in valid_languages:
            raise ValueError(f"Language must be one of: {', '.join(sorted(valid_languages))}")
        return v


class UserLoginRequest(BaseModel):
    """Login request payload."""
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """JWT token pair response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""
    refresh_token: str


class UserProfileResponse(BaseModel):
    """User profile response (excludes sensitive fields)."""
    id: str
    name: str
    phone: str
    age: int
    address: str | None
    role: str
    preferred_language: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    """Profile update request — all fields optional."""
    name: str | None = Field(None, min_length=2, max_length=100)
    age: int | None = Field(None, ge=8, le=25)
    address: str | None = Field(None, max_length=500)
    preferred_language: str | None = None

    @field_validator("preferred_language")
    @classmethod
    def validate_language(cls, v: str | None) -> str | None:
        if v is None:
            return v
        valid_languages = {"en", "hi", "mr", "bn", "ta", "te", "kn", "gu"}
        if v not in valid_languages:
            raise ValueError(f"Language must be one of: {', '.join(sorted(valid_languages))}")
        return v
