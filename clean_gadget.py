import re

# keywords up to C11 and C++17; immutable set
keywords = frozenset(['__asm', '__builtin', '__cdecl', '__declspec', '__except', '__export', '__far16', '__far32',
                      '__fastcall', '__finally', '__import', '__inline', '__int16', '__int32', '__int64', '__int8',
                      '__leave', '__optlink', '__packed', '__pascal', '__stdcall', '__system', '__thread', '__try',
                      '__unaligned', '_asm', '_Builtin', '_Cdecl', '_declspec', '_except', '_Export', '_Far16',
                      '_Far32', '_Fastcall', '_finally', '_Import', '_inline', '_int16', '_int32', '_int64',
                      '_int8', '_leave', '_Optlink', '_Packed', '_Pascal', '_stdcall', '_System', '_try', 'alignas',
                      'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor', 'bool', 'break', 'case',
                      'catch', 'char', 'char16_t', 'char32_t', 'class', 'compl', 'const', 'const_cast', 'constexpr',
                      'continue', 'decltype', 'default', 'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum',
                      'explicit', 'export', 'extern', 'false', 'final', 'float', 'for', 'friend', 'goto', 'if',
                      'inline', 'int', 'long', 'mutable', 'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr',
                      'operator', 'or', 'or_eq', 'override', 'private', 'protected', 'public', 'register',
                      'reinterpret_cast', 'return', 'short', 'signed', 'sizeof', 'static', 'static_assert',
                      'static_cast', 'struct', 'switch', 'template', 'this', 'thread_local', 'throw', 'true', 'try',
                      'typedef', 'typeid', 'typename', 'union', 'unsigned', 'using', 'virtual', 'void', 'volatile',
                      'wchar_t', 'while', 'xor', 'xor_eq', 'NULL', 'StrNCat', 'getaddrinfo', '_ui64toa', 'fclose',
                      'pthread_mutex_lock', 'gets_s', 'sleep', '_ui64tot', 'freopen_s', '_ui64tow', 'send', 'lstrcat',
                      'HMAC_Update', '__fxstat', 'StrCatBuff', '_mbscat', '_mbstok_s', '_cprintf_s',
                      'ldap_search_init_page', 'memmove_s', 'ctime_s', 'vswprintf', 'vswprintf_s', '_snwprintf',
                      '_gmtime_s', '_tccpy', '*RC6*', '_mbslwr_s', 'random', '__wcstof_internal', '_wcslwr_s',
                      '_ctime32_s', 'wcsncat*', 'MD5_Init', '_ultoa', 'snprintf', 'memset', 'syslog', '_vsnprintf_s',
                      'HeapAlloc', 'pthread_mutex_destroy', 'ChangeWindowMessageFilter', '_ultot', 'crypt_r',
                      '_strupr_s_l', 'LoadLibraryExA', '_strerror_s', 'LoadLibraryExW', 'wvsprintf', 'MoveFileEx',
                      '_strdate_s', 'SHA1', 'sprintfW', 'StrCatNW', '_scanf_s_l', 'pthread_attr_init', '_wtmpnam_s',
                      'snscanf', '_sprintf_s_l', 'dlopen', 'sprintfA', 'timed_mutex', 'OemToCharA', 'ldap_delete_ext',
                      'sethostid', 'popen', 'OemToCharW', '_gettws', 'vfork', '_wcsnset_s_l', 'sendmsg', '_mbsncat',
                      'wvnsprintfA', 'HeapFree', '_wcserror_s', 'realloc', '_snprintf*', 'wcstok', '_strncat*',
                      'StrNCpy', '_wasctime_s', 'push*', '_lfind_s', 'CC_SHA512', 'ldap_compare_ext_s', 'wcscat_s',
                      'strdup', '_chsize_s', 'sprintf_s', 'CC_MD4_Init', 'wcsncpy', '_wfreopen_s', '_wcsupr_s',
                      '_searchenv_s', 'ldap_modify_ext_s', '_wsplitpath', 'CC_SHA384_Final', 'MD2', 'RtlCopyMemory',
                      'lstrcatW', 'MD4', 'MD5', '_wcstok_s_l', '_vsnwprintf_s', 'ldap_modify_s', 'strerror',
                      '_lsearch_s', '_mbsnbcat_s', '_wsplitpath_s', 'MD4_Update', '_mbccpy_s', '_strncpy_s_l',
                      '_snprintf_s', 'CC_SHA512_Init', 'fwscanf_s', '_snwprintf_s', 'CC_SHA1', 'swprintf', 'fprintf',
                      'EVP_DigestInit_ex', 'strlen', 'SHA1_Init', 'strncat', '_getws_s', 'CC_MD4_Final', 'wnsprintfW',
                      'lcong48', 'lrand48', 'write', 'HMAC_Init', '_wfopen_s', 'wmemchr', '_tmakepath', 'wnsprintfA',
                      'lstrcpynW', 'scanf_s', '_mbsncpy_s_l', '_localtime64_s', 'fstream.open', '_wmakepath',
                      'Connection.open', '_tccat', 'valloc', 'setgroups', 'unlink', 'fstream.put', 'wsprintfA',
                      '*SHA1*', '_wsearchenv_s', 'ualstrcpyA', 'CC_MD5_Update', 'strerror_s', 'HeapCreate',
                      'ualstrcpyW', '__xstat', '_wmktemp_s', 'StrCatChainW', 'ldap_search_st', '_mbstowcs_s_l',
                      'ldap_modify_ext', '_mbsset_s', 'strncpy_s', 'move', 'execle', 'StrCat', 'xrealloc', 'wcsncpy_s',
                      '_tcsncpy*', 'execlp', 'RIPEMD160_Final', 'ldap_search_s', 'EnterCriticalSection', '_wctomb_s_l',
                      'fwrite', '_gmtime64_s', 'sscanf_s', 'wcscat', '_strupr_s', 'wcrtomb_s', 'VirtualLock',
                      'ldap_add_ext_s', '_mbscpy', '_localtime32_s', 'lstrcpy', '_wcsncpy*', 'CC_SHA1_Init', '_getts',
                      '_wfopen', '__xstat64', 'strcoll', '_fwscanf_s_l', '_mbslwr_s_l', 'RegOpenKey', 'makepath',
                      'seed48', 'CC_SHA256', 'sendto', 'execv', 'CalculateDigest', 'memchr', '_mbscpy_s', '_strtime_s',
                      'ldap_search_ext_s', '_chmod', 'flock', '__fxstat64', '_vsntprintf', 'CC_SHA256_Init', '_itoa_s',
                      '__wcserror_s', '_gcvt_s', 'fstream.write', 'sprintf', 'recursive_mutex', 'strrchr',
                      'gethostbyaddr', '_wcsupr_s_l', 'strcspn', 'MD5_Final', 'asprintf', '_wcstombs_s_l', '_tcstok',
                      'free', 'MD2_Final', 'asctime_s', '_alloca', '_wputenv_s', '_wcsset_s', '_wcslwr_s_l',
                      'SHA1_Update', 'filebuf.sputc', 'filebuf.sputn', 'SQLConnect', 'ldap_compare', 'mbstowcs_s',
                      'HMAC_Final', 'pthread_condattr_init', '_ultow_s', 'rand', 'ofstream.put', 'CC_SHA224_Final',
                      'lstrcpynA', 'bcopy', 'system', 'CreateFile*', 'wcscpy_s', '_mbsnbcpy*', 'open', '_vsnwprintf',
                      'strncpy', 'getopt_long', 'CC_SHA512_Final', '_vsprintf_s_l', 'scanf', 'mkdir', '_localtime_s',
                      '_snprintf', '_mbccpy_s_l', 'memcmp', 'final', '_ultoa_s', 'lstrcpyW', 'LoadModule',
                      '_swprintf_s_l', 'MD5_Update', '_mbsnset_s_l', '_wstrtime_s', '_strnset_s', 'lstrcpyA',
                      '_mbsnbcpy_s', 'mlock', 'IsBadHugeWritePtr', 'copy', '_mbsnbcpy_s_l', 'wnsprintf', 'wcscpy',
                      'ShellExecute', 'CC_MD4', '_ultow', '_vsnwprintf_s_l', 'lstrcpyn', 'CC_SHA1_Final', 'vsnprintf',
                      '_mbsnbset_s', '_i64tow', 'SHA256_Init', 'wvnsprintf', 'RegCreateKey', 'strtok_s', '_wctime32_s',
                      '_i64toa', 'CC_MD5_Final', 'wmemcpy', 'WinExec', 'CreateDirectory*', 'CC_SHA256_Update',
                      '_vsnprintf_s_l', 'jrand48', 'wsprintf', 'ldap_rename_ext_s', 'filebuf.open', '_wsystem',
                      'SHA256_Update', '_cwscanf_s', 'wsprintfW', '_sntscanf', '_splitpath', 'fscanf_s', 'strpbrk',
                      'wcstombs_s', 'wscanf', '_mbsnbcat_s_l', 'strcpynA', 'pthread_cond_init', 'wcsrtombs_s',
                      '_wsopen_s', 'CharToOemBuffA', 'RIPEMD160_Update', '_tscanf', 'HMAC', 'StrCCpy',
                      'Connection.connect', 'lstrcatn', '_mbstok', '_mbsncpy', 'CC_SHA384_Update', 'create_directories',
                      'pthread_mutex_unlock', 'CFile.Open', 'connect', '_vswprintf_s_l', '_snscanf_s_l', 'fputc',
                      '_wscanf_s', '_snprintf_s_l', 'strtok', '_strtok_s_l', 'lstrcatA', 'snwscanf',
                      'pthread_mutex_init', 'fputs', 'CC_SHA384_Init', '_putenv_s', 'CharToOemBuffW',
                      'pthread_mutex_trylock', '__wcstoul_internal', '_memccpy', '_snwprintf_s_l', '_strncpy*',
                      'wmemset', 'MD4_Init', '*RC4*', 'strcpyW', '_ecvt_s', 'memcpy_s', 'erand48', 'IsBadHugeReadPtr',
                      'strcpyA', 'HeapReAlloc', 'memcpy', 'ldap_rename_ext', 'fopen_s', 'srandom', '_cgetws_s',
                      '_makepath', 'SHA256_Final', 'remove', '_mbsupr_s', 'pthread_mutexattr_init',
                      '__wcstold_internal', 'StrCpy', 'ldap_delete', 'wmemmove_s', '_mkdir', 'strcat', '_cscanf_s_l',
                      'StrCAdd', 'swprintf_s', '_strnset_s_l', 'close', 'ldap_delete_ext_s', 'ldap_modrdn', 'strchr',
                      '_gmtime32_s', '_ftcscat', 'lstrcatnA', '_tcsncat', 'OemToChar', 'mutex', 'CharToOem', 'strcpy_s',
                      'lstrcatnW', '_wscanf_s_l', '__lxstat64', 'memalign', 'MD2_Init', 'StrCatBuffW', 'StrCpyN',
                      'CC_MD5', 'StrCpyA', 'StrCatBuffA', 'StrCpyW', 'tmpnam_r', '_vsnprintf', 'strcatA', 'StrCpyNW',
                      '_mbsnbset_s_l', 'EVP_DigestInit', '_stscanf', 'CC_MD2', '_tcscat', 'StrCpyNA', 'xmalloc',
                      '_tcslen', '*MD4*', 'vasprintf', 'strxfrm', 'chmod', 'ldap_add_ext', 'alloca', '_snscanf_s',
                      'IsBadWritePtr', 'swscanf_s', 'wmemcpy_s', '_itoa', '_ui64toa_s', 'EVP_DigestUpdate',
                      '__wcstol_internal', '_itow', 'StrNCatW', 'strncat_s', 'ualstrcpy', 'execvp', '_mbccat',
                      'EVP_MD_CTX_init', 'assert', 'ofstream.write', 'ldap_add', '_sscanf_s_l', 'drand48', 'CharToOemW',
                      'swscanf', '_itow_s', 'RIPEMD160_Init', 'CopyMemory', 'initstate', 'getpwuid', 'vsprintf',
                      '_fcvt_s', 'CharToOemA', 'setuid', 'malloc', 'StrCatNA', 'strcat_s', 'srand', 'getwd',
                      '_controlfp_s', 'olestrcpy', '__wcstod_internal', '_mbsnbcat', 'lstrncat', 'des_*',
                      'CC_SHA224_Init', 'set*', 'vsprintf_s', 'SHA1_Final', '_umask_s', 'gets', 'setstate',
                      'wvsprintfW', 'LoadLibraryEx', 'ofstream.open', 'calloc', '_mbstrlen', '_cgets_s', '_sopen_s',
                      'IsBadStringPtr', 'wcsncat_s', 'add*', 'nrand48', 'create_directory', 'ldap_search_ext',
                      '_i64toa_s', '_ltoa_s', '_cwscanf_s_l', 'wmemcmp', '__lxstat', 'lstrlen',
                      'pthread_condattr_destroy', '_ftcscpy', 'wcstok_s', '__xmknod', 'pthread_attr_destroy',
                      'sethostname', '_fscanf_s_l', 'StrCatN', 'RegEnumKey', '_tcsncpy', 'strcatW', 'AfxLoadLibrary',
                      'setenv', 'tmpnam', '_mbsncat_s_l', '_wstrdate_s', '_wctime64_s', '_i64tow_s', 'CC_MD4_Update',
                      'ldap_add_s', '_umask', 'CC_SHA1_Update', '_wcsset_s_l', '_mbsupr_s_l', 'strstr', '_tsplitpath',
                      'memmove', '_tcscpy', 'vsnprintf_s', 'strcmp', 'wvnsprintfW', 'tmpfile', 'ldap_modify',
                      '_mbsncat*', 'mrand48', 'sizeof', 'StrCatA', '_ltow_s', '*desencrypt*', 'StrCatW', '_mbccpy',
                      'CC_MD2_Init', 'RIPEMD160', 'ldap_search', 'CC_SHA224', 'mbsrtowcs_s', 'update', 'ldap_delete_s',
                      'getnameinfo', '*RC5*', '_wcsncat_s_l', 'DriverManager.getConnection', 'socket', '_cscanf_s',
                      'ldap_modrdn_s', '_wopen', 'CC_SHA256_Final', '_snwprintf*', 'MD2_Update', 'strcpy',
                      '_strncat_s_l', 'CC_MD5_Init', 'mbscpy', 'wmemmove', 'LoadLibraryW', '_mbslen', '*alloc',
                      '_mbsncat_s', 'LoadLibraryA', 'fopen', 'StrLen', 'delete', '_splitpath_s',
                      'CreateFileTransacted*', 'MD4_Final', '_open', 'CC_SHA384', 'wcslen', 'wcsncat', '_mktemp_s',
                      'pthread_mutexattr_destroy', '_snwscanf_s', '_strset_s', '_wcsncpy_s_l', 'CC_MD2_Final',
                      '_mbstok_s_l', 'wctomb_s', 'MySQL_Driver.connect', '_snwscanf_s_l', '*_des_*', 'LoadLibrary',
                      '_swscanf_s_l', 'ldap_compare_s', 'ldap_compare_ext', '_strlwr_s', 'GetEnvironmentVariable',
                      'cuserid', '_mbscat_s', 'strspn', '_mbsncpy_s', 'ldap_modrdn2', 'LeaveCriticalSection',
                      'CopyFile', 'getpwd', 'sscanf', 'creat', 'RegSetValue', 'ldap_modrdn2_s', 'CFile.Close',
                      '*SHA_1*', 'pthread_cond_destroy', 'CC_SHA512_Update', '*RC2*', 'StrNCatA', '_mbsnbcpy',
                      '_mbsnset_s', 'crypt', 'excel', '_vstprintf', 'xstrdup', 'wvsprintfA', 'getopt', 'mkstemp',
                      '_wcsnset_s', '_stprintf', '_sntprintf', 'tmpfile_s', 'OpenDocumentFile', '_mbsset_s_l',
                      '_strset_s_l', '_strlwr_s_l', 'ifstream.open', 'xcalloc', 'StrNCpyA', '_wctime_s',
                      'CC_SHA224_Update', '_ctime64_s', 'MoveFile', 'chown', 'StrNCpyW', 'IsBadReadPtr', '_ui64tow_s',
                      'IsBadCodePtr', 'getc', 'OracleCommand.ExecuteOracleScalar', 'AccessDataSource.Insert',
                      'IDbDataAdapter.FillSchema', 'IDbDataAdapter.Update', 'GetWindowText*', 'SendMessage',
                      'SqlCommand.ExecuteNonQuery', 'streambuf.sgetc', 'streambuf.sgetn', 'OracleCommand.ExecuteScalar',
                      'SqlDataSource.Update', '_Read_s', 'IDataAdapter.Fill', '_wgetenv', '_RecordsetPtr.Open*',
                      'AccessDataSource.Delete', 'Recordset.Open*', 'filebuf.sbumpc', 'DDX_*', 'RegGetValue',
                      'fstream.read*', 'SqlCeCommand.ExecuteResultSet', 'SqlCommand.ExecuteXmlReader', 'main',
                      'streambuf.sputbackc', 'read', 'm_lpCmdLine', 'CRichEditCtrl.Get*', 'istream.putback',
                      'SqlCeCommand.ExecuteXmlReader', 'SqlCeCommand.BeginExecuteXmlReader', 'filebuf.sgetn',
                      'OdbcDataAdapter.Update', 'filebuf.sgetc', 'SQLPutData', 'recvfrom',
                      'OleDbDataAdapter.FillSchema', 'IDataAdapter.FillSchema', 'CRichEditCtrl.GetLine',
                      'DbDataAdapter.Update', 'SqlCommand.ExecuteReader', 'istream.get', 'ReceiveFrom', '_main',
                      'fgetc', 'DbDataAdapter.FillSchema', 'kbhit', 'UpdateCommand.Execute*', 'Statement.execute',
                      'fgets', 'SelectCommand.Execute*', 'getch', 'OdbcCommand.ExecuteNonQuery', 'CDaoQueryDef.Execute',
                      'fstream.getline', 'ifstream.getline', 'SqlDataAdapter.FillSchema', 'OleDbCommand.ExecuteReader',
                      'Statement.execute*', 'SqlCeCommand.BeginExecuteNonQuery', 'OdbcCommand.ExecuteScalar',
                      'SqlCeDataAdapter.Update', 'sendmessage', 'mysqlpp.DBDriver', 'fstream.peek', 'Receive',
                      'CDaoRecordset.Open', 'OdbcDataAdapter.FillSchema', '_wgetenv_s', 'OleDbDataAdapter.Update',
                      'readsome', 'SqlCommand.BeginExecuteXmlReader', 'recv', 'ifstream.peek', '_Main', '_tmain',
                      '_Readsome_s', 'SqlCeCommand.ExecuteReader', 'OleDbCommand.ExecuteNonQuery', 'fstream.get',
                      'IDbCommand.ExecuteScalar', 'filebuf.sputbackc', 'IDataAdapter.Update', 'streambuf.sbumpc',
                      'InsertCommand.Execute*', 'RegQueryValue', 'IDbCommand.ExecuteReader', 'SqlPipe.ExecuteAndSend',
                      'Connection.Execute*', 'getdlgtext', 'ReceiveFromEx', 'SqlDataAdapter.Update', 'RegQueryValueEx',
                      'SQLExecute', 'pread', 'SqlCommand.BeginExecuteReader', 'AfxWinMain', 'getchar',
                      'istream.getline', 'SqlCeDataAdapter.Fill', 'OleDbDataReader.ExecuteReader',
                      'SqlDataSource.Insert', 'istream.peek', 'SendMessageCallback', 'ifstream.read*',
                      'SqlDataSource.Select', 'SqlCommand.ExecuteScalar', 'SqlDataAdapter.Fill',
                      'SqlCommand.BeginExecuteNonQuery', 'getche', 'SqlCeCommand.BeginExecuteReader', 'getenv',
                      'streambuf.snextc', 'Command.Execute*', '_CommandPtr.Execute*', 'SendNotifyMessage',
                      'OdbcDataAdapter.Fill', 'AccessDataSource.Update', 'fscanf', 'QSqlQuery.execBatch',
                      'DbDataAdapter.Fill', 'cin', 'DeleteCommand.Execute*', 'QSqlQuery.exec', 'PostMessage',
                      'ifstream.get', 'filebuf.snextc', 'IDbCommand.ExecuteNonQuery', 'Winmain', 'fread', 'getpass',
                      'GetDlgItemTextCCheckListBox.GetCheck', 'DISP_PROPERTY_EX', 'pread64', 'Socket.Receive*',
                      'SACommand.Execute*', 'SQLExecDirect', 'SqlCeDataAdapter.FillSchema', 'DISP_FUNCTION',
                      'OracleCommand.ExecuteNonQuery', 'CEdit.GetLine', 'OdbcCommand.ExecuteReader', 'CEdit.Get*',
                      'AccessDataSource.Select', 'OracleCommand.ExecuteReader', 'OCIStmtExecute', 'getenv_s',
                      'DB2Command.Execute*', 'OracleDataAdapter.FillSchema', 'OracleDataAdapter.Fill', 'CComboBox.Get*',
                      'SqlCeCommand.ExecuteNonQuery', 'OracleCommand.ExecuteOracleNonQuery', 'mysqlpp.Query',
                      'istream.read*', 'CListBox.GetText', 'SqlCeCommand.ExecuteScalar', 'ifstream.putback', 'readlink',
                      'CHtmlEditCtrl.GetDHtmlDocument', 'PostThreadMessage', 'CListCtrl.GetItemText',
                      'OracleDataAdapter.Update', 'OleDbCommand.ExecuteScalar', 'stdin', 'SqlDataSource.Delete',
                      'OleDbDataAdapter.Fill', 'fstream.putback', 'IDbDataAdapter.Fill', '_wspawnl', 'fwprintf',
                      'sem_wait', '_unlink', 'ldap_search_ext_sW', 'signal', 'PQclear', 'PQfinish', 'PQexec',
                      'PQresultStatus','ifdef','endif','bool','void'])
