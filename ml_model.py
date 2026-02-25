from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib
import os


class MLModel:
    """Simple machine learning model for scam detection using Logistic Regression."""
    
    def __init__(self, model_path: str = "model.pkl"):
        """Initialize and train the model with built-in dataset or load from file."""
        self.model_path = model_path
        
        # Check if saved model exists
        if os.path.exists(self.model_path):
            # Load existing model
            self.pipeline = joblib.load(self.model_path)
        else:
            # Train new model
            self._train_model()
            # Save the trained model
            joblib.dump(self.pipeline, self.model_path)
    
    def _train_model(self):
        """Train the model with built-in dataset."""
        # Built-in training dataset
        scam_messages = [
            "URGENT! Your bank account has been suspended. Verify now to avoid penalties.",
            "Congratulations! You won the lottery! Click here to claim your prize immediately.",
            "Your credit card will be blocked. Confirm your details now.",
            "Act fast! Limited time offer. Send money to claim your reward.",
            "ALERT: Suspicious activity detected. Verify your account immediately or face legal action.",
            "You have been selected for a cash prize. Reply with your bank details.",
            "Your package is pending. Pay customs fee now to receive delivery.",
            "Final notice: Your account will be closed. Click link to verify identity.",
            "Urgent security alert! Update your password now by clicking this link.",
            "You owe money. Pay immediately to avoid court action and penalties."
        ]
        
        legitimate_messages = [
            "Hi, are we still meeting for lunch tomorrow at noon?",
            "Thanks for your help with the project. I really appreciate it.",
            "Can you send me the report when you get a chance?",
            "Happy birthday! Hope you have a wonderful day.",
            "The meeting has been rescheduled to 3 PM on Friday.",
            "I'll be running a few minutes late. See you soon.",
            "Great job on the presentation today. Well done!",
            "Do you want to grab coffee this weekend?",
            "I sent you the documents via email. Let me know if you need anything else.",
            "Looking forward to working with you on this project."
        ]
        
        # Combine messages and create labels (1 = scam, 0 = legitimate)
        messages = scam_messages + legitimate_messages
        labels = [1] * len(scam_messages) + [0] * len(legitimate_messages)
        
        # Create a pipeline with TF-IDF vectorizer and Logistic Regression
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=100, stop_words='english')),
            ('classifier', LogisticRegression(random_state=42, max_iter=200))
        ])
        
        # Train the model
        self.pipeline.fit(messages, labels)
    
    def predict_probability(self, message: str) -> float:
        """
        Predict the probability that a message is a scam.
        
        Args:
            message: The message text to analyze
            
        Returns:
            Probability between 0 and 1 (higher = more likely to be scam)
        """
        if not message:
            return 0.0
        
        # Get probability for scam class (class 1)
        probability = self.pipeline.predict_proba([message])[0][1]
        
        return round(probability, 2)
    
    def retrain(self, scam_messages: list, legitimate_messages: list):
        """
        Retrain the model with new data.
        
        Args:
            scam_messages: List of scam message strings
            legitimate_messages: List of legitimate message strings
        """
        # Combine messages and create labels
        messages = scam_messages + legitimate_messages
        labels = [1] * len(scam_messages) + [0] * len(legitimate_messages)
        
        # Retrain the pipeline
        self.pipeline.fit(messages, labels)
        
        # Save the retrained model
        joblib.dump(self.pipeline, self.model_path)
        
        print(f"Model retrained with {len(messages)} samples and saved to {self.model_path}")
