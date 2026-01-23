# from django.shortcuts import render
# from django.http import StreamingHttpResponse, JsonResponse
# import json
# import threading
# import time

# from .models import YogaSession, WeekdaySession
# from .camera.weekday import WeekdayCamera
# from .camera.weekend import WeekendCamera

# # Global camera instances with lock
# weekday_cam = None
# weekend_cam = None
# camera_lock = threading.Lock()
# current_camera = None
# video_stream_active = False


# # =========================
# # CLEANUP FUNCTION
# # =========================
# def cleanup_all_cameras():
#     """Cleanup all camera instances and their MediaPipe models"""
#     global weekday_cam, weekend_cam, current_camera, video_stream_active
    
#     # Stop video stream first
#     video_stream_active = False
#     time.sleep(0.3)
    
#     with camera_lock:
#         print("🧹 Starting complete camera cleanup...")
        
#         # Cleanup weekday camera
#         if weekday_cam is not None:
#             print("🧹 Cleaning up weekday camera")
#             try:
#                 if hasattr(weekday_cam, 'face_mesh') and weekday_cam.face_mesh:
#                     weekday_cam.face_mesh.close()
#                 if hasattr(weekday_cam, 'pose') and weekday_cam.pose:
#                     weekday_cam.pose.close()
#                 weekday_cam.release()
#             except Exception as e:
#                 print(f"Warning during weekday cleanup: {e}")
#             weekday_cam = None
        
#         # Cleanup weekend camera
#         if weekend_cam is not None:
#             print("🧹 Cleaning up weekend camera")
#             try:
#                 if hasattr(weekend_cam, 'pose') and weekend_cam.pose:
#                     weekend_cam.pose.close()
#                 weekend_cam.release()
#             except Exception as e:
#                 print(f"Warning during weekend cleanup: {e}")
#             weekend_cam = None
        
#         current_camera = None
#         time.sleep(0.5)  # Extra delay for camera hardware
#         print("✅ All cameras cleaned up and released")


# # =========================
# # FRAME GENERATOR
# # =========================
# def frame_generator(camera):
#     """Generate frames from the camera object"""
#     global video_stream_active
#     video_stream_active = True
    
#     try:
#         while video_stream_active:
#             frame = camera.get_frame()
#             if frame is None:
#                 time.sleep(0.01)
#                 continue
            
#             yield (
#                 b"--frame\r\n"
#                 b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
#             )
#     except GeneratorExit:
#         print("🛑 Frame generator stopped")
#     except Exception as e:
#         print(f"❌ Frame generator error: {e}")
#     finally:
#         video_stream_active = False


# # =========================
# # STREAM VIEW
# # =========================
# def video_feed(request):
#     global weekday_cam, weekend_cam, current_camera, video_stream_active

#     mode = request.GET.get("mode", "weekday")
#     print(f"🔹 VIDEO FEED REQUEST: {mode}")

#     # Stop any existing stream
#     video_stream_active = False
#     time.sleep(0.5)

#     with camera_lock:
#         if mode == "weekday":
#             print("✅ Initializing WeekdayCamera")
            
#             # Clean up weekend camera if active
#             if weekend_cam is not None:
#                 print("🧹 Cleaning up weekend camera")
#                 try:
#                     if hasattr(weekend_cam, 'pose') and weekend_cam.pose:
#                         weekend_cam.pose.close()
#                     weekend_cam.release()
#                 except Exception as e:
#                     print(f"Warning during weekend cleanup: {e}")
#                 weekend_cam = None
#                 time.sleep(0.5)
            
#             # Clean up old weekday camera if exists
#             if weekday_cam is not None:
#                 print("🧹 Cleaning up old weekday camera")
#                 try:
#                     if hasattr(weekday_cam, 'face_mesh') and weekday_cam.face_mesh:
#                         weekday_cam.face_mesh.close()
#                     if hasattr(weekday_cam, 'pose') and weekday_cam.pose:
#                         weekday_cam.pose.close()
#                     weekday_cam.release()
#                 except Exception as e:
#                     print(f"Warning during old weekday cleanup: {e}")
#                 weekday_cam = None
#                 time.sleep(0.5)
            
#             # Create new weekday camera
#             print("🎬 Creating new WeekdayCamera")
#             weekday_cam = WeekdayCamera()
#             camera = weekday_cam
#             current_camera = "weekday"
            
#         else:  # weekend mode
#             print("✅ Initializing WeekendCamera")
            
