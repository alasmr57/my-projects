from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video(url):
    """
    تحميل الفيديو مع الصوت مدموجًا (YouTube / TikTok) وحفظه باسم مختلف
    """
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # اسم الملف = عنوان الفيديو
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)  # نجيب بيانات الفيديو
        filename = ydl.prepare_filename(info)        # الاسم النهائي للملف
        return filename

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/download", methods=["GET"])
def download():
    video_url = request.args.get("url")
    if not video_url:
        return jsonify({"success": False, "error": "يرجى إدخال رابط الفيديو"})

    try:
        local_file = download_video(video_url)
        filename = os.path.basename(local_file)
        return jsonify({
            "success": True,
            "url": f"/download_file/{filename}"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/download_file/<filename>")
def download_file(filename):
    path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "ملف الفيديو غير موجود", 404

if __name__ == "__main__":
    app.run(debug=True)
