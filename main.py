from bs4 import BeautifulSoup as bsoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import re
import requests
import smtplib
import time

disable_warnings(InsecureRequestWarning)

acts = ['sex', 'sexual', 'sexually', 'defile', 'defiled', 'defilement', 'defiling', 'rape', 'raped', 'raping',
        'abuse', 'abused', 'abusing', 'beating', 'beat', 'assault', 'assaulting', 'assaulted', 'burn', 'burnt',
        'burned', 'burning', 'harass', 'harassed', 'harassment', 'harassing', 'hurt', 'hurting', 'impregnate',
        'impregnating', 'impregnated', 'traffick', 'trafficked', 'trafficking', 'molest', 'molestation',
        'molesting', 'spank', 'spanked', 'caning', 'cane', 'slap', 'slapped', 'slapping', 'abduct', 'abduction',
        'abducting', 'abducted', 'inflict', 'inflicted', 'infliction', 'inflicting', 'rapist', 'sell', 'selling',
        'sold', 'lash', 'lashed', 'poison', 'poisoning', 'poisoned', 'sodomy', 'sodomized', 'sodomizing',
        'incest', 'sodomy', 'abandon', 'abandoned', 'abandoning']

id_words = ['police', 'arrest', 'arresting', 'arrested', 'court', 'bail', 'bailed', 'jail', 'jailed', 'jailing',
            'catch', 'catching', 'caught', 'remand', 'remanded', 'prosecute', 'prosecutor', 'prosecuted', 'victim',
            'victimized', 'complainant', 'alleged', 'inform', 'informed', 'suspect', 'suspected', 'convict',
            'convicted', 'sentence', 'imprison']

victim = ['child', 'children', 'baby', 'babies', 'boy', 'boys', 'girl', 'girls', 'son', 'sons', 'daughter',
          'daughters', 'student', 'students', 'pupil', 'pupils', 'minors', 'minor', 'niece', 'nephew', 'teenage',
          'stepson', 'grandson']

keywords = acts + id_words + victim

websites = {'A1 RADIOONLINE': 'https://www.a1radioonline.com/category/news',
             'AGOO FM ONLINE': 'http://agoofmonline.com/category/local/',
             'ANAPUA FM': 'https://anapuafm.com/local-news/',
             'ATL FM': 'https://atlfmnews.com/news/news/',
             'BEACH FM ONLINE': 'https://beachfmonline.com/category/news/',
             'CITINEWSROOM': 'https://citinewsroom.com/news/',
             'FOCUS NEWSROOM': 'https://focusfmknust.com/',
             'GHANAWEB': 'https://www.ghanaweb.com/GhanaHomePage/NewsArchive/',
             'GHANAWEB CRIME': 'https://www.ghanaweb.com/GhanaHomePage/crime/',
             'LORLORNYO FM': 'http://www.lorlornyofm.com/category/news/',
             'MYJOYONLINE': 'https://www.myjoyonline.com',
             'OTEC FM': 'https://otecfmghana.com/',
             'PINK FM': 'https://pinkfmonlinegh.com/category/news/',
             'SKYY POWER FM': 'https://skyypowerfm.com/news/',
             'SPIRIT FM': 'https://spiritfmonline.com/category/ghanaian-news/',
             'ZAARADIO': 'https://zaaradio.com/news/'}

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x84_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


