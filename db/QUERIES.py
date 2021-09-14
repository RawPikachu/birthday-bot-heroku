create_birthday_table = '''create table birthday (id text primary key, day numeric, month numeric, year NUMERIC )'''

delete_birthday_table = '''drop table if exists birthday'''

create_birthday = '''insert into birthday (id, day, month, year ) values (%s, %s, %s, %s) on conflict (id) do update set month = %s, day = %s, year = %s  where birthday.id = %s'''

update_birthday = '''update birthday set month = %s, day = %s, year = %s  where id = %s'''

delete_birthday = '''delete from birthday where id=%s'''

get_birthday_all = '''select * from birthday'''

get_birthday_one = '''select * from birthday where id = %s'''

create_server_list_table = '''create table server_list (name text primary key, total_players numeric, timestamp numeric, uptime text, min30_chest_count numeric, chest_count numeric, last_chest_count numeric )'''

delete_server_list_table = '''drop table if exists server_list'''

create_server_list = '''insert into server_list (name, total_players, timestamp, min30_chest_count, chest_count, last_chest_count ) values (%s, %s, %s, %s, %s, %s)'''

update_server_list = '''update server_list set total_players = %s, timestamp = %s, uptime = %s, min30_chest_count = %s, chest_count = %s, last_chest_count = %s where name = %s'''

delete_server_list = '''delete from server_list where name=%s'''

get_server_list_all = '''select * from server_list'''

get_server_list_one = '''select * from server_list where name = %s'''