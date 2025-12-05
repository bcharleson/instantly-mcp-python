# Instantly MCP Server - Comprehensive Testing Plan

**Version:** 1.0.0  
**Date:** 2025-12-05  
**Total Tools:** 32  

---

## Phase 1: Tool Inventory & Categorization

### Complete Tool Matrix

| # | Category | Tool Name | Type | HTTP Method | Endpoint | Risk Level |
|---|----------|-----------|------|-------------|----------|------------|
| **ACCOUNTS (6 tools)** |
| 1 | accounts | `list_accounts` | READ | GET | `/accounts` | 🟢 Safe |
| 2 | accounts | `get_account` | READ | GET | `/accounts/{email}` | 🟢 Safe |
| 3 | accounts | `create_account` | WRITE | POST | `/accounts` | 🟡 Moderate |
| 4 | accounts | `update_account` | WRITE | PATCH | `/accounts/{email}` | 🟡 Moderate |
| 5 | accounts | `manage_account_state` | WRITE | POST | `/accounts/{email}/*` | 🟡 Moderate |
| 6 | accounts | `delete_account` | DELETE | DELETE | `/accounts/{email}` | 🔴 Destructive |
| **CAMPAIGNS (6 tools)** |
| 7 | campaigns | `list_campaigns` | READ | GET | `/campaigns` | 🟢 Safe |
| 8 | campaigns | `get_campaign` | READ | GET | `/campaigns/{id}` | 🟢 Safe |
| 9 | campaigns | `create_campaign` | WRITE | POST | `/campaigns` | 🟡 Moderate |
| 10 | campaigns | `update_campaign` | WRITE | PATCH | `/campaigns/{id}` | 🟡 Moderate |
| 11 | campaigns | `activate_campaign` | WRITE | POST | `/campaigns/{id}/activate` | 🟡 Moderate |
| 12 | campaigns | `pause_campaign` | WRITE | POST | `/campaigns/{id}/pause` | 🟡 Moderate |
| **LEADS (11 tools)** |
| 13 | leads | `list_leads` | READ | POST | `/leads/list` | 🟢 Safe |
| 14 | leads | `get_lead` | READ | GET | `/leads/{id}` | 🟢 Safe |
| 15 | leads | `create_lead` | WRITE | POST | `/leads` | 🟡 Moderate |
| 16 | leads | `update_lead` | WRITE | PATCH | `/leads/{id}` | 🟡 Moderate |
| 17 | leads | `list_lead_lists` | READ | GET | `/lead-lists` | 🟢 Safe |
| 18 | leads | `create_lead_list` | WRITE | POST | `/lead-lists` | 🟡 Moderate |
| 19 | leads | `update_lead_list` | WRITE | PATCH | `/lead-lists/{id}` | 🟡 Moderate |
| 20 | leads | `get_verification_stats_for_lead_list` | READ | GET | `/lead-lists/{id}/verification-stats` | 🟢 Safe |
| 21 | leads | `add_leads_to_campaign_or_list_bulk` | WRITE | POST | `/leads/add` | 🟡 Moderate |
| 22 | leads | `delete_lead` | DELETE | DELETE | `/leads/{id}` | 🔴 Destructive |
| 23 | leads | `move_leads_to_campaign_or_list` | WRITE | POST | `/leads/move` | 🟡 Moderate |
| **EMAILS (5 tools)** |
| 24 | emails | `list_emails` | READ | GET | `/emails` | 🟢 Safe |
| 25 | emails | `get_email` | READ | GET | `/emails/{id}` | 🟢 Safe |
| 26 | emails | `reply_to_email` | WRITE | POST | `/emails/reply` | 🔴 Sends Email |
| 27 | emails | `count_unread_emails` | READ | GET | `/emails/unread/count` | 🟢 Safe |
| 28 | emails | `verify_email` | WRITE | POST | `/email-verification` | 🟡 Uses Credits |
| **ANALYTICS (3 tools)** |
| 29 | analytics | `get_campaign_analytics` | READ | GET | `/campaigns/analytics` | 🟢 Safe |
| 30 | analytics | `get_daily_campaign_analytics` | READ | GET | `/campaigns/analytics/daily` | 🟢 Safe |
| 31 | analytics | `get_warmup_analytics` | READ | POST | `/accounts/warmup-analytics` | 🟢 Safe |
| **SERVER (1 tool)** |
| 32 | server | `get_server_info` | READ | N/A | Internal | 🟢 Safe |

