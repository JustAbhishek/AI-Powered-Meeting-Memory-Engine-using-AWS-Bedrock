import os
def get_config():
    """Efficient config loader with environment variable fallbacks"""
    return {
        'LANGUAGE_CODE': os.getenv('LANGUAGE_CODE', 'en-US'),
        'MAX_SPEAKERS': int(os.getenv('MAX_SPEAKERS', '2')),
        'OUTPUT_PREFIX': os.getenv('OUTPUT_PREFIX', 'transcripts/')
    }