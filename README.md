# ALEXAM Tech Studio

Aplicación inicial para obtener y preparar historias de Reddit.

## Instalación

Desde esta carpeta, ejecuta:

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` con las credenciales de una aplicación creada en <https://www.reddit.com/prefs/apps>.
No compartas ni subas `.env` a Git.

## Ejecutar

```powershell
python app.py
```

La interfaz permite seleccionar un subreddit, obtener la publicación popular y dividir el texto en partes de aproximadamente 20 minutos a 130 palabras por minuto.

## Próximas fases

- TTS y generación de subtítulos.
- Edición con MoviePy y FFmpeg.
- Cola y programación de tareas.
- Publicación en Facebook mediante permisos y tokens oficiales.