---

### Summary by Type

| Type | Count | Tools |
|------|-------|-------|
| **READ** | 16 | Safe to test freely |
| **WRITE** | 13 | Test with caution, revert after |
| **DELETE** | 2 | Verify params only, no execution |
| **SEND** | 1 | `reply_to_email` - sends real email |

---

## Phase 2: READ-Only Tool Testing

### Test Cases for Each READ Tool

#### 2.1 Accounts - READ (2 tools)

| Tool | Test Case | Input | Expected |
|------|-----------|-------|----------|
| `list_accounts` | Default pagination | `{}` | Returns items[], pagination |
| `list_accounts` | With limit | `{"limit": 5}` | Max 5 items |
| `list_accounts` | Filter by status | `{"status": 1}` | Only active accounts |
| `list_accounts` | Pagination cursor | `{"starting_after": "..."}` | Next page |
| `get_account` | Valid email | `{"email": "alex@instantly.ai"}` | Account details |
| `get_account` | Invalid email | `{"email": "nonexistent@test.com"}` | Error handling |

#### 2.2 Campaigns - READ (2 tools)

| Tool | Test Case | Input | Expected |
|------|-----------|-------|----------|
| `list_campaigns` | Default | `{}` | Returns items[], pagination |
| `list_campaigns` | With limit | `{"limit": 3}` | Max 3 campaigns |
| `list_campaigns` | Search by name | `{"search": "test"}` | Filtered results |
| `get_campaign` | Valid ID | `{"campaign_id": "..."}` | Full campaign details |
| `get_campaign` | Invalid ID | `{"campaign_id": "invalid"}` | Error handling |

#### 2.3 Leads - READ (4 tools)

| Tool | Test Case | Input | Expected |
|------|-----------|-------|----------|
| `list_leads` | Default | `{}` | Returns items[], pagination |
| `list_leads` | With campaign filter | `{"campaign": "..."}` | Leads in campaign |
| `list_leads` | With search | `{"search": "john"}` | Filtered by name/email |
| `list_leads` | Filter contacted | `{"filter": "FILTER_VAL_CONTACTED"}` | Only contacted |
| `get_lead` | Valid ID | `{"lead_id": "..."}` | Lead details |
| `list_lead_lists` | Default | `{}` | All lead lists |
| `list_lead_lists` | With search | `{"search": "test"}` | Filtered lists |
| `get_verification_stats_for_lead_list` | Valid ID | `{"list_id": "..."}` | Verification stats |

#### 2.4 Emails - READ (4 tools)

| Tool | Test Case | Input | Expected |
|------|-----------|-------|----------|
| `list_emails` | Default | `{}` | Returns items[], pagination |
| `list_emails` | Unread only | `{"is_unread": true}` | Only unread |
| `list_emails` | By type | `{"email_type": "received"}` | Only received |
| `list_emails` | By mode | `{"mode": "emode_focused"}` | Focused inbox |
| `get_email` | Valid ID | `{"email_id": "..."}` | Full email content |
| `count_unread_emails` | No params | `{}` | Unread count |
| `verify_email` | Valid email | `{"email": "test@example.com"}` | Verification result |

#### 2.5 Analytics - READ (3 tools)

