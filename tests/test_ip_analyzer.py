import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ip_analyzer import IPAnalyzerGUI
import pytest
from unittest.mock import patch, MagicMock
import tkinter as tk

import pytest
from unittest.mock import patch, MagicMock
from ip_analyzer import IPAnalyzerGUI
import tkinter as tk

from ip_analyzer import IPAnalyzerGUI


@pytest.fixture
def gui():
    """Create a hidden Tk instance for testing."""
    root = tk.Tk()
    root.withdraw()
    return IPAnalyzerGUI(root)


def test_get_ip_ipv4(gui):
    """Test IPv4 retrieval."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"ip": "123.123.123.123"}
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        result = gui.get_ip("ipv4")
        assert result == "123.123.123.123"


def test_get_ip_ipv6(gui):
    """Test IPv6 retrieval."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"ip": "2001:db8::1"}
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        result = gui.get_ip("ipv6")
        assert result.startswith("2001")


def test_get_ip_api_error(gui):
    """Test error handling."""
    with patch("requests.get", side_effect=Exception("API Down")):
        result = gui.get_ip("ipv4")
        assert "Error" in result


def test_get_ip_info_success(gui):
    """Test successful geolocation info retrieval."""
    mock_data = {
        "status": "success",
        "city": "Manila",
        "region": "NCR",
        "country": "Philippines",
        "timezone": "Asia/Manila"
    }

    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        result = gui.get_ip_info()

        assert result["city"] == "Manila"
        assert result["country"] == "Philippines"


def test_get_ip_info_failure(gui):
    """Test API failure response."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "fail", "message": "Invalid query"}
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        result = gui.get_ip_info()

        assert "error" in result
        assert result["error"] == "Invalid query"
