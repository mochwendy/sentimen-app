# 🤖 Dual-Engine AI Suite: Sentiment Analysis & Intelligent Indonesian PDF RAG

Selamat datang di proyek portofolio **AI Engineering** pertama saya! Repositori ini berisi dua aplikasi kecerdasan buatan (AI) terintegrasi yang dibangun menggunakan model *open-source* terkini, basis data vektor, dan antarmuka web interaktif. 

Kedua proyek ini dideploy secara mandiri dari lingkungan *cloud* menggunakan akselerasi **T4 GPU** gratis.

---

## 🚀 Fitur Utama

### 1️⃣ AI Sentiment Analyzer (Aplikasi Web Klasifikasi Emosi)
Aplikasi berbasis **Streamlit** yang mampu menganalisis struktur kata dan mendeteksi sentimen/emosi teks dalam Bahasa Inggris secara dinamis.
* **Akurasi Tinggi:** Mencapai tingkat keyakinan model (*confidence score*) hingga **99.98%**.
* **Model Baseline:** `distilbert-base-uncased-finetuned-sst-2-english` (arsitektur *Encoder-Only*).
* **Fitur Terowongan:** Menggunakan enkripsi *tunneling* aman dari **Ngrok** untuk publikasi web global.

### 2️⃣ AI Intelligent PDF Reader (Sistem True RAG Bahasa Indonesia)
Sistem *Retrieval-Augmented Generation* (RAG) berbasis **Gradio** yang mampu membaca dokumen PDF terstruktur asli (seperti CV, portofolio, atau aturan internal) dan menjawab pertanyaan pengguna murni berdasarkan data tersebut tanpa risiko halusinasi.
* **Pencarian Semantik:** Menggunakan basis data vektor **ChromaDB** lokal untuk mencocokkan arti kata (*Cosine Similarity*), bukan sekadar pencarian kata kunci (*keyword matching*) yang kaku.
* **Otak LLM Lokal:** Menggunakan model canggih `Qwen/Qwen2.5-1.5B-Instruct` yang sepenuhnya *open-source* dan bebas token API eksternal.
* **Bahasa:** Dioptimalkan untuk pemahaman Bahasa Indonesia menggunakan model embeddings `indobenchmark/indobert-base-p2`.

---

## 🛠️ Tech Stack & Alat yang Digunakan

* **Bahasa Pemrograman:** Python 3.x
* **Framework Deep Learning:** PyTorch
* **Ekosistem AI:** Hugging Face (Transformers, Tokenizer, Pipeline)
* **Basis Data Vektor:** ChromaDB
* **Antarmuka (UI):** Streamlit & Gradio
* **Alat Infrastruktur:** Ngrok (Secure Tunneling), Google Colab (T4 GPU Environment)

---

## 🎯 Proses Pemecahan Masalah (Troubleshooting)

Sebagai seorang *AI Engineer*, proyek ini memberikan pengalaman berharga dalam mengatasi berbagai kendala teknis riil di lapangan, antara lain:
1. **Pembaruan Dependensi Hugging Face:** Menangani perubahan tugas (*breaking changes*) pada pustaka `transformers` v5.x dengan menyesuaikan alur pemanggilan model dari arsitektur *Causal-LM* ke fungsi penanganan *Seq2Seq* yang tepat.
2. **Tabrakan Port Server:** Mengatasi kendala penguncian port server (`Port 8501 is not available`) di latar belakang Google Colab dengan teknik pembersihan proses (*force kill/pkill*) dan pengalihan dinamis ke jalur kosong.
3. **Optimasi Generasi Teks LLM:** Memperbaiki luaran teks model Qwen 2.5 yang sempat terpotong di tengah kalimat melalui konfigurasi parameter `max_new_tokens=512` dan penyesuaian dimensi matriks dua dimensi (`output.logits`) pada PyTorch.

---

## 💻 Cara Menjalankan Proyek

Proyek ini dirancang agar dapat direplikasi dengan sangat mudah. Cukup klik lencana (*badge*) **Open In Colab** di bagian paling atas halaman repositori ini untuk membuka dokumen notebook langsung di browser Anda.

1. Aktifkan Hardware Accelerator ke **T4 GPU** di menu `Runtime` > `Change runtime type`.
2. Jalankan kotak kode instalasi library dasar (`!pip install...`).
3. Unggah file PDF Anda dengan nama `dokumen_kita.pdf` pada direktori kiri folder Colab.
4. Masukkan token Ngrok Anda pada bagian aplikasi Streamlit, atau jalankan langsung versi Gradio lokal untuk mendapatkan tautan publik `.gradio.live` secara gratis.

---

🔬 *Proyek ini dibangun secara mandiri sebagai bentuk pembuktian kompetensi praktis dalam siklus hidup pengembangan produk kecerdasan buatan (AI Product Lifecycle).*