def detect_child_abuse():
    global new_links
    new_links = []
    website = web_var.get()
    cur_website = Label(root, text=f'CHECKING ARTICLES ON {website}.', relief='groove', bg='white', font=(type_l, x),
                        fg=pda_color)
    cur_website.grid(row=1, column=0, columnspan=3, sticky='we')
    _continue.config(state='normal')
    for website in websites:
        print(website)
        cur_website = Label(root, text=f'CHECKING ARTICLES ON {website}.', relief='groove', bg='white',
                            font=(type_l, x),
                            fg=pda_color)
        cur_website.grid(row=1, column=0, columnspan=3, sticky='we')
        web_var.set(website)
        try:
            website_content = requests.get(websites[website], headers=header, verify=False).content
        except:
            cur_website = Label(root, text=f'STOPPED CHECKING AT {website} DUE TO AN ERROR.', relief='groove',
                                bg='white',
                                font=(type_l, x), fg=pda_color)
            cur_website.grid(row=1, column=0, columnspan=3, sticky='we')
            messagebox.showwarning(title='Error', message='Please check your internet connection and click continue.')
            raise
        website_soup = bsoup(website_content, 'lxml')
        if websites[website] in ['https://www.ghanaweb.com/GhanaHomePage/crime/',
                                 'https://www.ghanaweb.com/GhanaHomePage/NewsArchive/']:
            website_links = ['https://www.ghanaweb.com' + str(a['href']) for a in website_soup.find_all('a') \
                             if 'crime' in str(a)]
        else:
            website_links = set([str(a['href']) for a in website_soup.find_all('a') if 'href' in str(a)])

        for link in website_links:
            link_words = re.split('\. |  |, |, |\s|-|/', link)
            if any(key in acts for key in link_words):
                try:
                    link_soup_ = bsoup(requests.get(link, headers=header, verify=False).content, 'lxml')
                except:
                    cur_website = Label(root, text=f'STOPPED CHECKING AT {website}.', relief='groove', bg='white',
                                        font=(type_l, x), fg=pda_color)
                    cur_website.grid(row=1, column=0, columnspan=3, sticky='we')
                    messagebox.showwarning(title='Error',
                                           message='Please check your internet connection and click continue.')
                    raise
                link_soup = ''.join([p.text for p in link_soup_.find_all('p')])
                link_soup = link_soup.lower()
                link_soup = re.split('\. |  |, |, |\s', link_soup)
                if any(key in link_soup for key in acts) and any(id_ in link_soup for id_ in id_words) \
                        and any(_key in link_soup for _key in victim):
                    print(link)
                    new_links.append(link)
    # web_var.set('PEACE FM')
    try:
        peace = requests.get('https://peacefmonline.com/pages/local/crime/', headers=header)
    except:
        messagebox.showwarning(title='Error', message='Please check your internet connection and click continue.')
    peace_soup = bsoup(peace.content, 'lxml')
    peace_links = sorted(
        list(set([a['href'] for a in peace_soup.find_all('a') if 'crime' in str(a) and '.php' in str(a)])))
    for link in peace_links:
        if 'http' not in link:
            link = 'https://peacefmonline.com' + link
        try:
            article_title = bsoup(requests.get(link, headers=header).content, 'lxml').title.text
        except:
            messagebox.showwarning(title='Error', message='Please check your internet connection and click continue.')
            raise
        #         title_words = re.split('\. |  |, |, |\s', article_title)
        #         article_title = bsoup(requests.get(link, headers=header).content, 'lxml').title.text
        title_words = re.split('\. |  |, |, |\s', article_title)
        title_words = [word.lower() for word in title_words]
        if any(key in acts for key in title_words):
            print(link, ' '.join(title_words))
            try:
                link_soup_ = bsoup(requests.get(link, headers=header).content, 'lxml')
            except:
                messagebox.showwarning(title='Error',
                                       message='Please check your internet connection and click continue.')
                raise
            link_soup = ''.join([p.text for p in link_soup_.find_all('p')])
            link_soup = link_soup.lower()
            link_soup = re.split('\. |  |, |, |\s', link_soup)
            if any(key in link_soup for key in acts):
                if any(id_ in link_soup for id_ in id_words):
                    if any(_key in link_soup for _key in victim):
                        new_links.append(link)
    messagebox.showinfo(title='Complete!',
                        message='All websites checked. Click on SEND TO EMAIL to have links retrieved sent to your email.')
    cur_website = Label(root, text=f'DONE CHECKING.', relief='groove', bg='white', font=(type_l, x), fg=pda_color)
    cur_website.grid(row=1, column=0, columnspan=3, sticky='we')
    with open('new_links.txt', 'w') as file:
        for item in new_links:
            file.write(item + '\n')

    send.config(state='normal')


