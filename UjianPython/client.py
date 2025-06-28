

import requests
import threading
import time
from datetime import datetime

BASE_API_URL = "http://127.0.0.1:5000/get_stock"
SKUS_TO_CHECK = ["SKU-001", "SKU-003", "SKU-999", "SKU-002", "SKU-004"]
NUM_REQUESTS = len(SKUS_TO_CHECK)
CLIENT_LOG_FILE = "stock_checker_log.txt"

client_log_lock = threading.Lock()

with open(CLIENT_LOG_FILE, "w", encoding="utf-8") as f:
    f.write(f"--- Stock Checker Log Started: {datetime.now()} ---\n")

# ==============================================================================
# SOAL 1: Implementasi Logging Thread-Safe
# ==============================================================================

    """
    TUGAS ANDA (Soal 1):
    Lengkapi fungsi ini untuk mencatat 'message' dari 'thread_name' ke
    CLIENT_LOG_FILE secara thread-safe menggunakan 'client_log_lock'.

    Langkah-langkah:
    1. Dapatkan 'client_log_lock' (gunakan 'with' statement untuk kemudahan).
    2. Buat timestamp (contoh: datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")).
    3. Format pesan log (contoh: f"[{timestamp}] [{thread_name}] {message}\n").
    4. Tulis pesan log ke CLIENT_LOG_FILE (mode append 'a', encoding 'utf-8').
    5. (Opsional) Cetak pesan log ke konsol juga.
    """
    # ===== TULIS KODE ANDA UNTUK SOAL 1 DI SINI =====
    #
    #
    #
def log_client_activity_safe(thread_name, message):
    with client_log_lock:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        log_message = f"[{timestamp}] [{thread_name}] {message}\n"
        with open(CLIENT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_message)
        print(log_message) # Hapus 'pass' ini setelah Anda mengisi kode
    # =================================================


# ==============================================================================
# SOAL 2: Implementasi Fungsi Permintaan API
# ==============================================================================
    
    """
    TUGAS ANDA (Soal 2):
    Lengkapi fungsi ini untuk mengirim permintaan GET ke API stok produk
    dan mencatat hasilnya menggunakan fungsi 'log_client_activity_safe' yang
    telah Anda implementasikan di Soal 1.

    Langkah-langkah:
    1. Bentuk 'target_url' dengan menggunakan BASE_API_URL dan 'sku' yang diberikan.
    2. Catat (menggunakan 'log_client_activity_safe') bahwa permintaan akan dikirim.
    3. Gunakan blok 'try-except' untuk menangani potensi error saat request.
       a. Di dalam 'try':
          i.  Kirim permintaan GET ke 'target_url' menggunakan 'requests.get()'. Sertakan timeout.
          ii. Periksa 'response.status_code':
              - Jika 200 (sukses):
                  - Dapatkan JSON dari 'response.json()'.
                  - Catat pesan sukses. Contoh: f"Berhasil! Stok '{data.get('name', 'N/A')}' adalah {data.get('stock', 0)} unit di {data.get('warehouse', 'N/A')}."
              - Jika 404 (SKU tidak ditemukan):
                  - Dapatkan JSON dari 'response.json()'.
                  - Catat pesan error. Contoh: f"Error: SKU {sku} tidak ditemukan. Pesan: {data.get('message', 'Not found')}"
              - Untuk status code lain:
                  - Catat pesan error umum. Contoh: f"Menerima status error dari API: {response.status_code} - {response.text[:100]}"
       b. Di blok 'except requests.exceptions.Timeout':
          - Catat pesan timeout.
       c. Di blok 'except requests.exceptions.RequestException as e':
          - Catat pesan error permintaan umum.
       d. Di blok 'except Exception as e':
          - Catat pesan kesalahan tak terduga.
    4. Setelah blok try-except, catat bahwa tugas untuk SKU ini selesai.
    """
    
def request_stock_from_api(sku, current_thread_name):
    target_url = f"{BASE_API_URL}?sku={sku}"
    log_client_activity_safe(current_thread_name, f"Memulai permintaan untuk SKU: {sku}")
    try:
        response = requests.get(target_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            log_client_activity_safe(current_thread_name, f"Berhasil! Stok '{data.get('name', 'N/A')}' adalah {data.get('stock', 0)} unit di {data.get('warehouse', 'N/A')}.")
        elif response.status_code == 404:
            data = response.json()
            log_client_activity_safe(current_thread_name, f"Error: SKU {sku} tidak ditemukan. Pesan: {data.get('message', 'Not found')}")
        else:
            log_client_activity_safe(current_thread_name, f"Menerima status error dari API: {response.status_code} - {response.text[:100]}")
    except requests.exceptions.Timeout:
        log_client_activity_safe(current_thread_name, f"Permintaan untuk SKU {sku} telah melebihi batas waktu (timeout).")
    except requests.exceptions.RequestException as e:
        log_client_activity_safe(current_thread_name, f"Terjadi kesalahan permintaan: {e}")
    except Exception as e:
        log_client_activity_safe(current_thread_name, f"Terjadi kesalahan tak terduga: {e}")
    finally:
        log_client_activity_safe(current_thread_name, f"Selesai permintaan untuk SKU: {sku}")


    # ===== TULIS KODE ANDA UNTUK SOAL 2 DI SINI =====
    #
    #
     # Hapus 'pass' ini setelah Anda mengisi kode
    # =================================================

def worker_thread_task(sku, task_id):
    """Fungsi yang dijalankan oleh setiap worker thread."""
    thread_name = f"Worker-{task_id}"
    log_client_activity_safe(thread_name, f"Memulai pengecekan untuk SKU: {sku}")
    request_stock_from_api(sku, thread_name)
    log_client_activity_safe(thread_name, f"Selesai pengecekan untuk SKU: {sku}")

if __name__ == "__main__":
    log_client_activity_safe("MainClient", f"Memulai {NUM_REQUESTS} pengecekan stok produk secara concurrent.")
    
    threads = []
    start_time = time.time()

    for i, product_sku in enumerate(SKUS_TO_CHECK):
        thread = threading.Thread(target=worker_thread_task, args=(product_sku, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time
    
    log_client_activity_safe("MainClient", f"Semua pengecekan stok selesai dalam {total_time:.2f} detik.")
    print(f"\nLog aktivitas klien disimpan di: {CLIENT_LOG_FILE}")
    print(f"Total waktu eksekusi: {total_time:.2f} detik.")