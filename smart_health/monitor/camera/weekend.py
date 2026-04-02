# import cv2
# import mediapipe as mp
# import math
# import time
# from .base_camera import VideoCamera

# mp_pose = mp.solutions.pose
# mp_drawing = mp.solutions.drawing_utils

# class WeekendCamera(VideoCamera):
#     def __init__(self):
#         super().__init__()
#         print("🎯 WeekendCamera initialized!")

#         self.pose = mp_pose.Pose(
#             static_image_mode=False,
#             min_detection_confidence=0.5,
#             model_complexity=1
#         )

#         self.previous_pose = "Unknown Pose"
#         self.pose_counter = 0
#         self.POSE_STABILITY_THRESHOLD = 5

#         self.pose_locked = False
#         self.hold_start_time = None
#         self.HOLD_DURATION = 5
#         self.final_pose = "Unknown Pose"

#     def release(self):
#         """Cleanup MediaPipe and camera"""
#         try:
#             if hasattr(self, 'pose') and self.pose:
#                 self.pose.close()
#             print("🧹 WeekendCamera MediaPipe cleaned up")
#         except Exception as e:
#             print(f"Warning during MediaPipe cleanup: {e}")
        
#         # Call parent release
#         super().release()

#     # ---------- ANGLE CALCULATION ----------
#     def calculateAngle(self, a, b, c):
#         x1, y1, _ = a
#         x2, y2, _ = b
#         x3, y3, _ = c
#         angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
#                              math.atan2(y1 - y2, x1 - x2))
#         angle = abs(angle)
#         if angle > 180:
#             angle = 360 - angle
#         return angle

#     # ---------- YOGA CLASSIFICATION ----------
#     def classifyPose(self, landmarks):
#         label = "Unknown Pose"
#         L = mp_pose.PoseLandmark

#         left_elbow_angle = self.calculateAngle(landmarks[L.LEFT_SHOULDER.value],
#                                                landmarks[L.LEFT_ELBOW.value],
#                                                landmarks[L.LEFT_WRIST.value])

#         right_elbow_angle = self.calculateAngle(landmarks[L.RIGHT_SHOULDER.value],
#                                                 landmarks[L.RIGHT_ELBOW.value],
#                                                 landmarks[L.RIGHT_WRIST.value])

#         left_shoulder_angle = self.calculateAngle(landmarks[L.LEFT_ELBOW.value],
#                                                   landmarks[L.LEFT_SHOULDER.value],
#                                                   landmarks[L.LEFT_HIP.value])

#         right_shoulder_angle = self.calculateAngle(landmarks[L.RIGHT_HIP.value],
#                                                    landmarks[L.RIGHT_SHOULDER.value],
#                                                    landmarks[L.RIGHT_ELBOW.value])

#         left_knee_angle = self.calculateAngle(landmarks[L.LEFT_HIP.value],
#                                              landmarks[L.LEFT_KNEE.value],
#                                              landmarks[L.LEFT_ANKLE.value])

#         right_knee_angle = self.calculateAngle(landmarks[L.RIGHT_HIP.value],
#                                               landmarks[L.RIGHT_KNEE.value],
#                                               landmarks[L.RIGHT_ANKLE.value])

#         left_hip_angle = self.calculateAngle(landmarks[L.LEFT_SHOULDER.value],
#                                             landmarks[L.LEFT_HIP.value],
#                                             landmarks[L.LEFT_KNEE.value])

#         right_hip_angle = self.calculateAngle(landmarks[L.RIGHT_SHOULDER.value],
#                                              landmarks[L.RIGHT_HIP.value],
#                                              landmarks[L.RIGHT_KNEE.value])

#         # # -------- Virabhadrasana II or T Pose --------
#         # if 165 < left_elbow_angle < 195 and 165 < right_elbow_angle < 195:
#         #     if 80 < left_shoulder_angle < 110 and 80 < right_shoulder_angle < 110:
#         #         if 165 < left_knee_angle < 195 or 165 < right_knee_angle < 195:
#         #             if 90 < left_knee_angle < 120 or 90 < right_knee_angle < 120:
#         #                 label = "Virabhadrasana II"
#         #                 print("Virabhadrasana II Detected")