def continue_detect():
    send.config(state='normal')
    cur_web = web_var.get()
    webs = list(websites.keys())
    if cur_web == 'PEACE FM':
        cur_web = webs[-1]
    index = webs.index(cur_web)
    n = len(webs)
    new_list_websites = {webs[i]: websites[webs[i]] for i in range(index, n)}
    website = webs[index]
    cur_website = Label(root, text=f'CHECKING ARTICLES ON {website}.', relief='groove', bg='white', font=(type_l, x),
                        fg=pda_color)
    cur_website.grid(row=1, column=0, columnspan=3, sticky='we')
    for website in new_list_websites:
        print(website)
        cur_website = Label(root, text=f'CHECKING ARTICLES ON {website}.', relief='groove', bg='white',
                            font=(type_l, x),
                            fg=pda_color)
        cur_website.grid(row=1, column=0, columnspan=3, sticky='we')
        web_var.set(website)
        try:
            website_content = requests.get(websites[website], headers=header, verify=False).content
        except:
            cur_website = Label(root, text=f'STOPPED CHECKING AT {website} DUE TO AN ERROR.', relief='groove',
                                bg='white',
                                font=(type_l, x), fg=pda_color)
            cur_website.grid(row=1, column=0, columnspan=3, sticky='we')
            messagebox.showwarning(title='Error', message='Please check your internet connection and click continue.')
            raise
        website_soup = bsoup(website_content, 'lxml')
        if websites[website] in ['https://www.ghanaweb.com/GhanaHomePage/crime/',
                                 'https://www.ghanaweb.com/GhanaHomePage/NewsArchive/']:
            website_links = ['https://www.ghanaweb.com' + str(a['href']) for a in website_soup.find_all('a') \
                             if 'crime' in str(a)]
        else:
            website_links = set([str(a['href']) for a in website_soup.find_all('a') if 'href' in str(a)])
        for link in website_links:
            link_words = re.split('\. |  |, |, |\s|-|/', link)
            if any(key in acts for key in link_words):
                try:
                    link_soup_ = bsoup(requests.get(link, headers=header, verify=False).content, 'lxml')
                except:
                    cur_website = Label(root, text=f'STOPPED CHECKING AT {website}.', relief='groove', bg='white',
                                        font=(type_l, x), fg=pda_color)
                    cur_website.grid(row=1, column=0, columnspan=3, sticky='we')
                    messagebox.showwarning(title='Error',
                                           message='Please check your internet connection and click continue.')
                    raise
                link_soup = ''.join([p.text for p in link_soup_.find_all('p')])
                link_soup = link_soup.lower()
                link_soup = re.split('\. |  |, |, |\s', link_soup)
                if any(key in link_soup for key in acts) and any(id_ in link_soup for id_ in id_words) \
                        and any(_key in link_soup for _key in victim):
                    print(link)
                    new_links.append(link)
    peace = requests.get('https://peacefmonline.com/pages/local/crime/', headers=header)
    peace_soup = bsoup(peace.content, 'lxml')
    peace_links = sorted(
        list(set([a['href'] for a in peace_soup.find_all('a') if 'crime' in str(a) and '.php' in str(a)])))
    for link in peace_links:
        if 'http' not in link:
            link = 'https://peacefmonline.com' + link
        try:
            article_title = bsoup(requests.get(link, headers=header).content, 'lxml').title.text
        except:
            messagebox.showwarning(title='Error', message='Please check your internet connection and click continue.')
            raise
        title_words = re.split('\. |  |, |, |\s', article_title)
        title_words = [word.lower() for word in title_words]
        if any(key in acts for key in title_words):
            print(link, ' '.join(title_words))

            link_soup_ = bsoup(requests.get(link, headers=header).content, 'lxml')

            link_soup = ''.join([p.text for p in link_soup_.find_all('p')])
            link_soup = link_soup.lower()
            link_soup = re.split('\. |  |, |, |\s', link_soup)
            if any(key in link_soup for key in acts):
                if any(id_ in link_soup for id_ in id_words):
                    if any(_key in link_soup for _key in victim):
                        new_links.append(link)
    messagebox.showinfo(title='Complete!',
                        message='All websites checked. Click on SEND TO EMAIL to have links retrieved sent to your email.')
    cur_website = Label(root, text=f'DONE CHECKING.', relief='groove', bg='white', font=(type_l, x), fg=pda_color)
    cur_website.grid(row=1, column=0, columnspan=3, sticky='we')
    with open('new_links.txt', 'a') as file:
        for item in new_links:
            file.write(item + '\n')


