"""
Emotion Detection Module with Output Formatting

This module implements the modified emotion_detector function that uses IBM Watson's
Natural Language Processing service to analyze emotions in text input and returns
properly formatted output.

The function sends a POST request to the Watson NLU API endpoint with the required
headers, processes the JSON response, and returns emotion scores in a consistent,
formatted structure.
"""

import requests
import json


def emotion_detector(text_to_analyse):
    """
    Analyzes the emotions in the given text using Watson NLP API and returns formatted output.
    
    This function sends a POST request to the Watson Emotion Prediction service
    to identify and score emotions present in the input text. It processes the JSON
    response and returns the results in a properly formatted dictionary structure.
    
    Args:
        text_to_analyse (str): The text to be analyzed for emotions
        
    Returns:
        dict: A dictionary containing the formatted emotion analysis results:
            - anger (float): Emotion score for anger (0.0 to 1.0)
            - disgust (float): Emotion score for disgust (0.0 to 1.0)
            - fear (float): Emotion score for fear (0.0 to 1.0)
            - joy (float): Emotion score for joy (0.0 to 1.0)
            - sadness (float): Emotion score for sadness (0.0 to 1.0)
            - surprise (float): Emotion score for surprise (0.0 to 1.0)
            - dominant_emotion (str): The emotion with the highest score
            
        Returns None values if the API request fails or text is invalid.
        
    Example:
        >>> result = emotion_detector("I love this amazing project!")
        >>> print(result)
        {
            'anger': 0.02,
            'disgust': 0.01,
            'fear': 0.01,
            'joy': 0.95,
            'sadness': 0.01,
            'surprise': 0.00,
            'dominant_emotion': 'joy'
        }
    """
    
    # Watson NLU API URL for emotion prediction
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    # Set up headers for the API request
    # This header specifies the model to use for emotion analysis
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    
    # Prepare the input data in the format expected by Watson NLP API
    # The raw_document structure contains the text to be analyzed
    input_data = {
        "raw_document": {
            "text": text_to_analyse
        }
    }
    
    try:
        # Send POST request to Watson NLP API with the input data and headers
        response = requests.post(url, json=input_data, headers=headers)
        
        # Check if the HTTP request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response from the API
            response_data = response.json()
            
            # Extract the emotion predictions from the response structure
            # The API returns emotionPredictions as a list with emotion data
            emotions = response_data.get('emotionPredictions', [{}])[0].get('emotion', {})
            
            # Extract individual emotion scores from the response
            # Each emotion is scored between 0.0 and 1.0
            anger = emotions.get('anger', 0)
            disgust = emotions.get('disgust', 0)
            fear = emotions.get('fear', 0)
            joy = emotions.get('joy', 0)
            sadness = emotions.get('sadness', 0)
            surprise = emotions.get('surprise', 0)
            
            # Create a dictionary to identify the dominant emotion
            # (the emotion with the highest score)
            emotion_dict = {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness,
                'surprise': surprise
            }
            
            # Find the emotion with the maximum score
            dominant_emotion = max(emotion_dict, key=emotion_dict.get)
            
            # Return the formatted result with all emotions and dominant emotion
            # This ensures consistent output formatting across all calls
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
            # Handle HTTP error responses from the API
            # Return formatted response with None values and error information
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'surprise': None,
                'dominant_emotion': None
            }
            
    except requests.exceptions.ConnectionError:
        # Handle connection errors (network issues, API unavailable)
        # Return formatted response with None values
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'surprise': None,
            'dominant_emotion': None
        }
        
    except requests.exceptions.Timeout:
        # Handle timeout errors (API takes too long to respond)
        # Return formatted response with None values
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'surprise': None,
            'dominant_emotion': None
        }
        
    except requests.exceptions.RequestException as e:
        # Handle other request-related exceptions
        # Return formatted response with None values
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'surprise': None,
            'dominant_emotion': None
        }
        
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        # Handle JSON parsing errors or missing expected keys in response
        # Return formatted response with None values
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'surprise': None,
            'dominant_emotion': None
        }


# ============================================================================
# OUTPUT FORMATTING DEMONSTRATION
# ============================================================================

def format_emotion_output(emotion_result):
    """
    Formats the emotion detection output for display.
    
    Args:
        emotion_result (dict): The result dictionary from emotion_detector()
        
    Returns:
        str: Formatted string representation of emotion analysis
    """
    if emotion_result.get('dominant_emotion') is None:
        return "Unable to determine emotion from the provided text."
    
    # Format the output with clear labeling
    formatted_output = (
        f"Anger: {emotion_result['anger']:.2f}\n"
        f"Disgust: {emotion_result['disgust']:.2f}\n"
        f"Fear: {emotion_result['fear']:.2f}\n"
        f"Joy: {emotion_result['joy']:.2f}\n"
        f"Sadness: {emotion_result['sadness']:.2f}\n"
        f"Surprise: {emotion_result['surprise']:.2f}\n"
        f"\nDominant Emotion: {emotion_result['dominant_emotion']}"
    )
    
    return formatted_output


# Example usage and testing
if __name__ == '__main__':
    print("=" * 70)
    print("EMOTION DETECTION WITH OUTPUT FORMATTING")
    print("=" * 70)
    
    test_texts = [
        "I love this amazing project!",
        "I am angry and frustrated with this situation",
        "This is absolutely disgusting!",
        "I am very sad and depressed",
        "I am frightened and scared",
        "What a wonderful and surprising moment!"
    ]
    
    for text in test_texts:
        print(f"\nInput Text: '{text}'")
        print("-" * 70)
        result = emotion_detector(text)
        formatted = format_emotion_output(result)
        print(formatted)
        print("=" * 70)
