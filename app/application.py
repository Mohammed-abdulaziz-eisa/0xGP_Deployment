# Import necessary libraries

# Flask related imports
from flask import render_template, request, jsonify, Flask

# Bioinformatics related imports
from Bio import pairwise2

# HTTP requests
import requests

# Data processing and machine learning imports
import pandas as pd
from sklearn.preprocessing import MaxAbsScaler
from sklearn.feature_extraction.text import CountVectorizer
import lightgbm as lgb

# Sparse matrices and serialization
import pickle as pkl

# Error handling and threading
import traceback as tb
import threading
import time


application = Flask(__name__, template_folder='../templates', static_folder='../static')
API_URL = 'https://dna-testing-system-jl95.onrender.com/api/EisaAPI'

def needleman_wunsch_similarity(seq1, seq2, match_score=3, mismatch_penalty=-1, gap_penalty=-2):
    alignments = pairwise2.align.globalms(seq1, seq2, match_score, mismatch_penalty, gap_penalty, gap_penalty)
    """
    Calculates the similarity score between two sequences using the Needleman-Wunsch algorithm.

    Parameters:
        seq1 (str): First DNA sequence.
        seq2 (str): Second DNA sequence.
        match_score (int, optional): Score for matches. Defaults to 3.
        mismatch_penalty (int, optional): Penalty for mismatches. Defaults to -1.
        gap_penalty (int, optional): Penalty for gaps. Defaults to -2.

    Returns:
        float: Similarity score between the two sequences.
    """
    if not alignments:
        return 0.0
    best_alignment = alignments[0] # Highest score alignment 
    alignment_score = best_alignment[2]  # Score of the best alignment
    max_score = max(len(seq1), len(seq2)) * match_score  # Score of the maximum alignment
    similarity_score = alignment_score / max_score  # Calculate the similarity score
    # Return the similarity score
    return similarity_score 



def retrieve_dna_sequence_from_file(file, max_length=2000):
    """
    Retrieves DNA sequence data from a file, respecting a maximum length constraint.
    
    Parameters:
        file (file object): A file object containing DNA sequence data.
        max_length (int, optional): The maximum length of DNA sequence to retrieve. Defaults to 2000.
    Returns:
        str: DNA sequence data extracted from the file, truncated to `max_length` if necessary.
    """
    data = b''  # Initialize as bytes
    total_length = 0
    # Read the file line by line
    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace
        if line.startswith(b'>'):   # Check if the line is a header line (starts with '>')
            continue 
        remaining_length = max_length - total_length
        if remaining_length <= 0:
            break  # Exit loop if the limit is reached
        # Append data to the byte string, truncating if necessary
        data += line[:remaining_length]
        total_length += min(len(line), remaining_length)    # Update the total length
    return data.decode()  # Decode the byte string to a regular string and return it

def retrieve_api_data(API_URL):
    """
    Retrieve data from an API.

    Parameters:
        API_URL (str): The URL of the API.
    Returns:
        dict: The API response data, or an error message if the request fails.
    """
    try:
        # Make a GET request to the API
        response = requests.get(API_URL)
        # Check the status code of the response
        if response.status_code == 200:
            # return the response as a dictionary
            api_data = response.json()
            # Check if the response is in the expected format
            if not isinstance(api_data, dict) or 'population' not in api_data:
                # Return an error message if the response is not in the expected format or missing required keys
                return {"error": "API response is not in the expected format."}
            else:
                # Return the response as a dic
                return api_data
        else:
            # Return an error message if the response status code is not 200
            return {"error": "Failed to retrieve data from API"}
    # Catch any exceptions 
    except Exception as e:
        # Return an error message if the request fails    
        return {"error": str(e)}

# worker 

def worker():
    print("Starting worker")
    print(threading.current_thread().name)
    time.sleep(50)
    print("Exiting worker")
    
 # Home page
@application.route('/')
def home_page():
    return render_template('index.html')

# Compare page

@application.route('/compare')
def compare_page():
    """
    Renders the compare page.

    Parameters:
        None.
    """
    return render_template('compare.html')

