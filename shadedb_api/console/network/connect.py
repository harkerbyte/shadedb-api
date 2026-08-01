import json
import requests
from urllib.parse import urlparse

class ShadeDBCli:
    __slots__ = ("endpoint", "connection_token", "cluster_token", "database_id")
    
    def __init__(self, endpoint: str, connection_token: str, cluster_token: str = None):
        self.endpoint = endpoint
        self.connection_token = connection_token
        self.cluster_token = cluster_token
        
        # Robustly extract the last non-empty path component as database_id
        parsed_url = urlparse(endpoint)
        path_parts = [part for part in parsed_url.path.split("/") if part]
        self.database_id = path_parts[-1] if path_parts else ""
        
    def _get_auth_payload(self) -> dict:
        """Helper to generate base authentication payload."""
        return {
            "cntoken": self.connection_token, 
            "dbid": self.database_id, 
            "token": self.cluster_token
        }

    def _send_request(self, snl_command: str) -> dict | str:
        """Centralized HTTP POST handler with robust JSON and HTTP error parsing."""
        payload = {"SNL": snl_command}
        payload.update(self._get_auth_payload())
        
        try:
            response = requests.post(self.endpoint, json=payload, timeout=10)
            
            # Handle successful response
            if response.status_code == 200:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return response.text
            
            # Handle client/forbidden errors
            if response.status_code in (400, 403):
                try:
                    body = response.json()
                    return body.get("message", f"Status code [{response.status_code}]: message missing. ")
                except json.JSONDecodeError:
                  return f"\x1b[1;31m[server ~ console]: status code {response.status_code}\x1b[1;0m"
            
            return f"\x1b[1;31mUnexpected server error: {response.status_code}\x1b[1;0m"
            
        except requests.exceptions.RequestException as e:
            return f"\x1b[1;31m[Network Error]: {e}\x1b[1;0m"

    def remote_status_cli(self) -> str | dict:
        """Checks the remote connection status."""
        result = self._send_request(snl_command="")
        
        # If the server returned a valid dictionary and no error text string, it's active
        if isinstance(result, dict):
            return "\n\x1b[1;32m\nActive\n\x1b[1;0m\n        "
        return result
        
    def general_cli(self, command: str = None) -> dict | str:
        """Executes a basic general SNL command."""
        if not command:
            return "\x1b[1;31mNo command provided.\x1b[1;0m"
        return self._send_request(snl_command=command)
        
    def context_manage_cli(self, command: str = None, context: dict = None) -> dict | str:
        """Executes a command embedded with stringified dictionary contexts."""
        if not command or not context:
            return "\x1b[1;31mMissing command or context validation.\x1b[1;0m"
            
        if isinstance(context, dict):
            try:
                context_str = json.dumps(context)
            except (TypeError, ValueError) as e:
                raise ValueError(f"Context dict is not JSON serializable: {e}")
        else:
            context_str = str(context)
            
        formatted_command = f"{command};{context_str};"
        return self._send_request(snl_command=formatted_command)


if __name__ == "__main__":
    print("Oops, nah. Run this via your main console script.")
