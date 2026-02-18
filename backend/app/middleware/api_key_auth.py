# Authorization: Bearer sk_live_xxxxxx
'''receive token
→ decode
→ check exp
→ extract user_id
→ fetch user from DB
→ attach user to request
'''
