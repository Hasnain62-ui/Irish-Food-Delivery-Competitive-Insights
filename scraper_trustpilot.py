import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_trustpilot_reviews(company_url, platform_name, max_pages=15):
    """
    Updated scraper with correct Trustpilot HTML structure (2025)
    """
    reviews_data = []
    base_url = f"https://ie.trustpilot.com/review/{company_url}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        print(f"  Page {page}...", end='', flush=True)
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Updated selectors for 2025 Trustpilot structure
            # Try multiple possible selectors
            reviews = soup.find_all('article', {'class': lambda x: x and 'review' in x.lower()})
            
            if not reviews:
                # Alternative selector
                reviews = soup.find_all('div', {'data-service-review-card-paper': True})
            
            if not reviews:
                # Try another selector
                reviews = soup.find_all('section', {'class': lambda x: x and 'review' in x.lower()})
            
            if not reviews:
                print(f" ✗ No reviews found")
                break
            
            print(f" ✓ {len(reviews)} reviews", flush=True)
            
            for review in reviews:
                try:
                    # Extract rating (multiple methods)
                    rating = 0
                    rating_elem = review.find('div', {'data-service-review-rating': True})
                    if rating_elem:
                        rating = int(rating_elem.get('data-service-review-rating', 0))
                    else:
                        # Alternative: count stars
                        stars = review.find_all('img', {'alt': lambda x: x and 'star' in x.lower()})
                        if stars:
                            rating_text = stars[0].get('alt', '0')
                            rating = int(rating_text.split()[0]) if rating_text.split()[0].isdigit() else 0
                    
                    # Extract date
                    date = 'N/A'
                    date_elem = review.find('time')
                    if date_elem:
                        date = date_elem.get('datetime', date_elem.text.strip())[:10]
                    
                    # Extract title
                    title = 'N/A'
                    title_elem = review.find('h2')
                    if not title_elem:
                        title_elem = review.find('div', {'data-service-review-title-typography': True})
                    if title_elem:
                        title = title_elem.text.strip()
                    
                    # Extract review text
                    text = 'N/A'
                    text_elem = review.find('p', {'data-service-review-text-typography': True})
                    if not text_elem:
                        text_elem = review.find('p', class_=lambda x: x and 'review' in str(x).lower())
                    if text_elem:
                        text = text_elem.text.strip()
                    
                    # Extract author
                    author = 'Anonymous'
                    author_elem = review.find('span', {'data-consumer-name-typography': True})
                    if author_elem:
                        author = author_elem.text.strip()
                    
                    # Extract location
                    location = 'N/A'
                    location_elem = review.find('div', {'data-consumer-country-typography': True})
                    if location_elem:
                        location = location_elem.text.strip()
                    
                    # Only add if we have at least rating and text
                    if rating > 0 or text != 'N/A':
                        reviews_data.append({
                            'platform': platform_name,
                            'rating': rating,
                            'title': title,
                            'text': text,
                            'date': date,
                            'author': author,
                            'location': location
                        })
                
                except Exception as e:
                    continue
            
            # Random delay to avoid rate limiting
            time.sleep(random.uniform(2, 4))
            
        except requests.exceptions.RequestException as e:
            print(f" ✗ Error: {e}")
            break
    
    return pd.DataFrame(reviews_data)


# Main execution
if __name__ == "__main__":
    print("\n" + "="*70)
    print("TRUSTPILOT SCRAPER - Irish Food Delivery Platforms")
    print("="*70 + "\n")
    
    companies = {
        'Deliveroo': 'deliveroo.ie',
        'Just Eat': 'www.just-eat.ie',
        'Uber Eats': 'ubereats.com'
    }
    
    all_reviews = []
    stats = []
    
    for company_name, company_url in companies.items():
        print(f"\n📊 Scraping {company_name}...")
        print("-" * 70)
        
        df = scrape_trustpilot_reviews(company_url, company_name, max_pages=20)
        
        if len(df) > 0:
            all_reviews.append(df)
            
            # Calculate stats
            avg_rating = df['rating'].mean()
            total_reviews = len(df)
            
            stats.append({
                'Platform': company_name,
                'Total Reviews': total_reviews,
                'Average Rating': round(avg_rating, 2),
                '5 Star': len(df[df['rating'] == 5]),
                '4 Star': len(df[df['rating'] == 4]),
                '3 Star': len(df[df['rating'] == 3]),
                '2 Star': len(df[df['rating'] == 2]),
                '1 Star': len(df[df['rating'] == 1])
            })
            
            # Save individual file
            filename = f'trustpilot_{company_name.lower().replace(" ", "_")}_reviews.csv'
            df.to_csv(filename, index=False, encoding='utf-8')
            
            print(f"\n✓ Collected: {total_reviews} reviews")
            print(f"✓ Average Rating: {avg_rating:.2f}/5")
            print(f"✓ Saved to: {filename}")
        else:
            print(f"\n✗ No reviews collected for {company_name}")
    
    # Combine and save all reviews
    if all_reviews:
        print("\n" + "="*70)
        print("COMBINING ALL REVIEWS")
        print("="*70)
        
        combined_df = pd.concat(all_reviews, ignore_index=True)
        combined_df.to_csv('trustpilot_all_reviews.csv', index=False, encoding='utf-8')
        
        # Save summary statistics
        stats_df = pd.DataFrame(stats)
        stats_df.to_csv('trustpilot_summary_statistics.csv', index=False)
        
        print(f"\n✓ Total reviews collected: {len(combined_df)}")
        print(f"✓ Files saved:")
        print(f"  - trustpilot_all_reviews.csv ({len(combined_df)} reviews)")
        print(f"  - trustpilot_summary_statistics.csv")
        
        print("\n📈 SUMMARY BY PLATFORM:")
        print("-" * 70)
        print(stats_df.to_string(index=False))
        
        print("\n" + "="*70)
        print("✓ SCRAPING COMPLETE!")
        print("="*70 + "\n")
    else:
        print("\n✗ No reviews collected from any platform")
        print("\n🔧 TROUBLESHOOTING:")
        print("  1. Check your internet connection")
        print("  2. Trustpilot may be blocking automated requests")
        print("  3. Try manual data collection as backup")
        print("="*70 + "\n")