#             # Clean up weekday camera if active
#             if weekday_cam is not None:
#                 print("🧹 Cleaning up weekday camera")
#                 try:
#                     if hasattr(weekday_cam, 'face_mesh') and weekday_cam.face_mesh:
#                         weekday_cam.face_mesh.close()
#                     if hasattr(weekday_cam, 'pose') and weekday_cam.pose:
#                         weekday_cam.pose.close()
#                     weekday_cam.release()
#                 except Exception as e:
#                     print(f"Warning during weekday cleanup: {e}")
#                 weekday_cam = None
#                 time.sleep(0.5)
            
#             # Clean up old weekend camera if exists
#             if weekend_cam is not None:
#                 print("🧹 Cleaning up old weekend camera")
#                 try:
#                     if hasattr(weekend_cam, 'pose') and weekend_cam.pose:
#                         weekend_cam.pose.close()
#                     weekend_cam.release()
#                 except Exception as e:
#                     print(f"Warning during old weekend cleanup: {e}")
#                 weekend_cam = None
#                 time.sleep(0.5)
            
#             # Create new weekend camera
#             print("🎬 Creating new WeekendCamera")
#             weekend_cam = WeekendCamera()
#             camera = weekend_cam
#             current_camera = "weekend"

#     return StreamingHttpResponse(
#         frame_generator(camera),
#         content_type="multipart/x-mixed-replace; boundary=frame"
#     )


# # =========================
# # HOME PAGE
# # =========================
# def home_page(request):
#     """Home page - cleanup cameras and release hardware"""
#     print("🏠 Loading Home Page - Stopping streams and cleaning up cameras")
#     cleanup_all_cameras()
#     return render(request, "monitor/home.html")


# # =========================
# # PAGE VIEWS
# # =========================
# def weekday_page(request):
#     print("🌐 Loading Weekday Page")
#     return render(request, "monitor/weekday.html")


# def weekend_page(request):
#     print("🌐 Loading Weekend Page")
#     return render(request, "monitor/weekend.html")


# # =========================
# # SAVE WEEKDAY SESSION
# # =========================
# def reset_weekday_session(request):
#     """Reset session-specific counters when starting a new session"""
#     global weekday_cam
    
#     if request.method == "POST":
#         try:
#             if weekday_cam is not None:
#                 weekday_cam.session_blink_count = 0
#                 weekday_cam.total_bad_posture_time = 0
#                 weekday_cam.bad_posture_start = None
#                 print("🔄 Session counters reset")
#             return JsonResponse({"status": "reset"})
#         except Exception as e:
#             print(f"Warning: Reset error: {e}")
#             return JsonResponse({"status": "error"})
    
#     return JsonResponse({"status": "invalid"})


# def save_weekday_session(request):
#     global weekday_cam
    
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body.decode("utf-8"))
#             duration = data.get("duration")

#             if duration is None:
#                 return JsonResponse({"status": "error", "message": "No duration"})

#             # Get stats from camera if available
#             blink_count = 0
#             bad_posture_time = 0
            
#             if weekday_cam is not None:
#                 # Use session-specific blink count
#                 blink_count = getattr(weekday_cam, 'session_blink_count', 0)
#                 bad_posture_time = int(getattr(weekday_cam, 'total_bad_posture_time', 0))
                
#                 # Cap bad posture time to session duration
#                 if bad_posture_time > duration:
#                     bad_posture_time = duration

#             WeekdaySession.objects.create(
#                 duration=int(duration),
#                 blink_count=blink_count,
#                 bad_posture_time=bad_posture_time
#             )
            
#             # Reset session-specific counters for next session
#             if weekday_cam is not None:
#                 weekday_cam.session_blink_count = 0
#                 weekday_cam.total_bad_posture_time = 0
#                 weekday_cam.bad_posture_start = None
            
#             print(f"💾 Weekday session saved: {duration}s, blinks: {blink_count}, bad posture: {bad_posture_time}s")
#             return JsonResponse({
#                 "status": "saved",
#                 "blink_count": blink_count,
#                 "bad_posture_time": bad_posture_time
#             })

#         except Exception as e:
#             print(f"❌ Error saving weekday session: {e}")
#             return JsonResponse({"status": "error", "message": str(e)})

#     return JsonResponse({"status": "invalid"})


# # =========================
# # SAVE YOGA SESSION
# # =========================
# def save_session(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body.decode("utf-8"))
#             duration = data.get("duration")