def send_email():
    with open('all_links.txt', 'r') as all_links:
        all_links_scraped = all_links.readlines()

    all_links_scraped = [link.strip() for link in all_links_scraped]

    with open('new_links.txt', 'r') as new_link_file:
        new_links = new_link_file.readlines()

    new_links_ = [link.strip() for link in new_links]

    with open('all_links.txt', 'a') as all_links:
        new_links = list(set(new_links_) - set(all_links_scraped))
        all_links.write('\n\n' + time.ctime() + '\n\n')
        for content in new_links:
            all_links.write(content + '\n')
    if len(new_links) == 0:
        messagebox.showinfo(title='Info', message='No new links found.')
        raise
    mail_content = '\n\n'.join(new_links)
    mail_content = f'''Dear Peter,
    Kindly find below some links to possible child abuse cases. These links were scraped today {time.ctime()}. 
    The links are from 16 websites. The keywords used in detecting the cases are many so as to capture all the cases. 
    This may lead to the presence of other cases which may not be directly child abuse related. 
    Kindly ignore such links.


    ''' + mail_content + \
                   '\n\n Best regards,\n PDA Web Scraper'

    try:
        sender_address = 'emailpython6@gmail.com'
        sender_pass = 'dogwzjrchfexxrki'
        receiver_add = 'pamensah@pdaghana.com'
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_add
        # message['cc'] = cc_add
        message['Subject'] = 'Links to Child Abuse Cases'
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, [receiver_add], text)
        session.quit()
    except:
        messagebox.showwarning(title='Error', message='Kindly check your internet connection and try again.')
        raise
    messagebox.showinfo(title='Success', message=f'Email sent to {receiver_add}')


root = Tk()
root.title('PDA CHILD ABUSE WEB SCRAPER')
style = ttk.Style(root)
style.theme_use('vista')
app_width = 700
app_height = 130
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coord = screen_width // 2 - app_width // 2
y_coord = screen_height // 2 - app_height // 2
root.geometry(f'{app_width}x{app_height}+{x_coord}+{y_coord}')
# Grid.rowconfigure(root, 0, weight=1)
button_bg = 'lavender'
pda_color = '#D2691E'
lucida = 'Lucida Console'
type_l = 'Lucida Sans Typewriter'
arial_b = 'Arial Black'
arial = 'Arial'
arial_r = 'Arial Rounded MT Bold'
casc = 'Cascadia Code'
x = 12
Grid.columnconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 1, weight=1)
Grid.columnconfigure(root, 2, weight=1)
Label(text='SELECT A WEBSITE TO START SCRAPING', relief='groove', font=(lucida, x), bd=5,
      bg=pda_color).grid(row=0, column=0, sticky='we')
web_var = StringVar()
web_var.set(list(websites.keys())[0])
web_options = OptionMenu(root, web_var, *websites.keys())
web_options.config(font=(arial_r, x))
web_options.config(bg='white')
web_options.config(fg=pda_color)
web_options['menu'].config(fg='black', bg=pda_color)
web_options['menu'].config(font=('Cambria', x))
web_options.grid(row=0, column=1, columnspan=2, sticky='we')
cur_website = Label(root, text='Click SCRAPE ALL SITES to start.', relief='groove', bg='white', font=(type_l, x),
                    fg=pda_color)
cur_website.grid(row=1, column=0, columnspan=3, sticky='we')
i = 2
start = Button(root, text='SCRAPE ALL SITES', font=(lucida, x), fg=pda_color, bg=button_bg, command=detect_child_abuse)
start.grid(row=i, column=0, sticky='we')
_continue = Button(root, text='CONTINUE SCRAPING', font=(lucida, x), fg=pda_color, bg=button_bg, command=continue_detect)
_continue.grid(row=i, column=1, sticky='we', columnspan=2)
_continue.config(state='disabled')
send = Button(root, text='SEND TO EMAIL', font=(casc, x), fg=pda_color, bg=button_bg, command=send_email)
send.grid(row=i+1, column=0, columnspan=3, sticky='we')
send.config(state='disabled')
root.mainloop()