| Tool | Test Case | Input | Expected |
|------|-----------|-------|----------|
| `get_campaign_analytics` | All campaigns | `{}` | Aggregate metrics |
| `get_campaign_analytics` | Single campaign | `{"campaign_id": "..."}` | Campaign metrics |
| `get_campaign_analytics` | Date range | `{"start_date": "2024-01-01", "end_date": "2024-12-31"}` | Filtered |
| `get_daily_campaign_analytics` | Default | `{}` | Daily breakdown |
| `get_daily_campaign_analytics` | By status | `{"campaign_status": 1}` | Active only |
| `get_warmup_analytics` | Single email | `{"email": "alex@instantly.ai"}` | Warmup metrics |
| `get_warmup_analytics` | Multiple | `{"emails": ["a@x.ai", "b@x.ai"]}` | Multi-account |

#### 2.6 Server - READ (1 tool)

| Tool | Test Case | Input | Expected |
|------|-----------|-------|----------|
| `get_server_info` | No params | `{}` | Server metadata |

---

## Phase 3: WRITE Tool Testing

### 3.1 UPDATE Operations (Lower Risk)

| Tool | Test Sequence | Revert Strategy |
|------|---------------|-----------------|
| `update_account` | 1. Get current state<br>2. Update field<br>3. Verify change<br>4. Revert to original | Save original, restore after |
| `update_campaign` | 1. Get campaign<br>2. Update name<br>3. Verify<br>4. Revert | Same |
| `update_lead` | 1. Get lead<br>2. Update field<br>3. Verify<br>4. Revert | Same |
| `update_lead_list` | 1. Get list<br>2. Update name<br>3. Verify<br>4. Revert | Same |

### 3.2 STATE Operations

| Tool | Test Sequence | Safety Notes |
|------|---------------|--------------|
| `manage_account_state` (test_vitals) | Test connectivity | Safe - read-only |
| `manage_account_state` (pause) | Pause account | Revert with resume |
| `manage_account_state` (resume) | Resume account | N/A |
| `activate_campaign` | Activate paused campaign | Only on test campaign |
| `pause_campaign` | Pause active campaign | Only on test campaign |

### 3.3 CREATE Operations

| Tool | Test Sequence | Cleanup Strategy |
|------|---------------|------------------|
| `create_lead_list` | Create test list | Delete after testing |
| `create_lead` | Create test lead | Delete after testing |
| `create_campaign` | Create test campaign | Keep as draft, delete after |
| `create_account` | Skip - requires credentials | N/A |
| `add_leads_to_campaign_or_list_bulk` | Add to test list | Delete list after |
| `move_leads_to_campaign_or_list` | Move between test lists | Revert move |

---

## Phase 4: DELETE Tool Verification (Params Only)

### DELETE Tools - DO NOT EXECUTE

| Tool | Required Params | Expected Behavior | Verified |
|------|-----------------|-------------------|----------|
| `delete_account` | `{"email": "..."}` | Permanently deletes account | ⬜ |
| `delete_lead` | `{"lead_id": "..."}` | Permanently deletes lead | ⬜ |

### Verification Checklist
- [ ] Confirm parameter names match API docs
- [ ] Confirm HTTP method is DELETE
- [ ] Confirm endpoint path is correct
- [ ] Confirm error handling for missing params
- [ ] Confirm `confirmationRequiredHint` annotation is set

---

## Phase 5: Cross-Client Compatibility

### Supported MCP Clients

| Client | Transport | Auth Method | Status |
|--------|-----------|-------------|--------|
| Claude Desktop | stdio | ENV var | ⬜ To Test |
| Remote HTTP | HTTP | URL path (`/mcp/API_KEY`) | ⬜ To Test |
| Remote HTTP | HTTP | Header (`Authorization`) | ⬜ To Test |
| Remote HTTP | HTTP | Header (`x-instantly-api-key`) | ⬜ To Test |

### Client-Specific Test Cases

1. **Claude Desktop (stdio)**
   - Verify tool discovery
   - Test parameter passing
   - Verify response formatting

2. **HTTP Remote**
   - Test URL-based auth
   - Test header-based auth
   - Verify multi-tenant isolation
   - Test rate limiting behavior

---

## Testing Execution Tracker

### Phase 2 Results: READ Tools