#             if duration is None:
#                 return JsonResponse({"status": "error", "message": "No duration"})

#             YogaSession.objects.create(duration=int(duration))
#             print(f"💾 Yoga session saved: {duration} seconds")
#             return JsonResponse({"status": "saved"})

#         except Exception as e:
#             print(f"❌ Error saving yoga session: {e}")
#             return JsonResponse({"status": "error", "message": str(e)})

#     return JsonResponse({"status": "invalid"})


# # =========================
# # SESSION HISTORY
# # =========================
# def session_history(request):
#     sessions = YogaSession.objects.all().order_by("-date")
#     print(f"📊 Loading {sessions.count()} yoga sessions")
#     return render(request, "monitor/history.html", {"sessions": sessions})


# def weekday_history(request):
#     sessions = WeekdaySession.objects.all().order_by("-date")
#     print(f"📊 Loading {sessions.count()} weekday sessions")
#     return render(request, "monitor/history_weekday.html", {"sessions": sessions})

# def combined_history(request):
#     """Combined history view showing both weekday and weekend sessions"""
#     weekday_sessions = WeekdaySession.objects.all().order_by("-date")
#     weekend_sessions = YogaSession.objects.all().order_by("-date")
    
#     print(f"📊 Loading combined history - Weekday: {weekday_sessions.count()}, Weekend: {weekend_sessions.count()}")
    
#     context = {
#         'weekday_sessions': weekday_sessions,
#         'weekend_sessions': weekend_sessions,
#     }
    
#     return render(request, "monitor/combined_history.html", context)
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
import json
import threading
import time

from .models import YogaSession, WeekdaySession, ExamSession
from .camera.weekday import WeekdayCamera
from .camera.weekend import WeekendCamera
from .camera.exam import ExamCamera
from .camera.camera_manage import CameraManager

# Global camera instances with lock
weekday_cam = None
weekend_cam = None
exam_cam = None
camera_lock = threading.Lock()
current_camera = None
video_stream_active = False


# =========================
# CLEANUP FUNCTION
# =========================
def cleanup_all_cameras():
    """Cleanup all camera instances and their MediaPipe models"""
    global weekday_cam, weekend_cam, exam_cam, current_camera, video_stream_active
    
    # Stop video stream first
    video_stream_active = False
    time.sleep(0.3)
    
    with camera_lock:
        print("🧹 Starting complete camera cleanup...")
        
        # Cleanup weekday camera
        if weekday_cam is not None:
            print("🧹 Cleaning up weekday camera")
            try:
                if hasattr(weekday_cam, 'face_mesh') and weekday_cam.face_mesh:
                    weekday_cam.face_mesh.close()
                if hasattr(weekday_cam, 'pose') and weekday_cam.pose:
                    weekday_cam.pose.close()
                weekday_cam.release()
            except Exception as e:
                print(f"Warning during weekday cleanup: {e}")
            weekday_cam = None
        
        # Cleanup weekend camera
        if weekend_cam is not None:
            print("🧹 Cleaning up weekend camera")
            try:
                if hasattr(weekend_cam, 'pose') and weekend_cam.pose:
                    weekend_cam.pose.close()
                weekend_cam.release()
            except Exception as e:
                print(f"Warning during weekend cleanup: {e}")
            weekend_cam = None
        
        # Cleanup exam camera
        if exam_cam is not None:
            print("🧹 Cleaning up exam camera")
            try:
                if hasattr(exam_cam, 'detector') and exam_cam.detector:
                    exam_cam.detector.close()
                exam_cam.release()
            except Exception as e:
                print(f"Warning during exam cleanup: {e}")
            exam_cam = None
        
        current_camera = None
        time.sleep(0.5)  # Extra delay for camera hardware
        print("✅ All cameras cleaned up and released")


# =========================
# FRAME GENERATOR
# =========================
def frame_generator(camera):
    """Generate frames from the camera object"""
    global video_stream_active
    video_stream_active = True
    
    try:
        while video_stream_active:
            frame = camera.get_frame()
            if frame is None:
                time.sleep(0.01)
                continue
            
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )
    except GeneratorExit:
        print("🛑 Frame generator stopped")
    except Exception as e:
        print(f"❌ Frame generator error: {e}")
    finally:
        video_stream_active = False