# holds known non-user-defined functions; immutable set
main_set = frozenset({'main'})
# arguments in main function; immutable set
main_args = frozenset({'argc', 'argv'})

# input is a list of string lines
def clean_gadget(gadget):
    # dictionary; map function name to symbol name + number
    fun_symbols = {}
    # dictionary; map variable name to symbol name + number
    var_symbols = {}

    fun_count = 1
    var_count = 1

    # regular expression to catch multi-line comment
    rx_comment = re.compile('\*/\s*$')
    # regular expression to find function name candidates
    rx_fun = re.compile(r'\b([_A-Za-z]\w*)\b(?=\s*\()')
    # regular expression to find variable name candidates
    #rx_var = re.compile(r'\b([_A-Za-z]\w*)\b(?!\s*\()')
    rx_var = re.compile(r'\b([_A-Za-z]\w*)\b(?:(?=\s*\w+\()|(?!\s*\w+))(?!\s*\()')

    # final cleaned gadget output to return to interface
    cleaned_gadget = []

    for line in gadget:
        # process if not the header line and not a multi-line commented line
        if rx_comment.search(line) is None:
            # remove all string literals (keep the quotes)
            nostrlit_line = re.sub(r'".*?"', '""', line)
            # remove all character literals
            nocharlit_line = re.sub(r"'.*?'", "''", nostrlit_line)
            # replace any non-ASCII characters with empty string
            ascii_line = re.sub(r'[^\x00-\x7f]', r'', nocharlit_line)

            # return, in order, all regex matches at string list; preserves order for semantics
            user_fun = rx_fun.findall(ascii_line)
            user_var = rx_var.findall(ascii_line)

            # Could easily make a "clean gadget" type class to prevent duplicate functionality
            # of creating/comparing symbol names for functions and variables in much the same way.
            # The comparison frozenset, symbol dictionaries, and counters would be class scope.
            # So would only need to pass a string list and a string literal for symbol names to
            # another function.
            for fun_name in user_fun:
                if len({fun_name}.difference(main_set)) != 0 and len({fun_name}.difference(keywords)) != 0:
                    # DEBUG
                    #print('comparing ' + str(fun_name + ' to ' + str(main_set)))
                    #print(fun_name + ' diff len from main is ' + str(len({fun_name}.difference(main_set))))
                    #print('comparing ' + str(fun_name + ' to ' + str(keywords)))
                    #print(fun_name + ' diff len from keywords is ' + str(len({fun_name}.difference(keywords))))
                    ###
                    # check to see if function name already in dictionary
                    if fun_name not in fun_symbols.keys():
                        fun_symbols[fun_name] = 'FUN' + str(fun_count)
                        fun_count += 1
                    # ensure that only function name gets replaced (no variable name with same
                    # identifier); uses positive lookforward
                    ascii_line = re.sub(r'\b(' + fun_name + r')\b(?=\s*\()', fun_symbols[fun_name], ascii_line)

            for var_name in user_var:
                # next line is the nuanced difference between fun_name and var_name
                if len({var_name}.difference(keywords)) != 0 and len({var_name}.difference(main_args)) != 0:
                    # DEBUG
                    #print('comparing ' + str(var_name + ' to ' + str(keywords)))
                    #print(var_name + ' diff len from keywords is ' + str(len({var_name}.difference(keywords))))
                    #print('comparing ' + str(var_name + ' to ' + str(main_args)))
                    #print(var_name + ' diff len from main args is ' + str(len({var_name}.difference(main_args))))
                    ###
                    # check to see if variable name already in dictionary
                    if var_name not in var_symbols.keys():
                        var_symbols[var_name] = 'VAR' + str(var_count)
                        var_count += 1
                    # ensure that only variable name gets replaced (no function name with same
                    # identifier); uses negative lookforward
                    ascii_line = re.sub(r'\b(' + var_name + r')\b(?:(?=\s*\w+\()|(?!\s*\w+))(?!\s*\()', \
                                        var_symbols[var_name], ascii_line)

            cleaned_gadget.append(ascii_line)
    # return the list of cleaned lines
    # print(cleaned_gadget)
    return cleaned_gadget

