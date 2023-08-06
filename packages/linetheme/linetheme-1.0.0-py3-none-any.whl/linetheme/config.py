class Config:

    android_theme_dir_path = '/storage/emulated/0/Android/data/jp.naver.line.android/theme/'

    theme_id_dict = {
        'cony': 'a0768339-c2d3-4189-9653-2909e9bb6f58',
        'brown': 'ec4a14ea-7437-407b-aee7-96b1cbbc1b4b',
        'black': '34afc5b4-f330-40bc-a2ea-fae94207847a',
        'white': '3cc08ba6-5d04-4c52-ab76-651231ead8ef'
    }

    img_dict = {
        # 友達追加画面
        'add_list': {
            'invite_icon': ('addFriend.tab.icon', 'invite.image'), # 「招待」ボタンのアイコン
            'qrcode_icon': ('addFriend.tab.icon', 'qrcode.image'), # 「QRコード」ボタンのアイコン
            'shakeit_icon': ('addFriend.tab.icon', 'shakeit.image'), # 「ふるふる」ボタンのアイコン
            'idsearch_icon': ('addFriend.tab.icon', 'idsearch.image'), # 「ID検索」ボタンのアイコン
            'add_button_bg_normal': ('addFriend.tab.item', 'background.image', 'normal'), # 上記の4つのボタン通常背景色
            'add_button_bg_press': ('addFriend.tab.item', 'background.image', 'pressed') # 上記の4つのボタン押下背景色
        },
        # 通話タブ
        'call_list': {
            'logo_icon': ('calllist.item', 'logo.icon.image') # ロゴアイコン
        },
        # トーク画面の添付ファイル送信アイコン
        'chat_screen_attach': {
            'header_bg': ('chathistory.attach.header', 'background.image'), # ヘッダーの背景画像
            'audio_icon': ('chathistory.attach.item.image', 'audio.image', 'normal'), # 音声アイコン
            'photo_icon': ('chathistory.attach.item.image', 'choose.photo.image', 'normal'), # 写真選択アイコン
            'video_icon': ('chathistory.attach.item.image', 'choose.video.image', 'normal'), # 動画選択アイコン
            'contact_icon': ('chathistory.attach.item.image', 'contact.image', 'normal'), # 連絡先アイコン
            'location_icon': ('chathistory.attach.item.image', 'location.image', 'normal'), # 位置情報アイコン
            'take_photo_icon': ('chathistory.attach.item.image', 'take.photo.image', 'normal'), # 写真撮影アイコン
            'take_video_icon': ('chathistory.attach.item.image', 'take.video.image', 'normal'), # 動画撮影アイコン
            'file_icon': ('chathistory.attach.item.image', 'choose.file.image', 'normal') # ファイル選択アイコン
        },
        # トーク画面
        'chat_screen': {
            'checkbox_normal': ('chathistory.common', 'checkBox.image', 'normal'), # チェックボックスの通常画像
            'checkbox_select': ('chathistory.common', 'checkBox.image', 'selected'), # チェックボックスの選択画像
            'datebar_bg': ('chathistory.common', 'datebar.background.image', 'selected'), # 日付バーの背景画像
        }
    }

    egg_dict = {
        # 着せ替えの情報
        'theme_info': {
            'name': ('manifest', 'name'), # 着せ替えの名前
            'quality': ('manifest', 'quality'), # 着せ替えのクオリティ
            'platform': ('manifest', 'platform'), # 着せ替えのプラットフォーム
            'revision': ('manifest', 'revision'), # 着せ替えの変更回数
            'schemaVersion': ('manifest', 'schemaVersion'), # 着せ替えのスキーマバージョン
            'provider_name': ('manifest', 'provider', 'name'), # 着せ替えの供給元の名前
            'provider_url': ('manifest', 'provider', 'url') # 着せ替えの供給元のURL
        },
        # 友達リストやチャットリストなどの基本画面
        'common': {
            'bg_color': ('view.common', 'background.color'), # 基本の背景色
            'main_bg_color': ('main.view.common', 'background.color'), # 友達一覧、チャット一覧の背景色
            'main_bg_image': ('main.view.common', 'background.image') # 友達一覧、チャット一覧の背景画像
        },
        # 友達追加画面
        'add_list': {
            'make_group_text_color': ('addFriend.tab.addGroup', 'text.color'), # グル作成のテキスト色
            'make_group_subtext_color': ('addFriend.tab.addGroup', 'subtext.color'), # グル作成のサブテキスト色
            'make_group_arrow_color': ('addFriend.tab.addGroup', 'arrow.tintcolor'), # グル作成ボタンの矢印
            'make_group_icon_color': ('addFriend.tab.addGroup', 'icon.tintcolor'), # グル作成のアイコンの色
            'make_group_icon_bg_color': ('addFriend.tab.addGroup', 'icon.background.tintcolor'), # グル作成のアイコンの背景色
            'make_group_bg_color_normal': ('addFriend.tab.addGroup', 'background.color', 'normal'), # グル作成ボタンの通常背景色
            'make_group_bg_color_press': ('addFriend.tab.addGroup', 'background.color', 'pressed'), # グル作成ボタンの押下背景色
            'button_text_color': ('addFriend.tab.addGroup', 'addButton.text.color'), # 友達自動追加の「許可する」ボタンのテキスト色
            'button_bg_color_normal': ('addFriend.tab.addGroup', 'addButton.background.tintcolor', 'normal'), # 友達自動追加の「許可する」ボタンの通常背景色
            'button_bg_color_press': ('addFriend.tab.addGroup', 'addButton.background.tintcolor', 'pressed'), # 友達自動追加の「許可する」ボタンの押下背景色
            'item_text_color': ('addFriend.tab.item', 'text.color'), # 友達追加4つのボタンのテキスト色
            'badge_bg_color': ('addFriend.tab.addGroup', 'badge.on.background.tintcolor'), # 不明
            'update_button_color_normal': ('addFriend.tab.addGroup', 'updateButton.tintcolor', 'normal'), # 不明
            'update_button_color_pressed': ('addFriend.tab.addGroup', 'updateButton.tintcolor', 'pressed') # 不明
        },
        # 友達リスト
        'friendl_ist': {
            'no_result_text_color': ('friendlist.common', 'noresult.text.color'), # 友達0の時のテキスト色
            'category_open_arrow_color': ('friendlist.category', 'arrowOpen.tintcolor'),
            'category_close_arrow_color': ('friendlist.category', 'arrowClose.tintcolor'),
            'category_bg_color': ('friendlist.category', 'background.color'),
            'category_text_color': ('friendlist.category', 'text.color'),
            'category_see_all_arrow_color': ('friendlist.category', 'textSeeAll.arrow.tintcolor'), # 不明
            'category_see_all_arrow_text_color': ('friendlist.category', 'textSeeAll.color'), # 不明
            'add_invite_button_color': ('friendlist.item', 'addInviteButton.color'), # 不明
            'add_friend_bg_color_normal': ('friendlist.item', 'addFriend.background.tintcolor', 'normal'), # 不明
            'add_friend_bg_color_pressed': ('friendlist.item', 'addFriend.background.tintcolor', 'pressed'), # 不明
            'add_friend_icon_color': ('friendlist.item', 'addFriend.icon.tintcolor'), # 友達追加アイコン色
            'arrow_color': ('friendlist.item', 'arrowIcon.tintcolor'), # 矢印色
            'phone_icon_color': ('friendlist.item', 'phoneIcon.tintcolor', 'normal'), # 電話アイコン色
            'phone_icon_bg_color_normal': ('friendlist.item', 'phoneIcon.background.tintcolor', 'normal'), # 電話アイコン通常背景色
            'phone_icon_bg_color_pressed': ('friendlist.item', 'phoneIcon.background.tintcolor', 'pressed'), # 電話アイコン押下背景色
            'status_msg_text_color': ('friendlist.item', 'statusText.color'), # ひとことのテキスト色
            'update_icon_color': ('friendlist.item', 'updateIcon.tintcolor'), # 更新アイコン色
            'music_icon_color': ('friendlist.item', 'musicIcon.tintcolor'), # 音楽アイコン色
            'update_video_prof_color': ('friendlist.item', 'updateVideoProfile.tintcolor'), # 不明
            'logo_icon_color': ('friendlist.item', 'logo.icon.tintcolor'), # 不明
            'radiobutton_bg_color': ('friendlist.item', 'radiobutton.background.tintcolor'), # 不明
            'radiobutton_selected_bg_color': ('friendlist.item', 'radiobutton.selected.tintcolor'), # 不明
            'myprof_link_text_color': ('friendlist.item', 'myprofile.link.text.color'), # 自分のリンクテキスト色
            'myprof_arrow_color': ('friendlist.item', 'myprofile.arrow.tintcolor'), # 自分の矢印色
            'myprof_text_color': ('friendlist.item', 'myprofile.text.color'), # 自分の名前のテキスト色
            'create_group_icon_color': ('friendlist.item', 'createGroup.icon.tintcolor'), # グル作成のアイコン色
            'create_group_icon_bg_color': ('friendlist.item', 'createGroup.icon.background.tintcolor'), # グル作成のアイコン背景色
            'cell_bg_color_normal': ('friendlist.item.common', 'background.color', 'normal'), # セルの通常背景色
            'cell_bg_color_press': ('friendlist.item.common', 'background.color', 'pressed'), # セルの押下背景色
            'cell_new_bg_color_normal': ('friendlist.item.common', 'new.background.color', 'normal'), # 新規友達セルの通常背景色
            'cell_new_bg_color_press': ('friendlist.item.common', 'new.background.color', 'pressed'), # 新規友達セルの押下背景色
            'cell_new_bg_color_normal': ('friendlist.item.common', 'checked.background.color', 'normal'), # チェックしたセルの通常背景色
            'cell_new_bg_color_press': ('friendlist.item.common', 'checked.background.color', 'pressed') # チェックしたセルの押下背景色
        },
        #チャットリスト
        'chat_list': {
            'name_color': ('chatlist.item', 'nameText.color'), # 名前のテキスト色
            'msg_color': ('chatlist.item', 'messageText.color'), # メッセージテキスト色
            'msg_count_text_color': ('chatlist.item', 'messageCountText.color'), # 未読カウントのテキスト色
            'time_color': ('chatlist.item', 'timeText.color'), # 時間のテキスト色
            'mute_icon_color': ('chatlist.item', 'muteIcon.tintcolor'), # ミュートアイコン色
            'live_icon_color': ('chatlist.item', 'liveIcon.tintcolor'), # ライブアイコン色
            'call_icon_color_press': ('chatlist.item', 'closeIcon.tintcolor'), # 通話中のアイコン色
            'close_icon_color_normal': ('chatlist.item', 'closeIcon.tintcolor', 'normal'), # 不明
            'close_icon_color_press': ('chatlist.item', 'closeIcon.tintcolor', 'pressed') # 不明
        }, 
        # コールリスト
        'call_list': {
            'date_icon_color': ('calllist.item', 'dateIcon.tintcolor'), # 日付アイコン色
            'date_color': ('calllist.item', 'dateText.color'), # 日付テキスト色
            'name_color': ('calllist.item', 'nameText.color'), # 名前テキスト色
            'name_missed_color': ('calllist.item', 'nameMissedText.color'), # 不在着信の名前テキスト色
            'phone_icon_color': ('calllist.item', 'phoneIcon.tintcolor', 'normal'), # 名前テキスト色
            'phone_icon_bg_color_normal': ('calllist.item', 'phoneIcon.background.tintcolor', 'normal'), # 名前テキスト色
            'phone_icon_bg_color_press': ('calllist.item', 'phoneIcon.background.tintcolor', 'pressed') # 名前テキスト色
        },
        # トーク画面
        'chat_screen': {
            'recv_video_bg_color': ('chathistory.balloon.video.default.recv', 'background.color'), # 受信した動画の背景色
            'send_video_bg_color': ('chathistory.balloon.video.default.send', 'background.color'), # 送信した動画の背景色
            'resend_icon_color': ('chathistory.common', 'autoresend.icon.tintcolor'), # 再送信アイコン色
            'datebar_text_color': ('chathistory.common', 'datebar.text.color'), # 日付バーのテキスト色
            'name_color_normal': ('chathistory.common', 'name.color', 'normal'), # 名前の通常テキスト色
            'name_color_press': ('chathistory.common', 'name.color', 'press'), # 名前の押下テキスト色
            'time_color': ('chathistory.common', 'time.color'), # 時間テキスト色
            'sound_sticker_icon_color': ('chathistory.common', 'soundsticker.icon.tintcolor'), # 送信した動画の背景色
            'recent_icon_bg_color': ('chathistory.common', 'recentButton.background.tintcolor'), # 不明
            'recent_icon_color_normal': ('chathistory.common', 'recentButton.icon.tintcolor', 'normal'), # 不明
            'recent_icon_color_press': ('chathistory.common', 'recentButton.icon.tintcolor', 'pressed'), # 不明
            'retry_icon_color': ('chathistory.common', 'reply.icon.tintcolor') # 送信失敗時のアイコン色
        },
        # トーク画面の添付ファイル送信画面
        'chat_screen_attach': {
            'header_text_color': ('chathistory.attach.header', 'text.color'), # ヘッダーのテキスト色
            'bg_color_normal': ('chathistory.attach.item', 'background.color', 'normal'), # 添付ファイルの通常背景色
            'bg_color_press': ('chathistory.attach.item', 'background.color', 'pressed'), # 添付ファイルの押下背景色
            'external_icon_color': ('chathistory.attach.item', 'external.icon.tintcolor'), # 不明
            'icon_color': ('chathistory.attach.item', 'icon.tintcolor'), # アイコン色
            'text_color': ('chathistory.attach.item', 'text.color'), # テキスト色
            'divider_bg_color': ('chathistory.attach.item', 'top.divider.background.color'), # 背景を分ける色
            'blank_icon_color': ('chathistory.attach.item', 'blank.icon.tintcolor') # 何もない時のアイコン色
        },
        # トーク画面のメッセージ
        'chat_screen_msg': {
            # contact
            'recv_contact_arrow_color': ('chathistory.contact.recv.msg', 'arrow.tintcolor'), # 受信した連絡先の矢印色
            'recv_contact_text_color': ('chathistory.contact.recv.msg', 'text.color'), # 受信した連絡先のテキスト色
            'recv_contact_icon_color': ('chathistory.contact.recv.msg', 'contact.icon.tintcolor'), # 受信した連絡先のアイコン色
            'send_contact_arrow_color': ('chathistory.contact.send.msg', 'arrow.tintcolor'), # 送信した連絡先の矢印色
            'send_contact_text_color': ('chathistory.contact.send.msg', 'text.color'), # 送信した連絡先のテキスト色
            'send_contact_icon_color': ('chathistory.contact.send.msg', 'contact.icon.tintcolor'), # 送信した連絡先のアイコン色
            # file
            'recv_file_arrow_color': ('chathistory.file.recv.msg', 'arrow.tintcolor'), # 受信したファイルの矢印色
            'recv_file_text_color': ('chathistory.file.recv.msg', 'text.color'), # 受信したファイルのテキスト色
            'recv_file_expire_text_color': ('chathistory.file.recv.msg', 'expire.text.color'), # 受信したファイルの期限切れテキスト色
            'recv_file_icon_color': ('chathistory.file.recv.msg', 'file.icon.tintcolor'), # 受信したファイルのアイコン色
            'send_file_arrow_color': ('chathistory.file.send.msg', 'arrow.tintcolor'), # 送信したファイルの矢印色
            'send_file_expire_text_color': ('chathistory.file.send.msg', 'expire.text.color'), # 送信したファイルテキスト色
            'send_file_text_color': ('chathistory.file.send.msg', 'text.color'), # 送信したファイルの期限切れテキスト色
            'send_file_icon_color': ('chathistory.file.send.msg', 'file.icon.tintcolor'), # 送信したファイルのアイコン色
            # gift
            'recv_gift_button_text_color': ('chathistory.gift.recv.msg', 'button.text.color'), # 受信したギフトのボタンテキスト色
            'recv_gift_button_text_shadow': ('chathistory.gift.recv.msg', 'button.text.shadow'), # 受信したギフトのボタンテキストシャドウ
            'recv_gift_text_color': ('chathistory.gift.recv.msg', 'text.color'), # 受信したギフトのテキスト色
            'send_gift_text_color': ('chathistory.gift.send.msg', 'text.color'), # 送信したギフトのテキスト色
            # note
            'recv_note_text_color': ('chathistory.groupboard.recv.msg', 'text.color'), # 受信したギフトのテキスト色
            'recv_note_arrow_color': ('chathistory.groupboard.recv.msg', 'arrow.tintcolor'), # 受信したギフトのボタンテキスト色
            'recv_note_location_text_color': ('chathistory.groupboard.recv.msg', 'location.text.color'), # 受信したギフトのボタンテキスト色
            'recv_note_more_text_color': ('chathistory.groupboard.recv.msg', 'more.text.color'), # 受信したギフトのボタンテキスト色
            'recv_note_photo_color': ('chathistory.groupboard.recv.msg', 'photo.default.tintcolor'), # 受信したギフトのボタンテキスト色
            'recv_note_photo_icon_color': ('chathistory.groupboard.recv.msg', 'photoicon.tintcolor'), # 受信したギフトのボタンテキスト色
            'recv_note_sticker_color': ('chathistory.groupboard.recv.msg', 'sticker.default.tintcolor'), # 受信したギフトのボタンテキスト色
            'recv_note_bottom_text_color': ('chathistory.groupboard.recv.msg', 'bottom.text.color'), # 受信したギフトのボタンテキスト色
            'recv_note_video_color': ('chathistory.groupboard.recv.msg', 'video.default.tintcolor'), # 受信したギフトのボタンテキスト色
            'send_note_video_icon_color': ('chathistory.groupboard.send.msg', 'videoicon.tintcolor'), # 受信したギフトのボタンテキスト色
            'send_note_text_color': ('chathistory.groupboard.send.msg', 'text.color'), # 受信したギフトのテキスト色
            'send_note_arrow_color': ('chathistory.groupboard.send.msg', 'arrow.tintcolor'), # 受信したギフトのボタンテキスト色
            'send_note_location_text_color': ('chathistory.groupboard.send.msg', 'location.text.color'), # 受信したギフトのボタンテキスト色
            'send_note_more_text_color': ('chathistory.groupboard.send.msg', 'more.text.color'), # 受信したギフトのボタンテキスト色
            'send_note_photo_color': ('chathistory.groupboard.send.msg', 'photo.default.tintcolor'), # 受信したギフトのボタンテキスト色
            'send_note_photo_icon_color': ('chathistory.groupboard.send.msg', 'photoicon.tintcolor'), # 受信したギフトのボタンテキスト色
            'send_note_sticker_color': ('chathistory.groupboard.send.msg', 'sticker.default.tintcolor'), # 受信したギフトのボタンテキスト色
            'send_note_bottom_text_color': ('chathistory.groupboard.send.msg', 'bottom.text.color'), # 受信したギフトのボタンテキスト色
            'send_note_video_color': ('chathistory.groupboard.send.msg', 'video.default.tintcolor'), # 受信したギフトのボタンテキスト色
            'send_note_video_icon_color': ('chathistory.groupboard.send.msg', 'videoicon.tintcolor'), # 受信したギフトのボタンテキスト色
            'note_tip_text_color': ('chathistory.groupboard.tip', 'text.color'), # 受信したギフトのボタンテキスト色
        },
        # ノート、タイムラインの文字入力バー
        'note_input_bar': {
            'text_color': ('chathistory.input', 'inputText.color'), # 入力文字の色
            'text_hint_color': ('chathistory.input', 'inputText.hint'), # 入力文字のヒントの色
            'send_button_color': ('chathistory.input', 'sendButton.tintcolor'), # 送信ボタンのアイコン色
            'send_button_bg_color_normal': ('chathistory.input', 'sendButton.background.color', 'normal'), # 送信ボタンの通常背景色
            'send_button_bg_color_press': ('chathistory.input', 'sendButton.background.color', 'pressed'), # 送信ボタンの通常背景色
        },
        # アルバム詳細メニュー
        'album': {
            'item_color_normal': ('album.detail.menu', 'item.color', 'normal'), # 要素の通常色
            'item_color_select': ('album.detail.menu', 'item.color', 'selected'), # 要素の選択色
            'check_icon_color': ('album.detail.menu', 'checked.icon.tintcolor'), # チェックアイコン色
        },
        # 下部ボタン
        'bottom_button': {
            'button1_text_color_dimm': ('bottom.button.common', 'button1.text.color', 'dimmed'), # ボタン1の通常テキスト色
            'button1_text_color_normal': ('bottom.button.common', 'button1.text.color', 'normal'), # ボタン1の無効テキスト色
            'button1_bg_color_dimm': ('bottom.button.common', 'button1.background.color', 'dimmed'), # ボタン1の無効背景色
            'button1_bg_color_normal': ('bottom.button.common', 'button1.background.color', 'normal'), # ボタン1の通常背景色
            'button1_bg_color_press': ('bottom.button.common', 'button1.background.color', 'pressed'),  # ボタン1の押下背景色
            'button2_text_color_dimm': ('bottom.button.common', 'button2.text.color', 'dimmed'), # ボタン2の通常テキスト色
            'button2_text_color_normal': ('bottom.button.common', 'button2.text.color', 'normal'), # ボタン2の無効テキスト色
            'button2_bg_color_dimm': ('bottom.button.common', 'button2.background.color', 'dimmed'), # ボタン2の無効背景色
            'button2_bg_color_normal': ('bottom.button.common', 'button2.background.color', 'normal'), # ボタン2の通常背景色
            'button2_bg_color_press': ('bottom.button.common', 'button2.background.color', 'pressed'),  # ボタン2の押下背景色
            'button3_text_color_dimm': ('bottom.button.common', 'button3.text.color', 'dimmed'), # ボタン3の通常テキスト色
            'button3_text_color_normal': ('bottom.button.common', 'button3.text.color', 'normal'), # ボタン3の無効テキスト色
            'button3_bg_color_dimm': ('bottom.button.common', 'button3.background.color', 'dimmed'), # ボタン3の無効背景色
            'button3_bg_color_normal': ('bottom.button.common', 'button3.background.color', 'normal'), # ボタン3の通常背景色
            'button3_bg_color_press': ('bottom.button.common', 'button3.background.color', 'pressed'),  # ボタン3の押下背景色
        },
        "search_bar": {
            "bg_color": ("searchBar.common", "background.color"),
            "box_bg_color": ("searchBar.common", "inputBox.background.tintcolor"),
            "icon_color": ("searchBar.common", "icon.tintcolor"),
            "bg_color": ("searchBar.common", "hint.text.color"),
            "bg_color": ("searchBar.common", "keyword.text.color"),
            "bg_color": ("searchBar.common", "keyword.icon.tintcolor")
        }
    }