# =========================
# STREAM VIEW
# =========================
def video_feed(request):
    global weekday_cam, weekend_cam, exam_cam, current_camera, video_stream_active

    mode = request.GET.get("mode", "weekday")
    print(f"📹 VIDEO FEED REQUEST: {mode}")

    # Stop any existing stream
    video_stream_active = False
    time.sleep(0.5)

    with camera_lock:
        if mode == "weekday":
            print("✅ Initializing WeekdayCamera")
            
            # Clean up other cameras
            if weekend_cam is not None:
                try:
                    if hasattr(weekend_cam, 'pose') and weekend_cam.pose:
                        weekend_cam.pose.close()
                    weekend_cam.release()
                except Exception as e:
                    print(f"Warning during weekend cleanup: {e}")
                weekend_cam = None
                time.sleep(0.5)
            
            if exam_cam is not None:
                try:
                    if hasattr(exam_cam, 'detector') and exam_cam.detector:
                        exam_cam.detector.close()
                    exam_cam.release()
                except Exception as e:
                    print(f"Warning during exam cleanup: {e}")
                exam_cam = None
                time.sleep(0.5)
            
            # Clean up old weekday camera
            if weekday_cam is not None:
                try:
                    if hasattr(weekday_cam, 'face_mesh') and weekday_cam.face_mesh:
                        weekday_cam.face_mesh.close()
                    if hasattr(weekday_cam, 'pose') and weekday_cam.pose:
                        weekday_cam.pose.close()
                    weekday_cam.release()
                except Exception as e:
                    print(f"Warning during old weekday cleanup: {e}")
                weekday_cam = None
                time.sleep(0.5)
            
            weekday_cam = WeekdayCamera()
            camera = weekday_cam
            current_camera = "weekday"
            
        elif mode == "exam":
            print("✅ Initializing ExamCamera")
            
            # Clean up other cameras
            if weekday_cam is not None:
                try:
                    if hasattr(weekday_cam, 'face_mesh') and weekday_cam.face_mesh:
                        weekday_cam.face_mesh.close()
                    if hasattr(weekday_cam, 'pose') and weekday_cam.pose:
                        weekday_cam.pose.close()
                    weekday_cam.release()
                except Exception as e:
                    print(f"Warning during weekday cleanup: {e}")
                weekday_cam = None
                time.sleep(0.5)
            
            if weekend_cam is not None:
                try:
                    if hasattr(weekend_cam, 'pose') and weekend_cam.pose:
                        weekend_cam.pose.close()
                    weekend_cam.release()
                except Exception as e:
                    print(f"Warning during weekend cleanup: {e}")
                weekend_cam = None
                time.sleep(0.5)
            
            # Clean up old exam camera
            if exam_cam is not None:
                try:
                    if hasattr(exam_cam, 'detector') and exam_cam.detector:
                        exam_cam.detector.close()
                    exam_cam.release()
                except Exception as e:
                    print(f"Warning during old exam cleanup: {e}")
                exam_cam = None
                time.sleep(0.5)
            
            exam_cam = ExamCamera()
            camera = exam_cam
            current_camera = "exam"
            
        else:  # weekend mode
            print("✅ Initializing WeekendCamera")
            
            # Clean up other cameras
            if weekday_cam is not None:
                try:
                    if hasattr(weekday_cam, 'face_mesh') and weekday_cam.face_mesh:
                        weekday_cam.face_mesh.close()
                    if hasattr(weekday_cam, 'pose') and weekday_cam.pose:
                        weekday_cam.pose.close()
                    weekday_cam.release()
                except Exception as e:
                    print(f"Warning during weekday cleanup: {e}")
                weekday_cam = None
                time.sleep(0.5)
            
            if exam_cam is not None:
                try:
                    if hasattr(exam_cam, 'detector') and exam_cam.detector:
                        exam_cam.detector.close()
                    exam_cam.release()
                except Exception as e:
                    print(f"Warning during exam cleanup: {e}")
                exam_cam = None
                time.sleep(0.5)
            
            # Clean up old weekend camera
            if weekend_cam is not None:
                try:
                    if hasattr(weekend_cam, 'pose') and weekend_cam.pose:
                        weekend_cam.pose.close()
                    weekend_cam.release()
                except Exception as e:
                    print(f"Warning during old weekend cleanup: {e}")
                weekend_cam = None
                time.sleep(0.5)
            
            weekend_cam = WeekendCamera()
            camera = weekend_cam
            current_camera = "weekend"

    return StreamingHttpResponse(
        frame_generator(camera),
        content_type="multipart/x-mixed-replace; boundary=frame"
    )


