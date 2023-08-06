#  _____ _     _       _       ____  _             _     
# |_   _| |__ (_)___  (_)___  |  _ \(_)_ __  _   _| | __ _| |_ ___
#   | | | '_ \| / __| | / __| | |_) | | '_ \| | | | |/ _` | __/ _ \
#   | | | | | | \__ \ | \__ \ |  __/| | |_) | |_| | | (_| | ||  __/
#   |_| |_| |_|_|___/ |_|___/ |_|   |_| .__/ \__,_|_|\__,_|\__\___|
# There are many frameworks like it,  |_| but this one is mine. --MikeL


import pickle
import gspread
import pygsheets
import pandas as pd
from sys import stdout
from os import environ
from sys import exc_info as error
from apiclient.discovery import build
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


gspread_sheet = None
pygsheets_sheet = None
column_uniqueness = False
err = lambda : print(error()[0].__name__)


def key(url):
    return sheet(url)


def sheet(key):
    global gspread_authorized, pygsheets_authorized
    global gspread_sheet, pygsheets_sheet
    global credentials

    check_credentials(credentials)

    try:
        if key[:4].lower() == 'http':
            gspread_sheet = gspread_authorized.open_by_url(key)
            pygsheets_sheet = pygsheets_authorized.open_by_url(key)
        else:
            gspread_sheet = gspread_authorized.open_by_key(key)
            pygsheets_sheet = pygsheets_authorized.open_by_key(key)
        print("""<<< CONNECTED! >>> You can open the Google Sheet with the following link:""")
        if key[:4].lower() == 'http':
            print(key)
        else:
            print(link(key))
    except:
        err() 
        print("Make sure %s has permission to this document." % email())
        raise SystemExit()
    try:
        sheet1 = gspread_sheet.worksheets()[0].title
        print('Try: cl, df = pipulate.pull("%s", "A1:C3") # or pipulate.help() for help.' % sheet1)
    except:
        err()
        raise SystemExit()


def help():
    print("Welcome to Pipulate: eaiser Google Sheet automation for SEO and more.")
    print("To pipulate a Google Spreadsheet, you use the following command:")
    print()
    print('    pipulate.sheet("Insert your Google Sheet key or URL")')
    print()
    print('Now you can select a gspread "cell_list" (cl) and a pandas "DataFrame" (df) like this:')
    print()
    print('    cl, df = pipulate.pull("Sheet1", "A2:C4")')
    print()
    print('You can optionally leave off the last-row number. It will be figured out:')
    print()
    print('    cl, df = pipulate.pull("Sheet1", "A2:C")')
    print()
    print('Now you can use Python pandas to manipulate the pandas DataFrame (df) like this:')
    print()
    print('   df[["A", "B"]] = ["foo", "bar"]') 
    print()
    print("You can see your changes by running df on a line by itself in Jupyter Notebook.")
    print()
    print("    df")
    print()
    print("Now make append the values of columns A and B into column C:")
    print()
    print('    df["C"] = df["A"] + df["B"]')
    print()
    print('And finllay, "push" the altered DataFrame back into GSheet:')
    print()
    print('    pipulate.push("Sheet1", cl, df)')
    print()
    print("It's nice to work with column labels, so let's put some in:")
    print()
    print('    pipulate.poke("Sheet1", columns=["One" , "Two", "Three"])')
    print()
    print("And now we can select the DataFrame with row 1 as column labels:")
    print()
    print('    cl, df = pipulate.pull("Sheet1", "A1:C4", columns=True)')
    print()
    print('Learn more at https://github.com/miklevin/Pipulate')


def pull(tab, rows, cols=None, columns=None, start=None, end=None):
    return pipulate(tab, rows, cols=cols, columns=columns, start=start, end=end)


def push(tab, cl, df, formulas=False):
    return populate(tab, cl, df, formulas=formulas)


def poke(tab, columns, row=1, start=1):
    cl, df = pull(tab, (row, row), (start, len(columns)))
    df.loc[:,:] = columns
    return push(tab, cl, df)


