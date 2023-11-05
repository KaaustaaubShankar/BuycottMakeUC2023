"""
A sample Hello World server.
"""
import os
from flask import Flask, jsonify, request
import requests
import pandas as pd
from fuzzywuzzy import fuzz, process
from io import BytesIO
from google.cloud import storage
app = Flask(__name__)

@app.route("/")
def home():
    return "This is the home page"
storage_client = storage.Client()
def load_csv_from_gcs(bucket_name, blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    byte_stream = BytesIO()
    blob.download_to_file(byte_stream)
    byte_stream.seek(0)
    return pd.read_csv(byte_stream)

@app.route("/companyname", methods=["GET"])
def getCompanyName():
    barcode = request.args.get('barcode')
    url = f"https://go-upc.com/api/v1/code/{barcode}?key=9b027748e412b688f7b3a6d8bb70d2f4e4b357cbb35ee929137a4e846455939e&format=true"
    parameters = {
        "query": barcode,
        "mode": "artlist",
        "format": "json"
    }
    response = requests.get(url, params=parameters)
    result = response.json()
    companyName = result["product"]["brand"]
    companyName_1 = str(companyName)
    parentCompany = ""
    coca_cola_brands = {
    "Sprite": "Coca-Cola",
    "Fanta": "Coca-Cola",
    "Diet Coke": "Coca-Cola",
    "Coca-Cola Zero Sugar": "Coca-Cola",
    "Minute Maid": "Coca-Cola",
    "Powerade": "Coca-Cola",
    "Dasani": "Coca-Cola",
    "Vitaminwater": "Coca-Cola",
    "Simply Orange": "Coca-Cola",
    "Fresca": "Coca-Cola",
    "Smartwater": "Coca-Cola",
    "Fuze Beverage": "Coca-Cola",
    "Honest Tea": "Coca-Cola",
    "Odwalla": "Coca-Cola",
    "Fairlife": "Coca-Cola",
    "Costa Coffee": "Coca-Cola", # Note that Costa Coffee was acquired by Coca-Cola.
    "Barq's": "Coca-Cola",
    "Del Valle": "Coca-Cola",
    "Ayataka": "Coca-Cola",
    "Georgia Coffee": "Coca-Cola",
    "Gold Peak Tea": "Coca-Cola",
    "Innocent Drinks": "Coca-Cola",
    "Peace Tea": "Coca-Cola"
    } 
    if companyName in coca_cola_brands.keys():
        parentCompany = "Coca-Cola"
    
    pepsico_brands = {
    "Pepsi": "PepsiCo",
    "Mountain Dew": "PepsiCo",
    "Lay's": "PepsiCo",
    "Gatorade": "PepsiCo",
    "Tropicana": "PepsiCo",
    "7 Up": "PepsiCo",
    "Doritos": "PepsiCo",
    "Cheetos": "PepsiCo",
    "Quaker": "PepsiCo",
    "Bubly": "PepsiCo",
    "Aquafina": "PepsiCo",
    "Brisk": "PepsiCo",
    "Fritos": "PepsiCo",
    "Ruffles": "PepsiCo",
    "SoBe": "PepsiCo",
    "Mirinda": "PepsiCo",
    "Stacy's": "PepsiCo",
    "Sierra Mist": "PepsiCo",
    "Walkers": "PepsiCo",
    "Sabritas": "PepsiCo",
    "Smith's": "PepsiCo",
    "Mug Root Beer": "PepsiCo",
    "Kurkure": "PepsiCo",
    "Naked Juice": "PepsiCo",
    "Sun Chips": "PepsiCo",
    "Rockstar Energy": "PepsiCo",
    "KeVita": "PepsiCo",
    "Lipton" : "PepsiCo"  # Joint venture partnership with Unilever for ready-to-drink beverages.
    }

    if companyName in pepsico_brands.keys():
        parentCompany = "PepsiCo"
    pg_brands = {
    "Pampers": "Proctor Gamble",
    "Tide": "Proctor Gamble",
    "Gillette": "Proctor Gamble",
    "Ariel": "Proctor Gamble",
    "Pantene": "Proctor Gamble",
    "Bounty": "Proctor Gamble",
    "Charmin": "Proctor Gamble",
    "Crest": "Proctor Gamble",
    "Oral-B": "Proctor Gamble",
    "Head & Shoulders": "Proctor Gamble",
    "Febreze": "Proctor Gamble",
    "Olay": "Proctor Gamble",
    "Always": "Proctor Gamble",
    "Old Spice": "Proctor Gamble",
    "Dawn": "Proctor Gamble",
    "Gain": "Proctor Gamble",
    "Vicks": "Proctor Gamble",
    "Secret": "Proctor Gamble",
    "Herbal Essences": "Proctor Gamble",
    "Mr. Clean": "Proctor Gamble",
    "Swiffer": "Proctor Gamble",
    "Braun": "Proctor Gamble",
    "SK-II": "Proctor Gamble",
    }
    if companyName in pg_brands:
        parentCompany = "Proctor Gamble"
    nestle_brands = {
        "Nescafe": "Nestle",
        "KitKat": "Nestle",
        "Nestea": "Nestle",
        "Perrier": "Nestle",
        "San Pellegrino": "Nestle",
        "Maggi": "Nestle",
        "Stouffer's": "Nestle",
        "Gerber": "Nestle",
        "Purina": "Nestle",
        "Haagen-Dazs": "Nestle",  # In the United States, Nestle licenses the Häagen-Dazs brand to Froneri, a joint venture Nestle has a stake in.
        "Nespresso": "Nestle",
        "Nestle Pure Life": "Nestle",
        "Smarties": "Nestle",
        "Cheerios": "Nestle",  # Outside the United States, Canada and Spain.
        "Shreddies": "Nestle",
        "Lean Cuisine": "Nestle",
        "Dreyer's": "Nestle",
        "Hot Pockets": "Nestle",
        "DiGiorno": "Nestle",
        "Toll House": "Nestle",
        "Carnation": "Nestle",
        "Milo": "Nestle",
        "Nido": "Nestle",
        "La Laitière": "Nestle",
        "Buitoni": "Nestle",
        "Friskies": "Nestle",
        "Poland Spring": "Nestle",
        "Vittel": "Nestle",
        "Aero": "Nestle",
        "Rolo": "Nestle",  # Outside the United States.
        "Quality Street": "Nestle",
        "Coffee-Mate": "Nestle",
        "Fancy Feast": "Nestle",
    }
    if companyName in nestle_brands:
        parentCompany = "Nestle"


    # Define the company name you have
    if parentCompany == "":
        company_name = companyName
    else:
        companyName = parentCompany

    

    
     # Load your CSV data
    company_name = companyName
    bucket_name = os.getenv('GCS_BUCKET_NAME', 'tagged-all')
    blob_name = os.getenv('GCS_CSV_FILE_PATH', 'tagged_all.csv')


    df = load_csv_from_gcs(bucket_name, blob_name)
    # Create a list of unique company names from your DataFrame
    unique_company_names = df['company_name'].unique()

    # Find the most similar company name using fuzzy matching
    most_similar_name, similarity_score = process.extractOne(company_name, unique_company_names, scorer=fuzz.token_sort_ratio)

    # Set a similarity threshold (you can adjust this value)
    threshold = 75

    if similarity_score >= threshold:
        # If the similarity score is above the threshold, consider it a match
        company_var = most_similar_name
    else:
        print(f"No similar company name found for '{company_name}'.")
        result_dict = {
            "Company Name": "Unknown_company",
            "Sentiment": "Neutral",
            "Percentage": {
                "P": 1.0,
                "I": 1.0,
                "N": 1.0
            },
            "Confidence": 1.0,
        }
        return result_dict

    # Continue with the rest of your code using company_var
    filtered_df = df[df['company_name'] == company_var]
    if not filtered_df.empty:
        # Group by sentiment and count the number of rows in each group
        sentiment_counts = filtered_df.groupby('sentiment').size().reset_index(name='count')

        # Find the sentiment with the maximum count
        max_sentiment = sentiment_counts.loc[sentiment_counts['count'].idxmax()]['sentiment']

        # Filter the DataFrame to include only rows with the max_sentiment
        filtered_df_max_sentiment = filtered_df[filtered_df['sentiment'] == max_sentiment]

        # Calculate the percentage values
        total_rows = len(filtered_df_max_sentiment)
        # Calculate the Pro-Palestine and Pro-Israel percentages with one decimal place rounding down
        pro_palestine_percentage = len(filtered_df_max_sentiment[filtered_df_max_sentiment['sentiment'] == 'Pro-Palestine']) / total_rows * 100
        pro_israel_percentage = len(filtered_df_max_sentiment[filtered_df_max_sentiment['sentiment'] == 'Pro-Israel']) / total_rows * 100

        # Calculate the Neutral/Complex percentage, which is 100 minus the sum of the other two percentages
        # And then round to one decimal place
        neutral_complex_percentage = 100 - (pro_palestine_percentage + pro_israel_percentage)


        # Specify the number of rows to process
        num_rows_to_process = 10  # Adjust this value to the desired number of rows

        # Limit the number of rows in filtered_df_max_sentiment
        filtered_df_max_sentiment = filtered_df_max_sentiment.head(num_rows_to_process)

        # Calculate the "Confidence" field as the higher value between positive_confidence_percent and negative_confidence_percent
        confidence_values = filtered_df_max_sentiment[['positive_confidence_percent', 'negative_confidence_percent']].max(axis=1)

        # Create the result dictionary
        result_dict = {
            "Company Name": company_var,
            "Sentiment": max_sentiment,
            "Percentage": {
                "P": pro_palestine_percentage,
                "I": pro_israel_percentage,
                "N": neutral_complex_percentage
            },
            "Confidence": confidence_values.max(),
        }

        # Repeat the "Title" and "URL" fields for each row
        for i in range(num_rows_to_process):
            result_dict[f"Title_{i+1}"] = filtered_df_max_sentiment['title'].values[i]
            result_dict[f"URL_{i+1}"] = filtered_df_max_sentiment['url'].values[i]

       #return the json through internet
        result_dict["Company Name"] = companyName_1 + " ("+parentCompany+")"
        return result_dict
    else:
        print("No data matching the filter criteria.")
    
if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')