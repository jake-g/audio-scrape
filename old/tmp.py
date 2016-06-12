#!/usr/bin/env python




def main():
    """
    Run the interactive session
    """

        while search.strip() == '':     # enter search string
            search = raw_input('Enter Search String\n> ')
        search = quote_plus(search)

        if not valid_url(search):



if __name__ == '__main__':
    main()
