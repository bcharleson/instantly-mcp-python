"""
Instantly MCP Server - Campaign Tools

6 tools for email campaign management operations.
"""

import json
from typing import Any

from ..client import get_client
from ..models.campaigns import (
    CreateCampaignInput,
    ListCampaignsInput,
    GetCampaignInput,
    UpdateCampaignInput,
    ActivateCampaignInput,
    PauseCampaignInput,
    DEFAULT_TIMEZONE,
)


async def create_campaign(params: CreateCampaignInput) -> str:
    """
    Create email campaign. Two-step process:
    
    Step 1: Call with name/subject/body to discover available sender accounts
    Step 2: Call again with email_list to assign senders
    
    Personalization variables:
    - {{firstName}}, {{lastName}}, {{companyName}}
    - {{email}}, {{website}}, {{phone}}
    - Any custom variables defined for leads
    
    Use sequence_steps for multi-step follow-up sequences.
    """
    client = get_client()
    
    # Build campaign body
    body: dict[str, Any] = {
        "name": params.name,
    }
    
    # Build sequences array with the email content
    sequences = []
    num_steps = params.sequence_steps or 1
    
    for i in range(num_steps):
        step: dict[str, Any] = {}
        
        # Subject - use custom or base
        if params.sequence_subjects and i < len(params.sequence_subjects):
            step["subject"] = params.sequence_subjects[i]
        elif i == 0:
            step["subject"] = params.subject
        else:
            step["subject"] = f"Re: {params.subject}"
        
        # Body - use custom or base
        if params.sequence_bodies and i < len(params.sequence_bodies):
            step["body"] = params.sequence_bodies[i]
        else:
            step["body"] = params.body
        
        # Delay for follow-up steps
        if i > 0:
            step["delay"] = (params.step_delay_days or 3) * 24 * 60  # Convert days to minutes
        
        sequences.append(step)
    
    body["sequences"] = sequences
    
    # Add optional settings
    if params.email_list:
        body["email_list"] = params.email_list
    
    if params.track_opens is not None:
        body["open_tracking"] = params.track_opens
    if params.track_clicks is not None:
        body["link_tracking"] = params.track_clicks
    
    # Schedule settings
    body["campaign_schedule"] = {
        "schedules": [{
            "timezone": params.timezone or DEFAULT_TIMEZONE,
            "timing": {
                "from": params.timing_from or "09:00",
                "to": params.timing_to or "17:00",
            },
            "days": {
                "sun": False,
                "mon": True,
                "tue": True,
                "wed": True,
                "thu": True,
                "fri": True,
                "sat": False,
            }
        }]
    }
    
    if params.daily_limit:
        body["daily_limit"] = params.daily_limit
    if params.email_gap:
        body["email_gap"] = params.email_gap
    if params.stop_on_reply is not None:
        body["stop_on_reply"] = params.stop_on_reply
    if params.stop_on_auto_reply is not None:
        body["stop_on_auto_reply"] = params.stop_on_auto_reply
    
    result = await client.post("/campaigns", json=body)
    
    # Add helpful guidance if no email_list was provided
    if not params.email_list:
        result["_guidance"] = (
            "Campaign created! Next step: Call create_campaign again with the same "
            "parameters plus email_list containing sender account emails from your "
            "available accounts (use list_accounts to see eligible accounts)."
        )
    
    return json.dumps(result, indent=2)


async def list_campaigns(params: ListCampaignsInput) -> str:
    """
    List campaigns with pagination. Filter by name search or tags.
    
    Note: search filters by campaign NAME only, not by status.
    To filter by status, use campaign_status in get_daily_campaign_analytics.
    
    Returns campaign list with status, lead counts, and performance metrics.
    """
    client = get_client()
    
    query_params = {}
    if params.limit:
        query_params["limit"] = params.limit
    if params.starting_after:
        query_params["starting_after"] = params.starting_after
    if params.search:
        query_params["search"] = params.search
    if params.tag_ids:
        query_params["tag_ids"] = params.tag_ids
    
    result = await client.get("/campaigns", params=query_params)
    return json.dumps(result, indent=2)