#         #         if 160 < left_knee_angle < 195 and 160 < right_knee_angle < 195:
#         #             label = "T Pose"

#         # # -------- Vrikshasana (Tree Pose) --------
#         # if 165 < left_knee_angle < 195 or 165 < right_knee_angle < 195:
#         #     if 315 < left_knee_angle < 335 or 25 < right_knee_angle < 45:
#         #         label = "Vrikshasana"

#         # # -------- Adho Mukha Svanasana (Downward Dog) --------
#         # if 165 < left_elbow_angle < 195 and 165 < right_elbow_angle < 195:
#         #     if 165 < left_knee_angle < 195 and 165 < right_knee_angle < 195:
#         #         if 60 < left_hip_angle < 120 and 60 < right_hip_angle < 120:

#         #             left_wrist_y = landmarks[L.LEFT_WRIST.value][1]
#         #             left_ankle_y = landmarks[L.LEFT_ANKLE.value][1]
#         #             right_wrist_y = landmarks[L.RIGHT_WRIST.value][1]
#         #             right_ankle_y = landmarks[L.RIGHT_ANKLE.value][1]

#         #             if left_wrist_y > left_ankle_y or right_wrist_y > right_ankle_y:
#         #                 label = "Adho Mukha Svanasana"

#         # # -------- Uttanasana (Forward Bend) --------
#         # if 165 < left_knee_angle < 195 and 165 < right_knee_angle < 195:
#         #     if 20 < left_hip_angle < 60 and 20 < right_hip_angle < 60:

#         #         left_wrist_y = landmarks[L.LEFT_WRIST.value][1]
#         #         left_ankle_y = landmarks[L.LEFT_ANKLE.value][1]
#         #         right_wrist_y = landmarks[L.RIGHT_WRIST.value][1]
#         #         right_ankle_y = landmarks[L.RIGHT_ANKLE.value][1]

#         #         if abs(left_wrist_y - left_ankle_y) < 50 or abs(right_wrist_y - right_ankle_y) < 50:
#         #             label = "Uttanasana"

#         # # -------- Utkatasana (Chair Pose) --------
#         # if 80 < left_knee_angle < 120 and 80 < right_knee_angle < 120:
#         #     if 80 < left_hip_angle < 120 and 80 < right_hip_angle < 120:
#         #         if 160 < left_shoulder_angle < 200 and 160 < right_shoulder_angle < 200:
#         #             if 165 < left_elbow_angle < 195 and 165 < right_elbow_angle < 195:
#         #                 label = "Utkatasana"

#         # # -------- Urdhva Hastasana (Raised Hands Pose) --------
#         # if 165 < left_knee_angle < 195 and 165 < right_knee_angle < 195:
#         #     if 160 < left_hip_angle < 195 and 160 < right_hip_angle < 195:
#         #         if 160 < left_shoulder_angle < 200 and 160 < right_shoulder_angle < 200:
#         #             if 165 < left_elbow_angle < 195 and 165 < right_elbow_angle < 195:
#         #                 label = "Urdhva Hastasana"
#         # -------- Virabhadrasana II or T Pose --------
#         # if 150 < left_elbow_angle < 210 and 150 < right_elbow_angle < 210:
#         #     if 70 < left_shoulder_angle < 130 and 70 < right_shoulder_angle < 130:

#         #         # Warrior II (one knee bent)
#         #         if (80 < left_knee_angle < 140) or (80 < right_knee_angle < 140):
#         #             label = "Virabhadrasana II"
#         #             print("Virabhadrasana II Detected")

#         #         # T Pose (both legs straight)
#         #         if 150 < left_knee_angle < 210 and 150 < right_knee_angle < 210:
#         #             label = "T Pose"


#         # # -------- Vrikshasana (Tree Pose) --------
#         # if (150 < left_knee_angle < 210) or (150 < right_knee_angle < 210):
#         #     if (300 < left_knee_angle < 350) or (10 < right_knee_angle < 60):
#         #         label = "Vrikshasana"


