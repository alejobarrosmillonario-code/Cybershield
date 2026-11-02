#!/usr/bin/env python3
"""
Modulo de autenticacion con Google para CyberShield IA v3.
Implementa OAuth 2.0 para aplicaciones de escritorio.
"""

import os
import json
import webbrowser
import threading
import http.server
import urllib.parse
import urllib.request
from datetime import datetime

CONFIG_PATH = os.path.join("cybershield_datos", "google_config.json")
TOKEN_PATH = os.path.join("cybershield_datos", "google_token.json")

SCOPES = "openid email profile"
CALLBACK_PORT = 8765
REDIRECT_URI = "http://localhost:" + str(CALLBACK_PORT)


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(client_id, client_secret=""):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    config = {"client_id": client_id, "client_secret": client_secret}
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def load_token():
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_token(token_data):
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    token_data["saved_at"] = datetime.now().isoformat()
    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=2)


def clear_token():
    if os.path.exists(TOKEN_PATH):
        os.remove(TOKEN_PATH)


class GoogleAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    auth_code = None
    error = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            GoogleAuthCallbackHandler.auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body style='font-family:Arial;text-align:center;padding:50px;'><h2 style='color:#00AA00;'>Autenticacion exitosa</h2><p>Puedes cerrar esta ventana.</p></body></html>")
        elif "error" in params:
            GoogleAuthCallbackHandler.error = params["error"][0]
            self.send_response(400)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body style='font-family:Arial;text-align:center;padding:50px;'><h2 style='color:#FF3333;'>Error de autenticacion</h2></body></html>")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


class GoogleAuthService:
    def __init__(self):
        self.config = load_config()
        self.token = load_token()
        self.user_info = None
        if self.token:
            self._fetch_user_info()

    @property
    def is_configured(self):
        return bool(self.config.get("client_id"))

    @property
    def is_logged_in(self):
        return self.token is not None and self.user_info is not None

    def configure(self, client_id, client_secret=""):
        self.config = {"client_id": client_id, "client_secret": client_secret}
        save_config(client_id, client_secret)

    def login(self, callback=None):
        if not self.is_configured:
            if callback:
                callback(False, "No configurado. Necesitas un Client ID de Google Cloud Console.")
            return

        def _do_login():
            try:
                GoogleAuthCallbackHandler.auth_code = None
                GoogleAuthCallbackHandler.error = None

                auth_params = {
                    "client_id": self.config["client_id"],
                    "redirect_uri": REDIRECT_URI,
                    "response_type": "code",
                    "scope": SCOPES,
                    "access_type": "offline",
                    "prompt": "consent",
                }
                auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(auth_params)

                server = http.server.HTTPServer(("localhost", CALLBACK_PORT), GoogleAuthCallbackHandler)
                server.timeout = 120

                webbrowser.open(auth_url)
                server.handle_request()
                server.server_close()

                if GoogleAuthCallbackHandler.error:
                    raise Exception("Error de Google: " + str(GoogleAuthCallbackHandler.error))

                code = GoogleAuthCallbackHandler.auth_code
                if not code:
                    raise Exception("No se recibio codigo de autorizacion")

                token_data = self._exchange_code(code)
                self.token = token_data
                save_token(token_data)
                self._fetch_user_info()

                if callback:
                    callback(True, self.user_info)

            except Exception as e:
                if callback:
                    callback(False, str(e))

        thread = threading.Thread(target=_do_login, daemon=True)
        thread.start()

    def _exchange_code(self, code):
        data = {
            "code": code,
            "client_id": self.config["client_id"],
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        if self.config.get("client_secret"):
            data["client_secret"] = self.config["client_secret"]

        req = urllib.request.Request(
            "https://oauth2.googleapis.com/token",
            data=urllib.parse.urlencode(data).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())

    def _fetch_user_info(self):
        if not self.token or "access_token" not in self.token:
            self.user_info = None
            return
        try:
            req = urllib.request.Request(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": "Bearer " + self.token["access_token"]}
            )
            with urllib.request.urlopen(req) as resp:
                self.user_info = json.loads(resp.read().decode())
        except Exception:
            self.user_info = None
            self.token = None
            clear_token()

    def logout(self):
        self.token = None
        self.user_info = None
        clear_token()

    def get_user_display(self):
        if self.is_logged_in:
            name = self.user_info.get("name", "Usuario")
            email = self.user_info.get("email", "")
            return name + " (" + email + ")"
        return "No conectado"


_google_auth_service = None

def get_google_auth_service():
    global _google_auth_service
    if _google_auth_service is None:
        _google_auth_service = GoogleAuthService()
    return _google_auth_service
