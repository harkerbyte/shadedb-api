import json
import requests
from urllib.parse import urlparse
from shadedb_api.frame.excepts import (
    URLEndpointMissingError, 
    SNLMissingError, 
    SNLContextMissingError,
    ConnectionTokenMissingError, 
    DBUniqueIdentityError, 
    ClusterTokenMissingError
)


class SyncFrame:
    def __init__(
        self, 
        endpoint: str = None, 
        connection_token: str | int = None, 
        inspection: bool = False, 
        database_id: str = None, 
        cluster_token: str = None, 
        query_timeout: float = 0.5
    ):
        # 1. Enforce validation before manipulation
        if not endpoint:
            raise URLEndpointMissingError("SyncFrame")
        if not connection_token:
            raise ConnectionTokenMissingError("SyncFrame")
        if not cluster_token:
            raise ClusterTokenMissingError("SyncFrame")

        self.endpoint = endpoint
        self.connection_token = connection_token
        self.cluster_token = cluster_token
        self.inspection = inspection
        self.query_timeout = query_timeout

        parsed_url = urlparse(endpoint)
        path_parts = [part for part in parsed_url.path.split("/") if part]
        self.database_id = database_id or (path_parts[-1] if path_parts else None)
        
        if not self.database_id:
            raise DBUniqueIdentityError("SyncFrame")
        
    def _authenticator(self) -> dict:
        """Generates the routing and authentication metadata."""
        return {
            "cntoken": self.connection_token, 
            "dbid": self.database_id,
            "token": self.cluster_token
        }
        
    def _snl_process(self, body: dict) -> dict:
        """Transforms the server payload into an inspected summary framework."""
        return {
            "db_latency": body.get("took", ""),
            "message": body.get("message", "Message missing"),
            "status": body.get("status", "")
        }

    @staticmethod
    def _serialize_context(context: dict) -> str:
        """Safely serializes context blocks to a stringified payload structure."""
        try:
            return json.dumps(context)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Provided context dictionary is not JSON serializable: {e}")

    def _execute_request(self, command: str) -> str | dict | int:
        """Centralized HTTP processing cluster with comprehensive error handling."""
        payload = {"SNL": command}
        payload.update(self._authenticator())
        
        try:
            response = requests.post(self.endpoint, json=payload, timeout=self.query_timeout)
            
            # Fast parsing for structured JSON outcomes
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = None

            if response.status_code == 200:
                if response_data is None:
                    return response.text
                return self._snl_process(response_data) if self.inspection else response_data.get("message", "Message missing")
            
            if response.status_code in (400, 403):
                if response_data:
                    return response_data.get("message", f"Error message omitted by host. Status: {response.status_code}")
                return response.status_code

            return f"Unhandled server status code: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Network layer timeout or disconnect: {str(e)}"

    def snl_query(self, command: str = None) -> str | dict | int:
        """Executes an SNL query string."""
        if not command:
            raise SNLMissingError(self.snl_query.__name__)
        return self._execute_request(command)
        
    def snl_complex_query(self, command: str = None, context: dict = None) -> str | dict | int:
        """Appends contextual dictionaries safely to SNL query strings before pipeline delivery."""
        if not command:
            raise SNLMissingError(self.snl_complex_query.__name__)
        if not context:
            raise SNLContextMissingError(self.snl_complex_query.__name__)
            
        serialized_ctx = self._serialize_context(context)
        
        cleaned_cmd = command.strip()
        if cleaned_cmd.endswith(";"):
            formatted_command = f"{cleaned_cmd[:-1]};{serialized_ctx};"
        else:
            formatted_command = f"{cleaned_cmd};{serialized_ctx};"
            
        return self._execute_request(formatted_command)


if __name__ == "__main__":
    pass
