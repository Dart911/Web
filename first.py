import sqlite3, random

def main():
    """ Точка входа программы """
    db1 = "one" # наименование первой таблицы
    db2 = "two" # наименование второй таблицы
    create (db1)
    create (db2)
    print("TABLE 1")
    print("="*20)
    view(db1)
    print("\n\n\n")
    print("TABLE 2")
    print("="*20)
    view(db2)
    print("\n\n\n")
    print("COMPARISON")
    print("="*20)
    comparison (db1, db2)
    print("\n\n\n")
    print("COMPLEMENTATION")
    print("="*20)
    complement (db2, db1)
    view(db2)

def create(table):
    """ Создание таблицы, первичное заполнение случайными числами.

    Аргументы:
    table-- наименование таблицы

    """
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    try:
        c.execute("""
            DROP TABLE IF EXISTS {0}; 
            """.format(table))
        conn.commit()
        c.execute("""
            CREATE TABLE {0} (  
                first INTEGER, 
                second INTEGER
                );
            """.format(table))
        conn.commit()
    except sqlite3.DatabaseError as x:
        print ("Ошибка: ", x)

    v = 10
    while v:
        v-=1
        a = random.randint(0, 1000)
        b = random.randint(0, 1000)
        c.execute("""INSERT INTO {0} VALUES ({1},{2});
            """.format(table, a, b))
        conn.commit()
    c.close()

def view(table):
    """ Вывод содержимого таблицы на экран.

    Аргументы:
    table-- наименование таблицы

    """
    conn = sqlite3.connect('test.db')
    print ("*"*10)
    c = conn.cursor()
    c.execute("""
        SELECT first, second FROM {0};
        """.format(table))
    print("first\t second")
    for a, b in c.fetchall():
        print ("{0}\t{1}".format(a, b))
        
    c.close()

def comparison(tb1, tb2):
    """ Вывод различий в двух базах.

        Аргументы:
        tb1-- наименование таблицы 1
        tb2-- наименование таблицы 2

        """

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute(
          """SELECT * FROM {0}
          		WHERE not exists (SELECT * FROM {1} 
          			WHERE	{1}.first={0}.first AND {1}.second={0}.second)
          	 union 
          	 SELECT * FROM {1}
          		WHERE not exists (
          			SELECT * FROM {0} 
          				WHERE {1}.first={0}.first AND {1}.second={0}.second
          	)""".format(tb1, tb2))
    for row in c:
        print (row)
        
    c.close()

def complement(tb2, tb1):
    """ Дополнение таблицы 2 данными таблицы 1

    Аргументы:
        tb1-- наименование таблицы 1
        tb2-- наименование таблицы 2

    """
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("""INSERT INTO {1} SELECT * FROM {0} 
            			WHERE not exists 
            				(SELECT * FROM {1} 
            					WHERE {1}.first={0}.first AND {1}.second={0}.second)
            	""".format(tb1, tb2))
    conn.commit()
    c.close

if __name__ == '__main__':
    main ()
