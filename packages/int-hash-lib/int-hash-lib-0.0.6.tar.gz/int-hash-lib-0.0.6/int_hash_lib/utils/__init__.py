from .default import collect_hash_aggregates
from .email import collects_email_aggregates
from .ip_address import collect_ip_address_aggregates
from .phone import collect_phone_aggregates
from .user_agent import collect_user_agent_aggregates


class HashFunctions:
    COLLECT_HASH_AGGREGATES = 'collect_hash_aggregates'
    COLLECTS_EMAIL_AGGREGATES = 'collects_email_aggregates'
    COLLECT_IP_ADDRESS_AGGREGATES = 'collect_ip_address_aggregates'
    COLLECT_PHONE_AGGREGATES = 'collect_phone_aggregates'
    COLLECT_USER_AGENT_AGGREGATES = 'collect_user_agent_aggregates'
