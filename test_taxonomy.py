# test_taxonomy.py
from util.taxonomy_reader import taxonomy_reader

def test_taxonomies():
    # Test each taxonomy
    taxonomies = [
        'business_events',
        'industries',
        'locations',
        'languages',
        'sources'
    ]
    
    for taxonomy_name in taxonomies:
        try:
            print(f"\nTesting {taxonomy_name}:")
            data = taxonomy_reader.load_taxonomy(taxonomy_name)
            print(f"Total entries: {len(data)}")
            print("Sample entries:")
            for entry in data[:3]:  # Show first 3 entries
                print(entry)
        except Exception as e:
            print(f"Error loading {taxonomy_name}: {e}")

if __name__ == "__main__":
    test_taxonomies()