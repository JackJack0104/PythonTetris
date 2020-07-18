import game

# ゲームのタイトル
title = 'テトリス'
# 画面の幅 10マス分
width = 32 * 10
# 画面の高さ 20マス分
height = 32 * 20

tetris = game.Game(title, width, height)
tetris.start()