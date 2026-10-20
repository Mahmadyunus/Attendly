import time
import httpx
import bcrypt
from src.database.config import supabase


def with_retry(fn, tries=3):
    for i in range(tries):
        try:
            return fn()
        except (httpx.RemoteProtocolError, httpx.ConnectError, httpx.ReadTimeout):
            if i == tries - 1:
                raise
            time.sleep(1)


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    # True when username is already taken
    response = with_retry(
        lambda: supabase.table("teachers").select("user_name").eq("user_name", username).execute()
    )
    return len(response.data) > 0


def create_teacher(username, password, name):
    data = {"user_name": username, "password": hash_pass(password), "name": name}
    response = with_retry(lambda: supabase.table("teachers").insert(data).execute())
    return response.data


def teacher_login(username, password):
    response = with_retry(
        lambda: supabase.table("teachers").select("*").eq("user_name", username).execute()
    )
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher
    return None


def get_all_students():
    response = with_retry(lambda: supabase.table("students").select("*").execute())
    return response.data


def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {"name": new_name, "face_embedding": face_embedding, "voice_embedding": voice_embedding}
    response = with_retry(lambda: supabase.table("students").insert(data).execute())
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = with_retry(lambda: supabase.table("subjects").insert(data).execute())
    return response.data


def get_teacher_subjects(teacher_id):
    response = with_retry(
        lambda: supabase.table("subjects")
        .select("*, subject_students(count), attendance_logs(timestamp)")
        .eq("teacher_id", teacher_id)
        .execute()
    )
    subjects = response.data

    for sub in subjects:
        sub["total_students"] = (
            sub.get("subject_students", [{}])[0].get("count", 0) if sub.get("subject_students") else 0
        )
        attendance = sub.get("attendance_logs", [])
        sub["total_classes"] = len(set(log["timestamp"] for log in attendance))

        sub.pop("subject_students", None)
        sub.pop("attendance_logs", None)

    return subjects


def enroll_student_to_subject(student_id, subject_id):
    data = {"student_id": student_id, "subject_id": subject_id}
    response = with_retry(lambda: supabase.table("subject_students").insert(data).execute())
    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    response = with_retry(
        lambda: supabase.table("subject_students").delete()
        .eq("student_id", student_id).eq("subject_id", subject_id).execute()
    )
    return response.data


def get_student_subjects(student_id):
    response = with_retry(
        lambda: supabase.table("subject_students").select("*, subjects(*)").eq("student_id", student_id).execute()
    )
    return response.data


def get_student_attendance(student_id):
    response = with_retry(
        lambda: supabase.table("attendance_logs").select("*, subjects(*)").eq("student_id", student_id).execute()
    )
    return response.data


def create_attendance(logs):
    print("SAVING LOGS:", logs)
    response = with_retry(lambda: supabase.table("attendance_logs").insert(logs).execute())
    print("SAVED:", response.data)
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = with_retry(
        lambda: supabase.table("attendance_logs")
        .select("*, subjects!inner(*)")
        .eq("subjects.teacher_id", teacher_id)
        .execute()
    )
    return response.data