def pipulate(tab, rows, cols=None, columns=None, start=None, end=None):
    global credentials
    original_range, original_row1 = None, None

    try: 
        worksheet_ = check_worksheet(tab)
    except:
        check_credentials(credentials)
    
    if gspread_sheet == None:
        print('Make sure you pipulate.sheet("key or url") first.')
        raise SystemExit()

    if cols: 
        row1, row2 = rows
        if type(columns) == bool:
            original_row1 = row1
            row1 = row1 + 1
        col1, col2 = cols
        if not type(col1) == int and not type(col2) == int:
            col1, col2 = a1(col1, reverse=True), a1(col2, reverse=True)
        try:
            cl = worksheet_.range(row1, col1, row2, col2)
        except:
            print('Rate quota possibly exceeded. Wait a minute and try again.')
            raise SystemExit()
        list_of_lists = cl_to_list(cl)
        if not columns:
            cell_list = worksheet_.range(row1, col1, row1, col2)
            columns = [a1(x.col) for x in cell_list]
    elif ':' in rows:
        if not rows.split(':')[1][-1].isdigit():  # Figure out end of column
            aletter = rows.split(':')[1]
            col_length = len(worksheet_.col_values(a1(aletter, reverse=True))) 
            rows = "%s%s" % (rows, col_length)
        if type(columns) == bool:
            original_range = rows
            rows = shift_range(rows)
        try:
            cl = worksheet_.range(rows)
        except:
            print('Rate quota possibly exceeded. Wait a minute and try again.')
            raise SystemExit()
        list_of_lists = cl_to_list(cl)
        if not columns:
            columns = [a1(i+1) for i, x in enumerate(list_of_lists[0])]
    else:
        print("Check your rows or range definition.")
        raise SystemExit()

    if type(columns) == bool and columns == True:
        if cols:
            cl_cols = worksheet_.range(original_row1, col1, row2, col2)
        else:
            cl_cols = worksheet_.range(original_range)
        columns = cl_to_list(cl_cols)[0]
    if column_uniqueness: 
        if not all(v for v in columns):
            print(columns)
            print("All columns must have labels when using columns=True or columns=list.")
            raise SystemExit()
        if len(set(columns)) < len(columns):
            print(columns)
            print("All columns must have labels when using columns=True or columns=list.")
            raise SystemExit()

    df = pd.DataFrame(list_of_lists, columns=columns)

    print("<<< SUCCESSFUL! >>> Manipulate DataFrame but keep its (%s x %s) shape." % df.shape)
    print('To push updated DataFrame to GSheet: pipulate.push("%s", cl, df)' % worksheet_.title)
    return cl, df


def populate(tab, cl, df, formulas=False):
    """Push df back to spreadsheet."""

    try: 
        worksheet_ = check_worksheet(tab)
    except:
        check_credentials(credentials)


    if cl_df_fits(cl, df):
        lol = df.values.tolist()
        flat = [y for x in lol for y in x]
        flat[:] = ['N/A' if pd.isnull(x) else x for x in flat]
        for i, cell in enumerate(cl):
            cell.value = flat[i]
        if formulas:
            worksheet_.update_cells(cl, value_input_option='USER_ENTERED')
        else:
            worksheet_.update_cells(cl)
    else:
        raise SystemExit()
    print('pipulate.push("%s", cl, df) <<< GSHEET UPDATED! >>>' % worksheet_.title)


def shift_range(sheet_range):
    range_tuple = sheet_range.split(':')
    upper_left = range_tuple[0]
    for i, x in enumerate(upper_left):
        if x.isnumeric():
            break
    row_one = int(upper_left[len(upper_left) - 1:])
    col_one = upper_left[:len(upper_left) - 1]
    row_two = row_one + 1
    shifted_down = "".join([col_one, str(row_two), ":", range_tuple[1]])
    return shifted_down


def check_worksheet(worksheet):
    global gspread_sheet
    if type(worksheet) == gspread.models.Worksheet:
        tab = worksheet
    elif type(worksheet) == str:
        if 'gspread_sheet' in globals():
            if worksheet in [x.title for x in gspread_sheet.worksheets()]:
                tab = gspread_sheet.worksheet(worksheet)
            else:
                print("Worksheet not found")
                raise SystemExit()
        else:
            print("pipulate.sheet([your gsheets key here]) must be set")
            raise systemexit()
    elif type(worksheet) == int:
        if 'gspread_sheet' in globals():
            if worksheet <= len(gspread_sheet.worksheets()):
                tab = gspread_sheet.worksheets()[worksheet] 
            else:
                print("Worksheet ID too high. Try 0 for sheet 1.")
                raise SystemExit()
        else:
            print("pipulate.sheet([your gsheets key here]) must be set")
            raise systemexit()
    else:
        print("Worksheet must be exact tab-name as string, gspread Worksheet object or tab-index.")
        raise SystemExit()
    return tab


def cl_to_list(cl):
    new_table = []
    for i, cell in enumerate(cl):
        if i == 0:
            row_num = 1
            memory = cell.row
            row = [cell.value]
        if cell.row == memory and i > 0:
            row.append(cell.value)
        else:
            row_num += 1
            memory = cell.row
            row = [cell.value]
            new_table.append(row)
    return new_table


def cl_df_fits(cl, df):
    """Check if GSpread cell list same shape as Pandas dataframe."""
    list_of_lists = cl_to_list(cl)
    height = len(list_of_lists)
    width = len(list_of_lists[0])
    size_tuple = (height, width)
    if size_tuple == df.shape:
        return True
    print('GOOGLE SHEET NOT UPDATED.')
    print('cl %s and df %s different sizes.' % (size_tuple, df.shape))
    return False


def a1(pos, reverse=False):
    """Return the column letter for numeric column index."""
    if reverse:
        return gspread.utils.a1_to_rowcol('%s1' % pos)[1]
    if str(pos).isdigit():
        return gspread.utils.rowcol_to_a1(1, pos)[:-1]
    else:
        return "Must be integer"


def link(gsheet_key):
    """Return GSheet URL for data from Web UI."""
    return 'https://docs.google.com/spreadsheets/d/%s/edit' % gsheet_key


