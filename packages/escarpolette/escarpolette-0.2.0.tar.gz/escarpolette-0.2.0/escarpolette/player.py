from enum import Enum
from subprocess import Popen
from typing import Dict, List, Optional
import json
import select
import socket

from flask import current_app, _app_ctx_stack, Flask


State = Enum("State", ("PLAYING", "PAUSED", "STOPPED"))


class PlayerCommandError(ValueError):
    pass


class Player:
    """
    Control mpv using IPC.

    This is a Flask extension.
    """

    _command_id = 0
    _state = State.STOPPED

    def __init__(self, app: Flask = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        self.app = app

        app.config.setdefault("MPV_IPC_SOCKET", "/tmp/mpv-socket")
        app.teardown_appcontext(self.teardown)

        @app.before_first_request
        def init_mpv() -> None:
            self.mpv = Popen(
                [
                    "mpv",
                    "--idle",
                    "--no-terminal",
                    f"--input-ipc-server={app.config['MPV_IPC_SOCKET']}",
                ]
            )

    def teardown(self, exception: Optional[Exception]) -> None:
        ctx = _app_ctx_stack.top

        if hasattr(ctx, "mpv_socket"):
            ctx.mpv_socket.close()

    def add_item(self, url: str) -> None:
        """Add a new item to the playlist.

        If the player was stopped, play the music.
        """
        if self._state == State.STOPPED:
            self._send_command("loadfile", url, "append-play")
            self._state = State.PLAYING
        else:
            self._send_command("loadfile", url, "append")

    def get_current_item_title(self) -> Optional[str]:
        """Get the current playing item's title."""
        response = self._send_command("get_property", "metadata")
        if response is not None:
            return response["data"]["title"]

        return None

    def get_state(self) -> State:
        return self._state

    def play(self) -> None:
        """Play the current playlist."""
        if self._state == State.PLAYING:
            return
        elif self._state == State.STOPPED:
            raise PlayerCommandError("The player is stopped. Add an item to play it.")
        else:
            self._send_command("cycle", "pause")

        self._state = State.PLAYING

    def pause(self) -> None:
        """Pause the current playlist."""
        if self._state == State.PAUSED:
            return
        elif self._state == State.STOPPED:
            raise PlayerCommandError("The player is stopped.")

        self._send_command("cycle", "pause")
        self._state = State.PAUSED

    @property
    def _connection(self) -> socket.socket:
        ctx = _app_ctx_stack.top
        if ctx is None:
            raise RuntimeError("No app context available")

        if not hasattr(ctx, "mpv_socket"):
            ctx.mpv_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            ctx.mpv_socket.connect(current_app.config["MPV_IPC_SOCKET"])

        return ctx.mpv_socket

    def _get_command_id(self) -> int:
        self._command_id += 1
        return self._command_id

    def _send_command(self, *command: str) -> Optional[Dict]:
        """Send a command to MPV and return the response."""
        command_id = self._get_command_id()
        msg = {"command": command, "request_id": command_id}
        self.app.logger.debug("Sending MPV commanv %s", msg)

        data = json.dumps(msg).encode("utf8") + b"\n"
        self._connection.sendall(data)

        return self._read_response(command_id)

    def _read_response(self, command_id: int) -> Optional[Dict]:
        data = b""
        while True:
            r, _, _ = select.select([self._connection], [], [], 1)
            if not r:
                # timeout
                return None

            data += self._connection.recv(1024)

            newline = data.find(b"\n")
            if newline == -1:
                next

            response = data[:newline]
            data = data[newline:]

            msg = json.loads(response.decode("utf8"))
            self.app.logger.debug("Received MPV response %s", msg)
            if msg.get("request_id", -1) == command_id:
                return msg