async def get_campaign(params: GetCampaignInput) -> str:
    """
    Get campaign details: config, sequences, schedules, sender accounts, tracking, status.
    
    Returns comprehensive campaign information including:
    - Email sequences and their content
    - Schedule configuration
    - Sender account assignments
    - Tracking settings (opens, clicks)
    - Campaign status and statistics
    """
    client = get_client()
    result = await client.get(f"/campaigns/{params.campaign_id}")
    return json.dumps(result, indent=2)


async def update_campaign(params: UpdateCampaignInput) -> str:
    """
    Update campaign settings (partial update).
    
    Common updates:
    - name: Campaign display name
    - sequences: Email sequence steps
    - email_list: Sender account assignments
    - daily_limit: Max emails per day per account
    - email_gap: Minutes between sends
    - open_tracking, link_tracking: Tracking toggles
    
    Only include fields you want to update.
    """
    client = get_client()
    
    body = {}
    
    # Add all optional fields if provided
    if params.name is not None:
        body["name"] = params.name
    if params.pl_value is not None:
        body["pl_value"] = params.pl_value
    if params.is_evergreen is not None:
        body["is_evergreen"] = params.is_evergreen
    if params.campaign_schedule is not None:
        body["campaign_schedule"] = params.campaign_schedule
    if params.sequences is not None:
        body["sequences"] = params.sequences
    if params.email_gap is not None:
        body["email_gap"] = params.email_gap
    if params.random_wait_max is not None:
        body["random_wait_max"] = params.random_wait_max
    if params.text_only is not None:
        body["text_only"] = params.text_only
    if params.email_list is not None:
        body["email_list"] = params.email_list
    if params.daily_limit is not None:
        body["daily_limit"] = params.daily_limit
    if params.stop_on_reply is not None:
        body["stop_on_reply"] = params.stop_on_reply
    if params.email_tag_list is not None:
        body["email_tag_list"] = params.email_tag_list
    if params.link_tracking is not None:
        body["link_tracking"] = params.link_tracking
    if params.open_tracking is not None:
        body["open_tracking"] = params.open_tracking
    if params.stop_on_auto_reply is not None:
        body["stop_on_auto_reply"] = params.stop_on_auto_reply
    if params.daily_max_leads is not None:
        body["daily_max_leads"] = params.daily_max_leads
    if params.prioritize_new_leads is not None:
        body["prioritize_new_leads"] = params.prioritize_new_leads
    if params.auto_variant_select is not None:
        body["auto_variant_select"] = params.auto_variant_select
    if params.match_lead_esp is not None:
        body["match_lead_esp"] = params.match_lead_esp
    if params.stop_for_company is not None:
        body["stop_for_company"] = params.stop_for_company
    if params.insert_unsubscribe_header is not None:
        body["insert_unsubscribe_header"] = params.insert_unsubscribe_header
    if params.allow_risky_contacts is not None:
        body["allow_risky_contacts"] = params.allow_risky_contacts
    if params.disable_bounce_protect is not None:
        body["disable_bounce_protect"] = params.disable_bounce_protect
    if params.cc_list is not None:
        body["cc_list"] = params.cc_list
    if params.bcc_list is not None:
        body["bcc_list"] = params.bcc_list
    
    result = await client.patch(f"/campaigns/{params.campaign_id}", json=body)
    return json.dumps(result, indent=2)


async def activate_campaign(params: ActivateCampaignInput) -> str:
    """
    Activate campaign to start sending.
    
    Prerequisites (all required):
    1. At least one sender account assigned (email_list)
    2. At least one lead added to the campaign
    3. Email sequences configured
    4. Schedule configured
    
    Use get_campaign to verify all prerequisites are met.
    """
    client = get_client()
    result = await client.post(f"/campaigns/{params.campaign_id}/activate")
    return json.dumps(result, indent=2)


async def pause_campaign(params: PauseCampaignInput) -> str:
    """
    Pause campaign to stop sending.
    
    Effects:
    - Immediately stops all email sending
    - Leads remain in the campaign
    - In-progress sequences are paused
    
    Use activate_campaign to resume sending.
    """
    client = get_client()
    result = await client.post(f"/campaigns/{params.campaign_id}/pause")
    return json.dumps(result, indent=2)


# Export all campaign tools
CAMPAIGN_TOOLS = [
    create_campaign,
    list_campaigns,
    get_campaign,
    update_campaign,
    activate_campaign,
    pause_campaign,
]

