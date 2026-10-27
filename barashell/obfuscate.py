import sys
import re
import random

random.seed(42) # For reproducibility if needed, but random is fine

def obfuscate_char(c):
    # Same mapping as message.html
    mapping = {
        'a': '&#97;',
        'e': '&#101;',
        'i': '&#105;',
        'o': '&#111;',
        'u': '&#117;',
        's': '&#115;',
        'r': '&#114;',
        'l': '&#108;',
        'n': '&#110;',
        'c': '&#99;',
        't': '&#116;'
    }
    
    if c.lower() in mapping:
        # 40% chance to obfuscate a character to mimic realistic variance
        if random.random() < 0.4:
            return mapping[c.lower()]
    return c

def obfuscate_text(text):
    # We shouldn't obfuscate &nbsp; or other entities!
    # Let's temporarily protect &...; entities
    entities = re.findall(r'&[a-zA-Z0-9#]+;', text)
    temp_text = re.sub(r'&[a-zA-Z0-9#]+;', '\x00', text)
    
    result_chars = []
    for char in temp_text:
        if char == '\x00':
            result_chars.append('\x00')
        else:
            result_chars.append(obfuscate_char(char))
            
    result = ''.join(result_chars)
    for entity in entities:
        result = result.replace('\x00', entity, 1)
        
    return result

def obfuscate_html(html_content):
    # Split by HTML tags
    parts = re.split(r'(<[^>]+>)', html_content)
    new_parts = []
    for part in parts:
        if part.startswith('<'):
            new_parts.append(part)
        else:
            new_parts.append(obfuscate_text(part))
            
    new_html = "".join(new_parts)
    
    # Add random comment just after BODY tag
    body_pattern = re.compile(r'(<BODY[^>]*>)', re.IGNORECASE)
    new_html = body_pattern.sub(r'\1\n<!-- {random_comment} -->', new_html, count=1)
    
    # Add random text block just before </BODY>
    body_close_pattern = re.compile(r'(</BODY>)', re.IGNORECASE)
    new_html = body_close_pattern.sub(r'<div style="display:none;color:white;font-size:1px">{random_text_block}</div>\n\1', new_html, count=1)
    
    return new_html

if __name__ == '__main__':
    with open('/Users/gus/Downloads/SHELL/litigation_notice_input.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    obf = obfuscate_html(html)
    
    with open('/Users/gus/Downloads/SHELL/obfuscated_litigation_notice.html', 'w', encoding='utf-8') as f:
        f.write(obf)
    print("Obfuscation complete.")
