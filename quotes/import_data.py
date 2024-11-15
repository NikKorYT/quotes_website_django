# import_data.py
import os
import django
import json
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes.settings')
django.setup()

from quotesapp.models import Author, Quote, Tag

def import_data():
    # Import authors
    print("Importing authors...")
    with open('json/authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)

    for author_data in authors_data:
        author = Author.objects.create(
            full_name=author_data['fullname'],
            born_date=datetime.strptime(author_data['born_date'], '%B %d, %Y').date(),
            born_location=author_data['born_location'],
            description=author_data['description']
        )
        print(f"Created author: {author.full_name}")

    # Import quotes
    print("\nImporting quotes...")
    with open('json/quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)

    for quote_data in quotes_data:
        try:
            author = Author.objects.get(full_name=quote_data['author'])
            quote = Quote.objects.create(
                quote=quote_data['quote'],
                author=author
            )
            print(f"Created quote for author: {author.full_name}")
            
            for tag_name in quote_data['tags']:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)
        except Author.DoesNotExist:
            print(f"Missing author: {quote_data['author']}")

if __name__ == '__main__':
    import_data()