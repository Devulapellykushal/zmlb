
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import base64
from io import BytesIO
import os

from hybrid_insight_engine import generate_combined_insights
from trends import plot_health_trends

app = Flask(__name__)
CORS(app, resources={r"/upload-csv/*": {"origins": [
    "https://devulapellykushalhie.vercel.app/"  
]}}) 

@app.route('/upload-csv/', methods=['POST'])
def upload_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Read CSV into DataFrame
        df = pd.read_csv(file)
        print("✅ CSV successfully loaded.")
        print("📊 Data preview:\n", df.head())

        # Generate insights
        insights = generate_combined_insights(df)
        print("✅ Insights generated.")

        # Generate trend plot and convert to base64
        fig = plot_health_trends(df)

        print("trends completed  : **** " , fig)
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()

        return jsonify({
            "insights": insights,
            "trend_image": img_str
        })

    except Exception as e:
        print("❌ Error during processing:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)















# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd
# from hybrid_insight_engine import generate_combined_insights
# from trends import plot_health_trends
# import base64
# from io import BytesIO

# app = FastAPI()

# # 🌐 Allow requests from *any* origin (not recommended for production unless necessary)
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # ✅ CORS setup so frontend can access backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         # "https://cursor-nxh6cv6tb-devulapellykushals-projects.vercel.app/",
#         # "http://localhost:3000"  # 🟢 Replace this with your actual frontend URL
#         "*"
#     ],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )




# @app.post("/upload-csv/")
# async def upload_csv(file: UploadFile = File(...)):
#     try:
#         # Load CSV
#         df = pd.read_csv(file.file)
#         print("✅ CSV successfully loaded.")
#         print("📊 Data preview:\n", df.head())

#         # Generate insights
#         insights = generate_combined_insights(df)
#         print("✅ Insights generated.")

#         # Generate plot and convert to base64
#         fig = plot_health_trends(df)
#         buf = BytesIO()
#         fig.savefig(buf, format="png")
#         img_str = base64.b64encode(buf.getvalue()).decode()

#         return {
#             "insights": insights,
#             "trend_image": img_str
#         }
#     except Exception as e:
#         print("❌ Error during processing:", str(e))
#         return {"error": str(e)}
