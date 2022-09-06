��    &      L  5   |      P  g   Q  -  �  �   �  '  �  (  

  �   3  �   1  �       �      �  %   �     �     �          *     ;     L     Q  %   n  (   �  T   �  V     (   i  %   �     �  
   �     �  #   �           ,     H     W  !   g  3   �  #   �  `   �  *   B  t  m  �   �  7	  �  �  �    j     z"  �  �$  x  C&  �   �'  X  �(  W   �)  I   2*     |*     �*  C   �*  :   �*     +     3+  5   @+  8   v+  ;   �+  �   �+  �   �,  I   B-  `   �-  <   �-     *.  ,   3.  E   `.  I   �.  '   �.     /  :   8/  U   s/  s   �/  J   =0  �   �0  W   �1                           %              $                   "                                #             
                         !             &                     	              Admin %(admin)s at %(date)s add rule interruption by user %(signature_user_mxid)s with descr: %(descr)s I am admin reaction bot.
  1. help - this help
  2. add_signature - add signature to user
  3. enable_signature - enable/disable showing signature for user
  4. show_signature - show signature for user
  5. add_rule_interruption - increment rule interruption
  6. show_rule_interruption_stat - show active/all rule interruption count for user
  6. show_active_rule_interruption_descr - show active rule interruption description (for all interruption) - be cafule with many active interruption for user - bot will spam messages
  7. show_old_rule_interruption_descr - show old (not active) rule interruption description (for all old interruption) - be cafule with many old not active interruption for user - bot will spam messages
  8. clear_active_rule_interruption - clear active rule interruption count (when unban user)
  9. set_locale - change language of bot for this room
  10. set_my_descr - set own description for user (can do only mxid for it's mxid)
  11. show_user_descr - show description for user
  12. clear_user_descr - clear description for user
       This command clear user description. This can do only administrator or moderator.

  command `clear_user_descr` need 1 params.
  syntax:

    my_botname_in_this_room: clear_user_descr user_name

  example:
    rsbot: clear_user_descr Baduser
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
%s add_rule_interruption add_signature clear_active_rule_interruption clear_user_descr enable_signature help internal error in function:  internal error sql.check_user_exist() internal error sql.get_signature_descr() nickname %s not known. Please, correct, or select user by mxid (as @user:server.com) nickname %s not uniqum in this room. Please, select user by mxid (as @user:server.com) no active rule interruptions for user %s no old rule interruptions for user %s no such user in db: %s set_locale set_my_descr show_active_rule_interruption_descr show_old_rule_interruption_descr show_rule_interruption_stat show_signature show_user_descr success add user_descr to user %s success clear active rule interruptions for user %s success clear user_descr to user %s unknown command!
  Please, use 'help' or empty command (only my room nick name) for help.
       you need more power level for this command Project-Id-Version: 
PO-Revision-Date: 2022-09-06 20:02+1000
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
  5. замечание - добавить замечание пользователю
  6. статистика_замечаний - отобразить счётчик активных/всех замечаний для пользователя
  6. показать_описание_активных_замечаний - отобразить описания всех активных замечаний (будьте осторожны в случае большого количества замечаний - бот может завалить комнату сообщениями (проверьте сначала количество замечаний командой 'статистика_замечаний'
  7. показать_описание_неактивных_замечаний - отобразить описания всех неактивных замечаний (будьте осторожны в случае большого количества замечаний - бот может завалить комнату сообщениями (проверьте сначала количество замечаний командой 'статистика_замечаний'
  8. очистить_счётчик_активных_замечаний - замечания перейдут в статус "неактивные" и не будут показываться в подписи пользователя
  9. язык - поменять язык, на котором я говорю
  10. установить_моё_описание - установить собственное описание для своего же mxid/ника
  11. показать_описание_пользователя - показать собственное описание пользователя
  12. очистить_описание_пользователя - очистить описание другого пользователя
       Эта команда очищает описание пользователя. Это может делать только администратор (пользователь может просто установить пустое описание, если хочет очистить своё описание)

команда `очистить_описание_пользователя` нужен 1 параметр.
синтаксис:

  ник_бота: очистить_описание_пользователя имя_пользователя

пример:
  rsbot: очистить_описание_пользорвателя Максим

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
%s замечание подпись очистить_счётчик_активных_замечаний очистить_описание_пользователя вкл_подпись помощь внутренняя ошибка в функции:  внутренняя ошибка sql.check_user_exist() внутренняя ошибка sql.get_signature_descr() ник %s неизвестен. Пожалуйста, скорректируйте его или выберите пользователя по его mxid (т.е. @user:server.com) ник %s не уникален в этой комнате. Пожалуйста, выберите пользователя по mxid (т.е.: @user:server.com) нет активных замечаний у пользователя %s нет старых (неактивных) замечаний для пользователя %s нет такого пользователя в базе: %s язык установить_моё_описание показать_описание_активных_замечаний показать_описание_неактивных_замечаний статистика_замечаний показать_подпись показать_описание_пользователя успешно установил описание для пользователя %s успешно очистил счётчик активных нарушений для пользователя %s успешно очистил описание пользователя %s неизвестная команда!
  Пожалуйста, используйте команду 'помощь' или обатитесь ко мне без команды (только мой ник) для получения справки.
     вам не хватает прав для выполнения этой команды 