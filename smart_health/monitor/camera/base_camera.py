# # import cv2
# # import threading
# # import time

# # class VideoCamera:
# #     _instance = None
# #     _lock = threading.Lock()
# #     _current_mode = None

# #     def __new__(cls):
# #         with cls._lock:
# #             if cls._instance is None:
# #                 cls._instance = super().__new__(cls)
# #                 cls._instance.cap = None
# #             return cls._instance

# #     def _init_camera(self):
# #         """Initialize camera if not already initialized"""
# #         if self.cap is None or not self.cap.isOpened():
# #             print("📷 Opening camera...")
# #             self.cap = cv2.VideoCapture(0)
# #         if not self.cap.isOpened():
# #             print("⚠️ Camera 0 failed, trying camera 1...")
# #             self.cap = cv2.VideoCapture(1)
# #             if not self.cap.isOpened():
# #                 print("❌ Camera failed to open")
# #             else:
# #                 print("✅ Camera opened successfully")

# #     def get_raw_frame(self):
# #         if not self.cap or not self.cap.isOpened():
# #             self._init_camera()
# #             if not self.cap or not self.cap.isOpened():
# #                 return None

# #         success, frame = self.cap.read()
# #         if not success:
# #             return None
# #         return frame

# #     def release(self):
# #         """Release the camera properly"""
# #         with self._lock:
# #             if self.cap is not None and self.cap.isOpened():
# #                 print("🔒 Releasing camera...")
# #                 self.cap.release()
# #                 self.cap = None
# #                 # Small delay to ensure camera is fully released
# #                 time.sleep(0.3)
# #                 print("✅ Camera released successfully")
    
# #     @classmethod
# #     def reset_camera(cls):
# #         """Force reset the camera"""
# #         with cls._lock:
# #             if cls._instance and cls._instance.cap:
# #                 print("🔄 Resetting camera...")
# #                 cls._instance.cap.release()
# #                 cls._instance.cap = None
# #                 time.sleep(0.3)
# #                 print("✅ Camera reset complete")
    
# #     @classmethod
# #     def force_cleanup(cls):
# #         """Force cleanup of camera instance"""
# #         with cls._lock:
# #             if cls._instance:
# #                 if cls._instance.cap is not None:
# #                     try:
# #                         cls._instance.cap.release()
# #                     except:
# #                         pass
# #                     cls._instance.cap = None
# #                 cls._instance = None
# #                 print("🧹 Camera instance cleaned up")
# import cv2
# import threading
# import time

# class VideoCamera:
#     _instance = None
#     _lock = threading.Lock()
#     _current_mode = None

#     def __new__(cls):
#         with cls._lock:
#             if cls._instance is None:
#                 cls._instance = super().__new__(cls)
#                 cls._instance.cap = None
#             return cls._instance

#     def _init_camera(self):
#         """Initialize camera if not already initialized"""
#         if self.cap is None or not self.cap.isOpened():
#             print("📷 Opening camera...")
#             self.cap = cv2.VideoCapture(0)
            
#             # If camera 0 fails, try camera 1
#             if not self.cap.isOpened():
#                 print("⚠️ Camera 0 failed, trying camera 1...")
#                 self.cap = cv2.VideoCapture(1)
            
#             if not self.cap.isOpened():
#                 print("❌ Camera failed to open")
#             else:
#                 print("✅ Camera opened successfully")

#     def get_raw_frame(self):
#         if not self.cap or not self.cap.isOpened():
#             self._init_camera()
#             if not self.cap or not self.cap.isOpened():
#                 return None

#         success, frame = self.cap.read()
#         if not success:
#             return None
#         return frame

#     def release(self):
#         """Release the camera properly"""
#         with self._lock:
#             if self.cap is not None and self.cap.isOpened():
#                 print("🔒 Releasing camera...")
#                 self.cap.release()
#                 self.cap = None
#                 time.sleep(0.3)
#                 print("✅ Camera released successfully")
    
#     @classmethod
#     def reset_camera(cls):
#         """Force reset the camera"""
#         with cls._lock:
#             if cls._instance and cls._instance.cap:
#                 print("🔄 Resetting camera...")
#                 cls._instance.cap.release()
#                 cls._instance.cap = None
#                 time.sleep(0.3)
#                 print("✅ Camera reset complete")
    
#     @classmethod
#     def force_cleanup(cls):
#         """Force cleanup of camera instance"""
#         with cls._lock:
#             if cls._instance:
#                 if cls._instance.cap is not None:
#                     try:
#                         cls._instance.cap.release()
#                     except:
#                         pass
#                     cls._instance.cap = None
#                 cls._instance = None
#                 print("🧹 Camera instance cleaned up")
import cv2
import threading
import time


class VideoCamera:
    """
    Base camera class — NOT a singleton anymore.
    Each WeekdayCamera / WeekendCamera gets its own instance so that
    MediaPipe models are always freshly initialised on creation.
    """

    _camera_lock = threading.Lock()   # class-level lock guards the *hardware*
    _active_cap = None                # shared hardware handle

    def _init_camera(self):
        """Open the shared hardware capture if it is not already open."""
        with VideoCamera._camera_lock:
            if VideoCamera._active_cap is None or not VideoCamera._active_cap.isOpened():
                print("📷 Opening camera hardware...")
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    print("⚠️ Camera 0 failed, trying camera 1...")
                    cap = cv2.VideoCapture(1)
                if cap.isOpened():
                    print("✅ Camera hardware opened successfully")
                    VideoCamera._active_cap = cap
                else:
                    print("❌ No camera could be opened")
                    VideoCamera._active_cap = None

    def get_raw_frame(self):
        if VideoCamera._active_cap is None or not VideoCamera._active_cap.isOpened():
            self._init_camera()
            if VideoCamera._active_cap is None or not VideoCamera._active_cap.isOpened():
                return None

        with VideoCamera._camera_lock:
            success, frame = VideoCamera._active_cap.read()
        if not success:
            return None
        return frame

    def release(self):
        """Release the shared hardware capture."""
        with VideoCamera._camera_lock:
            if VideoCamera._active_cap is not None and VideoCamera._active_cap.isOpened():
                print("🔒 Releasing camera hardware...")
                VideoCamera._active_cap.release()
                VideoCamera._active_cap = None
                time.sleep(0.3)
                print("✅ Camera hardware released")

    @classmethod
    def force_cleanup(cls):
        """Force-release the hardware capture from anywhere."""
        with cls._camera_lock:
            if cls._active_cap is not None:
                try:
                    cls._active_cap.release()
                except Exception:
                    pass
                cls._active_cap = None
                print("🧹 Camera hardware force-cleaned")