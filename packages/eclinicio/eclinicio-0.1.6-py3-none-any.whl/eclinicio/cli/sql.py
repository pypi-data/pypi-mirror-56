from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import style_from_pygments_cls
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer
from pygments.styles import get_style_by_name
import click
from prettytable import PrettyTable

my_message = [('class:username', '\nmysql'), ('class:pound', '>')]


def SqlPrompt(message=None, ignore_case=True, completion_list=None, history_file=None,
              complete_while_typing=True, multiline=False, auto_suggest=True):
    'Returns an advanced prompt for working with your sql commandline apps'

    params = dict(complete_while_typing=complete_while_typing,
                  multiline=multiline,
                  lexer=PygmentsLexer(SqlLexer),
                  style=style_from_pygments_cls(get_style_by_name('monokai'))
                  )

    if isinstance(completion_list, list):
        params['completer'] = WordCompleter(completion_list, ignore_case=ignore_case)

    if history_file is not None:
        params['history'] = FileHistory(history_file)

    if auto_suggest is True:
        params['auto_suggest'] = AutoSuggestFromHistory()

    return prompt(message or my_message, **params)


def get_sql_keywords():
    'Returns a list standard sql keywords'

    keywords = ["ADD", "ADDCONSTRAINT", "ALTER", "ALTER COLUMN", "ALTER TABLE", "ALL",
                "AND", "ANY", "AS", "ASC", "BACKUP DATABASE", "BETWEEN", "CASE", "CHECK",
                "COLUMN", "CONSTRAINT", "CREATE", "CREATE DATABASE", "CREATE", "INDEX",
                "CREATE OR REPLACE VIEW", "CREATE TABLE", "CREATE PROCEDURE", "CREATE UNIQUE INDEX",
                "CREATE VIEW", "DATABASE", "DEFAULT", "DELETE", "DESC", "DISTINCT", "DROP",
                "DROP COLUMN", "DROP CONSTRAINT", "DROP DATABASE", "DROP DEFAULT", "DROP INDEX",
                "DROP TABLE", "DROP VIEW", "EXEC", "EXISTS", "FOREIGN KEY",
                "FROM", "FULL OUTER JOIN", "GROUP BY", "HAVING", "IN", "INDEX", "INNER JOIN",
                "INSERT", "INSERT INTO", "INSERT INTO SELECT", "IS NULL", "IS NOT NULL", "JOIN",
                "LEFT JOIN", "LIKE", "LIMIT", "NOT", "NOT NULL", "OR", "ORDER BY", "OUTER JOIN", "PRIMARY KEY",
                "PROCEDURE", "RIGHT JOIN", "ROWNUM", "SELECT", "SELECT DISTINCT", "SELECT INTO",
                "SELECT TOP", "SET", "TABLE", "TOP", "TRUNCATE TABLE", "UNION", "UNION ALL",
                "UNIQUE", "UPDATE", "VALUES", "VIEW", "WHERE"]

    keywords += ['ASCII', 'CHAR_LENGTH', 'CHARACTER_LENGTH', 'CONCAT', 'CONCAT_WS', 'FIELD', 'FIND_IN_SET', 'FORMAT', 'INSERT',
                 'INSTR', 'LCASE', 'LEFT', 'LENGTH', 'LOCATE', 'LOWER', 'LPAD', 'LTRIM', 'MID', 'POSITION', 'REPEAT', 'REPLACE', 'REVERSE', 'RIGHT', 'RPAD',
                 'RTRIM', 'SPACE', 'STRCMP', 'SUBSTR', 'SUBSTRING', 'SUBSTRING_INDEX', 'TRIM', 'UCASE', 'UPPER']

    keywords += ['ABS', 'ACOS', 'ASIN', 'ATAN', 'ATAN2', 'AVG', 'CEIL', 'CEILING', 'COS', 'COT',
                 'COUNT', 'DEGREES', 'DIV', 'EXP', 'FLOOR', 'GREATEST', 'LEAST', 'LN', 'LOG', 'LOG10', 'LOG2', 'MAX', 'MIN',
                 'MOD', 'PI', 'POW', 'POWER', 'RADIANS', 'RAND', 'ROUND', 'SIGN', 'SIN', 'SQRT', 'SUM', 'TAN', 'TRUNCATE']

    keywords += ['ADDDATE', 'ADDTIME', 'CURDATE', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURTIME', 'DATE', 'DATEDIFF',
                 'DATE_ADD', 'DATE_FORMAT', 'DATE_SUB', 'DAY', 'DAYNAME', 'DAYOFMONTH', 'DAYOFWEEK', 'DAYOFYEAR', 'EXTRACT', 'FROM_DAYS', 'HOUR', 'LAST_DAY',
                 'LOCALTIME', 'LOCALTIMESTAMP', 'MAKEDATE', 'MAKETIME', 'MICROSECOND', 'MINUTE', 'MONTH', 'MONTHNAME', 'NOW', 'PERIOD_ADD', 'PERIOD_DIFF',
                 'QUARTER', 'SECOND', 'SEC_TO_TIME', 'STR_TO_DATE', 'SUBDATE', 'SUBTIME', 'SYSDATE', 'TIME', 'TIME_FORMAT', 'TIME_TO_SEC',
                 'TIMEDIFF', 'TIMESTAMP', 'TO_DAYS', 'WEEK', 'WEEKDAY', 'WEEKOFYEAR', 'YEAR', 'YEARWEEK']

    keywords += ['BIN', 'BINARY', 'CASE', 'CAST', 'COALESCE', 'CONNECTION_ID', 'CONV', 'CONVERT', 'CURRENT_USER', 'DATABASE',
                 'IF', 'IFNULL', 'ISNULL', 'LAST_INSERT_ID', 'NULLIF', 'SESSION_USER', 'SYSTEM_USER', 'USER', 'VERSION']
    return keywords


def HandleSQLResults(results, foreground='blue', bg='black', bold=True):
    "Prints a list of dicts of Query results in a PrettyTable"

    if isinstance(results, list) and len(results) > 0:
        headers = results[0].keys()
        t = PrettyTable(headers)
        rows = [_dict.values() for _dict in results]

        for row in rows:
            new_row = []
            for item in row:
                new_row.append(item)
            t.add_row(new_row)

        click.secho(str(t), fg='blue', bold=True)
        click.secho("Returned: %s row(s) " % str(len(rows)), fg='green', bold=True)


def Input(msg, required=True, _type=str):
    '''
    Prompt for a value.
    msg: prompt message
    _type: The type of value(int, str, bool, float)
    if required is True, a value must be entered,
    otherwise a while loop will continue.
    '''

    while True:
        value = input(msg + ": ")
        value = value.strip()
        if not value and required is True:
            continue
        try:
            value = _type(value)
        except:
            print('Invalid Value: ', value)
            continue
        else:
            return value


if __name__ == '__main__':
    completion_list = get_sql_keywords()
    cli = SqlPrompt(completion_list=completion_list)