# =========================
# HOME PAGE
# =========================
def home_page(request):
    """Home page - cleanup cameras and release hardware"""
    print("🏠 Loading Home Page - Stopping streams and cleaning up cameras")
    cleanup_all_cameras()
    return render(request, "monitor/home.html")


# =========================
# PAGE VIEWS
# =========================
def weekday_page(request):
    print("🌐 Loading Weekday Page")
    return render(request, "monitor/weekday.html")


def weekend_page(request):
    print("🌐 Loading Weekend Page")
    return render(request, "monitor/weekend.html")


def exam_page(request):
    print("🌐 Loading Exam Page")
    return render(request, "monitor/exam.html")


# =========================
# WEEKDAY SESSION HANDLERS
# =========================
def reset_weekday_session(request):
    """Reset session-specific counters when starting a new session"""
    global weekday_cam
    
    if request.method == "POST":
        try:
            if weekday_cam is not None:
                weekday_cam.session_blink_count = 0
                weekday_cam.total_bad_posture_time = 0
                weekday_cam.bad_posture_start = None
                print("🔄 Session counters reset")
            return JsonResponse({"status": "reset"})
        except Exception as e:
            print(f"Warning: Reset error: {e}")
            return JsonResponse({"status": "error"})
    
    return JsonResponse({"status": "invalid"})


def save_weekday_session(request):
    global weekday_cam
    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            duration = data.get("duration")

            if duration is None:
                return JsonResponse({"status": "error", "message": "No duration"})

            # Get stats from camera
            blink_count = 0
            bad_posture_time = 0
            
            if weekday_cam is not None:
                blink_count = getattr(weekday_cam, 'session_blink_count', 0)
                bad_posture_time = int(getattr(weekday_cam, 'total_bad_posture_time', 0))
                
                if bad_posture_time > duration:
                    bad_posture_time = duration

            WeekdaySession.objects.create(
                duration=int(duration),
                blink_count=blink_count,
                bad_posture_time=bad_posture_time
            )
            
            # Reset for next session
            if weekday_cam is not None:
                weekday_cam.session_blink_count = 0
                weekday_cam.total_bad_posture_time = 0
                weekday_cam.bad_posture_start = None
            
            print(f"💾 Weekday session saved: {duration}s")
            return JsonResponse({
                "status": "saved",
                "blink_count": blink_count,
                "bad_posture_time": bad_posture_time
            })

        except Exception as e:
            print(f"❌ Error saving weekday session: {e}")
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "invalid"})


# =========================
# EXAM SESSION HANDLERS
# =========================
def reset_exam_session(request):
    """Reset exam session counters"""
    global exam_cam
    
    if request.method == "POST":
        try:
            if exam_cam is not None:
                exam_cam.session_start_time = time.time()
                exam_cam.total_eyes_away_time = 0
                exam_cam.total_multiple_person_time = 0
                exam_cam.alert_count = 0
                exam_cam.eyes_away_start = None
                exam_cam.multiple_person_start = None
                print("🔄 Exam session counters reset")
            return JsonResponse({"status": "reset"})
        except Exception as e:
            print(f"Warning: Reset error: {e}")
            return JsonResponse({"status": "error"})
    
    return JsonResponse({"status": "invalid"})


def save_exam_session(request):
    global exam_cam
    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            duration = data.get("duration")

            if duration is None:
                return JsonResponse({"status": "error", "message": "No duration"})

            # Get stats from camera
            eyes_away_time = 0
            multiple_person_time = 0
            alert_count = 0
            
            if exam_cam is not None:
                eyes_away_time = int(getattr(exam_cam, 'total_eyes_away_time', 0))
                multiple_person_time = int(getattr(exam_cam, 'total_multiple_person_time', 0))
                alert_count = getattr(exam_cam, 'alert_count', 0)
                
                # Cap times to duration
                if eyes_away_time > duration:
                    eyes_away_time = duration
                if multiple_person_time > duration:
                    multiple_person_time = duration

            ExamSession.objects.create(
                duration=int(duration),
                eyes_away_time=eyes_away_time,
                multiple_person_time=multiple_person_time,
                alert_count=alert_count
            )
            
            # Reset for next session
            if exam_cam is not None:
                exam_cam.total_eyes_away_time = 0
                exam_cam.total_multiple_person_time = 0
                exam_cam.alert_count = 0
                exam_cam.eyes_away_start = None
                exam_cam.multiple_person_start = None
            
            print(f"💾 Exam session saved: {duration}s, alerts: {alert_count}")
            return JsonResponse({
                "status": "saved",
                "eyes_away_time": eyes_away_time,
                "multiple_person_time": multiple_person_time,
                "alert_count": alert_count
            })

        except Exception as e:
            print(f"❌ Error saving exam session: {e}")
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "invalid"})


