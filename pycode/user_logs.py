from datetime import datetime
from pymongo import MongoClient


class UserActivityLogger:
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client['mht']
        self.logs = self.db.logs

    def log_login_activity(self, session_id, user, ip_address, device):
        self.logs.update_one(
            {'session_id': session_id},
            {'$set': {
                'user': user,
                'device': device,
                'ip_address': ip_address,
                'timestamp_login': datetime.utcnow()
            }},
            upsert=True
        )

    def log_logout_activity(self, session_id):
        log_entry = self.logs.find_one({'session_id': session_id})

        if log_entry and 'timestamp_login' in log_entry:
            timestamp_logout = datetime.utcnow()
            duration = timestamp_logout - log_entry['timestamp_login']

            self.logs.update_one(
                {'session_id': session_id},
                {'$set': {
                    'timestamp_logout': timestamp_logout,
                    'duration': duration.total_seconds()  # Dauer in Sekunden
                }}
            )
