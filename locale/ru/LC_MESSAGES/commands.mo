��          �      �       0  2  1  �   d  �   )     #     9     G     X  %   ]  (   �  
   �     �  \   �  t  #  x  �  w  	  W  �
     �     �            8   &  ;   _     �     �  �   �                                   
   	                    I am admin reaction bot.
1. help - this help
2. add_signature - add signature to user
3. enable_signature - enable/disable showing signature for user
4. show_signature - show signature for user
5. add_rule_interruption - increment rule interruption
6. set_locale - change language of bot for this room
     This command show signature record for user.

command `show_signature` need 1 params.
syntax:

  my_botname_in_this_room: show_signature user_name

example:
  rsbot: show_signature Baduser

       User %(signature_user_mxid)s:
1. signature: %(signature)s
2. Author of signature: %(signature_author)s
3. Time create/update of signature: %(signature_time_create)s
4. Show signature: %(signature_show)s
5. Description signature: %(signature_descr)s
 add_rule_interruption add_signature enable_signature help internal error sql.check_user_exist() internal error sql.get_signature_descr() set_locale show_signature unknown command!
Please, use 'help' or empty command (only my room nick name) for help.
     Project-Id-Version: 
PO-Revision-Date: 2022-08-22 15:28+1000
Last-Translator: 
Language-Team: 
Language: ru_RU
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Generated-By: pygettext.py 1.5
Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<12 || n%100>14) ? 1 : 2);
X-Generator: Poedit 2.3
 Я - админский бот для реакций.
1. помощь - эта справка
2. подпись - добавить подпись пользователю
3. вкл_подпись - включить/отключить показ подписи для пользователя
4. показать_подпись - показать текущую подпись для пользователя
5. замечание - добавить администраторское замечание пользователю
6. язык - поменять язык общения с ботом для этой комнаты
     Эта команда отображает подпись пользователя.

команде `показать_подпись` нужен 1 параметр.
синтаксис:

  ник_бота: показать_подпись ник_пользователя/mxid_пользователя

пример:
  rsbot: показать_подпись Максим

       Пользователь %(signature_user_mxid)s:
1. подпись: %(signature)s
2. Автор подписи: %(signature_author)s
3. Время создания/обновления подписи: %(signature_time_create)s
4. Показывать подпись: %(signature_show)s
5. Описание подписи: %(signature_descr)s
 замечание подпись вкл_подпись помощь внутренняя ошибка sql.check_user_exist() внутренняя ошибка sql.get_signature_descr() язык показать_подпись неизвестная команда!
Пожалуйста, используйте команду 'помощь' или обатитесь ко мне без команды (только мой ник) для получения справки.
     