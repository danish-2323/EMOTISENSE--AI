import cv2
import numpy as np
from collections import deque
import os
import warnings
import time

# Suppress all warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

# Global singleton detectors
_fer_detector = None
_opencv_cascade = None
_dlib_detector = None

def _get_fer_detector():
    global _fer_detector
    if _fer_detector is None:
        try:
            from fer import FER
            _fer_detector = FER(mtcnn=True)  # Use MTCNN for better face detection
            print("FER detector with MTCNN initialized")
        except Exception as e:
            try:
                from fer import FER
                _fer_detector = FER(mtcnn=False)
                print("FER detector with OpenCV initialized")
            except Exception as e2:
                print(f"FER initialization failed: {e2}")
                _fer_detector = False
    return _fer_detector if _fer_detector is not False else None

def _get_opencv_cascade():
    global _opencv_cascade
    if _opencv_cascade is None:
        try:
            _opencv_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            print("OpenCV cascade initialized")
        except Exception as e:
            print(f"OpenCV cascade failed: {e}")
            _opencv_cascade = False
    return _opencv_cascade if _opencv_cascade is not False else None

def _get_dlib_detector():
    global _dlib_detector
    if _dlib_detector is None:
        try:
            import dlib
            _dlib_detector = dlib.get_frontal_face_detector()
            print("Dlib detector initialized")
        except Exception as e:
            print(f"Dlib detector failed: {e}")
            _dlib_detector = False
    return _dlib_detector if _dlib_detector is not False else None

