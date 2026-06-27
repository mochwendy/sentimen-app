#!/usr/bin/env python3
"""
Thiqla Live Agent - Final Master Production (Cloud & Local Hybrid)
Author: Pak Wendy & AI Collaborator
Year: 2026
Description: Live camera stream combined with LangGraph orchestration 
             and real-time Sharia Guardrail (Face Blur) Monitor.
"""

import cv2
import sys
import time
import argparse
import os
from typing import TypedDict
from langgraph.graph import StateGraph, END

# =====================================================================
# 1. LANGGRAPH ENGINE CONFIGURATION
# =====================================================================
class LivestreamState(TypedDict):
    face_detected: bool
    duration_violating: float
    system_alert: str

def supervisor_node(state: LivestreamState):
    face_present = state.get("face_detected", False)
    current_duration = state.get("duration_violating", 0.0)
    
    alert = "✅ STATUS: PRIVACY CLEAN"
    if face_present:
        if current_duration >= 3.0:
            alert = f"🚨 CRITICAL: FACE DETECTED TOO LONG ({current_duration:.1f}s)"
        else:
            alert = f"⚠️ WARNING: SHARIA GUARDRAIL ACTIVE ({current_duration:.1f}s)"
            
    return {"system_alert": alert}

def compile_agent():
    workflow = StateGraph(LivestreamState)
    workflow.add_node("supervisor", supervisor_node)
    workflow.set_entry_point("supervisor")
    workflow.add_edge("supervisor", END)
    return workflow.compile()

# =====================================================================
# 2. MAIN CORE EXECUTION
# =====================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="0", help="0 untuk Kamera bawaan, atau path_video.mp4")
    args, _ = parser.parse_known_args()
    
    # Deteksi jika berjalan di Google Colab
    IS_COLAB = 'COLAB_GPU' in os.environ or 'GGL_colab_device' in os.environ
    
    # Jika di Colab dan inputnya default "0", paksa cari file video tes karena Colab tidak punya webcam fisik
    if IS_COLAB and args.source == "0":
        src = "video_lokal_tes.mp4"
        print(f"☁️ Mendeteksi Lingkungan Google Colab. Mengalihkan source kamera ke file video: '{src}'")
    else:
        src = int(args.source) if args.source.isdigit() else args.source
    
    print(f"🔄 Menyalakan Thiqla Live Engine pada Source: {src} ...")
    cap = cv2.VideoCapture(src)
    
    if not cap.isOpened():
        print(f"❌ Gagal mengakses Source ({src})! Pastikan file tersedia atau kamera tidak terkunci.")
        sys.exit()
        
    print("🚀 Thiqla AI Agent Active & Terhubung ke Data Stream!")
    
    # Setup Video Writer otomatis jika di Cloud/Colab untuk menyimpan hasil rekaman
    out = None
    if IS_COLAB:
        fps = cap.get(cv2.CAP_PROP_FPS) or 24
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 360
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output_production.mp4', fourcc, fps, (width, height))
        print("📁 Mode Produksi Cloud: Output akan disimpan ke 'output_production.mp4'")
    else:
        print("💡 TEKAN TOMBOL 'q' PADA KEYBOARD UNTUK MENUTUP APLIKASI LOKAL.")
    
    # Inisialisasi Detektor Wajah & LangGraph Agent
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    agent = compile_agent()
    
    # Variabel Tracking Waktu untuk LangGraph State
    face_detected_status = False
    start_detection_time = None
    duration_violating = 0.0
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("🎬 Selesai memproses seluruh frame/stream data.")
            break
            
        # Normalisasi Resolusi Layar
        frame = cv2.resize(frame, (640, 360))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Jalankan Deteksi Wajah OpenCV
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(50, 50))
        
        # Logika Penentuan State untuk dikirim ke LangGraph
        if len(faces) > 0:
            face_detected_status = True
            if start_detection_time is None:
                start_detection_time = time.time()
            duration_violating = time.time() - start_detection_time
            
            # Eksekusi Sharia Guardrail (Blur Efek)
            for (x, y, w, h) in faces:
                sub_face = frame[y:y+h, x:x+w]
                frame[y:y+h, x:x+w] = cv2.GaussianBlur(sub_face, (99, 99), 15)
        else:
            face_detected_status = False
            start_detection_time = None
            duration_violating = 0.0

        # ORKESTRASI STATE LEWAT LANGGRAPH AGENT 🧠
        graph_output = agent.invoke({
            "face_detected": face_detected_status,
            "duration_violating": duration_violating,
            "system_alert": ""
        })
        alert_text = graph_output["system_alert"]
        
        # Penentuan warna teks alert di monitor
        text_color = (0, 0, 255) if "⚠️" in alert_text or "🚨" in alert_text else (0, 255, 0)
        
        # Render Banner Alert Transparan di Layar Kamera
        cv2.rectangle(frame, (10, 10), (490, 45), (0, 0, 0), -1)
        cv2.putText(frame, alert_text, (20, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 2)
        
        # JALUR OUTPUT DUA ALAM
        if IS_COLAB:
            out.write(frame)
            frame_count += 1
            if frame_count % 30 == 0:
                print(f"🎬 Cloud Processing: Berhasil memproses {frame_count} frame...")
        else:
            # TAMPILKAN MONITOR UTAMA JIKA DI MAC LOKAL
            cv2.imshow("Thiqla Master Live Monitor", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()
    print("\n🛑 Sistem dihentikan secara aman. Kerja bagus, Pak Wendy!")