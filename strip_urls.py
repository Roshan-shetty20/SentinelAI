with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

bad_block = '''        # ====================================================
        # MODEL 1
        # TF-IDF + LOGISTIC REGRESSION
        # ====================================================

        clean_message = remove_markdown_links(processed_message)
        message_vector = (
            message_vectorizer.transform(
                [clean_message]
            )
        )'''

good_block = '''        # ====================================================
        # MODEL 1
        # TF-IDF + LOGISTIC REGRESSION
        # ====================================================

        from risk_engine import URL_PATTERN
        
        clean_message = remove_markdown_links(processed_message)
        
        # Remove URLs from text so the natural-language message model doesn't over-penalize them
        text_without_urls = URL_PATTERN.sub('', clean_message).strip()
        
        message_vector = (
            message_vectorizer.transform(
                [text_without_urls]
            )
        )'''

content = content.replace(bad_block, good_block)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