# =========================
# YOGA SESSION HANDLER
# =========================
def save_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            duration = data.get("duration")

            if duration is None:
                return JsonResponse({"status": "error", "message": "No duration"})

            YogaSession.objects.create(duration=int(duration))
            print(f"💾 Yoga session saved: {duration} seconds")
            return JsonResponse({"status": "saved"})

        except Exception as e:
            print(f"❌ Error saving yoga session: {e}")
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "invalid"})


# =========================
# HISTORY VIEWS
# =========================
def session_history(request):
    sessions = YogaSession.objects.all().order_by("-date")
    print(f"📊 Loading {sessions.count()} yoga sessions")
    return render(request, "monitor/history.html", {"sessions": sessions})


def weekday_history(request):
    sessions = WeekdaySession.objects.all().order_by("-date")
    print(f"📊 Loading {sessions.count()} weekday sessions")
    return render(request, "monitor/history_weekday.html", {"sessions": sessions})


def exam_history(request):
    sessions = ExamSession.objects.all().order_by("-date")
    print(f"📊 Loading {sessions.count()} exam sessions")
    return render(request, "monitor/history_exam.html", {"sessions": sessions})


def combined_history(request):
    """Combined history view showing all session types"""
    weekday_sessions = WeekdaySession.objects.all().order_by("-date")
    weekend_sessions = YogaSession.objects.all().order_by("-date")
    exam_sessions = ExamSession.objects.all().order_by("-date")
    
    print(f"📊 Loading combined history - Weekday: {weekday_sessions.count()}, Weekend: {weekend_sessions.count()}, Exam: {exam_sessions.count()}")
    
    context = {
        'weekday_sessions': weekday_sessions,
        'weekend_sessions': weekend_sessions,
        'exam_sessions': exam_sessions,
    }
    
    return render(request, "monitor/combined_history.html", context)


# =========================
# CAMERA MANAGEMENT API
# =========================
def get_available_cameras(request):
    """API endpoint to get list of available cameras"""
    try:
        camera_manager = CameraManager()
        cameras = camera_manager.get_available_cameras()
        selected_index = camera_manager.get_selected_camera_index()
        
        camera_list = []
        for i, cam in enumerate(cameras):
            camera_list.append({
                'id': i,
                'name': cam['name'],
                'type': cam['type'],
                'resolution': f"{cam['width']}x{cam['height']}",
                'fps': cam['fps'],
                'source': cam['source'],
                'index': cam['index'],
                'selected': i == camera_manager._selected_camera
            })
        
        print(f"📷 Returning {len(camera_list)} available camera(s)")
        return JsonResponse({
            'status': 'success',
            'cameras': camera_list,
            'selected': camera_manager._selected_camera,
            'total': len(cameras)
        })
    except Exception as e:
        print(f"❌ Error getting cameras: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


def select_camera(request):
    """API endpoint to select a camera"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            camera_id = data.get('camera_id')
            
            if camera_id is None:
                return JsonResponse({
                    'status': 'error',
                    'message': 'camera_id is required'
                })
            
            camera_manager = CameraManager()
            
            # Stop current stream
            global video_stream_active
            video_stream_active = False
            time.sleep(0.5)
            
            # Change camera selection
            if camera_manager.set_selected_camera(camera_id):
                selected_camera = camera_manager.get_selected_camera()
                print(f"📷 Camera switched to: {selected_camera['name']}")
                return JsonResponse({
                    'status': 'success',
                    'message': f"Camera switched to {selected_camera['name']}",
                    'camera': selected_camera['name']
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid camera_id'
                })
        except Exception as e:
            print(f"❌ Error selecting camera: {e}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error', 'message': 'POST required'})


def refresh_cameras(request):
    """API endpoint to refresh available cameras"""
    try:
        camera_manager = CameraManager()
        camera_manager.refresh_cameras()
        cameras = camera_manager.get_available_cameras()
        
        print(f"🔄 Camera list refreshed - Found {len(cameras)} camera(s)")
        return JsonResponse({
            'status': 'success',
            'total': len(cameras),
            'message': f"Found {len(cameras)} camera(s)"
        })
    except Exception as e:
        print(f"❌ Error refreshing cameras: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })