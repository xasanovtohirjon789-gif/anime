from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from utils import LoggerUtils
from datetime import datetime, timedelta

class UserSessionMiddleware:
    def __init__(self):
        self.db = Database()
        self.sessions = {}
    
    async def track_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        if user:
            user_id = user.id
            
            self.db.add_user(
                user_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            
            self.sessions[user_id] = {
                'last_activity': datetime.now(),
                'message_count': self.sessions.get(user_id, {}).get('message_count', 0) + 1,
                'is_bot': user.is_bot
            }
            
            LoggerUtils.log_user_action(user_id, "Activity tracked")
    
    def get_user_session(self, user_id: int) -> dict:
        return self.sessions.get(user_id, {})
    
    def cleanup_old_sessions(self, hours: int = 24):
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        to_delete = []
        for user_id, session in self.sessions.items():
            if session['last_activity'] < cutoff_time:
                to_delete.append(user_id)
        
        for user_id in to_delete:
            del self.sessions[user_id]
        
        return len(to_delete)

class RateLimitMiddleware:
    def __init__(self, max_requests: int = 30, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}
    
    def is_rate_limited(self, user_id: int) -> bool:
        now = datetime.now()
        
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if (now - req_time).seconds < self.time_window
        ]
        
        if len(self.requests[user_id]) >= self.max_requests:
            return True
        
        self.requests[user_id].append(now)
        return False
    
    def get_remaining_requests(self, user_id: int) -> int:
        now = datetime.now()
        
        if user_id not in self.requests:
            return self.max_requests
        
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if (now - req_time).seconds < self.time_window
        ]
        
        return max(0, self.max_requests - len(self.requests[user_id]))

class ErrorHandlerMiddleware:
    def __init__(self):
        self.error_count = {}
        self.error_log = []
    
    def log_error(self, user_id: int, error_type: str, error_message: str):
        if user_id not in self.error_count:
            self.error_count[user_id] = 0
        
        self.error_count[user_id] += 1
        
        error_entry = {
            'user_id': user_id,
            'type': error_type,
            'message': error_message,
            'timestamp': datetime.now()
        }
        
        self.error_log.append(error_entry)
        
        if len(self.error_log) > 1000:
            self.error_log = self.error_log[-500:]
    
    def get_user_errors(self, user_id: int, minutes: int = 60) -> int:
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        recent_errors = [
            e for e in self.error_log
            if e['user_id'] == user_id and e['timestamp'] > cutoff_time
        ]
        
        return len(recent_errors)
    
    def get_error_summary(self) -> dict:
        return {
            'total_errors': len(self.error_log),
            'error_by_type': self._count_errors_by_type(),
            'most_affected_users': self._get_most_affected_users()
        }
    
    def _count_errors_by_type(self) -> dict:
        error_counts = {}
        for error in self.error_log:
            error_type = error['type']
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        return error_counts
    
    def _get_most_affected_users(self, limit: int = 10) -> list:
        user_errors = {}
        for error in self.error_log:
            user_id = error['user_id']
            user_errors[user_id] = user_errors.get(user_id, 0) + 1
        
        sorted_users = sorted(user_errors.items(), key=lambda x: x[1], reverse=True)
        return sorted_users[:limit]

class CommandValidationMiddleware:
    @staticmethod
    async def validate_command(update: Update, command: str) -> bool:
        if not update.message or not update.message.text:
            return False
        
        text = update.message.text.strip()
        
        if not text.startswith('/'):
            return False
        
        parts = text.split()
        if not parts or not parts[0].startswith(f'/{command}'):
            return False
        
        return True

class ContextPreservationMiddleware:
    def __init__(self):
        self.context_storage = {}
    
    def save_context(self, user_id: int, context_key: str, context_value: any):
        if user_id not in self.context_storage:
            self.context_storage[user_id] = {}
        
        self.context_storage[user_id][context_key] = {
            'value': context_value,
            'timestamp': datetime.now()
        }
    
    def get_context(self, user_id: int, context_key: str, max_age_minutes: int = 30) -> any:
        if user_id not in self.context_storage:
            return None
        
        if context_key not in self.context_storage[user_id]:
            return None
        
        stored = self.context_storage[user_id][context_key]
        
        if (datetime.now() - stored['timestamp']).seconds > max_age_minutes * 60:
            del self.context_storage[user_id][context_key]
            return None
        
        return stored['value']
    
    def clear_context(self, user_id: int, context_key: str = None):
        if user_id not in self.context_storage:
            return
        
        if context_key:
            if context_key in self.context_storage[user_id]:
                del self.context_storage[user_id][context_key]
        else:
            self.context_storage[user_id] = {}
    
    def cleanup_old_contexts(self, max_age_minutes: int = 120):
        cutoff_time = datetime.now() - timedelta(minutes=max_age_minutes)
        
        for user_id in list(self.context_storage.keys()):
            for key in list(self.context_storage[user_id].keys()):
                if self.context_storage[user_id][key]['timestamp'] < cutoff_time:
                    del self.context_storage[user_id][key]
            
            if not self.context_storage[user_id]:
                del self.context_storage[user_id]

session_middleware = UserSessionMiddleware()
rate_limit_middleware = RateLimitMiddleware()
error_handler_middleware = ErrorHandlerMiddleware()
context_preservation_middleware = ContextPreservationMiddleware()
