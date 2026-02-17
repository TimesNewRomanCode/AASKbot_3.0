from app.common.db.core_model import CoreModel
from .user import User
from .group import Group
from .sender_logs import SenderLogs
from .address import Address
from .college import College

__all__ = ["CoreModel", "User", "Group", "SenderLogs", "Address", "College"]