class FaceEmotionDetector:
    def __init__(self):
        self.emotion_history = deque(maxlen=5)  # Smooth over 5 frames
        self.face_history = deque(maxlen=3)     # Track face positions
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        self.is_available = True
        self.frame_count = 0
        self.last_valid_emotions = None
        print("Advanced face emotion detector ready")
        
    def _detect_face_multi_method(self, frame):
        """Use multiple methods to detect face for better stability"""
        faces = []
        
        # Method 1: Try MTCNN via FER (most accurate)
        fer_detector = _get_fer_detector()
        if fer_detector:
            try:
                fer_results = fer_detector.detect_emotions(frame)
                if fer_results:
                    for result in fer_results:
                        box = result['box']
                        if box[2] > 60 and box[3] > 60:  # Minimum size
                            faces.append([box[0], box[1], box[2], box[3]])
            except:
                pass
        
        # Method 2: OpenCV Haar Cascade (backup)
        if not faces:
            cascade = _get_opencv_cascade()
            if cascade is not None:
                try:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    detected = cascade.detectMultiScale(
                        gray, scaleFactor=1.1, minNeighbors=5, 
                        minSize=(80, 80), maxSize=(400, 400)
                    )
                    for (x, y, w, h) in detected:
                        faces.append([x, y, w, h])
                except:
                    pass
        
        # Method 3: Dlib (alternative)
        if not faces:
            dlib_detector = _get_dlib_detector()
            if dlib_detector is not False:
                try:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    detected = dlib_detector(gray)
                    for face in detected:
                        x, y, w, h = face.left(), face.top(), face.width(), face.height()
                        if w > 60 and h > 60:
                            faces.append([x, y, w, h])
                except:
                    pass
        
        return self._select_best_face(faces, frame.shape)
    
    def _select_best_face(self, faces, frame_shape):
        """Select the best face from multiple detections"""
        if not faces:
            return None
        
        # Filter faces by size and position
        valid_faces = []
        h, w = frame_shape[:2]
        
        for face in faces:
            x, y, fw, fh = face
            # Check if face is reasonable size and position
            if (fw > 80 and fh > 80 and 
                x > 0 and y > 0 and 
                x + fw < w and y + fh < h and
                fw < w * 0.8 and fh < h * 0.8):
                valid_faces.append(face)
        
        if not valid_faces:
            return None
        
        # Select largest face (usually most reliable)
        best_face = max(valid_faces, key=lambda f: f[2] * f[3])
        
        # Smooth face position with history
        if self.face_history:
            last_face = self.face_history[-1]
            # If new face is very different, use weighted average
            if abs(best_face[0] - last_face[0]) > 50 or abs(best_face[1] - last_face[1]) > 50:
                alpha = 0.7  # Weight for new detection
                best_face = [
                    int(alpha * best_face[0] + (1-alpha) * last_face[0]),
                    int(alpha * best_face[1] + (1-alpha) * last_face[1]),
                    int(alpha * best_face[2] + (1-alpha) * last_face[2]),
                    int(alpha * best_face[3] + (1-alpha) * last_face[3])
                ]
        
        self.face_history.append(best_face)
        return best_face
    
    def _preprocess_face(self, face_crop):
        """Advanced face preprocessing for better emotion recognition"""
        try:
            # Resize to optimal size
            face_resized = cv2.resize(face_crop, (224, 224))
            
            # Convert to grayscale for processing
            gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
            
            # Apply CLAHE for better contrast
            enhanced = self.clahe.apply(gray)
            
            # Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(enhanced, (3, 3), 0.5)
            
            # Convert back to BGR
            processed = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
            
            # Normalize pixel values
            processed = cv2.normalize(processed, None, 0, 255, cv2.NORM_MINMAX)
            
            return processed
        except Exception as e:
            print(f"Preprocessing error: {e}")
            return cv2.resize(face_crop, (224, 224))
    
    def _get_stable_emotions(self, current_emotions):
        """Apply temporal smoothing for stable emotion detection"""
        if not current_emotions:
            return self.last_valid_emotions or self._get_neutral_emotions()
        
        # Add to history
        self.emotion_history.append(current_emotions)
        
        # If we have enough history, apply smoothing
        if len(self.emotion_history) >= 3:
            smoothed = {}
            for emotion in current_emotions.keys():
                values = [hist.get(emotion, 0) for hist in self.emotion_history]
                # Use weighted average (recent frames have more weight)
                weights = [0.1, 0.2, 0.3, 0.4] if len(values) >= 4 else [0.3, 0.7] if len(values) >= 2 else [1.0]
                weights = weights[-len(values):]  # Match length
                smoothed[emotion] = sum(v * w for v, w in zip(values, weights)) / sum(weights)
            
            self.last_valid_emotions = smoothed
            return smoothed
        else:
            self.last_valid_emotions = current_emotions
            return current_emotions
    
    def _get_neutral_emotions(self):
        """Return neutral emotion distribution"""
        return {
            "angry": 0.05,
            "disgust": 0.05,
            "fear": 0.05,
            "happy": 0.15,
            "sad": 0.05,
            "surprise": 0.05,
            "neutral": 0.60
        }
    
    def detect_emotions(self, frame):
        """Main emotion detection with enhanced stability"""
        if frame is None:
            return self._get_neutral_output()
        
        self.frame_count += 1
        
        try:
            # Detect face using multiple methods
            bbox = self._detect_face_multi_method(frame)
            
            if bbox is None:
                # Use last known emotions if face not detected
                if self.last_valid_emotions:
                    return {
                        "emotion": max(self.last_valid_emotions, key=self.last_valid_emotions.get),
                        "confidence": 0.3,
                        "negative_score": self._calculate_negative_score(self.last_valid_emotions),
                        "bbox": [0, 0, 0, 0],
                        "probs": self.last_valid_emotions
                    }
                return self._get_neutral_output()
            
            # Extract and preprocess face
            x, y, w, h = bbox
            face_crop = frame[y:y+h, x:x+w]
            
            if face_crop.size == 0:
                return self._get_neutral_output(bbox)
            
            processed_face = self._preprocess_face(face_crop)
            
            # Get FER predictions
            fer_detector = _get_fer_detector()
            if fer_detector is None:
                return self._get_neutral_output(bbox)
            
            results = fer_detector.detect_emotions(processed_face)
            
            if not results:
                return self._get_neutral_output(bbox)
            
            # Get emotion probabilities
            raw_probs = results[0]['emotions']
            
            # Apply temporal smoothing
            stable_probs = self._get_stable_emotions(raw_probs)
            
            # Get dominant emotion and confidence
            max_emotion = max(stable_probs, key=stable_probs.get)
            confidence = stable_probs[max_emotion]
            
            # Calculate negative score
            negative_score = self._calculate_negative_score(stable_probs)
            
            return {
                "emotion": max_emotion,
                "confidence": confidence,
                "negative_score": negative_score,
                "bbox": bbox,
                "probs": stable_probs
            }
            
        except Exception as e:
            print(f"Emotion detection error: {e}")
            return self._get_neutral_output()
    
    def _calculate_negative_score(self, emotions):
        """Calculate negative emotion score"""
        return (0.4 * emotions.get('sad', 0) + 
                0.3 * emotions.get('angry', 0) + 
                0.2 * emotions.get('fear', 0) +
                0.1 * emotions.get('disgust', 0))
    
    def _get_neutral_output(self, bbox=None):
        """Return neutral emotion output"""
        if bbox is None:
            bbox = [0, 0, 0, 0]
        
        neutral_emotions = self._get_neutral_emotions()
        
        return {
            "emotion": "neutral",
            "confidence": 0.6 if bbox != [0, 0, 0, 0] else 0.0,
            "negative_score": 0.075,
            "bbox": bbox,
            "probs": neutral_emotions
        }
    
    def draw_emotion_box(self, frame, result):
        """Draw enhanced bounding box and emotion info"""
        try:
            bbox = result.get('bbox', [0, 0, 0, 0])
            if bbox == [0, 0, 0, 0]:
                return frame
            
            x, y, w, h = bbox
            emotion = result.get('emotion', 'neutral')
            confidence = result.get('confidence', 0.0)
            
            # Draw bounding box with color based on emotion
            color_map = {
                'happy': (0, 255, 0),     # Green
                'sad': (255, 0, 0),       # Blue
                'angry': (0, 0, 255),     # Red
                'fear': (0, 165, 255),    # Orange
                'surprise': (255, 255, 0), # Cyan
                'disgust': (128, 0, 128),  # Purple
                'neutral': (128, 128, 128) # Gray
            }
            
            color = color_map.get(emotion, (0, 255, 0))
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            # Draw emotion label with background
            label = f"{emotion}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.rectangle(frame, (x, y - 25), (x + label_size[0], y), color, -1)
            cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            return frame
        except Exception as e:
            print(f"Draw error: {e}")
            return frame