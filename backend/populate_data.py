#!/usr/bin/env python
"""
Script to populate the database with sample data for testing.
"""
import os
import django
from datetime import datetime, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from assets.models import Asset, PriceData
from news.models import MarketNews
from watchlists.models import Watchlist, WatchlistAsset

def create_sample_data():
    print("Creating sample data...")
    
    # Create admin user
    admin, created = User.objects.get_or_create(
        email='admin@example.com',
        defaults={
            'is_admin': True,
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print(f"Created admin user: {admin.email}")
    
    # Create regular user
    user, created = User.objects.get_or_create(
        email='user@example.com',
        defaults={
            'is_admin': False,
        }
    )
    if created:
        user.set_password('user123')
        user.save()
        print(f"Created user: {user.email}")
    
    # Create sample assets
    sample_assets = [
        {'ticker': 'AAPL', 'name': 'Apple Inc.', 'type': 'stock', 'sector': 'Technology'},
        {'ticker': 'GOOGL', 'name': 'Alphabet Inc.', 'type': 'stock', 'sector': 'Technology'},
        {'ticker': 'MSFT', 'name': 'Microsoft Corporation', 'type': 'stock', 'sector': 'Technology'},
        {'ticker': 'AMZN', 'name': 'Amazon.com Inc.', 'type': 'stock', 'sector': 'Consumer Cyclical'},
        {'ticker': 'TSLA', 'name': 'Tesla Inc.', 'type': 'stock', 'sector': 'Automotive'},
        {'ticker': 'BTC', 'name': 'Bitcoin', 'type': 'crypto', 'sector': 'Cryptocurrency'},
        {'ticker': 'ETH', 'name': 'Ethereum', 'type': 'crypto', 'sector': 'Cryptocurrency'},
        {'ticker': 'EURUSD', 'name': 'Euro / US Dollar', 'type': 'forex', 'sector': 'Currency'},
        {'ticker': 'GBPUSD', 'name': 'British Pound / US Dollar', 'type': 'forex', 'sector': 'Currency'},
    ]
    
    assets = []
    for asset_data in sample_assets:
        asset, created = Asset.objects.get_or_create(
            ticker=asset_data['ticker'],
            defaults=asset_data
        )
        if created:
            print(f"Created asset: {asset.ticker}")
        assets.append(asset)
    
    # Create price data for each asset
    for asset in assets:
        base_price = random.uniform(50, 5000)
        for i in range(30):  # Last 30 days
            timestamp = datetime.now() - timedelta(days=i)
            change = random.uniform(-0.05, 0.05)
            close_price = base_price * (1 + change)
            open_price = close_price * random.uniform(0.98, 1.02)
            high_price = max(open_price, close_price) * random.uniform(1.01, 1.05)
            low_price = min(open_price, close_price) * random.uniform(0.95, 0.99)
            volume = random.randint(1000000, 100000000)
            
            PriceData.objects.get_or_create(
                asset=asset,
                timestamp=timestamp,
                defaults={
                    'open': round(open_price, 2),
                    'close': round(close_price, 2),
                    'high': round(high_price, 2),
                    'low': round(low_price, 2),
                    'volume': volume,
                }
            )
        print(f"Created price data for {asset.ticker}")
    
    # Create sample news
    sample_news = [
        {
            'title': 'Tech Stocks Rally as Market Sentiment Improves',
            'content': 'Major technology stocks saw significant gains today as investor sentiment improved following positive economic data.',
            'source': 'Financial Times',
        },
        {
            'title': 'Bitcoin Reaches New Monthly High',
            'content': 'Bitcoin surged past key resistance levels, reaching its highest price in a month amid increased institutional interest.',
            'source': 'Crypto News',
        },
        {
            'title': 'Federal Reserve Announces Interest Rate Decision',
            'content': 'The Federal Reserve maintained interest rates at current levels, signaling a cautious approach to monetary policy.',
            'source': 'Reuters',
        },
        {
            'title': 'Electric Vehicle Sales Continue Strong Growth',
            'content': 'Global electric vehicle sales continue to exceed expectations, driven by government incentives and improving infrastructure.',
            'source': 'Bloomberg',
        },
        {
            'title': 'European Markets Open Higher on Economic Data',
            'content': 'European stock markets opened higher following better-than-expected manufacturing data from Germany and France.',
            'source': 'CNBC',
        },
    ]
    
    for news_data in sample_news:
        news = MarketNews.objects.create(
            title=news_data['title'],
            content=news_data['content'],
            source=news_data['source'],
            published_at=datetime.now() - timedelta(hours=random.randint(1, 48)),
        )
        print(f"Created news: {news.title}")
    
    # Create a sample watchlist for the user
    watchlist, created = Watchlist.objects.get_or_create(
        user=user,
        name='My Favorites',
        defaults={}
    )
    if created:
        print(f"Created watchlist: {watchlist.name}")
        
        # Add some assets to the watchlist
        for asset in assets[:3]:
            WatchlistAsset.objects.get_or_create(
                watchlist=watchlist,
                asset=asset
            )
        print(f"Added assets to watchlist")
    
    print("\nSample data creation complete!")
    print("\nTest credentials:")
    print("  Admin: admin@example.com / admin123")
    print("  User: user@example.com / user123")

if __name__ == '__main__':
    create_sample_data()
