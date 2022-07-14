import bs4
import requests
from term_and_description import TermAndDescription


def convert_encoding_into_readable_symbols(text):
    #Note: "\xe2" corresponds to the undesired character "â" and note that each original symbol
    # has 3 characters example1: "\xe2", "\x80", and \x94" or example2: "\xe2", "\x80", and "¦"
    unwanted_char = {"\xe2\x80\x94": "--", "\xe2\x80\x99": "\'", "\xe2\x80\x9d": "\"", "\xe2\x80\x9c": "\"",
                     "\xe2\x80¦": "...", "\xe2\x80\x93":"--", "\xe2\x80\x98":"\'"}
    for key, value in unwanted_char.items():
        text = text.replace(key, value)
    return text


def blank_out_term_in_description(term, description):
    return description.replace(term, '______')


#Get Website Page
response = requests.get(url='https://docs.python.org/3/glossary.html#glossary')

html_text = response.text


#Make BeautifulSoup
# print(html_text)
soup = bs4.BeautifulSoup(html_text, "html.parser")


#Find the Desired Elements
term_elements = soup.find_all(name='dt')
# print(term_elements[0].get_text())
description_elements = soup.find_all(name='dd')
# print(description_elements[0].get_text())


#Make list of with Coupling each Term to its Description after converting the description into readable symbols
terms_and_descriptions_list = []
print("------------------------------")
for index in range(len(term_elements)):
    term = term_elements[index].get_text()
    description = description_elements[index].get_text().replace('\n', ' ')
    description = convert_encoding_into_readable_symbols(description)
    description = blank_out_term_in_description(term, description)
    terms_and_descriptions_list.append(TermAndDescription(term, description))

print(f'Length of list: {len(terms_and_descriptions_list)}')


#Write the term-description couple to file
count = 0
with open('python_glossary.csv', 'w') as file:
    for definition in terms_and_descriptions_list:
        try:
            file.write(f'{definition.description}\t{definition.term}\n')
        except Exception as error_message:
            count += 1
            print("@@@@@@@@@@@@@@@@@@@@@@@@")
            print(error_message)
            position_index = int(str(error_message).split(':')[0].split(' ')[-1].split('-')[0]) - 1
            original_description = definition.description

            list_of_words = str(original_description).split(' ')
            print(list_of_words)
            # description_corrected = f'{original_description[:position_index - 2]}??{original_description[position_index + 1:]}'
            # print(description_corrected)
            print('*************')
            print(f'{definition.description[:-1]}\t{definition.term}')
            print('###########')
print(f'Number of descriptions that still have (Exception-throwing) encodings: {count}')