#         # # -------- Adho Mukha Svanasana (Downward Dog) --------
#         # if 150 < left_elbow_angle < 210 and 150 < right_elbow_angle < 210:
#         #     if 150 < left_knee_angle < 210 and 150 < right_knee_angle < 210:
#         #         if 45 < left_hip_angle < 135 and 45 < right_hip_angle < 135:

#         #             left_wrist_y = landmarks[L.LEFT_WRIST.value][1]
#         #             left_ankle_y = landmarks[L.LEFT_ANKLE.value][1]
#         #             right_wrist_y = landmarks[L.RIGHT_WRIST.value][1]
#         #             right_ankle_y = landmarks[L.RIGHT_ANKLE.value][1]

#         #             if left_wrist_y > left_ankle_y or right_wrist_y > right_ankle_y:
#         #                 label = "Adho Mukha Svanasana"


#         # # -------- Uttanasana (Forward Bend) --------
#         # if 150 < left_knee_angle < 210 and 150 < right_knee_angle < 210:
#         #     if 15 < left_hip_angle < 75 and 15 < right_hip_angle < 75:

#         #         left_wrist_y = landmarks[L.LEFT_WRIST.value][1]
#         #         left_ankle_y = landmarks[L.LEFT_ANKLE.value][1]
#         #         right_wrist_y = landmarks[L.RIGHT_WRIST.value][1]
#         #         right_ankle_y = landmarks[L.RIGHT_ANKLE.value][1]

#         #         if abs(left_wrist_y - left_ankle_y) < 80 or abs(right_wrist_y - right_ankle_y) < 80:
#         #             label = "Uttanasana"


#         # # -------- Utkatasana (Chair Pose) --------
#         # if 70 < left_knee_angle < 140 and 70 < right_knee_angle < 140:
#         #     if 70 < left_hip_angle < 140 and 70 < right_hip_angle < 140:
#         #         if 140 < left_shoulder_angle < 220 and 140 < right_shoulder_angle < 220:
#         #             if 150 < left_elbow_angle < 210 and 150 < right_elbow_angle < 210:
#         #                 label = "Utkatasana"


#         # # -------- Urdhva Hastasana (Raised Hands Pose) --------
#         # if 150 < left_knee_angle < 210 and 150 < right_knee_angle < 210:
#         #     if 140 < left_hip_angle < 210 and 140 < right_hip_angle < 210:
#         #         if 140 < left_shoulder_angle < 220 and 140 < right_shoulder_angle < 220:
#         #             if 150 < left_elbow_angle < 210 and 150 < right_elbow_angle < 210:
#         #                 label = "Urdhva Hastasana"
#         if 150 < left_elbow_angle < 210 and 150 < right_elbow_angle < 210:
#             if 70 < left_shoulder_angle < 130 and 70 < right_shoulder_angle < 130:

#                 # Warrior II (one knee bent)
#                 if (80 < left_knee_angle < 140) or (80 < right_knee_angle < 140):
#                     label = "Virabhadrasana II"
#                     print("Virabhadrasana II Detected")

#                 # T Pose (both legs straight)
#                 if 150 < left_knee_angle < 210 and 150 < right_knee_angle < 210:
#                     label = "T Pose"


#         # -------- Vrikshasana (Tree Pose) --------
#         if (150 < left_knee_angle < 210) or (150 < right_knee_angle < 210):
#             if (300 < left_knee_angle < 350) or (10 < right_knee_angle < 60):
#                 label = "Vrikshasana"


#         # -------- Adho Mukha Svanasana (Downward Dog) --------
#         if 150 < left_elbow_angle < 210 and 150 < right_elbow_angle < 210:
#             if 150 < left_knee_angle < 210 and 150 < right_knee_angle < 210:
#                 if 45 < left_hip_angle < 135 and 45 < right_hip_angle < 135:

#                     left_wrist_y = landmarks[L.LEFT_WRIST.value][1]
#                     left_ankle_y = landmarks[L.LEFT_ANKLE.value][1]
#                     right_wrist_y = landmarks[L.RIGHT_WRIST.value][1]
#                     right_ankle_y = landmarks[L.RIGHT_ANKLE.value][1]

