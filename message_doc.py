from alexandra import Alexandra
from json import load
from os import listdir
from os.path import join as pathjoin

MESSAGES_FOLDER = 'messages'
DOC_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Message Doc for <code>%(name)s</code></title>
  </head>
  <body>
    <h2>Message Doc for <code>%(name)s</code></h2>
    <ul>
      <li><strong>Name:</strong> <code>%(name)s</code></li>
      <li><strong>Extensions:</strong> <code>%(extensions)s</code></li>
      <li><strong>Content:</strong> %(content)s</li>
      <li><strong>Meaning:</strong> %(meaning)s</li>
      <li><strong>Example:</strong> %(example)s</li>
    </ul>
  </body>
</html>
'''

def add_message_doc(filename):
    path = pathjoin(MESSAGES_FOLDER, filename)
    with open(path, 'r') as json_file:
        message_info = load(json_file)
        html = DOC_TEMPLATE % message_info
        alex.enter_in_library(html, '/messages/' + filename, 'text/html')

alex = Alexandra()
map(add_message_doc, listdir(MESSAGES_FOLDER))