@application.route('/compare', methods=['POST'])
def compare():
    """
    upload two files and compare them using the needleman_wunsch_similarity function 
    if the files are not uploaded or if the files are empty, return an error message

    Parameters:
        None.
        
    Returns:
        A JSON response with the similarity percentage, match status, and message.: dict
        A JSON response with an error message if the files are not uploaded or if the files are empty.: dict 
    """
    if 'file_a' not in request.files or 'file_b' not in request.files:
        return jsonify({
            "message": "Please upload a file for both DNA sequences.",
            "statusCode": 401
        })

    file_a = request.files['file_a']
    file_b = request.files['file_b']
    
    if file_a.filename == '' or file_b.filename == '':
        return jsonify({
            "message": "Please upload non-empty files for both DNA sequences.",
            "statusCode": 401
        })

    sequence_a = retrieve_dna_sequence_from_file(file_a)
    sequence_b = retrieve_dna_sequence_from_file(file_b)

    similarity_score = needleman_wunsch_similarity(sequence_a, sequence_b)
    similarity_percentage = round(similarity_score * 100)
    match_status = "DNA MATCH" if similarity_score == 1 else "DNA Not MATCH"  # Adjust threshold as needed

    return jsonify({
        "similarity_percentage": similarity_percentage,
        "match_status": match_status,
        "message": "Successful Comparison",
        "statusCode": 200
    })

# Define a generator function to periodically send data to keep the connection alive
@application.route('/identify')
def result():
    return render_template('identify.html')

@application.route('/identify', methods=['POST'])
def identify():
    # Check if 'file' parameter is provided in the request
    if 'file' not in request.files:
        return jsonify({
            "message": "Please upload a file of DNA sequences.",
            "statusCode": 401
        }), {'Connection': 'keep-alive'}

    # Get the uploaded file from the form
    file_a = request.files['file']
    if file_a.filename == '':
        return jsonify({
            "message": "Please upload a non-empty file for the DNA sequence.",
            "statusCode": 401
        }), {'Connection': 'keep-alive'}

    selected_status = request.form.get('status')

    # Retrieve API data
    api_data = retrieve_api_data(API_URL)
    if 'error' in api_data:
        return jsonify({
            "message": api_data['error'],
            "statusCode": 401
        }), {'Connection': 'keep-alive'}
    # Retrieve DNA sequence from the uploaded file
    sequence_a = retrieve_dna_sequence_from_file(file_a, max_length=2000)
    # Initialize variables for match information
    matches = []
    similarity_threshold = 1  # Threshold for similarity score (e.g., 99%)
    match_status = "No match found"

    # Extract necessary keys for match information
    info_keys = ['name', 'status', 'description', 'createdAt', 'updatedAt', 
                 'address', 'national_id', 'phone', 'gender', 'birthdate', 'bloodType']

    # Check if API data is a dictionary and contains 'population' key
    if isinstance(api_data, dict) and 'population' in api_data:
        # Filter API data based on selected status
        if selected_status == 'all':
            filtered_data = api_data['population']
        else:
            valid_statuses = ['missing', 'acknowledged', 'crime', 'disaster']
            if selected_status not in valid_statuses:
                return jsonify({
                    "message":
                        "Invalid status. Please select one of: 'missing', 'acknowledged', 'crime', 'disaster' or 'all' to search in all database.",
                    "statusCode": 400
                }), {'Connection': 'keep-alive'}
            filtered_data = [entry for entry in api_data['population'] if entry.get('status') == selected_status]

        for entry in filtered_data:
            if 'DNA_sequence' in entry:
                # Retrieve DNA sequence for comparison
                sequence_b = entry['DNA_sequence'][:2000]
                # Calculate similarity score
                similarity_score = needleman_wunsch_similarity(sequence_a, sequence_b)
                similarity_percentage = round(similarity_score * 100)
                print(f"Comparing with {entry.get('name', 'unknown')} - Similarity Score: {similarity_score}, Similarity Percentage: {similarity_percentage}%")
                # Check if similarity score meets the threshold
                if similarity_score == similarity_threshold:
                    # Extract match information
                    match_info = {key: entry[key] for key in info_keys if key in entry}
                    matches.append(match_info)
                    if similarity_percentage == 100:
                        # Stop the search if a perfect match is found
                        break
    # Check if there are any matches found
    if matches:
        response = jsonify({
            "matches": match_info,
            "similarity_percentage": similarity_percentage,
            "match_status": "DNA MATCH",
            "message": "Successful identification",
            "statusCode": 200
        })
    else:
        response = jsonify({
            "message": "Successful identification",
            "match_status": "DNA NOT MATCH",
            "statusCode": 200
        })
    # Set the connection header to keep-alive
    response.headers['Connection'] = 'keep-alive'
    return response