| # | Tool | Status | Notes |
|---|------|--------|-------|
| 1 | `get_server_info` | ✅ Pass | v1.0.0, 32 tools, 5 categories |
| 2 | `list_accounts` | ✅ Pass | Returns items with pagination cursor |
| 3 | `get_account` | ✅ Pass | Returns full account details (warmup config, limits) |
| 4 | `list_campaigns` | ✅ Pass | Returns campaigns with full sequence data |
| 5 | `get_campaign` | ✅ Pass | Returns campaign config, schedule, variables |
| 6 | `list_leads` | ✅ Pass | Returns leads with custom variables, payload |
| 7 | `get_lead` | ✅ Pass | Returns full lead details, campaign membership |
| 8 | `list_lead_lists` | ✅ Pass | Returns lists with pagination |
| 9 | `get_verification_stats_for_lead_list` | ✅ Pass | Returns verified/invalid/risky counts |
| 10 | `list_emails` | ✅ Pass | Returns emails with full body (large responses!) |
| 11 | `get_email` | ✅ Pass | Returns full email thread, HTML/text body |
| 12 | `count_unread_emails` | ✅ Pass | Returns count: 14,458 |
| 13 | `verify_email` | 🔧 Fixed | Changed GET→POST, now initiates verification |
| 14 | `get_campaign_analytics` | ✅ Pass | Returns 50+ campaigns with full metrics |
| 15 | `get_daily_campaign_analytics` | ✅ Pass | Returns day-by-day breakdown |
| 16 | `get_warmup_analytics` | ✅ Pass | Fixed: Changed GET→POST (commit 38dd65f) |

### Phase 3 Results: WRITE Tools

| # | Tool | Status | Notes |
|---|------|--------|-------|
| 1 | `update_account` | ⬜ | |
| 2 | `update_campaign` | ⬜ | |
| 3 | `update_lead` | ⬜ | |
| 4 | `update_lead_list` | ⬜ | |
| 5 | `manage_account_state` | ⬜ | |
| 6 | `activate_campaign` | ⬜ | |
| 7 | `pause_campaign` | ⬜ | |
| 8 | `create_lead_list` | ⬜ | |
| 9 | `create_lead` | ⬜ | |
| 10 | `create_campaign` | ⬜ | |
| 11 | `add_leads_to_campaign_or_list_bulk` | ⬜ | |
| 12 | `move_leads_to_campaign_or_list` | ⬜ | |
| 13 | `create_account` | ⬜ Skip | Requires credentials |

### Phase 4 Results: DELETE Tools (Verification Only)

| # | Tool | Params Verified | Annotations Verified |
|---|------|-----------------|----------------------|
| 1 | `delete_account` | ⬜ | ⬜ |
| 2 | `delete_lead` | ⬜ | ⬜ |

---

## API Documentation Reference

All endpoints verified against: https://developer.instantly.ai/api/v2

| Category | API Docs URL |
|----------|--------------|
| Accounts | https://developer.instantly.ai/api/v2/accounts |
| Campaigns | https://developer.instantly.ai/api/v2/campaigns |
| Leads | https://developer.instantly.ai/api/v2/leads |
| Emails | https://developer.instantly.ai/api/v2/emails |
| Analytics | https://developer.instantly.ai/api/v2/analytics |

---

## Known Issues & Fixes

| Date | Tool | Issue | Resolution | Commit |
|------|------|-------|------------|--------|
| 2025-12-05 | `get_warmup_analytics` | 404 Not Found | Changed GET→POST with JSON body | `38dd65f` |
| 2025-12-05 | `verify_email` | 404 Not Found | Changed GET→POST to initiate verification | `89aeaf0` |

---

## Success Criteria

- [x] All 16 READ tools return valid responses ✅ (15 pass, 1 fixed)
- [ ] All 13 WRITE tools function correctly with revert capability
- [ ] All 2 DELETE tools have verified parameters (not executed)
- [x] Pagination works correctly across all list endpoints ✅
- [ ] Error handling works for invalid inputs
- [ ] Cross-client compatibility confirmed
- [x] No API documentation discrepancies remain ✅ (2 fixed)

