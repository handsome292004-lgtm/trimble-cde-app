import os
import re
import ifcopenshell
import ifcopenshell.util.element

# 1. THIẾT LẬP ĐƯỜNG DẪN THƯ MỤC (Nhớ kiểm tra lại đường dẫn của bạn)
thu_muc_ifc = r"C:\Users\ASUS\OneDrive\Thư mục mới\OneDrive\CDE\02_IFC"
thu_muc_pdf = r"C:\Users\ASUS\OneDrive\Thư mục mới\OneDrive\CDE\03_PDF"

# Bộ nhớ ifc_mapping bây giờ sẽ chỉ lưu phần đuôi: {"Z001" : "Mã GUID Trimble"}
ifc_mapping = {}

print("--- BƯỚC 1: ĐỌC VÀ RÚT GỌN MÃ TỪ MÔ HÌNH IFC ---")
for ten_file in os.listdir(thu_muc_ifc):
    if ten_file.endswith(".ifc"):
        duong_dan_file = os.path.join(thu_muc_ifc, ten_file)
        model = ifcopenshell.open(duong_dan_file)
        elements = model.by_type("IfcElement")

        for element in elements:
            global_id = element.GlobalId
            psets = ifcopenshell.util.element.get_psets(element)

            if "Pset_QuanLyThiCong" in psets:
                ma_cau_kien = psets["Pset_QuanLyThiCong"].get("MaCauKien")
                if ma_cau_kien:
                    # Tự động cắt phần đuôi sau dấu gạch dưới "_" hoặc gạch ngang "-"
                    # Ví dụ: "BTN_Z001" sẽ bị cắt thành "Z001"
                    ma_rut_gon = re.split(r'[-_]', str(ma_cau_kien))[-1]

                    ifc_mapping[ma_rut_gon] = global_id

print(f"-> Đã ghi nhớ thành công {len(ifc_mapping)} mã cấu kiện (đã cắt hậu tố) từ IFC.\n")

print("--- BƯỚC 2: KIỂM TRA HỒ SƠ PDF ---")
danh_sach_pdf = [f for f in os.listdir(thu_muc_pdf) if f.endswith(".pdf")]

so_file_xanh = 0
so_file_do = 0

for ten_pdf in danh_sach_pdf:
    ma_tim_thay = None

    # Đối chiếu phần đuôi "Z001" với tên file PDF
    for ma_rut_gon in ifc_mapping.keys():
        if ma_rut_gon in ten_pdf:
            ma_tim_thay = ma_rut_gon
            break

    if ma_tim_thay:
        print(f"[XANH 🟢] File '{ten_pdf}' ---> Khớp với mã hậu tố: {ma_tim_thay}")
        so_file_xanh += 1
    else:
        print(f"[ĐỎ   🔴] File '{ten_pdf}' ---> BỊ TỪ CHỐI (Không tìm thấy mã hậu tố nào)")
        so_file_do += 1

print("\n--- TỔNG KẾT ---")
print(f"Hồ sơ Hợp lệ (XANH): {so_file_xanh}")
print(f"Hồ sơ Lỗi (ĐỎ)     : {so_file_do}")