from flask import flash
import os
import markdown
import bleach
from bs4 import BeautifulSoup, Tag
from ctrlv_client.app import SITE_CONFIG_FILE
temp_site_config_file = os.path.join(
    os.path.dirname(SITE_CONFIG_FILE),
    'site-config-testing.json'
)


def truncate_html(html, length):
    # Using lxml as it is rendering properly
    soup = BeautifulSoup(html[:length], 'html5lib')
    if len(html) > length:
        last_tag = soup.find_all(lambda x: isinstance(x, Tag))[-1]
        last_tag.append("...")
    return_val = str(soup)    
    return return_val


def error_flasher(form):
    for field, message_list in form.errors.items():
        for message in message_list:
            flash(form[field].label.text + ': ' + message, 'error')


def mask_config_file():
    if os.path.isfile(SITE_CONFIG_FILE):
        os.rename(SITE_CONFIG_FILE, temp_site_config_file)


def unmask_config_file():
    # Remove temporary site-config.json
    if os.path.isfile(SITE_CONFIG_FILE):
        os.remove(SITE_CONFIG_FILE)
    # Restore original site-config.json
    if os.path.isfile(temp_site_config_file):
        os.rename(temp_site_config_file, SITE_CONFIG_FILE)


def get_sanitized_html(markdown_text):
    html = markdown.markdown(markdown_text)
    # Tags deemed safe
    allowed_tags = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'img',
        'h1', 'h2', 'h3', 'p', 'br', 'hr'
    ]
    # Attributes deemed safe
    allowed_attrs = {
        '*': ['class'],
        'a': ['href', 'rel'],
        'img': ['src', 'alt']
    }
    # Sanitize the html using bleach &
    # Convert text links to actual links
    html_sanitized = bleach.clean(
        bleach.linkify(html),
        tags=allowed_tags,
        attributes=allowed_attrs
    )
    return html_sanitized