def analytics():
    return build('analyticsreporting', 'v4', credentials=credentials)


def searchconsole():
    return build('webmasters', 'v3', credentials=credentials)


def ga(gaid, start, end, path):
    """Return Google Analytics metrics for a URL."""

    path = path.replace(',', r'\,')
    service = analytics()
    metrics = ['users', 'newUsers', 'sessions', 'bounceRate',
               'pageviewsPerSession', 'avgSessionDuration']
    metrics = ''.join(['ga:%s,' % x for x in metrics])[:-1]
    ga_request = service.data().ga().get(
        ids='ga:' + gaid,
        start_date=start,
        end_date=end,
        metrics=metrics,
        dimensions='ga:pagePath',
        sort='-ga:users',
        filters='ga:pagePath==' + path,
        segment='sessions::condition::ga:medium==organic',
        max_results=1
    )
    ga_response = ga_request.execute()
    rval = []
    if 'rows' in ga_response:
        raw_rows = ga_response['rows'][0]
        rval = raw_rows
    return rval


def gsc(prop, start, end, query, url):
    service = searchconsole()
    request = {
        "startDate": start,
        "endDate": end,
        "dimensions": [
            "query",
            "page"],
        "dimensionFilterGroups": [
        {
            "filters": [
            {
                "operator": "equals",
                "expression": url,
                "dimension": "page"
            },
            {
                "operator": "equals",
                "expression": query,
                "dimension": "query"
            }]
        }]
    }
    dat = service.searchanalytics().query(siteUrl=prop, body=request).execute()
    val = []
    if 'rows' in dat:  # For the foolish Hobgoblins of PEP8 consistency
        r = dat['rows'][0]
        val = [start] + [r['keys'][0]] + [r['keys'][1]] + [
            r['position']] + [r['clicks']] + [r['impressions']] + [r['ctr']]
    return val


def api_date(a_datetime, time=False):
    """Return datetime string in Google API friendly format."""

    if time:
        return ('{0:%Y-%m-%d %H:%M:%S}'.format(a_datetime))
    else:
        return ('{0:%Y-%m-%d}'.format(a_datetime))


def human_date(a_datetime, time=False):
    """Return datetime object as American-friendly string."""

    if time:
        return ('{0:%m/%d/%Y %H:%M:%S}'.format(a_datetime))
    else:
        return ('{0:%m/%d/%Y}'.format(a_datetime))


def email():
    """Return email given provided Google OAuth account."""
    service = build("oauth2", "v2", credentials=credentials)
    user_document = service.userinfo().get().execute()
    email = user_document['email']
    return email


def login():
    client_id = "769904540573-knscs3mhvd56odnf7i8h3al13kiqulft.apps.googleusercontent.com"
    client_secret = "D2F1D--b_yKNLrJSPmrn2jik"
    environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
    scopes = ["https://www.googleapis.com/auth/analytics.readonly", 
              "https://www.googleapis.com/auth/webmasters.readonly", 
              "https://www.googleapis.com/auth/yt-analytics.readonly",
              "https://www.googleapis.com/auth/youtube.readonly", 
              "https://spreadsheets.google.com/feeds/", 
              "https://www.googleapis.com/auth/gmail.modify", 
              "https://www.googleapis.com/auth/userinfo.email"] 
    client_config = {
        "installed": {
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
            "client_id": client_id,
            "client_secret": client_secret
        }
    }
    flow = InstalledAppFlow.from_client_config(client_config, scopes)
    credentials = flow.run_console()
    credentials.access_token = credentials.token
    with open("credentials.pickle", "wb") as output_file:
        pickle.dump(credentials, output_file)
    return credentials


def check_credentials(credentials):
    if type(credentials) == google.oauth2.credentials.Credentials:
        if not credentials.valid:
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
            credentials.access_token = credentials.token
            with open("credentials.pickle", "wb") as output_file:
                pickle.dump(credentials, output_file)
            if not credentials.valid:
                credentials = login()
        elif not credentials:
            credentials = login()
    else:
        credentials = login()


def logout():
    import requests
    from os import remove
    global credentials
    requests.post('https://accounts.google.com/o/oauth2/revoke',
        params={'token': credentials.token},
        headers = {'content-type': 'application/x-www-form-urlencoded'})
    try:
        remove('credentials.pickle')
    except:
        pass
    credentials = None


class Unbuffered(object):
    """Provides more real-time streaming in Jupyter Notebook"""

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


try:
    with open("credentials.pickle", "rb") as input_file:
        credentials = pickle.load(input_file)
        check_credentials(credentials)
except:
    credentials = login()

check_credentials(credentials)
gspread_authorized = gspread.authorize(credentials)
pygsheets_authorized = pygsheets.authorize(custom_credentials=credentials)

print("CONGRATULATIONS! You are logged in as <<< %s >>>" % email())
print('Get started with: pipulate.sheet("Insert your GSheet key or URL")')
print("For help, run: pipulate.help()")

stdout = Unbuffered(stdout)