#                     if left_wrist_y > left_ankle_y or right_wrist_y > right_ankle_y:
#                         label = "Adho Mukha Svanasana"


#         # -------- Uttanasana (Forward Bend) --------
#         if 150 < left_knee_angle < 210 and 150 < right_knee_angle < 210:
#             if 15 < left_hip_angle < 75 and 15 < right_hip_angle < 75:

#                 left_wrist_y = landmarks[L.LEFT_WRIST.value][1]
#                 left_ankle_y = landmarks[L.LEFT_ANKLE.value][1]
#                 right_wrist_y = landmarks[L.RIGHT_WRIST.value][1]
#                 right_ankle_y = landmarks[L.RIGHT_ANKLE.value][1]

#                 if abs(left_wrist_y - left_ankle_y) < 80 or abs(right_wrist_y - right_ankle_y) < 80:
#                     label = "Uttanasana"


#         # -------- Utkatasana (Chair Pose) --------
#         if 70 < left_knee_angle < 140 and 70 < right_knee_angle < 140:
#             if 70 < left_hip_angle < 140 and 70 < right_hip_angle < 140:
#                 if 140 < left_shoulder_angle < 220 and 140 < right_shoulder_angle < 220:
#                     if 150 < left_elbow_angle < 210 and 150 < right_elbow_angle < 210:
#                         label = "Utkatasana"


#         # -------- Urdhva Hastasana (Raised Hands Pose) --------
#         if 150 < left_knee_angle < 210 and 150 < right_knee_angle < 210:
#             if 140 < left_hip_angle < 210 and 140 < right_hip_angle < 210:
#                 if 140 < left_shoulder_angle < 220 and 140 < right_shoulder_angle < 220:
#                     if 150 < left_elbow_angle < 210 and 150 < right_elbow_angle < 210:
#                         label = "Urdhva Hastasana"
        

        

#         return label


#     # ---------- GENERATE CAMERA FRAME ----------
#     def get_frame(self):
#         frame = self.get_raw_frame()

#         if frame is None:
#             return None

#         frame = cv2.flip(frame, 1)
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
#         results = None
#         try:
#             results = self.pose.process(rgb)
#         except Exception as e:
#             print(f"⚠️ MediaPipe processing error: {e}")
#             ret, jpeg = cv2.imencode(".jpg", frame)
#             return jpeg.tobytes() if ret else None

#         label = "Unknown Pose"

#         if results and results.pose_landmarks:
#             mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#             h, w, _ = frame.shape
#             lm = results.pose_landmarks.landmark
#             pts = [(int(p.x*w), int(p.y*h), p.z*w) for p in lm]

#             label = self.classifyPose(pts)

#             if not self.pose_locked:
#                 if label == self.previous_pose:
#                     self.pose_counter += 1
#                 else:
#                     self.pose_counter = 0
#                     self.previous_pose = label

#                 if self.pose_counter >= self.POSE_STABILITY_THRESHOLD and label != "Unknown Pose":
#                     self.pose_locked = True
#                     self.final_pose = label
#                     self.hold_start_time = time.time()

#                 # Display current pose
#                 cv2.putText(frame, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)

#             else:
#                 elapsed = int(time.time() - self.hold_start_time)
#                 remaining = self.HOLD_DURATION - elapsed

#                 if remaining > 0:
#                     cv2.putText(frame, f"HOLD {remaining}s", (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
#                     cv2.putText(frame, self.final_pose, (140, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
#                 else:
#                     self.pose_locked = False
#                     self.pose_counter = 0
#                     self.previous_pose = "Unknown Pose"

#         h, w, _ = frame.shape
#         # Add mode indicator
#         cv2.putText(frame, "WEEKEND MODE", (20, h - 20), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

#         ret, jpeg = cv2.imencode(".jpg", frame)
#         if not ret:
#             return None
#         return jpeg.tobytes()
import cv2
import mediapipe as mp
import math
import time
from .base_camera import VideoCamera

mp_pose    = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