if __name__ == '__main__':
    test_gadget = ['231 151712/shm_setup.c inputfunc 11\n',
                   'int main(int argc, char **argv) {\n',
                   'while ((c = getopt(argc, argv, "k:s:m:o:h")) != -1) {\n',
                   'switch(c) {']

    test_gadget2 = ['278 151587/ffmpeg.c inputfunc 3159', 'int main(int argc,char **argv)',
                    'parse_loglevel(argc,argv,options);', 'if (argc > 1 && !strcmp(argv[1],"-d")) {',
                    'argc--;', 'argv++;', 'show_banner(argc,argv,options);',
                    'ret = ffmpeg_parse_options(argc,argv);', 'if (ret < 0) {']

    test_gadget3 = ['invalid_memory_access_012_s_001 *s;',
                    's = (invalid_memory_access_012_s_001 *)calloc(1,sizeof(invalid_memory_access_012_s_001));',
                    's->a = 20;', 's->b = 20;', 's->uninit = 20;', 'free(s);]']

    test_gadgetline = ['function(File file, Buffer buff)', 'this is a comment test */']

    split_test = 'printf ( " " , variable ++  )'.split()

    print(test_gadget)
    clean_gadget(test_gadget)
    # print(clean_gadget(test_gadget))
    # print(clean_gadget(test_gadget2))
    # print(clean_gadget(test_gadget3))
    # print(clean_gadget(test_gadgetline))
    # print(split_test)
