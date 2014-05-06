import gdata.spreadsheet.service

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
from pytagcloud.colors import COLOR_SCHEMES


# Username and password is your Google Username and password
username = ''
password = ''
# Title of your spread sheet
spreadsheet_title = ''
# Custom Column Header that you want to retrieve. In my case it is author
custom_column_header1 = 'author'
custom_column_header2 = 'category'
custom_column_header3 = 'publisher'
custom_column_header4 = 'originallanguage'
custom_column_header5= 'placeorbookstore'

def main():
    client = gdata.spreadsheet.service.SpreadsheetsService()
    client.ClientLogin(username, password)
    documents_feed = client.GetSpreadsheetsFeed()
    author = ""
    genre = ""
    language = ""
    publisher = ""
    store=""
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
              authorname = row.custom[custom_column_header1].text;
              if(authorname != None):
                  author = author + " " + authorname.replace(" ", "").replace(".", "")
              
              genre_name = row.custom[custom_column_header2].text
              if(genre_name != None):
                  genre = genre + " " + genre_name.replace(" ", "").replace(".", "")
              
              publishers = row.custom[custom_column_header3].text
              if(publishers != None):
                  publisher = publisher + " " + publishers.replace(" ", "").replace(".", "")
              
              languages = row.custom[custom_column_header4].text
              if(languages != None):
                  language = language + " " + languages.replace(" ", "").replace(".", "")
              
              bookstore = row.custom[custom_column_header5].text
              if(bookstore != None):
                  store = store + " " + bookstore.replace(" ", "").replace(".", "dot").replace(",", "").replace("-", "")     
                  
      
    print get_tag_counts(author);
    print get_tag_counts(genre);
    print get_tag_counts(publisher);
    print get_tag_counts(language);
    print get_tag_counts(store);
    
    tags = make_tags(get_tag_counts(author),minsize = 10,  maxsize=200, colors=COLOR_SCHEMES['audacity'])
    create_tag_image(tags, 'authors.png', size=(2500, 1500), background=(0, 0, 0, 255), fontname='PT Sans Regular')
     
    tags = make_tags(get_tag_counts(genre), minsize = 10, maxsize=200, colors=COLOR_SCHEMES['oldschool'])
    create_tag_image(tags, 'genre.png', size=(1000, 800), background=(0, 0, 0, 255), fontname='PT Sans Regular')
     
    tags = make_tags(get_tag_counts(publisher),minsize = 10,  maxsize=200, colors=COLOR_SCHEMES['oldschool'])
    create_tag_image(tags, 'publisher.png', size=(2500, 1500), background=(0, 0, 0, 255), fontname='PT Sans Regular')
     
    tags = make_tags(get_tag_counts(language), minsize = 20, maxsize=120, colors=COLOR_SCHEMES['oldschool'])
    create_tag_image(tags, 'language.png', size=(1500, 1200), background=(0, 0, 0, 255), fontname='PT Sans Regular')
    
    tags = make_tags(get_tag_counts(store), minsize = 10, maxsize=120, colors=COLOR_SCHEMES['oldschool'])
    create_tag_image(tags, 'store.png', size=(3000, 2000), background=(0, 0, 0, 255), fontname='PT Sans Regular')
    
     

if __name__ == "__main__":
    main();  
