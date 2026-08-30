"""Aplicación inicial de automatización de historias de Reddit."""

from __future__ import annotations

import os
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

import praw
from dotenv import load_dotenv
from prawcore.exceptions import ResponseException

load_dotenv()


@dataclass(frozen=True)
class RedditConfig:
    client_id: str
    client_secret: str
    user_agent: str

    @classmethod
    def from_environment(cls) -> "RedditConfig":
        client_id = os.getenv("REDDIT_CLIENT_ID", "").strip()
        client_secret = os.getenv("REDDIT_CLIENT_SECRET", "").strip()
        user_agent = os.getenv(
            "REDDIT_USER_AGENT", "AlexamTechStudio/1.0 by ALEXAMTechStudio"
        ).strip()

        if not client_id or not client_secret:
            raise ValueError(
                "Configura REDDIT_CLIENT_ID y REDDIT_CLIENT_SECRET en el archivo .env."
            )
        return cls(client_id, client_secret, user_agent)


def split_story(text: str, words_per_minute: int = 130, minutes_per_part: int = 20) -> list[str]:
    """Divide una historia en partes aproximadas según su duración narrada."""
    words = text.split()
    words_per_part = max(1, words_per_minute * minutes_per_part)
    return [
        " ".join(words[index : index + words_per_part])
        for index in range(0, len(words), words_per_part)
    ] or [""]


def fetch_story(subreddit_name: str) -> tuple[str, str, str]:
    config = RedditConfig.from_environment()
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
        check_for_async=False,
    )
    submission = next(reddit.subreddit(subreddit_name).hot(limit=1), None)
    if submission is None:
        raise RuntimeError("No se encontró ninguna publicación.")
    return submission.title, submission.selftext, submission.url


class StoryApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ALEXAM Tech Studio — Historias de Reddit")
        self.geometry("920x700")
        self.minsize(760, 560)
        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self, padding=18)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            container,
            text="Automatizador de historias",
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor=tk.W)
        ttk.Label(
            container,
            text="Paso 1: obtención y preparación de historias de Reddit",
        ).pack(anchor=tk.W, pady=(0, 14))

        controls = ttk.LabelFrame(container, text="Fuente", padding=10)
        controls.pack(fill=tk.X)
        ttk.Label(controls, text="Subreddit:").grid(row=0, column=0, sticky=tk.W)
        self.subreddit = ttk.Entry(controls, width=28)
        self.subreddit.insert(0, "desahogo")
        self.subreddit.grid(row=0, column=1, padx=(8, 16))
        ttk.Button(controls, text="Obtener historia", command=self._load_story).grid(
            row=0, column=2, padx=4
        )
        ttk.Button(controls, text="Dividir en partes", command=self._split_current).grid(
            row=0, column=3, padx=4
        )
        controls.columnconfigure(1, weight=1)

        self.status = ttk.Label(container, text="Listo")
        self.status.pack(anchor=tk.W, pady=(12, 6))
        self.output = ScrolledText(container, wrap=tk.WORD, height=24, font=("Consolas", 10))
        self.output.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            container,
            text="La publicación automática, TTS y edición de video se añadirán en módulos posteriores.",
            foreground="#666666",
        ).pack(anchor=tk.W, pady=(8, 0))

    def _load_story(self) -> None:
        subreddit = self.subreddit.get().strip()
        if not subreddit:
            messagebox.showwarning("Dato requerido", "Escribe un subreddit.")
            return
        self.status.configure(text="Consultando Reddit...")
        self.update_idletasks()
        try:
            title, story, url = fetch_story(subreddit)
        except ValueError as error:
            self.status.configure(text="Falta configuración")
            messagebox.showerror("Configuración requerida", str(error))
            return
        except ResponseException as error:
            self.status.configure(text="Error de autenticación")
            if error.response.status_code == 401:
                messagebox.showerror(
                    "Credenciales rechazadas",
                    "Reddit devolvió 401. Revisa el client ID y client secret del archivo .env.",
                )
            else:
                messagebox.showerror("Error de Reddit", str(error))
            return
        except Exception as error:
            self.status.configure(text="Error")
            messagebox.showerror("No se pudo obtener la historia", str(error))
            return

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"TÍTULO: {title}\n\n{story}\n\nFUENTE: {url}")
        self.status.configure(text="Historia obtenida correctamente")

    def _split_current(self) -> None:
        content = self.output.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Sin historia", "Obtén o pega una historia primero.")
            return
        parts = split_story(content)
        self.output.delete("1.0", tk.END)
        for index, part in enumerate(parts, start=1):
            self.output.insert(tk.END, f"PARTE {index}\n{'=' * 60}\n{part}\n\n")
        self.status.configure(text=f"Historia dividida en {len(parts)} parte(s)")


if __name__ == "__main__":
    StoryApp().mainloop()
