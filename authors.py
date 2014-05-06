import gdata.spreadsheet.service

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
from pytagcloud.colors import COLOR_SCHEMES


# Username and password is your Google Username and password
username = ''
password = ''
# Title of your spread sheet
spreadsheet_title = ''
#Custom Column Header that you want to retrieve. In my case it is author
custom_column_header = ''

def main():
    client = gdata.spreadsheet.service.SpreadsheetsService()
    client.ClientLogin(username, password)
    documents_feed = client.GetSpreadsheetsFeed()
    author = "";
    # Loop through the feed and extract each document entry.
    for document_entry in documents_feed.entry:
      if(document_entry.title.text == spreadsheet_title):
          for link in document_entry.link:
              if "ccc?key=" in link.href:
                   worksheet_key = link.href.split('=')[-1]
          worksheetFeed = client.GetWorksheetsFeed(worksheet_key)
          worksheet_entry = worksheetFeed.entry[0];
          worksheet_id = worksheet_entry.id.text.split('/')[-1];
          rows_feed = client.GetListFeed(worksheet_key, worksheet_id)
          for row in rows_feed.entry:
              authorname = row.custom[custom_column_header].text;
              if(authorname != None):
                  author = author + " " + authorname.replace(" ", "").replace(".", "")
      
    print author;
    
    tags = make_tags(get_tag_counts(author), maxsize=120, colors=COLOR_SCHEMES['audacity'])
    create_tag_image(tags, 'authors.png', size=(2500, 1500), background=(0, 0, 0, 255), fontname='PT Sans Regular')

if __name__ == "__main__":
    main();  
