"""
Pydantic models for Email operations.
"""

from typing import Any, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


class ListEmailsInput(BaseModel):
    """Input for listing emails with pagination and filtering."""
    
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    
    limit: Optional[int] = Field(default=None, ge=1, le=100, description="1-100, default: 100")
    starting_after: Optional[str] = Field(default=None, description="Cursor from pagination")
    search: Optional[str] = Field(
        default=None,
        description="Search (use 'thread:UUID' for threads)"
    )
    campaign_id: Optional[str] = Field(default=None)
    i_status: Optional[int] = Field(default=None, description="Interest status")
    eaccount: Optional[str] = Field(
        default=None,
        description="Sender accounts (comma-separated)"
    )
    is_unread: Optional[bool] = Field(default=None)
    has_reminder: Optional[bool] = Field(default=None)
    mode: Optional[Literal["emode_focused", "emode_others", "emode_all"]] = Field(default=None)
    preview_only: Optional[bool] = Field(default=None)
    sort_order: Optional[Literal["asc", "desc"]] = Field(default=None)
    scheduled_only: Optional[bool] = Field(default=None)
    assigned_to: Optional[str] = Field(default=None)
    lead: Optional[str] = Field(default=None, description="Lead email")
    company_domain: Optional[str] = Field(default=None)
    marked_as_done: Optional[bool] = Field(default=None)
    email_type: Optional[Literal["received", "sent", "manual"]] = Field(default=None)


class GetEmailInput(BaseModel):
    """Input for getting email details."""
    
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    
    email_id: str = Field(..., description="Email UUID")


class EmailBody(BaseModel):
    """Email body content."""
    
    model_config = ConfigDict(extra="forbid")
    
    html: Optional[str] = Field(default=None, description="HTML content")
    text: Optional[str] = Field(default=None, description="Plain text content")


class ReplyToEmailInput(BaseModel):
    """
    Input for replying to an email.
    
    🚨 SENDS REAL EMAIL! Confirm with user first. Cannot undo!
    """
    
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    
    reply_to_uuid: str = Field(..., description="Email UUID to reply to")
    eaccount: str = Field(..., description="Sender account (must be active)")
    subject: str = Field(..., description="Subject line")
    body: EmailBody = Field(..., description="Email body (html or text)")


class VerifyEmailInput(BaseModel):
    """
    Input for verifying email deliverability.
    
    Takes 5-45 seconds. Returns status, score, flags.
    """
    
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    
    email: str = Field(..., description="Email to verify")

