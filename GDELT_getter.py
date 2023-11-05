import requests
import csv

def get_sentiment_queries(query, tone, max_results, sort_order):
    api_url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query} sourcelang:english&tone:{tone}&maxrecords={max_results}&sort={sort_order}&format=json"
    
    # Make the API request
    response = requests.get(api_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Parse the response as JSON
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to save articles to CSV
def save_to_csv(articles, filename):
    if not articles:
        print(f"No articles to save for {filename}.")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        # Assuming articles is a list of dictionaries
        keys = articles[0].keys()
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(articles)

max_results = 150


def get_and_save_sentiment_queries(file_with_companies):
    with open(file_with_companies, 'r') as file:
        company_names = file.read().splitlines()

    # Initialize lists to hold all articles for each sentiment
    all_negative_articles = []
    all_positive_articles = []

    for company in company_names:
        query = f'{company} AND (Palestine OR Israel)'
        max_results = 50

        # Get negative sentiment queries sorted by HybridRelMag and tone in descending order
        negative_sentiment_data = get_sentiment_queries(query, '<0', max_results, 'tonedesc,HybridRelMag')
        if negative_sentiment_data and 'articles' in negative_sentiment_data:
            for article in negative_sentiment_data['articles']:
                article['company_name'] = company
            all_negative_articles.extend(negative_sentiment_data['articles'])

        # Get positive sentiment queries sorted by HybridRelMag and tone in ascending order
        positive_sentiment_data = get_sentiment_queries(query, '>0', max_results, 'toneasc,HybridRelMag')
        if positive_sentiment_data and 'articles' in positive_sentiment_data:
            for article in positive_sentiment_data['articles']:
                article['company_name'] = company
                print(company)
            all_positive_articles.extend(positive_sentiment_data['articles'])

    # Save all negative articles to a single CSV file
    negative_csv_filename = 'negative_sentiment_articles.csv'
    save_to_csv(all_negative_articles, negative_csv_filename)
    print(f"All negative sentiment articles saved to {negative_csv_filename}")

    # Save all positive articles to a single CSV file
    positive_csv_filename = 'positive_sentiment_articles.csv'
    save_to_csv(all_positive_articles, positive_csv_filename)
    print(f"All positive sentiment articles saved to {positive_csv_filename}")

get_and_save_sentiment_queries(r'C:\Users\Hackathon\Desktop\F_100.txt')