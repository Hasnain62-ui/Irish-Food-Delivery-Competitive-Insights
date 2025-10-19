from google_play_scraper import app, reviews, Sort
import pandas as pd
import time

def scrape_playstore_reviews(app_id, app_name, count=500):
    """
    Scrape Google Play Store reviews
    """
    print(f"Scraping {app_name}...")
    
    # Get app details
    app_details = app(app_id, lang='en', country='ie')
    
    # Get reviews
    result, _ = reviews(
        app_id,
        lang='en',
        country='ie',
        sort=Sort.NEWEST,
        count=count
    )
    
    reviews_data = []
    for review in result:
        reviews_data.append({
            'platform': app_name,
            'rating': review['score'],
            'text': review['content'],
            'date': review['at'],
            'thumbsUp': review['thumbsUpCount'],
            'reviewer': review['userName']
        })
    
    df = pd.DataFrame(reviews_data)
    
    # Save
    filename = f'playstore_{app_name.lower().replace(" ", "_")}_reviews.csv'
    df.to_csv(filename, index=False)
    
    print(f"✓ Collected {len(df)} reviews")
    print(f"✓ App rating: {app_details['score']}")
    print(f"✓ Total ratings: {app_details['ratings']}")
    print(f"✓ Saved to: {filename}\n")
    
    return df, app_details

# Main execution
if __name__ == "__main__":
    apps = {
        'Deliveroo': 'com.deliveroo.orderapp',
        'Just Eat': 'com.justeat.app.ie',
        'Uber Eats': 'com.ubercab.eats'
    }
    
    all_reviews = []
    app_stats = []
    
    for app_name, app_id in apps.items():
        df, details = scrape_playstore_reviews(app_id, app_name, count=500)
        all_reviews.append(df)
        
        app_stats.append({
            'platform': app_name,
            'app_rating': details['score'],
            'total_ratings': details['ratings'],
            'installs': details['installs']
        })
        
        time.sleep(2)
    
    # Combine all reviews
    combined_df = pd.concat(all_reviews, ignore_index=True)
    combined_df.to_csv('playstore_all_reviews.csv', index=False)
    
    # Save app statistics
    stats_df = pd.DataFrame(app_stats)
    stats_df.to_csv('playstore_app_statistics.csv', index=False)
    
    print(f"{'='*60}")
    print(f"Total reviews: {len(combined_df)}")
    print(f"Files saved:")
    print(f"  - playstore_all_reviews.csv")
    print(f"  - playstore_app_statistics.csv")
    print(f"{'='*60}")
