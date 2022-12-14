??    6      ?  I   |      ?  g   ?  _  	  ?   i	  #  P
  ?   t  ;  o  '  ?  (  ?  ?   ?  ?   ?  ?   ?    c      i  %   ?     ?     ?     ?     ?             ?  ?   ?    G    b     x     ?     ?  %   ?  (   ?  T   ?  V   O  (   ?  %   ?     ?  
          #   $      H     i     ?     ?  (   ?      ?  !   ?  3     #   D  #   h  $   ?  #   ?  `   ?  ;   6     r  *   v  t  ?  ?     ?	  ?  J  k)  ?  ?*  ?  ?,  }  K/    ?0    ?2  ?  ?4  x  ?6  ?   8  X  ?8  W   9:  I   ?:     ?:     ?:  C   ?:     A;  :   _;  ?  ?;  y  ?=  p  
@  ?  {A  ?  YC     OE     eE  5   rE  8   ?E  ;   ?E  ?   F  ?   ?F  I   tG  `   ?G  <   H     \H  ,   eH  E   ?H  I   ?H  '   "I     JI  :   jI  L   ?I  H   ?I  U   ;J  s   ?J  K   K  J   QK  h   ?K  f   L  ?   lL  a   jM     ?M  W   ?M     /      -           )   %                     .           2              &             4            +           6         1   (          
         *   #            0   5             3   '   !            ,            $       "          	                          Admin %(admin)s at %(date)s add rule interruption by user %(signature_user_mxid)s with descr: %(descr)s I am admin reaction bot.
  1. help - this help
  2. add_signature - add signature to user
  3. enable_signature - enable/disable showing signature for user
  4. show_signature - show signature for user
  5. clear_signature - clear signature for user
  6. add_rule_interruption - increment rule interruption
  7. show_rule_interruption_stat - show active/all rule interruption count for user
  8. show_active_rule_interruption_descr - show active rule interruption description (for all interruption) - be cafule with many active interruption for user - bot will spam messages
  9. show_old_rule_interruption_descr - show old (not active) rule interruption description (for all old interruption) - be cafule with many old not active interruption for user - bot will spam messages
  10. clear_active_rule_interruption - clear active rule interruption count (when unban user)
  11. set_locale - change language of bot for this room
  12. set_my_descr - set own description for user (can do only mxid for it's mxid)
  13. show_user_descr - show description for user
  14. clear_user_descr - clear description for user
       This command allow switch language for this room.

  command `set_locale` need 1 param: locale. Locale can be 'ru', 'us', etc.
  syntax:

    my_botname_in_this_room: set_locale locale

  example:
    rsbot: set_locale ru
         This command clear active rule interruptions for user.
  They will become as not active.

  command `clear_active_rule_interruption` need 1 param.
  syntax:

    my_botname_in_this_room: clear_active_rule_interruption user_name

  example:
    rsbot: clear_active_rule_interruption Baduser

 This command clear user description. This can do only administrator or moderator.

  command `clear_user_descr` need 1 params.
  syntax:

    my_botname_in_this_room: clear_user_descr user_name

  example:
    rsbot: clear_user_descr Baduser
         This command disable or enable showing signature for user.
  Disabling - is not delete signature in db, but it will not be show.

  command `enable_signature` need 2 params.
  syntax:

    my_botname_in_this_room: enable_signature user_name_for_signature yes/no

  example:
    rsbot: enable_signature Baduser yes

 This command show description for active rule interruption for user.

  command `show_active_rule_interruption_descr` need 1 params.
  syntax:

    my_botname_in_this_room: show_active_rule_interruption_descr user_name

  example:
    rsbot: show_active_rule_interruption_descr Baduser

         This command show description for old (not active) rule interruption for user.

  command `show_old_rule_interruption_descr` need 1 params.
  syntax:

    my_botname_in_this_room: show_old_rule_interruption_descr user_name

  example:
    rsbot: show_old_rule_interruption_descr Baduser

         This command show rule interruption stat for user.

  command `show_rule_interruption_stat` need 1 params.
  syntax:

    my_botname_in_this_room: show_rule_interruption_stat user_name

  example:
    rsbot: show_rule_interruption_stat Baduser

         This command show signature record for user.

  command `show_signature` need 1 params.
  syntax:

    my_botname_in_this_room: show_signature user_name

  example:
    rsbot: show_signature Baduser

         User %(signature_user_mxid)s have:
  1. active rule interruption: %(active_rule_interruption)d
  2. all rule interruption: %(all_rule_interruption)d
   User %(signature_user_mxid)s:
  1. signature: %(signature)s
  2. Author of signature: %(signature_author)s
  3. Time create/update of signature: %(signature_time_create)s
  4. Show signature: %(signature_show)s
  5. Description signature: %(signature_descr)s
   User '%s' has no own description User description for user '%s' is:
%s add_rule_interruption add_signature clear_active_rule_interruption clear_signature clear_user_descr command `add_rule_interruption` need 2 params.
  syntax:

    my_botname_in_this_room: add_rule_interruption user_name_for_inc_rule_interruption "description - Why rule is interrupt"

  example:
    rsbot: add_rule_interruption Baduser "rule paragraph 3 at message url: https://matrix.to/#/!tBHU3434554VVVfuMP:matrix.org/$UV232444VR8-F9ch3eAZxlG2nUdakJXDMfYETdZVYCQ?via=matrix.org"

 command `add_signature` need 3 params.
  syntax:

    my_botname_in_this_room: add_signature user_name_for_signature signature_text "description - Why signature added to user"

  example:
    rsbot: add_signature Baduser "spammer" "This user spam in this room!"

 command `clear_signature` need 1 params.
  syntax:

    my_botname_in_this_room: clear_signature user_name_for_signature

  example:
    rsbot: clear_signature goodUser

 command `set_my_descr` need 1 params.
Command set own description for user. This can do only some user for self.
  syntax:

    my_botname_in_this_room: set_my_descr "description of me"

  example:
    rsbot: set_my_descr "I am good user. My github url: xxxx, My social url: xxxx"

 command `show_user_descr` need 1 params.
Command show own description for user. This description was seted user for self.
  syntax:

    my_botname_in_this_room: show_user_descr username

  examples:
    rsbot: show_user_descr UserNick
    rsbot: show_user_descr @user:server

 enable_signature help internal error in function:  internal error sql.check_user_exist() internal error sql.get_signature_descr() nickname %s not known. Please, correct, or select user by mxid (as @user:server.com) nickname %s not uniqum in this room. Please, select user by mxid (as @user:server.com) no active rule interruptions for user %s no old rule interruptions for user %s no such user in db: %s set_locale set_my_descr show_active_rule_interruption_descr show_old_rule_interruption_descr show_rule_interruption_stat show_signature show_user_descr success add rule_interruption to user %s success add signature to user %s success add user_descr to user %s success clear active rule interruptions for user %s success clear signature for user %s success clear user_descr to user %s success disable signature to user %s success enable signature to user %s unknown command!
  Please, use 'help' or empty command (only my room nick name) for help.
       unsupported locale name '%s'. Try 'en' or 'ru' for example. yes you need more power level for this command Project-Id-Version: 
PO-Revision-Date: 2022-10-17 09:48+1000
Last-Translator: 
Language-Team: 
Language: ru_RU
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Generated-By: pygettext.py 1.5
Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<12 || n%100>14) ? 1 : 2);
X-Generator: Poedit 2.3
 Администратор %(admin)s в %(date)s добавил замечание пользователю %(signature_user_mxid)s со следующим описанием: %(descr)s Я информационный бот.
  1. помощь - эта помощь
  2. подпись - добавить подпись пользователю
  3. вкл_подпись - вкл./выкл.отображение подписи для пользователя
  4. показать_подпись - отобразить какая у пользователя подпись
  5. очистка_подписи - очистить подпись у пользователя
  6. замечание - добавить замечание пользователю
  7. статистика_замечаний - отобразить счётчик активных/всех замечаний для пользователя
  8. показать_описание_активных_замечаний - отобразить описания всех активных замечаний (будьте осторожны в случае большого количества замечаний - бот может завалить комнату сообщениями (проверьте сначала количество замечаний командой 'статистика_замечаний'
  9. показать_описание_неактивных_замечаний - отобразить описания всех неактивных замечаний (будьте осторожны в случае большого количества замечаний - бот может завалить комнату сообщениями (проверьте сначала количество замечаний командой 'статистика_замечаний'
  10. очистить_счётчик_активных_замечаний - замечания перейдут в статус "неактивные" и не будут показываться в подписи пользователя
  11. язык - поменять язык, на котором я говорю
  12. установить_моё_описание - установить собственное описание для своего же mxid/ника
  13. показать_описание_пользователя - показать собственное описание пользователя
  14. очистить_описание_пользователя - очистить описание другого пользователя
       Эта команда позволяет переключить язык бота.

команде `язык` нужен 1 параметр: локаль. Локаль может быть: 'ru', 'us', 'en', и т.д.
синтаксис:

  ник_бота: язык код_локали

пример: 
  rsbot: язык ru

       Эта команда очищает число активных замечаний пользователя.

команде `очистить_счётчик_активных_замечаний` нужен 1 параметр.
синтаксис:

  ник_бота: очистить_счётчик_активных_замечаний ник_пользователя/mxid_пользователя

пример:
  rsbot: очистить_счётчик_активных_замечаний Максим

      
 Эта команда очищает описание пользователя. Это может делать только администратор (пользователь может просто установить пустое описание, если хочет очистить своё описание)

команда `очистить_описание_пользователя` нужен 1 параметр.
синтаксис:

  ник_бота: очистить_описание_пользователя имя_пользователя

пример:
  rsbot: очистить_описание_пользорвателя Максим

       Эта команда включает или отключает показ подписи у пользователя.

команде `вкл_подпись` нужено 2 параметра.
синтаксис:

  ник_бота: вкл_подпись ник_пользователя/mxid_да/нет

пример: 
  rsbot: вкл_подпись Максим нет

      
 Эта команда отображает описание активных замечаний пользователя.

команде `показать_описание_активных_замечаний` нужен 1 параметр.
синтаксис:

  ник_бота: показать_описание_активных_замечаний ник_пользователя/mxid_пользователя

пример:
  rsbot: показать_описание_активных_замечаний Максим

       Эта команда отображает описание неактивных замечаний пользователя.

команде `показать_описание_неактивных_замечаний` нужен 1 параметр.
синтаксис:

  ник_бота: показать_описание_неактивных_замечаний ник_пользователя/mxid_пользователя

пример:
  rsbot: показать_описание_неактивных_замечаний Максим

       Эта команда отображает статистику замечаний пользователя.

команде `статистика_замечаний` нужен 1 параметр.
синтаксис:

  ник_бота: статистика_замечаний ник_пользователя/mxid_пользователя

пример:
  rsbot: статистика_замечаний Максим

       Эта команда отображает подпись пользователя.

команде `показать_подпись` нужен 1 параметр.
синтаксис:

  ник_бота: показать_подпись ник_пользователя/mxid_пользователя

пример: 
  rsbot: показать_подпись Максим

       Пользователь %(signature_user_mxid)s имеет:
  1. Активных замечаний: %(active_rule_interruption)d
  2. Всего замечаний: %(all_rule_interruption)d
   Пользователь %(signature_user_mxid)s:
1. подпись: %(signature)s
2. Автор подписи: %(signature_author)s
3. Время создания/обновления подписи: %(signature_time_create)s
4. Показывать подпись: %(signature_show)s
5. Описание подписи: %(signature_descr)s
  Пользователь '%s' не имеет собственного описания Собственное описание пользователя '%s':
%s замечание подпись очистить_счётчик_активных_замечаний очистка_подписи очистить_описание_пользователя команде `замечание` нужно 2 параметра.
  синтаксис:

    ник_бота: замечание ник_пользователя "описание из-за чего выдано замечание"

  пример:
    rsbot: замечание Максим"нарушение параграфа 3 правил в сообщении по ссылке: https://matrix.to/#/!tBHU3434554VVVfuMP:matrix.org/$UV232444VR8-F9ch3eAZxlG2nUdakJXDMfYETdZVYCQ?via=matrix.org"

 команда добавляет подпись пользователю.

команде `подпись` нужно 3 параметра.
синтаксис:

  ник_бота: подпись ник_пользователя/mxid_пользователя "текст подписи" "описание - почему эта подпись дана"

пример: 
  rsbot: подпись Максим провокатор "вбрасывает лживые ссылки, признаёт это, но продолжает делать, чтобы наблюдать за реакцией других пользователей"

 эта команда очищает подпись у пользователя.

команде `очистка_подписи` нужен 1 параметр.
синтаксис:

  ник_бота: очистка_подписи ник_пользователя/mxid_пользователя

пример: 
  rsbot: очистка_подписи Максим

      
 команде `установить_моё_описание` нужен один параметр.
Команда устанавливает личное описание для пользователя.

синтаксис:

  ник_бота: установить_моё_описание "моё описание"

пример:
  rsbot: установить_моё_описание "моя страничка в социальных сетях: http://vk.com/43434

      
 команда отображает описание пользователя, которое он сам себе установил.

команде `показать_описание_пользователя` нужен 1 параметр.
синтаксис:

  ник_бота: показать_описание_пользователя ник_пользователя/mxid_пользователя

пример:
  rsbot: показать_описание_пользователя Максим

 вкл_подпись помощь внутренняя ошибка в функции:  внутренняя ошибка sql.check_user_exist() внутренняя ошибка sql.get_signature_descr() ник %s неизвестен. Пожалуйста, скорректируйте его или выберите пользователя по его mxid (т.е. @user:server.com) ник %s не уникален в этой комнате. Пожалуйста, выберите пользователя по mxid (т.е.: @user:server.com) нет активных замечаний у пользователя %s нет старых (неактивных) замечаний для пользователя %s нет такого пользователя в базе: %s язык установить_моё_описание показать_описание_активных_замечаний показать_описание_неактивных_замечаний статистика_замечаний показать_подпись показать_описание_пользователя успешно добавил замечание пользователю %s успешно добавил подпись пользователю %s успешно установил описание для пользователя %s успешно очистил счётчик активных нарушений для пользователя %s успешно очистил подпись у пользователя %s успешно очистил описание пользователя %s успешно отключил отображение подписи для пользователя %s успешно включил отображение подписи для пользователя %s неизвестная команда!
  Пожалуйста, используйте команду 'помощь' или обратитесь ко мне без команды (только мой ник) для получения справки.
     неподдерживаемое имя локали '%s'. Попробуйте 'en' или 'ru'. да вам не хватает прав для выполнения этой команды 