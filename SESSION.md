# SESSION — 2026-03-20
# Claude update file ini otomatis tiap task selesai

## FOKUS HARI INI
- [x] Task 1: Buat file Alembic untuk Batch 1 (tenants, brands, outlets)
- [x] Task 2: Buat file Alembic untuk Batch 2 (roles, users, sessions, devices, suppliers, customers, outlet_tax_config, tables)
- [x] Task 3: Buat file Alembic untuk Batch 3 (products, inventory, recipes)
- [x] Task 4: Buat file Alembic untuk Batch 4 (pricing_rules, shifts, orders, payments, reservations, purchase_orders)

## MODUL AKTIF
Modul: Database Migrations
File dikerjakan:
- backend/migrations/versions/023_pricing_rules.py
- backend/migrations/versions/023b_shifts.py
- backend/migrations/versions/024_orders.py
- backend/migrations/versions/025_order_items.py
- backend/migrations/versions/026_payments.py
- backend/migrations/versions/027_reservations.py
- backend/migrations/versions/028_purchase_orders.py
- backend/migrations/versions/029_purchase_order_items.py

## PROGRESS
✅ Selesai:
- Setup Alembic file 023_pricing_rules.py
- Setup Alembic file 023b_shifts.py (ENUM shift_status)
- Setup Alembic file 024_orders.py (ENUM order_status, order_type, SEQUENCE order_display_seq, FK shift_session_id, service_charge_amount)
- Setup Alembic file 025_order_items.py (JSONB modifiers)
- Setup Alembic file 026_payments.py (ENUM payment_method, payment_status, idempotency_key, amount_due, amount_paid, change_amount, qris_url, midtrans_raw, dll)
- Setup Alembic file 027_reservations.py
- Setup Alembic file 028_purchase_orders.py
- Setup Alembic file 029_purchase_order_items.py

⏳ In Progress:
   Nama: Inisialisasi FastAPI Project
   File: -
   Sudah: Migration Batch 1, 2, 3, & 4
   Tinggal: FastAPI project init, Auth, CRUD, dll
   Catatan: Melanjutkan ke batch berikutnya (FastAPI init).

❌ Belum:
- FastAPI project init + Auth + JWT + PIN

## FILE YANG DIUBAH HARI INI
- backend/migrations/versions/001_tenants.py s/d 029_purchase_order_items.py
- MEMORY.md
- SESSION.md

## KEPUTUSAN BARU HARI INI
- Menambahkan tabel `shifts` (023b) untuk tracking sesi kasir.
- Menambahkan `order_display_seq` dan `display_number` di tabel `orders` (Golden Rule #28).
- Menambahkan `shift_session_id` dan `service_charge_amount` di tabel `orders`.
- Mengubah struktur tabel `payments` (026) dengan menambahkan `amount_due`, `amount_paid`, `change_amount`, `qris_url`, `midtrans_raw`, `reconciled_at`, dll. Serta mengupdate ENUM `payment_status` menjadi lebih lengkap.
- Menambahkan `idempotency_key` pada tabel `payments` dengan unique index (where not null) untuk mencegah double payment.
- Menggunakan JSONB untuk `modifiers` di `order_items` agar fleksibel menyimpan data modifier yang dipilih.
- Menambahkan `received_quantity` di `purchase_order_items` untuk tracking penerimaan barang parsial.

## BLOCKER
- Tidak ada.

## CHECKPOINT TERAKHIR
Terakhir sampai di: Selesai membuat file migration batch 4 dan fix tabel orders & payments.
Besok lanjut dari: Inisialisasi FastAPI project dan setup Auth.