@application.route('/missing', methods=['GET', 'POST'])
def missing():
    if request.method == 'GET':
        return render_template('missing.html')

    if 'file' not in request.files:
        return jsonify({
            "message": "Please upload a file of DNA sequences.",
            "statusCode": 401
        }), {'Connection': 'keep-alive'}

    file_a = request.files['file']
    if file_a.filename == '':
        return jsonify({
            "message": "Please upload a non-empty file for the DNA sequence.",
            "statusCode": 401
        }), {'Connection': 'keep-alive'}

    sequence_a = retrieve_dna_sequence_from_file(file_a, max_length=2000)
    api_data = retrieve_api_data(API_URL)
    if 'error' in api_data:
        return jsonify({
            "message": api_data['error'],
            "statusCode": 401
        }), {'Connection': 'keep-alive'}

    match_info = {}
    potential_children_info = []
    info_keys = ['name', 'status', 'description', 'createdAt', 'updatedAt', 
                 'address', 'national_id', 'phone', 'gender', 'birthdate', 'bloodType']
    SIMILARITY_THRESHOLD = 100
    SIMILARITY_THRESHOLD_CHILD = 96
    
    
    if isinstance(api_data, dict) and 'population' in api_data:
        for entry in api_data['population']:
            if 'DNA_sequence' in entry:
                sequence_b = entry['DNA_sequence'][:2000]
                similarity_score = needleman_wunsch_similarity(sequence_a, sequence_b)
                similarity_percentage = round(similarity_score * 100)

                print(f"Comparing with {entry.get('name', 'unknown')} - Similarity Score: {similarity_score}, Similarity Percentage: {similarity_percentage}%")

                if similarity_percentage == SIMILARITY_THRESHOLD:
                    match_info = {key: entry[key] for key in info_keys if key in entry}
                    match_info["similarity_percentage"] = similarity_percentage
                    match_info["match_status"] = "DNA MATCH"
                   
                if similarity_percentage >= SIMILARITY_THRESHOLD_CHILD :
                    child_info = {key: entry[key] for key in info_keys if key in entry}
                    potential_children_info.append({
                        "relative_data": child_info
                    })

    if match_info:
        main_national_id = match_info.get("national_id")
        potential_children_info = [child for child in potential_children_info if child["relative_data"].get("national_id") != main_national_id]

        if potential_children_info:
            return jsonify({
                "main_match_info": match_info,
                "potential_relative_info": potential_children_info,
                "message": "Successful identification",
                "statusCode": 200
            })
        else:
            return jsonify({
                "main_match_info": match_info,
                "potential_relative_info": None,
                "message": "Successful identification",
                "statusCode": 200
            })
    elif not potential_children_info and not match_info:
        return jsonify({
            "main_match_info": None,
            "potential_relative_info": None,
            "message": "No match found.",
            "statusCode": 200
        }), {'Connection': 'keep-alive'}
        
    else: 
            return jsonify({
                "main_match_info": None,
                "potential_relative_info": potential_children_info,
                "message": "Founded a potential relative.",
                "statusCode": 200
            }), {'Connection': 'keep-alive'}

def pickle_deserialize_object(file_path_name):
    """Deserializes the object from the given path"""
    data_object = None
    try:
        with open(file_path_name, "rb") as data_infile:
            data_object = pkl.load(data_infile)
    except Exception as e:
        print(f"Error occurred while deserializing object: {e}")
        tb.print_exc()
    return data_object
