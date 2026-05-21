"""
Emotion Detection Module using Watson NLP Library

This module implements the emotion_detector function that uses IBM Watson's
Natural Language Processing service to analyze emotions in text input.

The function sends a POST request to the Watson NLU API endpoint and returns
emotion scores for six emotions: anger, disgust, fear, joy, sadness, and surprise.
"""

import requests
import json


def emotion_detector(text_to_analyse):
    """
    Analyzes the emotions in the given text using Watson NLP API.
    
    This function sends a POST request to the Watson Emotion Prediction service
    to identify and score emotions present in the input text.
    
    Args:
        text_to_analyse (str): The text to be analyzed for emotions
        
    Returns:
        dict: A dictionary containing:
            - anger: float (emotion score 0-1)
            - disgust: float (emotion score 0-1)
            - fear: float (emotion score 0-1)
            - joy: float (emotion score 0-1)
            - sadness: float (emotion score 0-1)
            - surprise: float (emotion score 0-1)
            - dominant_emotion: str (emotion with highest score)
            
    Example:
        >>> result = emotion_detector("I love this!")
        >>> print(result['dominant_emotion'])
        'joy'
    """
    
    # Watson NLU API URL for emotion prediction
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    # Set up headers for the API request
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    
    # Prepare the input data with proper format
    input_data = {
        "raw_document": {
            "text": text_to_analyse
        }
    }
    
    try:
        # Send POST request to Watson NLP API
        response = requests.post(url, json=input_data, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            response_data = response.json()
            
            # Extract emotion predictions from the response
            emotions = response_data.get('emotionPredictions', [{}])[0].get('emotion', {})
            
            # Initialize emotion scores
            anger = emotions.get('anger', 0)
            disgust = emotions.get('disgust', 0)
            fear = emotions.get('fear', 0)
            joy = emotions.get('joy', 0)
            sadness = emotions.get('sadness', 0)
            surprise = emotions.get('surprise', 0)
            
            # Determine dominant emotion (emotion with highest score)
            emotion_dict = {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness,
                'surprise': surprise
            }
            
            dominant_emotion = max(emotion_dict, key=emotion_dict.get)
            
            # Return emotion scores and dominant emotion
            return {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness,
                'surprise': surprise,
                'dominant_emotion': dominant_emotion
            }
        else:
            # Handle API error response
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'surprise': None,
                'dominant_emotion': None,
                'error': f'API request failed with status code {response.status_code}'
            }
            
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (connection errors, timeouts, etc.)
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'surprise': None,
            'dominant_emotion': None,
            'error': f'Request failed: {str(e)}'
        }
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        # Handle JSON parsing errors
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'surprise': None,
            'dominant_emotion': None,
            'error': f'Error parsing response: {str(e)}'
        }


# Example usage and testing
if __name__ == '__main__':
    # Test the emotion_detector function with sample texts
    
    test_texts = [
        "I love this!",
        "I am angry and frustrated",
        "This is disgusting!",
        "I am very sad",
        "I am scared!",
        "What a wonderful surprise!"
    ]
    
    print("=" * 70)
    print("EMOTION DETECTION TEST RESULTS")
    print("=" * 70)
    
    for text in test_texts:
        result = emotion_detector(text)
        print(f"\nText: '{text}'")
        print(f"Emotions: {result}")
        print(f"Dominant Emotion: {result.get('dominant_emotion')}")
        print("-" * 70)
