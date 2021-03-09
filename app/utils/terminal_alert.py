from colorama import Fore




class alerts():
    good = Fore.GREEN + '[*]' + Fore.RESET
    bad = Fore.RED + '[!]' + Fore.RESET
    warning = Fore.RED + '[$]' + Fore.RESET
    excellent = Fore.CYAN + '[$]' + Fore.RESET
    debug = '{}{}{}'.format(Fore.GREEN + '{' + Fore.RESET, Fore.RED + ' DEBUG ' + Fore.RESET, Fore.GREEN + '}' + Fore.RESET)
    debug_point = Fore.RED + '{*}' + Fore.RESET