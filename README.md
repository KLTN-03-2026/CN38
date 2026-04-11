XÂY DỰNG HỆ THỐNG QUẢN LÝ PHÒNG GYM TÍCH HỢP AI PHÂN TÍCH HÀNH VI TẬP LUYỆN

Thông tin đề tài
Tên đề tài: Xây dựng hệ thống quản lý phòng gym tích hợp AI phân tích hành vi tập luyện của hội viên
Sinh viên thực hiện: Nguyễn Tuấn Cường
Giảng viên hướng dẫn: Th.S Trần Bàn Thạch
Thời gian thực hiện: 12/03/2026 – 15/05/2026

Công nghệ sử dụng
Backend: FastAPI (Python)
Frontend: ReactJS + TypeScript
Database: PostgreSQL
Authentication: JWT
AI: Scikit-learn, XGBoost (phân tích hành vi, dự đoán churn)


## Hướng dẫn chạy Backend
```bash
cd backend
py -m venv venv  
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000
