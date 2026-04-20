import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

import threading
from flask import Flask, request, Response, render_template, abort
from pyrogram import Client
from config import *
from database import get_file
from utils import verify_hash
from bson.objectid import ObjectId

app = Flask(__name__)

# ✅ START BOT IN BACKGROUND (NO WORKER NEEDED)
def run_bot():
    from bot import bot
    bot.run()

threading.Thread(target=run_bot).start()


@app.route("/")
def home():
    return "✅ Streaming Server Running"


@app.route("/watch/<id>")
def watch(id):
    h = request.args.get("hash")
    if not verify_hash(id, h):
        return "Invalid link ❌"

    return render_template("player.html", id=id, hash=h)


@app.route("/download/<id>")
def download(id):
    h = request.args.get("hash")
    if not verify_hash(id, h):
        abort(403)

    file = get_file(ObjectId(id))
    if not file:
        return "File not found"

    return Response(
        stream_generator(file["file_id"]),
        headers={
            "Content-Disposition": f'attachment; filename="{file["name"]}"'
        }
    )


@app.route("/stream/<id>")
def stream(id):
    h = request.args.get("hash")
    if not verify_hash(id, h):
        abort(403)

    file = get_file(ObjectId(id))
    if not file:
        return "File not found"

    file_id = file["file_id"]
    file_size = file["size"]
    mime = file["mime"]

    range_header = request.headers.get("Range", None)

    start = 0
    end = file_size - 1

    if range_header:
        parts = range_header.replace("bytes=", "").split("-")
        start = int(parts[0])
        if parts[1]:
            end = int(parts[1])

    chunk_size = end - start + 1

    async def generate():
        async for chunk in bot.stream_media(
            file_id,
            offset=start,
            limit=chunk_size
        ):
            yield chunk

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    response = Response(
        loop.run_until_complete(generate()),
        status=206 if range_header else 200,
        content_type=mime
    )

    response.headers.add("Content-Range", f"bytes {start}-{end}/{file_size}")
    response.headers.add("Accept-Ranges", "bytes")
    response.headers.add("Content-Length", str(chunk_size))
    response.headers.add("Cache-Control", "public, max-age=3600")

    return response


def stream_generator(file_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def gen():
        async for chunk in bot.stream_media(file_id):
            yield chunk

    return loop.run_until_complete(gen())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