# Load models and vectorizers at startup
try:
    vectorizer = pickle_deserialize_object("../models/vectorizer.pkl")
    model = pickle_deserialize_object("../models/finalized_model_lgb.pkl")
    scaler = pickle_deserialize_object("../models/scaler.pkl")
except Exception as e:
    print(f"Error loading model/vectorizer: {e}")

#Helper functions from doctor bonat script 
def k_mer_words_original(dna_sequence_string, k_mer_length=7):
    return [dna_sequence_string[x:x + k_mer_length].lower() for x in range(len(dna_sequence_string) - k_mer_length + 1)]

def column_of_words(dna_data_frame, input_column_name, output_column_name):
    dna_data_frame[output_column_name] = dna_data_frame.apply(lambda x: k_mer_words_original(x[input_column_name]), axis=1)
    dna_data_frame = dna_data_frame.drop(input_column_name, axis=1)
    return dna_data_frame

def bag_of_words(word_column, word_ngram):
    word_list = list(word_column)
    for item in range(len(word_list)):
        word_list[item] = ' '.join(word_list[item])
    count_vectorizer = CountVectorizer(ngram_range=(word_ngram, word_ngram))
    X = count_vectorizer.fit_transform(word_list)
    return X


def pickle_deserialize_object(file_path_name):
    """
    Deserialize an object from a file using pickle.
    
    Args:
        file_path_name (str): The path and name of the file from which the object will be loaded.
    
    Returns:
        object: The deserialized object. Returns None if deserialization fails.
    
    Raises:
        Exception: If there is any error during the deserialization process.
    """
    data_object = None
    try:
        with open(file_path_name, "rb") as data_infile:
            data_object = pkl.load(data_infile)
    except Exception as e:
        print(f"Error occurred while deserializing object: {e}")
        tb.print_exc()
    return data_object

# Helper functions from Model script 
def generate_k_mers(sequence, k):
    return [sequence[i:i+k] for i in range(len(sequence)-k+1)]
@application.route('/predict', methods=['GET'])
def home():
    return render_template('predict.html')
@application.route('/predict', methods=['POST'])
  
def predict():

    if 'file_a' not in request.files or 'file_b' not in request.files:
        return jsonify({
            "message": "Please upload a file for both DNA sequences.",
            "statusCode": 401
        })

    file_a = request.files['file_a']
    file_b = request.files['file_b']
    
    if file_a.filename == '' or file_b.filename == '':
        return jsonify({
            "message": "Please upload non-empty files for both DNA sequences.",
            "statusCode": 401
        })

    parent_dna = retrieve_dna_sequence_from_file(file_a)
    child_dna = retrieve_dna_sequence_from_file(file_b)
    # Generate k-mers
    k = 7
    parent_kmers = ' '.join(generate_k_mers(parent_dna, k))
    child_kmers = ' '.join(generate_k_mers(child_dna, k))
    # Vectorize sequences
    try:
        parent_vector = vectorizer.transform([parent_kmers]).toarray()
        child_vector = vectorizer.transform([child_kmers]).toarray()
    except Exception as e:
        return jsonify({'error': f'Error in vectorization: {e}'}), 500
    # Concatenate features
    X_parent_new = pd.DataFrame(parent_vector)
    X_child_new = pd.DataFrame(child_vector)
    features = pd.concat([X_parent_new, X_child_new], axis=1)
    # Scale features
    try:
        features = scaler.transform(features)
    except Exception as e:
        return jsonify({'error': f'Error in scaling features: {e}'}), 500
    # Make a prediction
    try:
        prediction = model.predict(features)
    except Exception as e:
        return jsonify({'error': f'Error in making prediction: {e}'}), 500 
    result = 'relative' if prediction[0] == 1 else 'not relative'
    if result == 'relative':
        return jsonify({
            'prediction': result,
            "message": "Successful Prediction",
            "statusCode": 200,
        })
    else :
        return jsonify({
            'prediction': result,
            "message": "Successful Prediction",
            "statusCode": 200,
        })
if __name__ == "__main__":
    application.run(debug=True)

