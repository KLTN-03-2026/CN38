from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.deps import get_current_user
from ..models.user import User
from ..models.ai_chat_log import AIChatLog
from ..schemas.ai_chat import (
    ChatRequest,
    ChatResponse,
    AnalyzeWorkoutRequest,
    AnalyzeWorkoutResponse,
    AIChatLogCreate,
    AIChatLogUpdate,
    AIChatLogResponse,
)
from ..ml.workout_model import predict_workout_quality

router = APIRouter(prefix="/ai", tags=["AI"])


def _simple_reply(text: str) -> str:
    t = text.lower().strip()
    if any(k in t for k in ["xin chào", "chào", "hello", "hi"]):
        return "Xin chào! Mình là trợ lý gym. Bạn muốn hỏi về gói tập, lịch tập hay dinh dưỡng?"
    if "gói" in t or "package" in t:
        return "Bạn có thể xem các gói membership trong mục Gói tập và đặt mua trực tiếp."
    if "tập" in t or "workout" in t:
        return "Nên khởi động 10 phút, tập 45–60 phút và ghi lại buổi tập để theo dõi tiến độ."
    if "calo" in t or "calorie" in t:
        return "Calories tiêu hao phụ thuộc cường độ và thời lượng; hãy điền số liệu vào buổi tập để hệ thống phân tích."
    return "Mình đang học thêm. Bạn thử hỏi về gói tập, lịch tập hoặc calo nhé."


@router.post("/chat", response_model=ChatResponse)
def chat(
    body: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reply = _simple_reply(body.message)
    log = AIChatLog(user_id=current_user.id, message=body.message, response=reply)
    db.add(log)
    db.commit()
    return ChatResponse(reply=reply)


@router.post("/analyze-workout", response_model=AnalyzeWorkoutResponse)
def analyze_workout(
    body: AnalyzeWorkoutRequest,
    _: User = Depends(get_current_user),
):
    label, proba = predict_workout_quality(
        body.duration_minutes,
        body.calories_burned,
        body.intensity_score,
        body.sessions_last_week,
    )
    if label == "tốt":
        hint = "Tiến độ ổn, có thể tăng nhẹ cường độ hoặc duy trì đều đặn."
    else:
        hint = "Thử kéo dài thời gian vận động hoặc tăng số buổi trong tuần."
    return AnalyzeWorkoutResponse(label=label, probability=round(proba, 4), hint=hint)


@router.post("/chat-logs", response_model=AIChatLogResponse, status_code=status.HTTP_201_CREATED)
def create_chat_log(
    body: AIChatLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = AIChatLog(user_id=current_user.id, message=body.message, response=body.response)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/chat-logs", response_model=List[AIChatLogResponse])
def list_chat_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(AIChatLog)
        .filter(AIChatLog.user_id == current_user.id)
        .order_by(AIChatLog.id.desc())
        .all()
    )
    return rows


@router.get("/chat-logs/{log_id}", response_model=AIChatLogResponse)
def get_chat_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = db.query(AIChatLog).filter(AIChatLog.id == log_id).first()
    if not row or row.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Không tìm thấy log")
    return row


@router.put("/chat-logs/{log_id}", response_model=AIChatLogResponse)
def update_chat_log(
    log_id: int,
    body: AIChatLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = db.query(AIChatLog).filter(AIChatLog.id == log_id).first()
    if not row or row.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Không tìm thấy log")
    data = body.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(row, k, v)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/chat-logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = db.query(AIChatLog).filter(AIChatLog.id == log_id).first()
    if not row or row.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Không tìm thấy log")
    db.delete(row)
    db.commit()
    return None
