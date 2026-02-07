
import os
import json
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from typing import Dict, List, Optional
from src.models.novelty_detector import NoveltyDetector

class MechanismClassifier:
    def __init__(self, 
                 seed_path: str = "data/mechanism_seeds.json",
                 model_path: str = "data/models/mechanism_clf.pkl"):
        self.seed_path = seed_path
        self.model_path = model_path
        self.detector = NoveltyDetector() # Reusing embedding logic
        self.model = None
        self.label_encoder = None
        
        # Load or Train
        if os.path.exists(self.model_path):
            self._load_model()
        else:
            self.train_classifier_from_seeds()

    def _load_model(self):
        try:
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.label_encoder = data['encoder']
        except Exception as e:
            print(f"Failed to load model: {e}")

    def _save_model(self):
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump({
                'model': self.model,
                'encoder': self.label_encoder
            }, self.model_path)
        except Exception as e:
            print(f"Failed to save model: {e}")

    def train_classifier_from_seeds(self):
        if not os.path.exists(self.seed_path):
            print("Seed file not found.")
            return

        with open(self.seed_path, 'r') as f:
            seeds = json.load(f)

        X = []
        y = []
        
        for item in seeds:
            det = item['determinant']
            cls = item['class']
            
            # For each seed, we need an embedding.
            # We can use the detector's cache if available.
            # Using NoveltyDetector's compute_novelty to trigger embedding fetch/cache
            # But compute_novelty expects determinant name in bank. 
            # We need direct embedding access.
            
            # Check cache directly via detector helper or generate
            embedding = self.detector._get_cached_embedding(det)
            if not embedding:
                # Need sequence. For seeds, we might not have fasta files for all (only ndm1).
                # Need sequence. For seeds without cached embeddings, we need to fetch them.
                # However, without a real sequence database for all seeds, we cannot generate live embeddings.
                # For this Live Mode enforcement, we will skip seeds that lack embeddings/sequences.
                print(f"Skipping seed {det}: No cached embedding and no sequence available.")
                continue
            
            X.append(embedding)
            y.append(cls)

        if not X:
            return

        # Train
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        self.model = LogisticRegression(random_state=42)
        self.model.fit(X, y_encoded)
        
        self._save_model()
        print("Classifier trained and saved.")

    def predict_mechanism(self, sequence: str) -> Dict:
        """
        Predict mechanism class for a raw protein sequence.
        """
        if not self.model:
            # Try training if missing
            self.train_classifier_from_seeds()
            if not self.model:
                return {"error": "Model not available"}

        # Get embedding
        embedding = self.detector.get_embedding(sequence)
        
        # Predict
        # Reshape for sklearn
        vec = np.array(embedding).reshape(1, -1)
        
        # Probabilities
        probs = self.model.predict_proba(vec)[0]
        max_idx = np.argmax(probs)
        confidence = float(probs[max_idx])
        pred_class = self.label_encoder.inverse_transform([max_idx])[0]
        
        return {
            "predicted_class": pred_class,
            "confidence": round(confidence, 3),
            "explanation": f"Embedding pattern consistent with {pred_class} group.",
            "disclaimer": "AI Classifier decision. Research support only."
        }