class WeekendCamera(VideoCamera):
    def __init__(self):
        self._init_camera()          # open shared hardware handle
        print("🎯 WeekendCamera initialized!")

        self.pose = mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            model_complexity=1,
        )

        self.previous_pose    = "Unknown Pose"
        self.pose_counter     = 0
        self.POSE_STABILITY_THRESHOLD = 5

        self.pose_locked    = False
        self.hold_start_time = None
        self.HOLD_DURATION  = 5
        self.final_pose     = "Unknown Pose"

    # ─────────────────────────────────────────────────────────────────────
    def release(self):
        try:
            if hasattr(self, "pose") and self.pose:
                self.pose.close()
        except Exception as e:
            print(f"Warning closing pose: {e}")
        print("🧹 WeekendCamera MediaPipe cleaned up")
        super().release()

    # ─────────────────────────────────────────────────────────────────────
    def calculateAngle(self, a, b, c):
        x1, y1, _ = a
        x2, y2, _ = b
        x3, y3, _ = c
        angle = math.degrees(
            math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        )
        angle = abs(angle)
        if angle > 180:
            angle = 360 - angle
        return angle

    # ─────────────────────────────────────────────────────────────────────
    def classifyPose(self, landmarks):
        label = "Unknown Pose"
        L = mp_pose.PoseLandmark

        lae = self.calculateAngle(landmarks[L.LEFT_SHOULDER.value],
                                  landmarks[L.LEFT_ELBOW.value],
                                  landmarks[L.LEFT_WRIST.value])
        rae = self.calculateAngle(landmarks[L.RIGHT_SHOULDER.value],
                                  landmarks[L.RIGHT_ELBOW.value],
                                  landmarks[L.RIGHT_WRIST.value])
        lsa = self.calculateAngle(landmarks[L.LEFT_ELBOW.value],
                                  landmarks[L.LEFT_SHOULDER.value],
                                  landmarks[L.LEFT_HIP.value])
        rsa = self.calculateAngle(landmarks[L.RIGHT_HIP.value],
                                  landmarks[L.RIGHT_SHOULDER.value],
                                  landmarks[L.RIGHT_ELBOW.value])
        lka = self.calculateAngle(landmarks[L.LEFT_HIP.value],
                                  landmarks[L.LEFT_KNEE.value],
                                  landmarks[L.LEFT_ANKLE.value])
        rka = self.calculateAngle(landmarks[L.RIGHT_HIP.value],
                                  landmarks[L.RIGHT_KNEE.value],
                                  landmarks[L.RIGHT_ANKLE.value])
        lha = self.calculateAngle(landmarks[L.LEFT_SHOULDER.value],
                                  landmarks[L.LEFT_HIP.value],
                                  landmarks[L.LEFT_KNEE.value])
        rha = self.calculateAngle(landmarks[L.RIGHT_SHOULDER.value],
                                  landmarks[L.RIGHT_HIP.value],
                                  landmarks[L.RIGHT_KNEE.value])

        # ── Virabhadrasana II / T-Pose ──────────────────────────────────
        if 150 < lae < 210 and 150 < rae < 210:
            if 70 < lsa < 130 and 70 < rsa < 130:
                if (80 < lka < 140) or (80 < rka < 140):
                    label = "Virabhadrasana II"
                if 150 < lka < 210 and 150 < rka < 210:
                    label = "T Pose"

        # ── Vrikshasana (Tree Pose) ─────────────────────────────────────
        if (150 < lka < 210) or (150 < rka < 210):
            if (300 < lka < 350) or (10 < rka < 60):
                label = "Vrikshasana"

        # ── Adho Mukha Svanasana (Downward Dog) ────────────────────────
        if 150 < lae < 210 and 150 < rae < 210:
            if 150 < lka < 210 and 150 < rka < 210:
                if 45 < lha < 135 and 45 < rha < 135:
                    lwy = landmarks[L.LEFT_WRIST.value][1]
                    lay = landmarks[L.LEFT_ANKLE.value][1]
                    rwy = landmarks[L.RIGHT_WRIST.value][1]
                    ray = landmarks[L.RIGHT_ANKLE.value][1]
                    if lwy > lay or rwy > ray:
                        label = "Adho Mukha Svanasana"

        # ── Uttanasana (Forward Bend) ───────────────────────────────────
        if 150 < lka < 210 and 150 < rka < 210:
            if 15 < lha < 75 and 15 < rha < 75:
                lwy = landmarks[L.LEFT_WRIST.value][1]
                lay = landmarks[L.LEFT_ANKLE.value][1]
                rwy = landmarks[L.RIGHT_WRIST.value][1]
                ray = landmarks[L.RIGHT_ANKLE.value][1]
                if abs(lwy - lay) < 80 or abs(rwy - ray) < 80:
                    label = "Uttanasana"

        # ── Utkatasana (Chair Pose) ─────────────────────────────────────
        if 70 < lka < 140 and 70 < rka < 140:
            if 70 < lha < 140 and 70 < rha < 140:
                if 140 < lsa < 220 and 140 < rsa < 220:
                    if 150 < lae < 210 and 150 < rae < 210:
                        label = "Utkatasana"

        # ── Urdhva Hastasana (Raised Hands) ────────────────────────────
        if 150 < lka < 210 and 150 < rka < 210:
            if 140 < lha < 210 and 140 < rha < 210:
                if 140 < lsa < 220 and 140 < rsa < 220:
                    if 150 < lae < 210 and 150 < rae < 210:
                        label = "Urdhva Hastasana"

        return label

    # ─────────────────────────────────────────────────────────────────────
    def get_frame(self):
        frame = self.get_raw_frame()
        if frame is None:
            return None

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = None
        try:
            results = self.pose.process(rgb)
        except Exception as e:
            print(f"⚠️ MediaPipe processing error: {e}")

        label = "Unknown Pose"

        if results and results.pose_landmarks:
            # ── Draw skeleton ────────────────────────────────────────────
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2),
            )

            lm  = results.pose_landmarks.landmark
            pts = [(int(p.x * w), int(p.y * h), p.z * w) for p in lm]

            label = self.classifyPose(pts)

            if not self.pose_locked:
                if label == self.previous_pose:
                    self.pose_counter += 1
                else:
                    self.pose_counter  = 0
                    self.previous_pose = label

                if (self.pose_counter >= self.POSE_STABILITY_THRESHOLD
                        and label != "Unknown Pose"):
                    self.pose_locked     = True
                    self.final_pose      = label
                    self.hold_start_time = time.time()

                # Show current detection
                pose_color = (0, 255, 0) if label != "Unknown Pose" else (0, 165, 255)
                cv2.putText(frame, label,
                            (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, pose_color, 3)

                # Stability progress bar
                if label != "Unknown Pose":
                    bar_w = int((self.pose_counter / self.POSE_STABILITY_THRESHOLD) * 200)
                    cv2.rectangle(frame, (20, 60), (220, 75), (50, 50, 50), -1)
                    cv2.rectangle(frame, (20, 60), (20 + bar_w, 75), (0, 255, 0), -1)
                    cv2.putText(frame, "Stabilising...",
                                (20, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

            else:
                elapsed   = int(time.time() - self.hold_start_time)
                remaining = self.HOLD_DURATION - elapsed

                if remaining > 0:
                    cv2.putText(frame, self.final_pose,
                                (140, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                    cv2.putText(frame, f"HOLD: {remaining}s",
                                (150, 260), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

                    # Countdown circle
                    pct   = remaining / self.HOLD_DURATION
                    angle = int(360 * pct)
                    cv2.ellipse(frame, (w - 60, 60), (40, 40), -90, 0, angle,
                                (0, 255, 0), 4)
                    cv2.putText(frame, str(remaining),
                                (w - 70, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                else:
                    self.pose_locked   = False
                    self.pose_counter  = 0
                    self.previous_pose = "Unknown Pose"

        else:
            # No person detected
            cv2.putText(frame, "No pose detected – step into frame",
                        (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)

        # ── Mode watermark ────────────────────────────────────────────────
        cv2.putText(frame, "WEEKEND MODE",
                    (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes() if ret else None