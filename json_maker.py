import pandas as pd
from fuzzywuzzy import fuzz, process
import json

# Define the company name you have
company_name = "McDonald's"

# Load your CSV data
df = pd.read_csv(r"C:\Users\Hackathon\Desktop\tagged_all.csv")
unique_company_names = df['company_name'].unique()
most_similar_name, similarity_score = process.extractOne(company_name, unique_company_names, scorer=fuzz.token_sort_ratio)
threshold = 80
if similarity_score >= threshold:
    # If the similarity score is above the threshold, consider it a match
    company_var = most_similar_name
else:
    print(f"No similar company name found for '{company_name}'.")
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
    pro_palestine_percentage = int(len(filtered_df_max_sentiment[filtered_df_max_sentiment['sentiment'] == 'Pro-Palestine']) / total_rows * 100)
    pro_israel_percentage = int(len(filtered_df_max_sentiment[filtered_df_max_sentiment['sentiment'] == 'Pro-Israel']) / total_rows * 100)
    neutral_complex_percentage = int(len(filtered_df_max_sentiment[filtered_df_max_sentiment['sentiment'].isin(['Neutral', 'Complex'])]) / total_rows * 100)

    # Specify the number of rows to process
    num_rows_to_process = 3  # Adjust this value to the desired number of rows

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

    # Save the dictionary as a JSON file
    #result = json.dumps(result_dict, indent=4)
    print(type(result_dict))
    print(result_dict)

    print("Filtered data saved as 'filtered_data.json'")
else:
    print("No data matching the filter criteria.")
