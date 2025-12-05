"""
Instantly MCP Server - Email Tools

5 tools for email management operations.
"""

import json
from typing import Any, Optional
from urllib.parse import quote

from ..client import get_client
from ..models.emails import (
    ListEmailsInput,
    GetEmailInput,
    ReplyToEmailInput,
    VerifyEmailInput,
)


async def list_emails(params: Optional[ListEmailsInput] = None) -> str:
    """
    List emails with pagination. Filter by campaign, account, type, or status.
    
    Search tips:
    - Use "thread:UUID" to find all emails in a thread
    - Filter by email_type: received, sent, manual
    
    Modes:
    - emode_focused: Primary inbox
    - emode_others: Other/filtered emails
    - emode_all: All emails
    """
    client = get_client()
    
    # Handle case where params is None (for OpenAI/non-Claude clients)
    if params is None:
        params = ListEmailsInput()
    
    query_params: dict[str, Any] = {}
    
    if params.limit:
        query_params["limit"] = params.limit
    if params.starting_after:
        query_params["starting_after"] = params.starting_after
    if params.search:
        query_params["search"] = params.search
    if params.campaign_id:
        query_params["campaign_id"] = params.campaign_id
    if params.i_status is not None:
        query_params["i_status"] = params.i_status
    if params.eaccount:
        query_params["eaccount"] = params.eaccount
    if params.is_unread is not None:
        query_params["is_unread"] = params.is_unread
    if params.has_reminder is not None:
        query_params["has_reminder"] = params.has_reminder
    if params.mode:
        query_params["mode"] = params.mode
    if params.preview_only is not None:
        query_params["preview_only"] = params.preview_only
    if params.sort_order:
        query_params["sort_order"] = params.sort_order
    if params.scheduled_only is not None:
        query_params["scheduled_only"] = params.scheduled_only
    if params.assigned_to:
        query_params["assigned_to"] = params.assigned_to
    if params.lead:
        query_params["lead"] = params.lead
    if params.company_domain:
        query_params["company_domain"] = params.company_domain
    if params.marked_as_done is not None:
        query_params["marked_as_done"] = params.marked_as_done
    if params.email_type:
        query_params["email_type"] = params.email_type
    
    result = await client.get("/emails", params=query_params)
    return json.dumps(result, indent=2)


async def get_email(params: GetEmailInput) -> str:
    """
    Get email details by ID.
    
    Returns:
    - Full email content (subject, body, attachments)
    - Thread information
    - Sender and recipient details
    - Tracking data (opens, clicks)
    - Associated lead and campaign
    """
    client = get_client()
    result = await client.get(f"/emails/{params.email_id}")
    return json.dumps(result, indent=2)


async def reply_to_email(params: ReplyToEmailInput) -> str:
    """
    🚨 SENDS REAL EMAIL! Confirm with user first. Cannot undo!
    
    Sends a reply to an existing email thread.
    
    Requirements:
    - reply_to_uuid: The email UUID to reply to
    - eaccount: Must be an active sender account
    - body: HTML or plain text content
    
    The reply will be sent immediately and appear in the lead's inbox.
    """
    client = get_client()
    
    body: dict[str, Any] = {
        "reply_to_uuid": params.reply_to_uuid,
        "eaccount": params.eaccount,
        "subject": params.subject,
        "body": params.body.model_dump(exclude_none=True),
    }
    
    result = await client.post("/emails/reply", json=body)
    return json.dumps(result, indent=2)


async def count_unread_emails() -> str:
    """
    Count unread emails in inbox.
    
    Returns the total number of unread emails across all accounts.
    Useful for inbox zero tracking and notification badges.
    """
    client = get_client()
    result = await client.get("/emails/unread/count")
    return json.dumps(result, indent=2)


async def verify_email(params: VerifyEmailInput) -> str:
    """
    Verify email deliverability (takes 5-45 seconds).
    
    Returns:
    - status: valid, invalid, risky, unknown
    - score: Deliverability score (0-100)
    - flags: Specific issues detected
    
    Common flags:
    - disposable: Temporary email address
    - role_based: Generic address (info@, support@)
    - catch_all: Domain accepts all addresses
    - smtp_error: Mail server issues
    """
    client = get_client()
    email_encoded = quote(params.email, safe="")
    result = await client.get(f"/email-verification/{email_encoded}")
    return json.dumps(result, indent=2)


# Export all email tools
EMAIL_TOOLS = [
    list_emails,
    get_email,
    reply_to_email,
    count_unread_emails,
    verify_email,
]

